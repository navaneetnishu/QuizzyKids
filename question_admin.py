#!/usr/bin/env python3
"""
Admin interface for managing questions in the database
"""

from question_database import QuestionDatabase, create_question, add_maths_question, add_science_question
import json

def print_menu():
    """Print the admin menu"""
    print("\n" + "="*50)
    print("🎓 Question Bank Admin Interface")
    print("="*50)
    print("1. Add a single question")
    print("2. Add multiple questions from file")
    print("3. View question statistics")
    print("4. List all questions")
    print("5. Quick add maths question")
    print("6. Quick add science question")
    print("7. Export questions to JSON")
    print("8. Exit")
    print("="*50)

def add_single_question():
    """Interactive function to add a single question"""
    print("\n📝 Adding a Single Question")
    print("-" * 30)
    
    # Get subject
    subject = input("Subject (maths/science/computing/history/geography): ").strip().lower()
    
    # Get topic
    topic = input("Topic (e.g., place_value, addition_subtraction): ").strip().lower()
    
    # Get year group
    year_group = input("Year Group (Year 1/Year 2/Year 3/Year 4/Year 5/Year 6): ").strip()
    
    # Get difficulty
    difficulty = input("Difficulty (Easy/Medium/Hard): ").strip()
    
    # Get question details
    question_text = input("Question text: ").strip()
    
    print("\nEnter 4 options:")
    options = []
    for i in range(4):
        option = input(f"Option {chr(65+i)}: ").strip()
        options.append(option)
    
    correct_answer = input("Correct answer (exact text): ").strip()
    explanation = input("Explanation: ").strip()
    
    # Create question
    question = create_question(question_text, options, correct_answer, explanation)
    
    # Add to database
    db = QuestionDatabase()
    success = db.add_question(subject, topic, year_group, difficulty, question)
    
    if success:
        print("✅ Question added successfully!")
    else:
        print("❌ Failed to add question.")

def add_questions_from_file():
    """Add multiple questions from a JSON file"""
    print("\n📁 Adding Questions from File")
    print("-" * 30)
    
    filename = input("Enter JSON file path: ").strip()
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        db = QuestionDatabase()
        success_count = 0
        total_count = 0
        
        # Expected format: list of question objects with subject, topic, etc.
        for question_obj in data:
            total_count += 1
            if db.add_question(
                question_obj['subject'],
                question_obj['topic'],
                question_obj['year_group'],
                question_obj['difficulty'],
                {
                    'question': question_obj['question'],
                    'options': question_obj['options'],
                    'correct_answer': question_obj['correct_answer'],
                    'explanation': question_obj['explanation']
                }
            ):
                success_count += 1
        
        print(f"✅ Added {success_count}/{total_count} questions successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def view_statistics():
    """View question statistics"""
    print("\n📊 Question Statistics")
    print("-" * 30)
    
    db = QuestionDatabase()
    stats = db.list_all_questions()
    
    for subject, topics in stats.items():
        print(f"\n📚 {subject.upper()}:")
        for topic, year_groups in topics.items():
            print(f"  📖 {topic}:")
            for year_group, difficulties in year_groups.items():
                print(f"    📅 {year_group}:")
                for difficulty, count in difficulties.items():
                    print(f"      🎯 {difficulty}: {count} questions")

def list_all_questions():
    """List all questions in detail"""
    print("\n📋 All Questions")
    print("-" * 30)
    
    db = QuestionDatabase()
    
    for subject in db.get_available_subjects():
        print(f"\n📚 {subject.upper()}:")
        topics = db.get_topics_for_subject(subject)
        
        for topic_key, topic_name in topics.items():
            print(f"  📖 {topic_name}:")
            
            for year_group in ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5', 'Year 6']:
                for difficulty in ['Easy', 'Medium', 'Hard']:
                    count = db.get_question_count(subject, topic_key, year_group, difficulty)
                    if count > 0:
                        print(f"    📅 {year_group} - {difficulty}: {count} questions")

def quick_add_maths():
    """Quick add a maths question"""
    print("\n🔢 Quick Add Maths Question")
    print("-" * 30)
    
    topic = input("Topic (place_value/addition_subtraction/multiplication_division/fractions_decimals/ratio_proportion/algebra/measurement/geometry_shape/geometry_position/statistics): ").strip()
    year_group = input("Year Group (Year 1-6): ").strip()
    difficulty = input("Difficulty (Easy/Medium/Hard): ").strip()
    question_text = input("Question: ").strip()
    
    print("Enter 4 options:")
    options = []
    for i in range(4):
        option = input(f"Option {chr(65+i)}: ").strip()
        options.append(option)
    
    correct_answer = input("Correct answer: ").strip()
    explanation = input("Explanation: ").strip()
    
    success = add_maths_question(topic, year_group, difficulty, question_text, options, correct_answer, explanation)
    
    if success:
        print("✅ Maths question added successfully!")
    else:
        print("❌ Failed to add question.")

def quick_add_science():
    """Quick add a science question"""
    print("\n🔬 Quick Add Science Question")
    print("-" * 30)
    
    topic = input("Topic (living_things/materials/forces/earth_space/light_sound): ").strip()
    year_group = input("Year Group (Year 1-6): ").strip()
    difficulty = input("Difficulty (Easy/Medium/Hard): ").strip()
    question_text = input("Question: ").strip()
    
    print("Enter 4 options:")
    options = []
    for i in range(4):
        option = input(f"Option {chr(65+i)}: ").strip()
        options.append(option)
    
    correct_answer = input("Correct answer: ").strip()
    explanation = input("Explanation: ").strip()
    
    success = add_science_question(topic, year_group, difficulty, question_text, options, correct_answer, explanation)
    
    if success:
        print("✅ Science question added successfully!")
    else:
        print("❌ Failed to add question.")

def export_questions():
    """Export questions to JSON file"""
    print("\n💾 Export Questions")
    print("-" * 30)
    
    filename = input("Export filename (e.g., questions_export.json): ").strip()
    
    db = QuestionDatabase()
    all_questions = []
    
    # Get all questions from database
    for subject in db.get_available_subjects():
        topics = db.get_topics_for_subject(subject)
        
        for topic_key in topics:
            for year_group in ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5', 'Year 6']:
                for difficulty in ['Easy', 'Medium', 'Hard']:
                    questions = db.get_questions(subject, topic_key, year_group, difficulty, 1000)
                    
                    for question in questions:
                        question_obj = {
                            'subject': subject,
                            'topic': topic_key,
                            'year_group': year_group,
                            'difficulty': difficulty,
                            'question': question['question'],
                            'options': question['options'],
                            'correct_answer': question['correct_answer'],
                            'explanation': question['explanation']
                        }
                        all_questions.append(question_obj)
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_questions, f, indent=2, ensure_ascii=False)
        print(f"✅ Exported {len(all_questions)} questions to {filename}")
    except Exception as e:
        print(f"❌ Error exporting: {e}")

def main():
    """Main admin interface"""
    print("🎓 Welcome to the Question Bank Admin Interface!")
    print("This tool helps you manage questions without changing code.")
    
    while True:
        print_menu()
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            add_single_question()
        elif choice == '2':
            add_questions_from_file()
        elif choice == '3':
            view_statistics()
        elif choice == '4':
            list_all_questions()
        elif choice == '5':
            quick_add_maths()
        elif choice == '6':
            quick_add_science()
        elif choice == '7':
            export_questions()
        elif choice == '8':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
