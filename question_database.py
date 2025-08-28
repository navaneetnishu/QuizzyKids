import json
import os
import random
from typing import List, Dict, Any
from datetime import datetime

class QuestionDatabase:
    """Flexible question database that loads questions from separate JSON files per subject"""
    
    def __init__(self, data_dir="question_data"):
        self.data_dir = data_dir
        self.questions_cache = {}
        self.last_modified = {}
        self._ensure_data_directory()
        self._load_all_questions()
    
    def _ensure_data_directory(self):
        """Create the data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            self._create_sample_files()
    
    def _create_sample_files(self):
        """Create sample question files for each subject"""
        subjects = {
            "maths": "maths_questions.json",
            "science": "science_questions.json", 
            "computing": "computing_questions.json",
            "history": "history_questions.json",
            "geography": "geography_questions.json"
        }
        
        for subject, filename in subjects.items():
            filepath = os.path.join(self.data_dir, filename)
            if not os.path.exists(filepath):
                sample_data = self._get_sample_questions(subject)
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(sample_data, f, indent=2, ensure_ascii=False)
                print(f"✅ Created sample {subject} questions file: {filename}")
    
    def _get_sample_questions(self, subject):
        """Get sample questions for each subject"""
        if subject == "maths":
            return [
                {
                    "topic": "place_value",
                    "year_group": "Year 2",
                    "difficulty": "Easy",
                    "question": "What is the value of the tens digit in 34?",
                    "options": ["3", "4", "30", "40"],
                    "correct_answer": "3",
                    "explanation": "In 34, the tens digit is 3."
                },
                {
                    "topic": "addition_subtraction",
                    "year_group": "Year 3",
                    "difficulty": "Medium",
                    "question": "What is 156 + 89?",
                    "options": ["235", "245", "255", "265"],
                    "correct_answer": "245",
                    "explanation": "156 + 89 = 245"
                }
            ]
        elif subject == "science":
            return [
                {
                    "topic": "plants",
                    "year_group": "Year 2",
                    "difficulty": "Easy",
                    "question": "What do plants need to grow?",
                    "options": ["Water, sunlight, soil", "Only water", "Only sunlight", "Only soil"],
                    "correct_answer": "Water, sunlight, soil",
                    "explanation": "Plants need water, sunlight, and soil to grow properly."
                }
            ]
        elif subject == "computing":
            return [
                {
                    "topic": "algorithms",
                    "year_group": "Year 3",
                    "difficulty": "Easy",
                    "question": "What is an algorithm?",
                    "options": ["A set of instructions", "A computer", "A program", "A game"],
                    "correct_answer": "A set of instructions",
                    "explanation": "An algorithm is a set of step-by-step instructions to solve a problem."
                }
            ]
        elif subject == "history":
            return [
                {
                    "topic": "ancient_egypt",
                    "year_group": "Year 3",
                    "difficulty": "Easy",
                    "question": "What were the ancient Egyptians famous for building?",
                    "options": ["Pyramids", "Castles", "Bridges", "Towers"],
                    "correct_answer": "Pyramids",
                    "explanation": "The ancient Egyptians built the famous pyramids as tombs for their pharaohs."
                }
            ]
        elif subject == "geography":
            return [
                {
                    "topic": "continents",
                    "year_group": "Year 2",
                    "difficulty": "Easy",
                    "question": "How many continents are there?",
                    "options": ["5", "6", "7", "8"],
                    "correct_answer": "7",
                    "explanation": "There are 7 continents: Asia, Africa, North America, South America, Antarctica, Europe, and Australia."
                }
            ]
        return []
    
    def _get_subject_filename(self, subject):
        """Get the filename for a given subject"""
        subject_files = {
            "maths": "maths_questions.json",
            "science": "science_questions.json",
            "computing": "computing_questions.json", 
            "history": "history_questions.json",
            "geography": "geography_questions.json"
        }
        return subject_files.get(subject, f"{subject}_questions.json")
    
    def _load_all_questions(self):
        """Load all questions from JSON files"""
        subjects = ["maths", "science", "computing", "history", "geography"]
        
        for subject in subjects:
            self._load_subject_questions(subject)
    
    def _load_subject_questions(self, subject):
        """Load questions for a specific subject"""
        filename = self._get_subject_filename(subject)
        filepath = os.path.join(self.data_dir, filename)
        
        if os.path.exists(filepath):
            try:
                # Check if file has been modified
                current_mtime = os.path.getmtime(filepath)
                if subject not in self.last_modified or self.last_modified[subject] != current_mtime:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        questions = json.load(f)
                    
                    # Organize questions by topic, year group, and difficulty
                    organized_questions = {}
                    for q in questions:
                        topic = q.get('topic', 'general')
                        year_group = q.get('year_group', 'Year 1')
                        difficulty = q.get('difficulty', 'Easy')
                        
                        if topic not in organized_questions:
                            organized_questions[topic] = {}
                        if year_group not in organized_questions[topic]:
                            organized_questions[topic][year_group] = {}
                        if difficulty not in organized_questions[topic][year_group]:
                            organized_questions[topic][year_group][difficulty] = []
                        
                        organized_questions[topic][year_group][difficulty].append(q)
                    
                    self.questions_cache[subject] = organized_questions
                    self.last_modified[subject] = current_mtime
                    print(f"✅ Loaded {len(questions)} questions for {subject}")
                    
            except Exception as e:
                print(f"❌ Error loading {subject} questions: {e}")
                self.questions_cache[subject] = {}
        else:
            print(f"⚠️ No question file found for {subject}: {filename}")
            self.questions_cache[subject] = {}
    
    def get_questions(self, subject: str, topic: str, year_group: str, difficulty: str, num_questions: int) -> List[Dict]:
        """Get questions for the specified criteria with hot-reload"""
        # Check if we need to reload the subject's questions
        self._load_subject_questions(subject)
        
        questions = []
        subject_questions = self.questions_cache.get(subject, {})
        topic_questions = subject_questions.get(topic, {})
        year_questions = topic_questions.get(year_group, {})
        difficulty_questions = year_questions.get(difficulty, [])
        
        if difficulty_questions:
            # Randomly select questions
            selected_questions = random.sample(difficulty_questions, min(num_questions, len(difficulty_questions)))
            questions.extend(selected_questions)
        
        # If we don't have enough questions, try other difficulties
        if len(questions) < num_questions:
            remaining_needed = num_questions - len(questions)
            other_difficulties = [d for d in year_questions.keys() if d != difficulty]
            
            for other_diff in other_difficulties:
                if remaining_needed <= 0:
                    break
                other_questions = year_questions[other_diff]
                additional = random.sample(other_questions, min(remaining_needed, len(other_questions)))
                questions.extend(additional)
                remaining_needed -= len(additional)
        
        return questions[:num_questions]
    
    def add_question(self, subject: str, question_data: Dict) -> bool:
        """Add a new question to the appropriate JSON file"""
        try:
            filename = self._get_subject_filename(subject)
            filepath = os.path.join(self.data_dir, filename)
            
            # Load existing questions
            existing_questions = []
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    existing_questions = json.load(f)
            
            # Add new question
            existing_questions.append(question_data)
            
            # Save back to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(existing_questions, f, indent=2, ensure_ascii=False)
            
            # Invalidate cache for this subject
            if subject in self.last_modified:
                del self.last_modified[subject]
            
            print(f"✅ Added question to {subject}")
            return True
            
        except Exception as e:
            print(f"❌ Error adding question to {subject}: {e}")
            return False
    
    def get_subject_stats(self, subject: str) -> Dict:
        """Get statistics for a subject"""
        self._load_subject_questions(subject)
        subject_questions = self.questions_cache.get(subject, {})
        
        stats = {
            "total_questions": 0,
            "topics": {},
            "year_groups": {},
            "difficulties": {}
        }
        
        for topic, topic_data in subject_questions.items():
            topic_count = 0
            for year_group, year_data in topic_data.items():
                year_count = 0
                for difficulty, questions in year_data.items():
                    count = len(questions)
                    stats["total_questions"] += count
                    topic_count += count
                    year_count += count
                    
                    if difficulty not in stats["difficulties"]:
                        stats["difficulties"][difficulty] = 0
                    stats["difficulties"][difficulty] += count
                
                if year_group not in stats["year_groups"]:
                    stats["year_groups"][year_group] = 0
                stats["year_groups"][year_group] += year_count
            
            stats["topics"][topic] = topic_count
        
        return stats
    
    def export_questions(self, subject: str, output_file: str = None) -> str:
        """Export questions for a subject to a JSON file"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"{subject}_questions_export_{timestamp}.json"
        
        try:
            filename = self._get_subject_filename(subject)
            filepath = os.path.join(self.data_dir, filename)
            
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    questions = json.load(f)
                
                export_path = os.path.join(self.data_dir, output_file)
                with open(export_path, 'w', encoding='utf-8') as f:
                    json.dump(questions, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Exported {len(questions)} questions to {output_file}")
                return export_path
            else:
                print(f"❌ No questions found for {subject}")
                return None
                
        except Exception as e:
            print(f"❌ Error exporting {subject} questions: {e}")
            return None

# Helper functions for easy question addition
def add_maths_question(topic: str, year_group: str, difficulty: str, question_text: str, 
                      options: List[str], correct_answer: str, explanation: str) -> bool:
    """Add a maths question to the database"""
    db = QuestionDatabase()
    question_data = {
        "topic": topic,
        "year_group": year_group,
        "difficulty": difficulty,
        "question": question_text,
        "options": options,
        "correct_answer": correct_answer,
        "explanation": explanation
    }
    return db.add_question("maths", question_data)

def add_science_question(topic: str, year_group: str, difficulty: str, question_text: str,
                        options: List[str], correct_answer: str, explanation: str) -> bool:
    """Add a science question to the database"""
    db = QuestionDatabase()
    question_data = {
        "topic": topic,
        "year_group": year_group,
        "difficulty": difficulty,
        "question": question_text,
        "options": options,
        "correct_answer": correct_answer,
        "explanation": explanation
    }
    return db.add_question("science", question_data)

def add_computing_question(topic: str, year_group: str, difficulty: str, question_text: str,
                          options: List[str], correct_answer: str, explanation: str) -> bool:
    """Add a computing question to the database"""
    db = QuestionDatabase()
    question_data = {
        "topic": topic,
        "year_group": year_group,
        "difficulty": difficulty,
        "question": question_text,
        "options": options,
        "correct_answer": correct_answer,
        "explanation": explanation
    }
    return db.add_question("computing", question_data)

def add_history_question(topic: str, year_group: str, difficulty: str, question_text: str,
                        options: List[str], correct_answer: str, explanation: str) -> bool:
    """Add a history question to the database"""
    db = QuestionDatabase()
    question_data = {
        "topic": topic,
        "year_group": year_group,
        "difficulty": difficulty,
        "question": question_text,
        "options": options,
        "correct_answer": correct_answer,
        "explanation": explanation
    }
    return db.add_question("history", question_data)

def add_geography_question(topic: str, year_group: str, difficulty: str, question_text: str,
                          options: List[str], correct_answer: str, explanation: str) -> bool:
    """Add a geography question to the database"""
    db = QuestionDatabase()
    question_data = {
        "topic": topic,
        "year_group": year_group,
        "difficulty": difficulty,
        "question": question_text,
        "options": options,
        "correct_answer": correct_answer,
        "explanation": explanation
    }
    return db.add_question("geography", question_data)
