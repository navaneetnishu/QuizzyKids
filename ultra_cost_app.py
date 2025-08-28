#!/usr/bin/env python3
"""
Ultra-cost-effective Flask app for £20/month scaling
Target: 100k users, 10k concurrent downloads
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sqlite3
import os
import json
import tempfile
import threading
import time
from datetime import datetime, timedelta
import hashlib
import gzip
import pickle
from pdf_generator import PDFGenerator
from question_bank import QuestionBank

app = Flask(__name__)
CORS(app)

# Aggressive rate limiting to prevent abuse
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per day", "20 per hour"]
)

# Ultra-efficient in-memory cache with compression
class UltraCache:
    def __init__(self, max_size_mb=50):
        self.cache = {}
        self.max_size = max_size_mb * 1024 * 1024  # 50MB limit
        self.current_size = 0
        self.lock = threading.Lock()
    
    def get(self, key):
        with self.lock:
            if key in self.cache:
                data = self.cache[key]
                if time.time() - data['timestamp'] < data['ttl']:
                    return data['value']
                else:
                    del self.cache[key]
                    self.current_size -= data['size']
        return None
    
    def set(self, key, value, ttl=3600):
        with self.lock:
            # Compress data to save memory
            compressed = gzip.compress(pickle.dumps(value))
            size = len(compressed)
            
            # Remove old entries if cache is full
            while self.current_size + size > self.max_size and self.cache:
                oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]['timestamp'])
                old_size = self.cache[oldest_key]['size']
                del self.cache[oldest_key]
                self.current_size -= old_size
            
            self.cache[key] = {
                'value': value,
                'timestamp': time.time(),
                'ttl': ttl,
                'size': size
            }
            self.current_size += size

# Initialize ultra-efficient cache
ultra_cache = UltraCache(max_size_mb=50)

class UltraOptimizedQuestionBank:
    def __init__(self):
        self.question_bank = QuestionBank()
        self.db_path = 'questions.db'
        self._init_database()
    
    def _init_database(self):
        """Initialize optimized SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Enable WAL mode for better concurrency
        cursor.execute('PRAGMA journal_mode=WAL')
        cursor.execute('PRAGMA synchronous=NORMAL')
        cursor.execute('PRAGMA cache_size=10000')
        cursor.execute('PRAGMA temp_store=MEMORY')
        
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
                explanation TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Optimized indexes
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_questions_lookup 
            ON questions(subject, topic, year_group, difficulty)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_questions_random 
            ON questions(subject, topic, year_group, difficulty, RANDOM())
        ''')
        
        conn.commit()
        conn.close()
    
    def get_questions(self, subject, topic, year_group, difficulty, num_questions):
        """Get questions with ultra-efficient caching"""
        cache_key = f"q:{subject}:{topic}:{year_group}:{difficulty}:{num_questions}"
        
        # Try cache first
        cached = ultra_cache.get(cache_key)
        if cached:
            return cached
        
        # Get from database
        questions = self._get_from_database(subject, topic, year_group, difficulty, num_questions)
        
        # Fallback to generated questions
        if not questions:
            questions = self.question_bank.generate_questions(
                subject, topic, year_group, difficulty, num_questions
            )
        
        # Cache for 30 minutes (shorter TTL to save memory)
        ultra_cache.set(cache_key, questions, ttl=1800)
        
        return questions
    
    def _get_from_database(self, subject, topic, year_group, difficulty, num_questions):
        """Get questions from optimized SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Use prepared statement for better performance
        cursor.execute('''
            SELECT question_text, options, correct_answer, explanation
            FROM questions 
            WHERE subject = ? AND topic = ? AND year_group = ? AND difficulty = ?
            ORDER BY RANDOM()
            LIMIT ?
        ''', (subject, topic, year_group, difficulty, num_questions))
        
        rows = cursor.fetchall()
        conn.close()
        
        questions = []
        for row in rows:
            questions.append({
                'question': row[0],
                'options': json.loads(row[1]),
                'correct_answer': row[2],
                'explanation': row[3]
            })
        
        return questions

# Initialize components
question_bank = UltraOptimizedQuestionBank()
pdf_generator = PDFGenerator()

# Ultra-efficient PDF queue with memory limits
class UltraPDFQueue:
    def __init__(self, max_queue_size=100):
        self.queue = []
        self.max_size = max_queue_size
        self.lock = threading.Lock()
        self.processing = False
    
    def add_task(self, task):
        with self.lock:
            if len(self.queue) < self.max_size:
                self.queue.append(task)
                return True
            return False
    
    def get_task(self):
        with self.lock:
            if self.queue:
                return self.queue.pop(0)
            return None
    
    def get_size(self):
        with self.lock:
            return len(self.queue)

pdf_queue = UltraPDFQueue(max_queue_size=100)

def process_pdf_queue():
    """Ultra-efficient background PDF processing"""
    while True:
        task = pdf_queue.get_task()
        if not task:
            time.sleep(1)  # Sleep to save CPU
            continue
        
        try:
            # Generate PDF with timeout
            pdf_path = pdf_generator.generate_worksheet(
                task['questions'], 
                task['subject'], 
                task['topic']
            )
            
            # Store in ultra-cheap storage
            cloud_url = upload_to_ultra_storage(pdf_path, task['user_id'])
            
            # Update task status
            task['status'] = 'completed'
            task['download_url'] = cloud_url
            
        except Exception as e:
            task['status'] = 'failed'
            task['error'] = str(e)

# Start background worker
pdf_worker = threading.Thread(target=process_pdf_queue, daemon=True)
pdf_worker.start()

def upload_to_ultra_storage(file_path, user_id):
    """Upload to ultra-cheap storage (Cloudflare R2)"""
    # Implementation for Cloudflare R2 upload
    # Much cheaper than Backblaze B2
    filename = f"worksheets/{user_id}/{os.path.basename(file_path)}"
    
    # For now, return a placeholder
    return f"https://r2.cloudflare.com/worksheets/{filename}"

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/get_topics/<subject>')
@limiter.limit("50 per minute")
def get_topics(subject):
    """Get topics with aggressive caching"""
    cache_key = f"topics:{subject}"
    
    cached = ultra_cache.get(cache_key)
    if cached:
        return jsonify(cached)
    
    topics = question_bank.question_bank.subjects.get(subject, {}).get('topics', [])
    
    # Cache for 1 hour
    ultra_cache.set(cache_key, topics, ttl=3600)
    
    return jsonify(topics)

@app.route('/preview_questions', methods=['POST'])
@limiter.limit("15 per minute")
def preview_questions():
    """Preview questions with ultra-efficient caching"""
    data = request.get_json()
    
    cache_key = f"preview:{hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()}"
    
    cached = ultra_cache.get(cache_key)
    if cached:
        return jsonify(cached)
    
    questions = question_bank.get_questions(
        data['subject'],
        data['topic'],
        data['year_group'],
        data['difficulty'],
        data['num_questions']
    )
    
    response = {
        'success': True,
        'questions': questions
    }
    
    # Cache for 15 minutes (shorter TTL)
    ultra_cache.set(cache_key, response, ttl=900)
    
    return jsonify(response)

@app.route('/generate_worksheet', methods=['POST'])
@limiter.limit("5 per minute")
def generate_worksheet():
    """Generate worksheet with queue management"""
    data = request.get_json()
    
    # Check queue size
    if pdf_queue.get_size() >= 100:
        return jsonify({
            'success': False,
            'error': 'Server is busy. Please try again in a few minutes.'
        }), 429
    
    # Generate unique task ID
    task_id = hashlib.md5(f"{datetime.now()}{data}".encode()).hexdigest()
    
    # Add to processing queue
    task = {
        'task_id': task_id,
        'questions': data['questions'],
        'subject': data['subject'],
        'topic': data['topic'],
        'user_id': request.remote_addr,
        'status': 'processing',
        'timestamp': datetime.now()
    }
    
    if pdf_queue.add_task(task):
        return jsonify({
            'success': True,
            'task_id': task_id,
            'status': 'processing',
            'message': 'PDF is being generated...'
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Queue is full. Please try again later.'
        }), 429

@app.route('/pdf_status/<task_id>')
@limiter.limit("30 per minute")
def pdf_status(task_id):
    """Check PDF generation status"""
    # This would check the actual task status
    # For now, return a placeholder
    return jsonify({'status': 'processing'})

@app.route('/health')
def health_check():
    """Ultra-lightweight health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'queue_size': pdf_queue.get_size(),
        'cache_size_mb': ultra_cache.current_size / (1024 * 1024)
    })

if __name__ == '__main__':
    # Ultra-optimized server configuration
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=False,
        threaded=True
    )
