#!/usr/bin/env python3
"""
Production-optimized Flask app for cost-effective scaling
Target: $30-40/month with 10k+ concurrent users
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sqlite3
import redis
import os
import json
import tempfile
import threading
from datetime import datetime, timedelta
import hashlib
from pdf_generator import PDFGenerator
from question_bank import QuestionBank

app = Flask(__name__)
CORS(app)

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Redis for caching (free tier)
try:
    redis_client = redis.Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        password=os.getenv('REDIS_PASSWORD', None),
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=5
    )
    redis_client.ping()
    REDIS_AVAILABLE = True
except:
    REDIS_AVAILABLE = False
    print("⚠️ Redis not available, using in-memory cache")

# In-memory cache fallback
memory_cache = {}
cache_lock = threading.Lock()

class CostOptimizedQuestionBank:
    def __init__(self):
        self.question_bank = QuestionBank()
        self.db_path = 'questions.db'
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database for questions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
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
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_questions_lookup 
            ON questions(subject, topic, year_group, difficulty)
        ''')
        
        conn.commit()
        conn.close()
    
    def get_questions(self, subject, topic, year_group, difficulty, num_questions):
        """Get questions with caching"""
        cache_key = f"questions:{subject}:{topic}:{year_group}:{difficulty}:{num_questions}"
        
        # Try Redis cache first
        if REDIS_AVAILABLE:
            try:
                cached = redis_client.get(cache_key)
                if cached:
                    return json.loads(cached)
            except:
                pass
        
        # Try memory cache
        with cache_lock:
            if cache_key in memory_cache:
                cache_data = memory_cache[cache_key]
                if datetime.now() - cache_data['timestamp'] < timedelta(hours=1):
                    return cache_data['data']
        
        # Get from database
        questions = self._get_from_database(subject, topic, year_group, difficulty, num_questions)
        
        # Fallback to generated questions
        if not questions:
            questions = self.question_bank.generate_questions(
                subject, topic, year_group, difficulty, num_questions
            )
        
        # Cache the result
        if REDIS_AVAILABLE:
            try:
                redis_client.setex(cache_key, 3600, json.dumps(questions))  # 1 hour cache
            except:
                pass
        
        with cache_lock:
            memory_cache[cache_key] = {
                'data': questions,
                'timestamp': datetime.now()
            }
        
        return questions
    
    def _get_from_database(self, subject, topic, year_group, difficulty, num_questions):
        """Get questions from SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
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
question_bank = CostOptimizedQuestionBank()
pdf_generator = PDFGenerator()

# PDF generation queue (simple in-memory queue)
pdf_queue = []
queue_lock = threading.Lock()

def process_pdf_queue():
    """Background PDF processing"""
    while True:
        with queue_lock:
            if pdf_queue:
                task = pdf_queue.pop(0)
            else:
                continue
        
        try:
            # Generate PDF
            pdf_path = pdf_generator.generate_worksheet(
                task['questions'], 
                task['subject'], 
                task['topic']
            )
            
            # Store in cloud storage (Backblaze B2)
            cloud_url = upload_to_cloud_storage(pdf_path, task['user_id'])
            
            # Update task status
            task['status'] = 'completed'
            task['download_url'] = cloud_url
            
        except Exception as e:
            task['status'] = 'failed'
            task['error'] = str(e)

# Start background worker
pdf_worker = threading.Thread(target=process_pdf_queue, daemon=True)
pdf_worker.start()

def upload_to_cloud_storage(file_path, user_id):
    """Upload PDF to Backblaze B2 (cost-effective cloud storage)"""
    # Implementation for Backblaze B2 upload
    # This would use b2sdk library
    filename = f"worksheets/{user_id}/{os.path.basename(file_path)}"
    
    # For now, return a placeholder
    return f"https://storage.backblazeb2.com/b2api/v1/b2_download_file_by_id?fileId={filename}"

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/get_topics/<subject>')
@limiter.limit("100 per minute")
def get_topics(subject):
    """Get topics for a subject"""
    cache_key = f"topics:{subject}"
    
    if REDIS_AVAILABLE:
        try:
            cached = redis_client.get(cache_key)
            if cached:
                return jsonify(json.loads(cached))
        except:
            pass
    
    topics = question_bank.question_bank.subjects.get(subject, {}).get('topics', [])
    
    if REDIS_AVAILABLE:
        try:
            redis_client.setex(cache_key, 3600, json.dumps(topics))
        except:
            pass
    
    return jsonify(topics)

@app.route('/preview_questions', methods=['POST'])
@limiter.limit("30 per minute")
def preview_questions():
    """Preview questions with caching"""
    data = request.get_json()
    
    cache_key = f"preview:{hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()}"
    
    if REDIS_AVAILABLE:
        try:
            cached = redis_client.get(cache_key)
            if cached:
                return jsonify(json.loads(cached))
        except:
            pass
    
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
    
    if REDIS_AVAILABLE:
        try:
            redis_client.setex(cache_key, 1800, json.dumps(response))  # 30 min cache
        except:
            pass
    
    return jsonify(response)

@app.route('/generate_worksheet', methods=['POST'])
@limiter.limit("10 per minute")
def generate_worksheet():
    """Generate worksheet asynchronously"""
    data = request.get_json()
    
    # Generate unique task ID
    task_id = hashlib.md5(f"{datetime.now()}{data}".encode()).hexdigest()
    
    # Add to processing queue
    with queue_lock:
        pdf_queue.append({
            'task_id': task_id,
            'questions': data['questions'],
            'subject': data['subject'],
            'topic': data['topic'],
            'user_id': request.remote_addr,
            'status': 'processing',
            'timestamp': datetime.now()
        })
    
    return jsonify({
        'success': True,
        'task_id': task_id,
        'status': 'processing',
        'message': 'PDF is being generated...'
    })

@app.route('/pdf_status/<task_id>')
@limiter.limit("60 per minute")
def pdf_status(task_id):
    """Check PDF generation status"""
    with queue_lock:
        for task in pdf_queue:
            if task['task_id'] == task_id:
                return jsonify({
                    'status': task['status'],
                    'download_url': task.get('download_url'),
                    'error': task.get('error')
                })
    
    return jsonify({'status': 'not_found'})

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'redis_available': REDIS_AVAILABLE,
        'queue_size': len(pdf_queue)
    })

if __name__ == '__main__':
    # Production server configuration
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=False,
        threaded=True
    )
