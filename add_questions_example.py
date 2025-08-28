#!/usr/bin/env python3
"""
Example script showing different ways to add questions to the database
"""

from question_database import QuestionDatabase, create_question, add_maths_question, add_science_question

def example_1_single_question():
    """Example 1: Add a single question using the helper function"""
    print("📝 Example 1: Adding a single maths question")
    
    success = add_maths_question(
        topic="place_value",
        year_group="Year 3",
        difficulty="Medium",
        question_text="What is the value of the hundreds digit in 456?",
        options=["4", "5", "6", "400"],
        correct_answer="4",
        explanation="In 456, the hundreds digit is 4."
    )
    
    if success:
        print("✅ Question added successfully!")
    else:
        print("❌ Failed to add question.")

def example_2_multiple_questions():
    """Example 2: Add multiple questions using the database directly"""
    print("\n📝 Example 2: Adding multiple science questions")
    
    db = QuestionDatabase()
    
    science_questions = [
        {
            "question": "Which planet is closest to the Sun?",
            "options": ["Mercury", "Venus", "Earth", "Mars"],
            "correct_answer": "Mercury",
            "explanation": "Mercury is the closest planet to the Sun in our solar system."
        },
        {
            "question": "What is the main gas that plants need for photosynthesis?",
            "options": ["Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen"],
            "correct_answer": "Carbon dioxide",
            "explanation": "Plants use carbon dioxide and water to make their own food through photosynthesis."
        },
        {
            "question": "Which of these is a vertebrate animal?",
            "options": ["Spider", "Snail", "Fish", "Jellyfish"],
            "correct_answer": "Fish",
            "explanation": "Fish have a backbone (spine), making them vertebrates."
        }
    ]
    
    success = db.add_multiple_questions(
        subject="science",
        topic="living_things",
        year_group="Year 4",
        difficulty="Medium",
        questions=science_questions
    )
    
    if success:
        print("✅ All questions added successfully!")
    else:
        print("❌ Some questions failed to add.")

def example_3_create_and_add():
    """Example 3: Create questions using helper function and add them"""
    print("\n📝 Example 3: Creating questions with helper function")
    
    db = QuestionDatabase()
    
    # Create questions using the helper function
    question1 = create_question(
        question_text="What is 8 × 7?",
        options=["54", "56", "58", "60"],
        correct_answer="56",
        explanation="8 × 7 = 56"
    )
    
    question2 = create_question(
        question_text="What is 72 ÷ 8?",
        options=["8", "9", "10", "11"],
        correct_answer="9",
        explanation="72 ÷ 8 = 9"
    )
    
    # Add them to the database
    success1 = db.add_question("maths", "multiplication_division", "Year 4", "Medium", question1)
    success2 = db.add_question("maths", "multiplication_division", "Year 4", "Medium", question2)
    
    if success1 and success2:
        print("✅ Both questions added successfully!")
    else:
        print("❌ Some questions failed to add.")

def example_4_view_statistics():
    """Example 4: View question statistics"""
    print("\n📊 Example 4: Viewing question statistics")
    
    db = QuestionDatabase()
    stats = db.list_all_questions()
    
    print("Current question statistics:")
    for subject, topics in stats.items():
        print(f"\n📚 {subject.upper()}:")
        for topic, year_groups in topics.items():
            print(f"  📖 {topic}:")
            for year_group, difficulties in year_groups.items():
                print(f"    📅 {year_group}:")
                for difficulty, count in difficulties.items():
                    if count > 0:
                        print(f"      🎯 {difficulty}: {count} questions")

def example_5_bulk_import():
    """Example 5: Bulk import from JSON file"""
    print("\n📁 Example 5: Bulk import from JSON file")
    
    # This would typically be done through the admin interface
    # but here's how you could do it programmatically
    
    import json
    
    # Sample questions to add
    bulk_questions = [
        {
            "subject": "computing",
            "topic": "digital_literacy",
            "year_group": "Year 5",
            "difficulty": "Easy",
            "question": "What should you do if you receive a suspicious email?",
            "options": ["Open all attachments", "Reply with personal information", "Delete it without opening", "Forward it to friends"],
            "correct_answer": "Delete it without opening",
            "explanation": "Suspicious emails should be deleted without opening to avoid viruses or scams."
        },
        {
            "subject": "history",
            "topic": "world_history",
            "year_group": "Year 6",
            "difficulty": "Hard",
            "question": "In which year did World War II end?",
            "options": ["1943", "1944", "1945", "1946"],
            "correct_answer": "1945",
            "explanation": "World War II ended in 1945 with the surrender of Germany and Japan."
        }
    ]
    
    db = QuestionDatabase()
    success_count = 0
    
    for question_obj in bulk_questions:
        question = create_question(
            question_obj['question'],
            question_obj['options'],
            question_obj['correct_answer'],
            question_obj['explanation']
        )
        
        if db.add_question(
            question_obj['subject'],
            question_obj['topic'],
            question_obj['year_group'],
            question_obj['difficulty'],
            question
        ):
            success_count += 1
    
    print(f"✅ Successfully added {success_count}/{len(bulk_questions)} questions!")

def main():
    """Run all examples"""
    print("🎓 Question Database Examples")
    print("=" * 50)
    print("This script demonstrates different ways to add questions to the database.")
    print("No code changes needed - just run this script!")
    
    # Run all examples
    example_1_single_question()
    example_2_multiple_questions()
    example_3_create_and_add()
    example_4_view_statistics()
    example_5_bulk_import()
    
    print("\n" + "=" * 50)
    print("✅ All examples completed!")
    print("\n💡 Tips:")
    print("1. Use the admin interface: python question_admin.py")
    print("2. Create JSON files for bulk imports")
    print("3. Use helper functions for quick additions")
    print("4. Questions are automatically saved to JSON files")
    print("5. No code changes needed to add new questions!")

if __name__ == "__main__":
    main()
