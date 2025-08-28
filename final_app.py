#!/usr/bin/env python3
"""
Final Production Application
Oracle Cloud + Cloudflare R2 + SQLite + GitHub Backup
Cost: £0-£2/month for 500,000+ users
"""

import os
import sqlite3
import json
import tempfile
import shutil
import subprocess
import threading
import time
import gzip
import pickle
from datetime import datetime, timedelta
from collections import defaultdict, OrderedDict
from functools import wraps
from flask import Flask, request, jsonify, render_template, send_file, abort
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from logging.handlers import RotatingFileHandler
import psutil
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import boto3
from botocore.exceptions import ClientError

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Setup logging
def setup_logging():
    """Setup application logging"""
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s',
        handlers=[
            RotatingFileHandler('logs/app.log', maxBytes=10000000, backupCount=5),
            logging.StreamHandler()
        ]
    )

setup_logging()

# Global error monitor
class ErrorMonitor:
    def __init__(self):
        self.errors = defaultdict(int)
        self.total_requests = 0
        self.last_reset = time.time()
    
    def log_error(self, error_type):
        """Log an error"""
        self.errors[error_type] += 1
        self.total_requests += 1
    
    def log_request(self):
        """Log a successful request"""
        self.total_requests += 1
    
    def get_error_rate(self):
        """Calculate error rate"""
        if self.total_requests == 0:
            return 0
        total_errors = sum(self.errors.values())
        return (total_errors / self.total_requests) * 100
    
    def reset_metrics(self):
        """Reset metrics (call daily)"""
        self.errors.clear()
        self.total_requests = 0
        self.last_reset = time.time()

error_monitor = ErrorMonitor()

# Ultra Cache (In-Memory with Compression)
class UltraCache:
    def __init__(self, max_size_mb=50):
        self.cache = OrderedDict()
        self.max_size = max_size_mb * 1024 * 1024
        self.current_size = 0
        self.lock = threading.Lock()
    
    def get(self, key):
        """Get value from cache"""
        with self.lock:
            if key in self.cache:
                # Move to end (LRU)
                value = self.cache.pop(key)
                self.cache[key] = value
                return value
            return None
    
    def set(self, key, value, ttl=3600):
        """Set value in cache with compression"""
        with self.lock:
            # Compress data
            compressed_data = gzip.compress(pickle.dumps(value))
            data_size = len(compressed_data)
            
            # Remove old entry if exists
            if key in self.cache:
                old_data = self.cache.pop(key)
                self.current_size -= len(old_data)
            
            # Evict if needed
            while self.current_size + data_size > self.max_size and self.cache:
                _, old_data = self.cache.popitem(last=False)
                self.current_size -= len(old_data)
            
            # Add new entry
            self.cache[key] = compressed_data
            self.current_size += data_size
    
    def clear(self):
        """Clear cache"""
        with self.lock:
            self.cache.clear()
            self.current_size = 0

ultra_cache = UltraCache(max_size_mb=50)

# SQLite Database Manager
class SQLiteManager:
    def __init__(self, db_path='questions.db'):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database with optimizations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # SQLite optimizations
        cursor.execute('PRAGMA journal_mode=WAL')
        cursor.execute('PRAGMA synchronous=NORMAL')
        cursor.execute('PRAGMA cache_size=10000')
        cursor.execute('PRAGMA temp_store=MEMORY')
        cursor.execute('PRAGMA mmap_size=268435456')  # 256MB
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                topic TEXT NOT NULL,
                year_group TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                question_text TEXT NOT NULL,
                options TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                explanation TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_questions_lookup 
            ON questions(subject, topic, year_group, difficulty)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_questions_subject 
            ON questions(subject)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_questions_topic 
            ON questions(topic)
        ''')
        
        conn.commit()
        conn.close()
    
    def get_questions(self, subject, topic, year_group, difficulty, limit=10):
        """Get questions from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT question_text, options, correct_answer, explanation
            FROM questions 
            WHERE subject = ? AND topic = ? AND year_group = ? AND difficulty = ?
            ORDER BY RANDOM()
            LIMIT ?
        '''
        
        cursor.execute(query, (subject, topic, year_group, difficulty, limit))
        results = cursor.fetchall()
        conn.close()
        
        questions = []
        for row in results:
            question_text, options_json, correct_answer, explanation = row
            options = json.loads(options_json)
            questions.append({
                'question': question_text,
                'options': options,
                'correct_answer': correct_answer,
                'explanation': explanation
            })
        
        return questions
    
    def add_question(self, subject, topic, year_group, difficulty, question_text, options, correct_answer, explanation=None):
        """Add question to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            INSERT INTO questions (subject, topic, year_group, difficulty, question_text, options, correct_answer, explanation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        cursor.execute(query, (subject, topic, year_group, difficulty, question_text, json.dumps(options), correct_answer, explanation))
        conn.commit()
        conn.close()
    
    def get_stats(self):
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM questions')
        total_questions = cursor.fetchone()[0]
        
        cursor.execute('SELECT subject, COUNT(*) FROM questions GROUP BY subject')
        subject_stats = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'total_questions': total_questions,
            'subject_stats': subject_stats,
            'db_size_mb': os.path.getsize(self.db_path) / (1024 * 1024)
        }

db_manager = SQLiteManager()

# Cloudflare R2 Storage Manager
class R2StorageManager:
    def __init__(self):
        self.bucket_name = os.getenv('R2_BUCKET_NAME', 'kids-practice-pdf')
        self.account_id = os.getenv('R2_ACCOUNT_ID')
        self.access_key_id = os.getenv('R2_ACCESS_KEY_ID')
        self.secret_access_key = os.getenv('R2_SECRET_ACCESS_KEY')
        
        if all([self.account_id, self.access_key_id, self.secret_access_key]):
            self.s3_client = boto3.client(
                's3',
                endpoint_url=f'https://{self.account_id}.r2.cloudflarestorage.com',
                aws_access_key_id=self.access_key_id,
                aws_secret_access_key=self.secret_access_key
            )
            self.storage_available = True
        else:
            self.storage_available = False
            logging.warning("R2 credentials not configured, using local storage")
        
        # Local cache directory
        self.local_cache_dir = '/tmp/pdf_cache'
        os.makedirs(self.local_cache_dir, exist_ok=True)
    
    def upload_pdf(self, file_path, user_id, subject, topic):
        """Upload PDF to R2 storage"""
        if not self.storage_available:
            return self._local_fallback(file_path, user_id)
        
        try:
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"pdfs/{user_id}/{subject}/{topic}/{timestamp}.pdf"
            
            # Compress PDF
            compressed_path = self._compress_pdf(file_path)
            
            # Upload to R2
            with open(compressed_path, 'rb') as file:
                self.s3_client.upload_fileobj(
                    file, 
                    self.bucket_name, 
                    filename,
                    ExtraArgs={'ContentEncoding': 'gzip', 'ContentType': 'application/pdf'}
                )
            
            # Clean up compressed file
            os.remove(compressed_path)
            
            # Generate download URL
            download_url = f"https://{self.bucket_name}.r2.cloudflarestorage.com/{filename}"
            
            logging.info(f"PDF uploaded to R2: {filename}")
            return download_url
            
        except Exception as e:
            logging.error(f"R2 upload failed: {e}")
            return self._local_fallback(file_path, user_id)
    
    def _compress_pdf(self, file_path):
        """Compress PDF file"""
        compressed_path = file_path + '.gz'
        with open(file_path, 'rb') as f_in:
            with gzip.open(compressed_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        return compressed_path
    
    def _local_fallback(self, file_path, user_id):
        """Local storage fallback"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        local_filename = f"{user_id}_{timestamp}.pdf"
        local_path = os.path.join(self.local_cache_dir, local_filename)
        
        shutil.copy2(file_path, local_path)
        logging.info(f"PDF stored locally: {local_path}")
        return local_path
    
    def cleanup_old_files(self, days=7):
        """Clean up old files"""
        if not self.storage_available:
            return
        
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # List objects in bucket
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            
            for obj in response.get('Contents', []):
                if obj['LastModified'].replace(tzinfo=None) < cutoff_date:
                    self.s3_client.delete_object(Bucket=self.bucket_name, Key=obj['Key'])
                    logging.info(f"Deleted old file: {obj['Key']}")
        
        except Exception as e:
            logging.error(f"Cleanup failed: {e}")

r2_storage = R2StorageManager()

# PDF Generator
class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom styles"""
        self.styles.add(ParagraphStyle(
            name='QuestionStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=12,
            spaceBefore=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='OptionStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            leftIndent=20,
            spaceAfter=6
        ))
    
    def generate_worksheet(self, questions, subject, topic, year_group, difficulty):
        """Generate PDF worksheet"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_file.close()
        
        doc = SimpleDocTemplate(temp_file.name, pagesize=A4)
        story = []
        
        # Header
        header_text = f"{subject.title()} - {topic.title()} - Year {year_group} - {difficulty.title()}"
        story.append(Paragraph(header_text, self.styles['Title']))
        story.append(Spacer(1, 20))
        
        # Questions
        for i, question_data in enumerate(questions, 1):
            # Question
            question_text = f"Question {i}: {question_data['question']}"
            story.append(Paragraph(question_text, self.styles['QuestionStyle']))
            
            # Options
            for j, option in enumerate(question_data['options'], 1):
                option_text = f"{chr(64+j)}. {option}"
                story.append(Paragraph(option_text, self.styles['OptionStyle']))
            
            story.append(Spacer(1, 15))
        
        doc.build(story)
        return temp_file.name
    
    def generate_answer_key(self, questions, subject, topic, year_group, difficulty):
        """Generate PDF answer key"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_file.close()
        
        doc = SimpleDocTemplate(temp_file.name, pagesize=A4)
        story = []
        
        # Header
        header_text = f"Answer Key - {subject.title()} - {topic.title()} - Year {year_group} - {difficulty.title()}"
        story.append(Paragraph(header_text, self.styles['Title']))
        story.append(Spacer(1, 20))
        
        # Answers
        for i, question_data in enumerate(questions, 1):
            # Question and answer
            answer_text = f"Question {i}: {question_data['correct_answer']}"
            story.append(Paragraph(answer_text, self.styles['QuestionStyle']))
            
            # Explanation if available
            if question_data.get('explanation'):
                explanation_text = f"Explanation: {question_data['explanation']}"
                story.append(Paragraph(explanation_text, self.styles['OptionStyle']))
            
            story.append(Spacer(1, 15))
        
        doc.build(story)
        return temp_file.name

pdf_generator = PDFGenerator()

# Backup Manager
class BackupManager:
    def __init__(self, backup_dir='backups'):
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
    
    def backup_database(self):
        """Backup database to GitHub"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(self.backup_dir, f"questions_{timestamp}.db")
            
            # Copy database file
            shutil.copy2('questions.db', backup_file)
            
            # Git operations
            subprocess.run(['git', 'add', backup_file], check=True)
            subprocess.run(['git', 'commit', '-m', f'Database backup {timestamp}'], check=True)
            subprocess.run(['git', 'push'], check=True)
            
            # Clean old backups (keep last 7 days)
            self._cleanup_old_backups(days=7)
            
            logging.info(f"Database backup completed: {backup_file}")
            return True
            
        except Exception as e:
            logging.error(f"Database backup failed: {e}")
            return False
    
    def _cleanup_old_backups(self, days=7):
        """Clean up old backup files"""
        cutoff_time = time.time() - (days * 24 * 60 * 60)
        
        for filename in os.listdir(self.backup_dir):
            file_path = os.path.join(self.backup_dir, filename)
            if os.path.getmtime(file_path) < cutoff_time:
                os.remove(file_path)
                logging.info(f"Deleted old backup: {filename}")

backup_manager = BackupManager()

# Performance monitoring decorator
def monitor_response_time(func):
    """Decorator to monitor response times"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to ms
        logging.info(f"{func.__name__} response time: {response_time:.2f}ms")
        
        # Alert if response time is too high
        if response_time > 5000:  # 5 seconds
            logging.warning(f"Slow response time: {response_time:.2f}ms for {func.__name__}")
        
        return result
    return wrapper

# Routes
@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Check database
        db_stats = db_manager.get_stats()
        
        # Check memory
        memory_percent = psutil.virtual_memory().percent
        
        # Check disk
        disk_percent = psutil.disk_usage('/').percent
        
        # Check error rate
        error_rate = error_monitor.get_error_rate()
        
        status = 'healthy' if all([
            db_stats['total_questions'] > 0,
            memory_percent < 90,
            disk_percent < 90,
            error_rate < 5
        ]) else 'unhealthy'
        
        return {
            'status': status,
            'timestamp': datetime.now().isoformat(),
            'database': db_stats,
            'system': {
                'memory_percent': memory_percent,
                'disk_percent': disk_percent,
                'error_rate': error_rate
            }
        }
    
    except Exception as e:
        logging.error(f"Health check failed: {e}")
        return {'status': 'error', 'error': str(e)}, 500

@app.route('/dashboard')
def dashboard():
    """Monitoring dashboard"""
    try:
        # System metrics
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent
        
        # Application metrics
        error_rate = error_monitor.get_error_rate()
        db_stats = db_manager.get_stats()
        
        return {
            'system': {
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'disk_percent': disk_percent
            },
            'application': {
                'error_rate': error_rate,
                'db_size_mb': db_stats['db_size_mb'],
                'total_questions': db_stats['total_questions']
            },
            'storage': {
                'r2_available': r2_storage.storage_available
            },
            'timestamp': datetime.now().isoformat()
        }
    
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/get_topics/<subject>')
@limiter.limit("100 per hour")
@monitor_response_time
def get_topics(subject):
    """Get topics for a subject"""
    try:
        error_monitor.log_request()
        
        # Cache key
        cache_key = f"topics:{subject}"
        cached_topics = ultra_cache.get(cache_key)
        if cached_topics:
            return jsonify(cached_topics)
        
        # Get topics from database
        conn = sqlite3.connect(db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT topic FROM questions WHERE subject = ?', (subject,))
        topics = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        # Cache results
        ultra_cache.set(cache_key, topics, ttl=3600)
        
        return jsonify(topics)
    
    except Exception as e:
        error_monitor.log_error('get_topics')
        logging.error(f"Get topics failed: {e}")
        return jsonify([])

@app.route('/preview_questions', methods=['POST'])
@limiter.limit("50 per hour")
@monitor_response_time
def preview_questions():
    """Preview questions"""
    try:
        error_monitor.log_request()
        
        data = request.get_json()
        subject = data.get('subject')
        topic = data.get('topic')
        year_group = data.get('year_group')
        difficulty = data.get('difficulty')
        num_questions = min(int(data.get('num_questions', 5)), 10)
        
        # Cache key
        cache_key = f"questions:{subject}:{topic}:{year_group}:{difficulty}:{num_questions}"
        cached_questions = ultra_cache.get(cache_key)
        if cached_questions:
            return jsonify(cached_questions)
        
        # Get questions from database
        questions = db_manager.get_questions(subject, topic, year_group, difficulty, num_questions)
        
        if not questions:
            return jsonify({'error': 'No questions found'}), 404
        
        # Cache results
        ultra_cache.set(cache_key, questions, ttl=1800)  # 30 minutes
        
        return jsonify(questions)
    
    except Exception as e:
        error_monitor.log_error('preview_questions')
        logging.error(f"Preview questions failed: {e}")
        return jsonify({'error': 'Failed to get questions'}), 500

@app.route('/generate_worksheet', methods=['POST'])
@limiter.limit("20 per hour")
@monitor_response_time
def generate_worksheet():
    """Generate PDF worksheet"""
    try:
        error_monitor.log_request()
        
        data = request.get_json()
        questions = data.get('questions', [])
        subject = data.get('subject')
        topic = data.get('topic')
        year_group = data.get('year_group')
        difficulty = data.get('difficulty')
        
        if not questions:
            return jsonify({'error': 'No questions provided'}), 400
        
        # Generate PDF
        pdf_path = pdf_generator.generate_worksheet(questions, subject, topic, year_group, difficulty)
        
        # Upload to R2
        user_id = request.remote_addr
        download_url = r2_storage.upload_pdf(pdf_path, user_id, subject, topic)
        
        # Clean up temp file
        os.unlink(pdf_path)
        
        return jsonify({
            'success': True,
            'download_url': download_url,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        error_monitor.log_error('generate_worksheet')
        logging.error(f"Generate worksheet failed: {e}")
        return jsonify({'error': 'Failed to generate worksheet'}), 500

@app.route('/generate_answer_key', methods=['POST'])
@limiter.limit("20 per hour")
@monitor_response_time
def generate_answer_key():
    """Generate PDF answer key"""
    try:
        error_monitor.log_request()
        
        data = request.get_json()
        questions = data.get('questions', [])
        subject = data.get('subject')
        topic = data.get('topic')
        year_group = data.get('year_group')
        difficulty = data.get('difficulty')
        
        if not questions:
            return jsonify({'error': 'No questions provided'}), 400
        
        # Generate PDF
        pdf_path = pdf_generator.generate_answer_key(questions, subject, topic, year_group, difficulty)
        
        # Upload to R2
        user_id = request.remote_addr
        download_url = r2_storage.upload_pdf(pdf_path, user_id, subject, topic)
        
        # Clean up temp file
        os.unlink(pdf_path)
        
        return jsonify({
            'success': True,
            'download_url': download_url,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        error_monitor.log_error('generate_answer_key')
        logging.error(f"Generate answer key failed: {e}")
        return jsonify({'error': 'Failed to generate answer key'}), 500

@app.route('/backup', methods=['POST'])
def trigger_backup():
    """Trigger manual backup"""
    try:
        success = backup_manager.backup_database()
        if success:
            return jsonify({'success': True, 'message': 'Backup completed'})
        else:
            return jsonify({'error': 'Backup failed'}), 500
    except Exception as e:
        logging.error(f"Manual backup failed: {e}")
        return jsonify({'error': 'Backup failed'}), 500

@app.route('/cleanup', methods=['POST'])
def cleanup_old_files():
    """Clean up old files"""
    try:
        r2_storage.cleanup_old_files(days=7)
        return jsonify({'success': True, 'message': 'Cleanup completed'})
    except Exception as e:
        logging.error(f"Cleanup failed: {e}")
        return jsonify({'error': 'Cleanup failed'}), 500

# Background tasks
def background_cleanup():
    """Background cleanup task"""
    while True:
        try:
            time.sleep(24 * 60 * 60)  # Run daily
            r2_storage.cleanup_old_files(days=7)
            logging.info("Background cleanup completed")
        except Exception as e:
            logging.error(f"Background cleanup failed: {e}")

def background_backup():
    """Background backup task"""
    while True:
        try:
            time.sleep(24 * 60 * 60)  # Run daily
            backup_manager.backup_database()
            logging.info("Background backup completed")
        except Exception as e:
            logging.error(f"Background backup failed: {e}")

# Start background threads
cleanup_thread = threading.Thread(target=background_cleanup, daemon=True)
cleanup_thread.start()

backup_thread = threading.Thread(target=background_backup, daemon=True)
backup_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
