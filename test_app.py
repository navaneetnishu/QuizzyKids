#!/usr/bin/env python3
"""
Test script for the Kids Practice PDF Generator
"""

from question_bank import QuestionBank
from pdf_generator import PDFGenerator
import tempfile
import os

def test_question_generation():
    """Test question generation for different subjects and topics"""
    print("🧪 Testing Question Generation...")
    
    qb = QuestionBank()
    
    # Test subjects
    subjects = qb.get_subjects()
    print(f"✅ Available subjects: {list(subjects.keys())}")
    
    # Test topics for maths
    maths_topics = qb.get_topics('maths')
    print(f"✅ Maths topics: {list(maths_topics.keys())}")
    
    # Test question generation
    test_cases = [
        ('maths', 'place_value', 'Year 3', 'Medium', 5),
        ('maths', 'addition_subtraction', 'Year 2', 'Easy', 3),
        ('maths', 'multiplication_division', 'Year 4', 'Hard', 4),
    ]
    
    for subject, topic, year_group, difficulty, num_questions in test_cases:
        print(f"\n📝 Testing: {subject} - {topic} - {year_group} - {difficulty}")
        
        questions = qb.generate_questions(subject, topic, year_group, difficulty, num_questions)
        
        if questions:
            print(f"✅ Generated {len(questions)} questions")
            print(f"   Sample question: {questions[0]['question']}")
            print(f"   Options: {questions[0]['options']}")
            print(f"   Correct answer: {questions[0]['correct_answer']}")
        else:
            print(f"❌ No questions generated")

def test_pdf_generation():
    """Test PDF generation"""
    print("\n📄 Testing PDF Generation...")
    
    qb = QuestionBank()
    pdf_gen = PDFGenerator()
    
    # Generate some test questions
    questions = qb.generate_questions('maths', 'place_value', 'Year 3', 'Medium', 3)
    
    if questions:
        # Create temporary files
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as worksheet_file:
            worksheet_path = worksheet_file.name
            
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as answer_file:
            answer_path = answer_file.name
        
        try:
            # Generate PDFs
            pdf_gen.generate_worksheet(questions, 'maths', 'place_value', 'Year 3', 'Medium', worksheet_path)
            pdf_gen.generate_answer_key(questions, 'maths', 'place_value', 'Year 3', 'Medium', answer_path)
            
            # Check if files were created
            if os.path.exists(worksheet_path):
                print(f"✅ Worksheet PDF created: {worksheet_path}")
                print(f"   File size: {os.path.getsize(worksheet_path)} bytes")
            else:
                print("❌ Worksheet PDF not created")
                
            if os.path.exists(answer_path):
                print(f"✅ Answer key PDF created: {answer_path}")
                print(f"   File size: {os.path.getsize(answer_path)} bytes")
            else:
                print("❌ Answer key PDF not created")
                
        except Exception as e:
            print(f"❌ PDF generation error: {e}")
        finally:
            # Clean up temporary files
            try:
                os.unlink(worksheet_path)
                os.unlink(answer_path)
            except:
                pass

def test_preview_generation():
    """Test HTML preview generation"""
    print("\n👀 Testing Preview Generation...")
    
    qb = QuestionBank()
    pdf_gen = PDFGenerator()
    
    questions = qb.generate_questions('maths', 'fractions_decimals', 'Year 5', 'Hard', 2)
    
    if questions:
        # Generate HTML preview
        html_preview = pdf_gen.generate_preview_worksheet(questions, 'maths', 'fractions_decimals', 'Year 5', 'Hard')
        html_answer = pdf_gen.generate_preview_answer_key(questions, 'maths', 'fractions_decimals', 'Year 5', 'Hard')
        
        print(f"✅ HTML preview generated ({len(html_preview)} characters)")
        print(f"✅ HTML answer key generated ({len(html_answer)} characters)")
        
        # Save preview to file for inspection
        with open('test_preview.html', 'w', encoding='utf-8') as f:
            f.write(html_preview)
        print("💾 Preview saved to test_preview.html")

if __name__ == "__main__":
    print("🎓 Kids Practice PDF Generator - Test Suite")
    print("=" * 50)
    
    test_question_generation()
    test_pdf_generation()
    test_preview_generation()
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print("\n🚀 To run the web application:")
    print("   python app.py")
    print("   Then open http://localhost:5000 in your browser")
