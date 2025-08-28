import random
import math
from question_database import QuestionDatabase

class QuestionBank:
    def __init__(self):
        # Initialize the question database
        self.db = QuestionDatabase()
        
        self.subjects = {
            'maths': {
                'name': 'Mathematics',
                'topics': {
                    'place_value': 'Number: Place Value',
                    'addition_subtraction': 'Number: Addition & Subtraction',
                    'multiplication_division': 'Number: Multiplication & Division',
                    'fractions_decimals': 'Number: Fractions, Decimals & Percentages',
                    'ratio_proportion': 'Ratio & Proportion',
                    'algebra': 'Algebra',
                    'measurement': 'Measurement',
                    'geometry_shape': 'Geometry: Properties of Shape',
                    'geometry_position': 'Geometry: Position & Direction',
                    'statistics': 'Statistics'
                }
            },
            'science': {
                'name': 'Science',
                'topics': {
                    'living_things': 'Living Things and Their Habitats',
                    'materials': 'Materials and Their Properties',
                    'forces': 'Forces and Motion',
                    'earth_space': 'Earth and Space',
                    'light_sound': 'Light and Sound'
                }
            },
            'computing': {
                'name': 'Computing',
                'topics': {
                    'algorithms': 'Algorithms and Programming',
                    'data': 'Data and Information',
                    'networks': 'Computer Networks',
                    'digital_literacy': 'Digital Literacy',
                    'computational_thinking': 'Computational Thinking'
                }
            },
            'history': {
                'name': 'History',
                'topics': {
                    'ancient_civilizations': 'Ancient Civilizations',
                    'british_history': 'British History',
                    'world_history': 'World History',
                    'local_history': 'Local History',
                    'historical_skills': 'Historical Skills'
                }
            },
            'geography': {
                'name': 'Geography',
                'topics': {
                    'physical_geography': 'Physical Geography',
                    'human_geography': 'Human Geography',
                    'environmental': 'Environmental Geography',
                    'map_skills': 'Map Skills',
                    'fieldwork': 'Fieldwork and Investigation'
                }
            }
        }
        
        self.year_groups = ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5', 'Year 6']
        self.difficulty_levels = ['Easy', 'Medium', 'Hard']

    def get_subjects(self):
        """Get all available subjects"""
        return {key: value['name'] for key, value in self.subjects.items()}

    def get_topics(self, subject):
        """Get topics for a specific subject"""
        if subject in self.subjects:
            return self.subjects[subject]['topics']
        return {}

    def generate_questions(self, subject, topic, year_group, difficulty, num_questions):
        """Generate questions based on criteria"""
        # First try to get questions from the database
        db_questions = self.db.get_questions(subject, topic, year_group, difficulty, num_questions)
        
        if db_questions:
            return db_questions
        
        # If no questions in database, fall back to generated questions
        if subject == 'maths':
            return self._generate_maths_questions(topic, year_group, difficulty, num_questions)
        elif subject == 'science':
            return self._generate_science_questions(topic, year_group, difficulty, num_questions)
        elif subject == 'computing':
            return self._generate_computing_questions(topic, year_group, difficulty, num_questions)
        elif subject == 'history':
            return self._generate_history_questions(topic, year_group, difficulty, num_questions)
        elif subject == 'geography':
            return self._generate_geography_questions(topic, year_group, difficulty, num_questions)
        return []

    def _generate_maths_questions(self, topic, year_group, difficulty, num_questions):
        """Generate mathematics questions"""
        questions = []
        
        if topic == 'place_value':
            questions = self._generate_place_value_questions(year_group, difficulty, num_questions)
        elif topic == 'addition_subtraction':
            questions = self._generate_addition_subtraction_questions(year_group, difficulty, num_questions)
        elif topic == 'multiplication_division':
            questions = self._generate_multiplication_division_questions(year_group, difficulty, num_questions)
        elif topic == 'fractions_decimals':
            questions = self._generate_fractions_decimals_questions(year_group, difficulty, num_questions)
        elif topic == 'ratio_proportion':
            questions = self._generate_ratio_proportion_questions(year_group, difficulty, num_questions)
        elif topic == 'algebra':
            questions = self._generate_algebra_questions(year_group, difficulty, num_questions)
        elif topic == 'measurement':
            questions = self._generate_measurement_questions(year_group, difficulty, num_questions)
        elif topic == 'geometry_shape':
            questions = self._generate_geometry_shape_questions(year_group, difficulty, num_questions)
        elif topic == 'geometry_position':
            questions = self._generate_geometry_position_questions(year_group, difficulty, num_questions)
        elif topic == 'statistics':
            questions = self._generate_statistics_questions(year_group, difficulty, num_questions)
        
        return questions

    def _generate_place_value_questions(self, year_group, difficulty, num_questions):
        """Generate place value questions"""
        questions = []
        year_num = int(year_group.split()[-1])
        
        for i in range(num_questions):
            if year_num <= 2:
                # Years 1-2: Numbers up to 100
                if difficulty == 'Easy':
                    num = random.randint(10, 50)
                elif difficulty == 'Medium':
                    num = random.randint(20, 80)
                else:  # Hard
                    num = random.randint(50, 100)
                
                question_text = f"What is the value of the digit {random.choice(['tens', 'ones'])} in {num}?"
                
                if 'tens' in question_text:
                    correct_answer = num // 10
                else:
                    correct_answer = num % 10
                
                # Generate wrong answers
                wrong_answers = []
                while len(wrong_answers) < 3:
                    wrong = random.randint(0, 9)
                    if wrong != correct_answer and wrong not in wrong_answers:
                        wrong_answers.append(wrong)
                
            elif year_num <= 4:
                # Years 3-4: Numbers up to 1000
                if difficulty == 'Easy':
                    num = random.randint(100, 500)
                elif difficulty == 'Medium':
                    num = random.randint(200, 800)
                else:  # Hard
                    num = random.randint(500, 999)
                
                place = random.choice(['hundreds', 'tens', 'ones'])
                question_text = f"What is the value of the {place} digit in {num}?"
                
                if place == 'hundreds':
                    correct_answer = num // 100
                elif place == 'tens':
                    correct_answer = (num // 10) % 10
                else:
                    correct_answer = num % 10
                
                # Generate wrong answers
                wrong_answers = []
                while len(wrong_answers) < 3:
                    wrong = random.randint(0, 9)
                    if wrong != correct_answer and wrong not in wrong_answers:
                        wrong_answers.append(wrong)
            
            else:
                # Years 5-6: Numbers up to 10000
                if difficulty == 'Easy':
                    num = random.randint(1000, 5000)
                elif difficulty == 'Medium':
                    num = random.randint(2000, 8000)
                else:  # Hard
                    num = random.randint(5000, 9999)
                
                place = random.choice(['thousands', 'hundreds', 'tens', 'ones'])
                question_text = f"What is the value of the {place} digit in {num}?"
                
                if place == 'thousands':
                    correct_answer = num // 1000
                elif place == 'hundreds':
                    correct_answer = (num // 100) % 10
                elif place == 'tens':
                    correct_answer = (num // 10) % 10
                else:
                    correct_answer = num % 10
                
                # Generate wrong answers
                wrong_answers = []
                while len(wrong_answers) < 3:
                    wrong = random.randint(0, 9)
                    if wrong != correct_answer and wrong not in wrong_answers:
                        wrong_answers.append(wrong)
            
            # Shuffle answers
            all_answers = [correct_answer] + wrong_answers
            random.shuffle(all_answers)
            
            questions.append({
                'question': question_text,
                'options': all_answers,
                'correct_answer': correct_answer,
                'explanation': f"The {place if 'place' in locals() else 'digit'} value is {correct_answer}."
            })
        
        return questions

    def _generate_addition_subtraction_questions(self, year_group, difficulty, num_questions):
        """Generate addition and subtraction questions"""
        questions = []
        year_num = int(year_group.split()[-1])
        
        for i in range(num_questions):
            operation = random.choice(['addition', 'subtraction'])
            
            if year_num <= 2:
                # Years 1-2: Numbers up to 100
                if difficulty == 'Easy':
                    a = random.randint(1, 20)
                    b = random.randint(1, 20)
                elif difficulty == 'Medium':
                    a = random.randint(10, 50)
                    b = random.randint(10, 50)
                else:  # Hard
                    a = random.randint(20, 80)
                    b = random.randint(20, 80)
                
            elif year_num <= 4:
                # Years 3-4: Numbers up to 1000
                if difficulty == 'Easy':
                    a = random.randint(50, 200)
                    b = random.randint(50, 200)
                elif difficulty == 'Medium':
                    a = random.randint(100, 500)
                    b = random.randint(100, 500)
                else:  # Hard
                    a = random.randint(200, 800)
                    b = random.randint(200, 800)
            
            else:
                # Years 5-6: Numbers up to 10000
                if difficulty == 'Easy':
                    a = random.randint(500, 2000)
                    b = random.randint(500, 2000)
                elif difficulty == 'Medium':
                    a = random.randint(1000, 5000)
                    b = random.randint(1000, 5000)
                else:  # Hard
                    a = random.randint(2000, 8000)
                    b = random.randint(2000, 8000)
            
            if operation == 'addition':
                question_text = f"What is {a} + {b}?"
                correct_answer = a + b
                explanation = f"{a} + {b} = {correct_answer}"
            else:
                # Ensure a > b for subtraction
                if a < b:
                    a, b = b, a
                question_text = f"What is {a} - {b}?"
                correct_answer = a - b
                explanation = f"{a} - {b} = {correct_answer}"
            
            # Generate wrong answers
            wrong_answers = []
            while len(wrong_answers) < 3:
                if operation == 'addition':
                    wrong = correct_answer + random.randint(-10, 10)
                else:
                    wrong = correct_answer + random.randint(-10, 10)
                
                if wrong != correct_answer and wrong > 0 and wrong not in wrong_answers:
                    wrong_answers.append(wrong)
            
            # Shuffle answers
            all_answers = [correct_answer] + wrong_answers
            random.shuffle(all_answers)
            
            questions.append({
                'question': question_text,
                'options': all_answers,
                'correct_answer': correct_answer,
                'explanation': explanation
            })
        
        return questions

    def _generate_multiplication_division_questions(self, year_group, difficulty, num_questions):
        """Generate multiplication and division questions"""
        questions = []
        year_num = int(year_group.split()[-1])
        
        for i in range(num_questions):
            operation = random.choice(['multiplication', 'division'])
            
            if year_num <= 2:
                # Years 1-2: Simple multiplication tables
                if difficulty == 'Easy':
                    a = random.randint(2, 5)
                    b = random.randint(2, 5)
                elif difficulty == 'Medium':
                    a = random.randint(2, 10)
                    b = random.randint(2, 10)
                else:  # Hard
                    a = random.randint(5, 12)
                    b = random.randint(5, 12)
            
            elif year_num <= 4:
                # Years 3-4: Extended tables
                if difficulty == 'Easy':
                    a = random.randint(2, 12)
                    b = random.randint(2, 12)
                elif difficulty == 'Medium':
                    a = random.randint(5, 15)
                    b = random.randint(5, 15)
                else:  # Hard
                    a = random.randint(10, 20)
                    b = random.randint(10, 20)
            
            else:
                # Years 5-6: Larger numbers
                if difficulty == 'Easy':
                    a = random.randint(10, 25)
                    b = random.randint(10, 25)
                elif difficulty == 'Medium':
                    a = random.randint(15, 50)
                    b = random.randint(15, 50)
                else:  # Hard
                    a = random.randint(25, 100)
                    b = random.randint(25, 100)
            
            if operation == 'multiplication':
                question_text = f"What is {a} × {b}?"
                correct_answer = a * b
                explanation = f"{a} × {b} = {correct_answer}"
            else:
                # Ensure clean division
                product = a * b
                question_text = f"What is {product} ÷ {a}?"
                correct_answer = b
                explanation = f"{product} ÷ {a} = {correct_answer}"
            
            # Generate wrong answers
            wrong_answers = []
            while len(wrong_answers) < 3:
                if operation == 'multiplication':
                    wrong = correct_answer + random.randint(-20, 20)
                else:
                    wrong = correct_answer + random.randint(-5, 5)
                
                if wrong != correct_answer and wrong > 0 and wrong not in wrong_answers:
                    wrong_answers.append(wrong)
            
            # Shuffle answers
            all_answers = [correct_answer] + wrong_answers
            random.shuffle(all_answers)
            
            questions.append({
                'question': question_text,
                'options': all_answers,
                'correct_answer': correct_answer,
                'explanation': explanation
            })
        
        return questions

    def _generate_fractions_decimals_questions(self, year_group, difficulty, num_questions):
        """Generate fractions and decimals questions"""
        questions = []
        year_num = int(year_group.split()[-1])
        
        for i in range(num_questions):
            question_type = random.choice(['fraction_equivalent', 'decimal_fraction', 'percentage'])
            
            if year_num <= 2:
                # Years 1-2: Simple fractions
                if question_type == 'fraction_equivalent':
                    num = random.randint(1, 4)
                    den = random.randint(2, 6)
                    question_text = f"What fraction is equivalent to {num}/{den}?"
                    correct_answer = f"{num}/{den}"
                    explanation = f"{num}/{den} is already in simplest form."
                
            elif year_num <= 4:
                # Years 3-4: Fractions and simple decimals
                if question_type == 'fraction_equivalent':
                    num = random.randint(1, 6)
                    den = random.randint(2, 8)
                    question_text = f"What fraction is equivalent to {num}/{den}?"
                    correct_answer = f"{num}/{den}"
                    explanation = f"{num}/{den} is already in simplest form."
                elif question_type == 'decimal_fraction':
                    decimal = random.choice([0.25, 0.5, 0.75, 0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9])
                    question_text = f"What is {decimal} as a fraction?"
                    if decimal == 0.25:
                        correct_answer = "1/4"
                    elif decimal == 0.5:
                        correct_answer = "1/2"
                    elif decimal == 0.75:
                        correct_answer = "3/4"
                    else:
                        correct_answer = f"{int(decimal * 10)}/10"
                    explanation = f"{decimal} = {correct_answer}"
            
            else:
                # Years 5-6: Complex fractions, decimals, and percentages
                if question_type == 'fraction_equivalent':
                    num = random.randint(1, 8)
                    den = random.randint(2, 12)
                    question_text = f"What fraction is equivalent to {num}/{den}?"
                    correct_answer = f"{num}/{den}"
                    explanation = f"{num}/{den} is already in simplest form."
                elif question_type == 'decimal_fraction':
                    decimal = random.choice([0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875])
                    question_text = f"What is {decimal} as a fraction?"
                    if decimal == 0.125:
                        correct_answer = "1/8"
                    elif decimal == 0.25:
                        correct_answer = "1/4"
                    elif decimal == 0.375:
                        correct_answer = "3/8"
                    elif decimal == 0.5:
                        correct_answer = "1/2"
                    elif decimal == 0.625:
                        correct_answer = "5/8"
                    elif decimal == 0.75:
                        correct_answer = "3/4"
                    elif decimal == 0.875:
                        correct_answer = "7/8"
                    explanation = f"{decimal} = {correct_answer}"
                elif question_type == 'percentage':
                    percentage = random.choice([25, 50, 75, 10, 20, 30, 40, 60, 70, 80, 90])
                    question_text = f"What is {percentage}% as a decimal?"
                    correct_answer = percentage / 100
                    explanation = f"{percentage}% = {correct_answer}"
            
            # Generate wrong answers
            wrong_answers = []
            while len(wrong_answers) < 3:
                if question_type == 'fraction_equivalent':
                    wrong = f"{random.randint(1, 8)}/{random.randint(2, 12)}"
                elif question_type == 'decimal_fraction':
                    wrong = random.choice([0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9])
                elif question_type == 'percentage':
                    wrong = random.choice([0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9])
                
                if wrong != correct_answer and wrong not in wrong_answers:
                    wrong_answers.append(wrong)
            
            # Shuffle answers
            all_answers = [correct_answer] + wrong_answers
            random.shuffle(all_answers)
            
            questions.append({
                'question': question_text,
                'options': all_answers,
                'correct_answer': correct_answer,
                'explanation': explanation
            })
        
        return questions

    def _generate_ratio_proportion_questions(self, year_group, difficulty, num_questions):
        """Generate ratio and proportion questions"""
        questions = []
        year_num = int(year_group.split()[-1])
        
        for i in range(num_questions):
            if year_num <= 4:
                # Years 3-4: Simple ratios
                a = random.randint(1, 5)
                b = random.randint(1, 5)
                question_text = f"What is the ratio of {a} to {b}?"
                correct_answer = f"{a}:{b}"
                explanation = f"The ratio of {a} to {b} is {a}:{b}"
            
            else:
                # Years 5-6: More complex ratios
                a = random.randint(2, 10)
                b = random.randint(2, 10)
                c = random.randint(2, 10)
                question_text = f"If {a} items cost £{b}, how much do {c} items cost?"
                correct_answer = round((b / a) * c, 2)
                explanation = f"Cost per item = £{b} ÷ {a} = £{b/a}. Total cost = £{b/a} × {c} = £{correct_answer}"
            
            # Generate wrong answers
            wrong_answers = []
            while len(wrong_answers) < 3:
                if year_num <= 4:
                    wrong = f"{random.randint(1, 5)}:{random.randint(1, 5)}"
                else:
                    wrong = round(random.uniform(1, 20), 2)
                
                if wrong != correct_answer and wrong not in wrong_answers:
                    wrong_answers.append(wrong)
            
            # Shuffle answers
            all_answers = [correct_answer] + wrong_answers
            random.shuffle(all_answers)
            
            questions.append({
                'question': question_text,
                'options': all_answers,
                'correct_answer': correct_answer,
                'explanation': explanation
            })
        
        return questions

    def _generate_algebra_questions(self, year_group, difficulty, num_questions):
        """Generate algebra questions"""
        questions = []
        year_num = int(year_group.split()[-1])
        
        for i in range(num_questions):
            if year_num <= 4:
                # Years 3-4: Simple patterns
                pattern = random.choice(['add', 'multiply'])
                start = random.randint(1, 10)
                
                if pattern == 'add':
                    step = random.randint(2, 5)
                    question_text = f"What comes next in the pattern: {start}, {start + step}, {start + 2*step}, ?"
                    correct_answer = start + 3*step
                    explanation = f"Add {step} each time: {start + 3*step}"
                else:
                    step = random.randint(2, 3)
                    question_text = f"What comes next in the pattern: {start}, {start * step}, {start * step * step}, ?"
                    correct_answer = start * step * step * step
                    explanation = f"Multiply by {step} each time: {correct_answer}"
            
            else:
                # Years 5-6: Simple equations
                x = random.randint(1, 10)
                operation = random.choice(['add', 'subtract', 'multiply'])
                
                if operation == 'add':
                    b = random.randint(1, 10)
                    result = x + b
                    question_text = f"If x + {b} = {result}, what is x?"
                    correct_answer = x
                    explanation = f"x = {result} - {b} = {x}"
                elif operation == 'subtract':
                    b = random.randint(1, 10)
                    result = x - b
                    question_text = f"If x - {b} = {result}, what is x?"
                    correct_answer = x
                    explanation = f"x = {result} + {b} = {x}"
                else:
                    b = random.randint(2, 5)
                    result = x * b
                    question_text = f"If {b}x = {result}, what is x?"
                    correct_answer = x
                    explanation = f"x = {result} ÷ {b} = {x}"
            
            # Generate wrong answers
            wrong_answers = []
            while len(wrong_answers) < 3:
                wrong = random.randint(1, 20)
                if wrong != correct_answer and wrong not in wrong_answers:
                    wrong_answers.append(wrong)
            
            # Shuffle answers
            all_answers = [correct_answer] + wrong_answers
            random.shuffle(all_answers)
            
            questions.append({
                'question': question_text,
                'options': all_answers,
                'correct_answer': correct_answer,
                'explanation': explanation
            })
        
        return questions

    def _generate_measurement_questions(self, year_group, difficulty, num_questions):
        """Generate measurement questions"""
        questions = []
        year_num = int(year_group.split()[-1])
        
        for i in range(num_questions):
            measurement_type = random.choice(['length', 'mass', 'capacity', 'time'])
            
            if measurement_type == 'length':
                if year_num <= 2:
                    # Years 1-2: Simple length comparisons
                    a = random.randint(1, 10)
                    b = random.randint(1, 10)
                    question_text = f"Which is longer: {a}cm or {b}cm?"
                    correct_answer = max(a, b)
                    explanation = f"{max(a, b)}cm is longer than {min(a, b)}cm"
                
                elif year_num <= 4:
                    # Years 3-4: Converting units
                    cm = random.randint(10, 100)
                    question_text = f"How many metres is {cm}cm?"
                    correct_answer = cm / 100
                    explanation = f"{cm}cm = {cm/100}m"
                
                else:
                    # Years 5-6: Complex conversions
                    km = random.randint(1, 10)
                    question_text = f"How many metres is {km}km?"
                    correct_answer = km * 1000
                    explanation = f"{km}km = {km * 1000}m"
            
            elif measurement_type == 'mass':
                if year_num <= 2:
                    # Years 1-2: Simple mass comparisons
                    a = random.randint(1, 10)
                    b = random.randint(1, 10)
                    question_text = f"Which is heavier: {a}kg or {b}kg?"
                    correct_answer = max(a, b)
                    explanation = f"{max(a, b)}kg is heavier than {min(a, b)}kg"
                
                elif year_num <= 4:
                    # Years 3-4: Converting units
                    g = random.randint(100, 1000)
                    question_text = f"How many kilograms is {g}g?"
                    correct_answer = g / 1000
                    explanation = f"{g}g = {g/1000}kg"
                
                else:
                    # Years 5-6: Complex conversions
                    kg = random.randint(1, 10)
                    question_text = f"How many grams is {kg}kg?"
                    correct_answer = kg * 1000
                    explanation = f"{kg}kg = {kg * 1000}g"
            
            elif measurement_type == 'capacity':
                if year_num <= 2:
                    # Years 1-2: Simple capacity comparisons
                    a = random.randint(1, 10)
                    b = random.randint(1, 10)
                    question_text = f"Which holds more: {a}L or {b}L?"
                    correct_answer = max(a, b)
                    explanation = f"{max(a, b)}L holds more than {min(a, b)}L"
                
                elif year_num <= 4:
                    # Years 3-4: Converting units
                    ml = random.randint(100, 1000)
                    question_text = f"How many litres is {ml}ml?"
                    correct_answer = ml / 1000
                    explanation = f"{ml}ml = {ml/1000}L"
                
                else:
                    # Years 5-6: Complex conversions
                    l = random.randint(1, 10)
                    question_text = f"How many millilitres is {l}L?"
                    correct_answer = l * 1000
                    explanation = f"{l}L = {l * 1000}ml"
            
            else:  # time
                if year_num <= 2:
                    # Years 1-2: Simple time
                    hour = random.randint(1, 12)
                    minute = random.choice([0, 15, 30, 45])
                    question_text = f"What time is {hour}:{minute:02d}?"
                    correct_answer = f"{hour}:{minute:02d}"
                    explanation = f"The time is {hour}:{minute:02d}"
                
                elif year_num <= 4:
                    # Years 3-4: Time calculations
                    hours = random.randint(1, 5)
                    question_text = f"How many minutes are in {hours} hours?"
                    correct_answer = hours * 60
                    explanation = f"{hours} hours = {hours * 60} minutes"
                
                else:
                    # Years 5-6: Complex time
                    minutes = random.randint(60, 300)
                    question_text = f"How many hours and minutes is {minutes} minutes?"
                    hours = minutes // 60
                    mins = minutes % 60
                    correct_answer = f"{hours}h {mins}m"
                    explanation = f"{minutes} minutes = {hours} hours and {mins} minutes"
            
            # Generate wrong answers
            wrong_answers = []
            while len(wrong_answers) < 3:
                if measurement_type == 'length':
                    wrong = random.randint(1, 20)
                elif measurement_type == 'mass':
                    wrong = random.randint(1, 20)
                elif measurement_type == 'capacity':
                    wrong = random.randint(1, 20)
                else:  # time
                    if year_num <= 2:
                        wrong = f"{random.randint(1, 12)}:{random.choice([0, 15, 30, 45]):02d}"
                    elif year_num <= 4:
                        wrong = random.randint(30, 300)
                    else:
                        wrong = f"{random.randint(1, 5)}h {random.randint(0, 59)}m"
                
                if wrong != correct_answer and wrong not in wrong_answers:
                    wrong_answers.append(wrong)
            
            # Shuffle answers
            all_answers = [correct_answer] + wrong_answers
            random.shuffle(all_answers)
            
            questions.append({
                'question': question_text,
                'options': all_answers,
                'correct_answer': correct_answer,
                'explanation': explanation
            })
        
        return questions

    def _generate_geometry_shape_questions(self, year_group, difficulty, num_questions):
        """Generate geometry shape questions"""
        questions = []
        year_num = int(year_group.split()[-1])
        
        for i in range(num_questions):
            if year_num <= 2:
                # Years 1-2: Basic shapes
                shapes = ['circle', 'square', 'triangle', 'rectangle']
                shape = random.choice(shapes)
                question_text = f"How many sides does a {shape} have?"
                
                if shape == 'circle':
                    correct_answer = 0
                elif shape == 'square':
                    correct_answer = 4
                elif shape == 'triangle':
                    correct_answer = 3
                elif shape == 'rectangle':
                    correct_answer = 4
                
                explanation = f"A {shape} has {correct_answer} sides."
            
            elif year_num <= 4:
                # Years 3-4: Properties of shapes
                shapes = ['square', 'rectangle', 'triangle', 'pentagon', 'hexagon']
                shape = random.choice(shapes)
                question_text = f"How many sides does a {shape} have?"
                
                if shape == 'square':
                    correct_answer = 4
                elif shape == 'rectangle':
                    correct_answer = 4
                elif shape == 'triangle':
                    correct_answer = 3
                elif shape == 'pentagon':
                    correct_answer = 5
                elif shape == 'hexagon':
                    correct_answer = 6
                
                explanation = f"A {shape} has {correct_answer} sides."
            
            else:
                # Years 5-6: Angles and properties
                angle_type = random.choice(['acute', 'obtuse', 'right', 'straight'])
                question_text = f"What type of angle is {random.choice([45, 90, 120, 180])} degrees?"
                
                if angle_type == 'acute':
                    angle = 45
                    correct_answer = 'acute'
                elif angle_type == 'right':
                    angle = 90
                    correct_answer = 'right'
                elif angle_type == 'obtuse':
                    angle = 120
                    correct_answer = 'obtuse'
                else:  # straight
                    angle = 180
                    correct_answer = 'straight'
                
                question_text = f"What type of angle is {angle} degrees?"
                explanation = f"An angle of {angle} degrees is a {correct_answer} angle."
            
            # Generate wrong answers
            wrong_answers = []
            while len(wrong_answers) < 3:
                if year_num <= 4:
                    wrong = random.randint(0, 8)
                else:
                    wrong = random.choice(['acute', 'obtuse', 'right', 'straight'])
                
                if wrong != correct_answer and wrong not in wrong_answers:
                    wrong_answers.append(wrong)
            
            # Shuffle answers
            all_answers = [correct_answer] + wrong_answers
            random.shuffle(all_answers)
            
            questions.append({
                'question': question_text,
                'options': all_answers,
                'correct_answer': correct_answer,
                'explanation': explanation
            })
        
        return questions

    def _generate_geometry_position_questions(self, year_group, difficulty, num_questions):
        """Generate geometry position questions"""
        questions = []
        year_num = int(year_group.split()[-1])
        
        for i in range(num_questions):
            if year_num <= 2:
                # Years 1-2: Basic position words
                positions = ['above', 'below', 'left', 'right', 'in front of', 'behind']
                position = random.choice(positions)
                question_text = f"What is the opposite of '{position}'?"
                
                opposites = {
                    'above': 'below',
                    'below': 'above',
                    'left': 'right',
                    'right': 'left',
                    'in front of': 'behind',
                    'behind': 'in front of'
                }
                correct_answer = opposites[position]
                explanation = f"The opposite of '{position}' is '{correct_answer}'."
            
            elif year_num <= 4:
                # Years 3-4: Coordinates
                x = random.randint(1, 5)
                y = random.randint(1, 5)
                question_text = f"What are the coordinates of point ({x}, {y})?"
                correct_answer = f"({x}, {y})"
                explanation = f"The coordinates are ({x}, {y})."
            
            else:
                # Years 5-6: Reflections and translations
                transformations = ['reflection', 'translation', 'rotation']
                transform = random.choice(transformations)
                question_text = f"What type of transformation moves a shape without changing its size?"
                correct_answer = 'translation'
                explanation = "Translation moves a shape without changing its size or shape."
            
            # Generate wrong answers
            wrong_answers = []
            while len(wrong_answers) < 3:
                if year_num <= 2:
                    wrong = random.choice(['above', 'below', 'left', 'right', 'in front of', 'behind'])
                elif year_num <= 4:
                    wrong = f"({random.randint(1, 5)}, {random.randint(1, 5)})"
                else:
                    wrong = random.choice(['reflection', 'translation', 'rotation'])
                
                if wrong != correct_answer and wrong not in wrong_answers:
                    wrong_answers.append(wrong)
            
            # Shuffle answers
            all_answers = [correct_answer] + wrong_answers
            random.shuffle(all_answers)
            
            questions.append({
                'question': question_text,
                'options': all_answers,
                'correct_answer': correct_answer,
                'explanation': explanation
            })
        
        return questions

    def _generate_statistics_questions(self, year_group, difficulty, num_questions):
        """Generate statistics questions"""
        questions = []
        year_num = int(year_group.split()[-1])
        
        for i in range(num_questions):
            if year_num <= 2:
                # Years 1-2: Simple counting
                numbers = [random.randint(1, 5) for _ in range(4)]
                question_text = f"How many items are there: {', '.join(map(str, numbers))}?"
                correct_answer = len(numbers)
                explanation = f"There are {len(numbers)} items in the list."
            
            elif year_num <= 4:
                # Years 3-4: Mode and range
                numbers = [random.randint(1, 10) for _ in range(5)]
                question_text = f"What is the mode of {numbers}?"
                from collections import Counter
                counter = Counter(numbers)
                correct_answer = counter.most_common(1)[0][0]
                explanation = f"The mode is {correct_answer} (appears most often)."
            
            else:
                # Years 5-6: Mean and median
                numbers = sorted([random.randint(1, 20) for _ in range(5)])
                question_text = f"What is the median of {numbers}?"
                correct_answer = numbers[2]  # Middle number
                explanation = f"The median is {correct_answer} (middle number when ordered)."
            
            # Generate wrong answers
            wrong_answers = []
            while len(wrong_answers) < 3:
                if year_num <= 2:
                    wrong = random.randint(1, 10)
                elif year_num <= 4:
                    wrong = random.randint(1, 10)
                else:
                    wrong = random.randint(1, 20)
                
                if wrong != correct_answer and wrong not in wrong_answers:
                    wrong_answers.append(wrong)
            
            # Shuffle answers
            all_answers = [correct_answer] + wrong_answers
            random.shuffle(all_answers)
            
            questions.append({
                'question': question_text,
                'options': all_answers,
                'correct_answer': correct_answer,
                'explanation': explanation
            })
        
        return questions

    # Placeholder methods for other subjects
    def _generate_science_questions(self, topic, year_group, difficulty, num_questions):
        """Generate science questions - placeholder for now"""
        return []

    def _generate_computing_questions(self, topic, year_group, difficulty, num_questions):
        """Generate computing questions - placeholder for now"""
        return []

    def _generate_history_questions(self, topic, year_group, difficulty, num_questions):
        """Generate history questions - placeholder for now"""
        return []

    def _generate_geography_questions(self, topic, year_group, difficulty, num_questions):
        """Generate geography questions - placeholder for now"""
        return []
