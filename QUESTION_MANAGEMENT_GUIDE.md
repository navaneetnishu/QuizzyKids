# 📚 Question Management Guide

## 🎯 Overview

This guide shows you how to add questions to the database **without changing any code**. The system uses JSON files to store questions, making it easy to manage and expand your question bank.

## 🚀 Quick Start

### Method 1: Admin Interface (Easiest)
```bash
python question_admin.py
```
This opens an interactive menu where you can:
- Add single questions
- Import questions from JSON files
- View statistics
- Export questions

### Method 2: Programmatic Addition
```python
from question_database import add_maths_question

# Add a single question
add_maths_question(
    topic="place_value",
    year_group="Year 3", 
    difficulty="Medium",
    question_text="What is the value of the hundreds digit in 456?",
    options=["4", "5", "6", "400"],
    correct_answer="4",
    explanation="In 456, the hundreds digit is 4."
)
```

### Method 3: Bulk Import from JSON
Create a JSON file like `my_questions.json`:
```json
[
  {
    "subject": "maths",
    "topic": "place_value",
    "year_group": "Year 2",
    "difficulty": "Easy",
    "question": "What is the value of the tens digit in 34?",
    "options": ["3", "4", "30", "40"],
    "correct_answer": "3",
    "explanation": "In 34, the tens digit is 3."
  }
]
```

Then import it using the admin interface.

## 📁 File Structure

```
KidsPracticePDF/
├── question_data/              # Questions stored here
│   ├── maths_questions.json    # Maths questions
│   ├── science_questions.json  # Science questions
│   ├── computing_questions.json # Computing questions
│   └── template.json          # Template for new subjects
├── question_database.py        # Database management
├── question_admin.py          # Admin interface
└── sample_questions.json      # Example format
```

## 🎨 Question Format

Each question has this structure:
```json
{
  "question": "What is 2 + 3?",
  "options": ["4", "5", "6", "7"],
  "correct_answer": "5",
  "explanation": "2 + 3 = 5"
}
```

## 📚 Available Subjects & Topics

### Mathematics
- `place_value` - Number: Place Value
- `addition_subtraction` - Number: Addition & Subtraction
- `multiplication_division` - Number: Multiplication & Division
- `fractions_decimals` - Number: Fractions, Decimals & Percentages
- `ratio_proportion` - Ratio & Proportion
- `algebra` - Algebra
- `measurement` - Measurement
- `geometry_shape` - Geometry: Properties of Shape
- `geometry_position` - Geometry: Position & Direction
- `statistics` - Statistics

### Science
- `living_things` - Living Things and Their Habitats
- `materials` - Materials and Their Properties
- `forces` - Forces and Motion
- `earth_space` - Earth and Space
- `light_sound` - Light and Sound

### Computing
- `algorithms` - Algorithms and Programming
- `data` - Data and Information
- `networks` - Computer Networks
- `digital_literacy` - Digital Literacy
- `computational_thinking` - Computational Thinking

### History
- `ancient_civilizations` - Ancient Civilizations
- `british_history` - British History
- `world_history` - World History
- `local_history` - Local History
- `historical_skills` - Historical Skills

### Geography
- `physical_geography` - Physical Geography
- `human_geography` - Human Geography
- `environmental` - Environmental Geography
- `map_skills` - Map Skills
- `fieldwork` - Fieldwork and Investigation

## 📅 Year Groups
- Year 1
- Year 2
- Year 3
- Year 4
- Year 5
- Year 6

## 🎯 Difficulty Levels
- Easy
- Medium
- Hard

## 🛠️ Step-by-Step Examples

### Example 1: Add a Single Question
```python
from question_database import add_maths_question

add_maths_question(
    topic="place_value",
    year_group="Year 3",
    difficulty="Medium",
    question_text="What is the value of the hundreds digit in 789?",
    options=["7", "8", "9", "700"],
    correct_answer="7",
    explanation="In 789, the hundreds digit is 7."
)
```

### Example 2: Add Multiple Questions
```python
from question_database import QuestionDatabase, create_question

db = QuestionDatabase()

questions = [
    create_question(
        "What is 5 × 6?",
        ["28", "30", "32", "35"],
        "30",
        "5 × 6 = 30"
    ),
    create_question(
        "What is 48 ÷ 6?",
        ["6", "7", "8", "9"],
        "8",
        "48 ÷ 6 = 8"
    )
]

db.add_multiple_questions("maths", "multiplication_division", "Year 4", "Medium", questions)
```

### Example 3: Bulk Import from JSON
```json
[
  {
    "subject": "science",
    "topic": "living_things",
    "year_group": "Year 2",
    "difficulty": "Easy",
    "question": "Which of these is a mammal?",
    "options": ["Fish", "Bird", "Dog", "Snake"],
    "correct_answer": "Dog",
    "explanation": "A dog is a mammal that gives birth to live young and feeds them milk."
  },
  {
    "subject": "science",
    "topic": "materials",
    "year_group": "Year 3",
    "difficulty": "Medium",
    "question": "What material is best for making a window?",
    "options": ["Wood", "Glass", "Metal", "Plastic"],
    "correct_answer": "Glass",
    "explanation": "Glass is transparent, allowing light to pass through, making it ideal for windows."
  }
]
```

## 🔧 Advanced Usage

### View Question Statistics
```python
from question_database import QuestionDatabase

db = QuestionDatabase()
stats = db.list_all_questions()
print(stats)
```

### Get Question Count
```python
count = db.get_question_count("maths", "place_value", "Year 3", "Medium")
print(f"Available questions: {count}")
```

### Export All Questions
```python
from question_admin import export_questions
export_questions()  # This will prompt for filename
```

## 📋 Best Practices

### 1. Question Writing
- Keep questions clear and age-appropriate
- Ensure all options are plausible
- Provide clear explanations
- Follow UK curriculum guidelines

### 2. Difficulty Levels
- **Easy**: Basic concepts, simple calculations
- **Medium**: More complex problems, multiple steps
- **Hard**: Advanced concepts, problem-solving

### 3. Year Group Progression
- **Year 1-2**: Numbers to 100, basic operations
- **Year 3-4**: Numbers to 1000, multiplication tables
- **Year 5-6**: Larger numbers, complex operations

### 4. File Management
- Keep JSON files well-organized
- Use descriptive filenames
- Backup your question files regularly
- Validate JSON syntax before importing

## 🚨 Troubleshooting

### Common Issues

**1. Question not appearing**
- Check the subject/topic spelling
- Verify year group and difficulty match exactly
- Ensure JSON syntax is correct

**2. Import errors**
- Validate JSON format using online tools
- Check file encoding (should be UTF-8)
- Ensure all required fields are present

**3. Duplicate questions**
- The system allows duplicates
- Use the admin interface to view existing questions
- Consider adding unique identifiers if needed

### Validation Checklist
- [ ] Question text is clear and complete
- [ ] Exactly 4 options provided
- [ ] Correct answer matches one of the options
- [ ] Explanation is helpful and accurate
- [ ] Subject and topic names are correct
- [ ] Year group and difficulty are valid
- [ ] JSON syntax is correct

## 🔄 Integration with Main App

The question database automatically integrates with the main application. When you add questions:

1. They're saved to JSON files in `question_data/`
2. The main app loads them automatically
3. No code changes needed in `app.py` or `question_bank.py`
4. Questions appear immediately in the web interface

## 📈 Scaling Up

### For Large Question Banks
1. **Organize by subject**: Create separate JSON files for each subject
2. **Use bulk imports**: Prepare questions in Excel/Google Sheets, export as JSON
3. **Version control**: Keep question files in Git for tracking changes
4. **Backup regularly**: Questions are valuable - back them up!

### For Teams
1. **Shared templates**: Use the provided JSON templates
2. **Review process**: Have questions reviewed before adding
3. **Quality control**: Regular audits of question quality
4. **Documentation**: Keep notes on question sources and curriculum alignment

## 🎉 Success Tips

1. **Start small**: Add a few questions and test them
2. **Use the admin interface**: It's designed to be user-friendly
3. **Follow the format**: Use the provided templates and examples
4. **Test regularly**: Generate worksheets to check question quality
5. **Get feedback**: Ask teachers and students for input

---

**Remember**: You can add unlimited questions without touching any code! The system is designed to be flexible and user-friendly. 🚀
