from flask import Flask, render_template, request, send_file, jsonify
from pdf_generator import PDFGenerator
from question_bank import QuestionBank
import os
import tempfile
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialize question bank and PDF generator
question_bank = QuestionBank()
pdf_generator = PDFGenerator()

@app.route('/')
def index():
    """Main page with subject and topic selection"""
    subjects = question_bank.get_subjects()
    return render_template('index.html', subjects=subjects)

@app.route('/get_topics/<subject>')
def get_topics(subject):
    """Get topics for a specific subject"""
    topics = question_bank.get_topics(subject)
    return jsonify(topics)

@app.route('/generate_worksheet', methods=['POST'])
def generate_worksheet():
    """Generate PDF worksheet based on user selections"""
    try:
        data = request.get_json()
        subject = data.get('subject')
        topic = data.get('topic')
        year_group = data.get('year_group')
        difficulty = data.get('difficulty')
        num_questions = int(data.get('num_questions', 10))
        
        # Generate questions
        questions = question_bank.generate_questions(
            subject, topic, year_group, difficulty, num_questions
        )
        
        if not questions:
            return jsonify({'error': 'No questions available for the selected criteria'}), 400
        
        # Generate PDF files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as worksheet_file:
            worksheet_path = worksheet_file.name
            
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as answer_file:
            answer_path = answer_file.name
        
        # Generate worksheet PDF
        pdf_generator.generate_worksheet(
            questions, subject, topic, year_group, difficulty, worksheet_path
        )
        
        # Generate answer key PDF
        pdf_generator.generate_answer_key(
            questions, subject, topic, year_group, difficulty, answer_path
        )
        
        return jsonify({
            'success': True,
            'worksheet_path': worksheet_path,
            'answer_path': answer_path,
            'timestamp': timestamp
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<file_type>/<timestamp>')
def download_file(file_type, timestamp):
    """Download generated PDF files"""
    try:
        if file_type == 'worksheet':
            file_path = request.args.get('path')
            filename = f"worksheet_{timestamp}.pdf"
        elif file_type == 'answer':
            file_path = request.args.get('path')
            filename = f"answer_key_{timestamp}.pdf"
        else:
            return jsonify({'error': 'Invalid file type'}), 400
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(file_path, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/preview_questions', methods=['POST'])
def preview_questions():
    """Preview questions without generating PDF"""
    try:
        data = request.get_json()
        subject = data.get('subject')
        topic = data.get('topic')
        year_group = data.get('year_group')
        difficulty = data.get('difficulty')
        num_questions = int(data.get('num_questions', 5))
        
        questions = question_bank.generate_questions(
            subject, topic, year_group, difficulty, num_questions
        )
        
        return jsonify({
            'success': True,
            'questions': questions
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
