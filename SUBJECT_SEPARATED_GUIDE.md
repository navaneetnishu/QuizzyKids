# 📚 Subject-Separated Question Management Guide

## 🎯 Overview

This system now uses **separate JSON files for each subject**, making it much easier to manage questions without redeploying the application. Questions are automatically reloaded when files are updated!

## 📁 File Structure

```
question_data/
├── maths_questions.json          # Mathematics questions
├── science_questions.json        # Science questions  
├── computing_questions.json      # Computing questions
├── history_questions.json        # History questions
└── geography_questions.json      # Geography questions
```

## 🚀 Key Benefits

### ✅ **No Redeployment Required**
- Questions are **automatically reloaded** when JSON files are updated
- The application detects file changes and refreshes the question cache
- You can add questions while the app is running!

### ✅ **Organized by Subject**
- Each subject has its own dedicated JSON file
- Easy to manage and maintain
- Clear separation of concerns

### ✅ **Hot-Reload System**
- File modification timestamps are tracked
- Changes are detected automatically
- No need to restart the Flask application

## 📝 JSON File Format

Each subject file follows this simple format:

```json
[
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
```

## 🛠️ How to Add Questions

### Method 1: Direct JSON Editing (Recommended)

1. **Open the subject file** you want to edit:
   ```bash
   # For maths questions
   notepad question_data/maths_questions.json
   
   # For science questions  
   notepad question_data/science_questions.json
   ```

2. **Add your question** in the correct format:
   ```json
   {
     "topic": "your_topic_name",
     "year_group": "Year 2",
     "difficulty": "Easy",
     "question": "Your question here?",
     "options": ["A", "B", "C", "D"],
     "correct_answer": "A",
     "explanation": "Explanation here."
   }
   ```

3. **Save the file** - questions are automatically reloaded!

### Method 2: Using Python Functions

```python
from question_database import add_maths_question

# Add a maths question
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

### Method 3: Admin Interface

```bash
python question_admin.py
```

## 📊 Topic Names for Each Subject

### Mathematics (`maths_questions.json`)
- `place_value`
- `addition_subtraction`
- `multiplication_division`
- `fractions_decimals`
- `ratio_proportion`
- `algebra`
- `measurement`
- `geometry_shape`
- `geometry_position`
- `statistics`

### Science (`science_questions.json`)
- `living_things`
- `materials`
- `forces`
- `earth_space`
- `light_sound`

### Computing (`computing_questions.json`)
- `algorithms`
- `data`
- `networks`
- `digital_literacy`
- `computational_thinking`

### History (`history_questions.json`)
- `ancient_civilizations`
- `british_history`
- `world_history`
- `local_history`
- `historical_skills`

### Geography (`geography_questions.json`)
- `physical_geography`
- `human_geography`
- `environmental`
- `map_skills`
- `fieldwork`

## 🔄 Hot-Reload System

### How It Works
1. **File Monitoring**: The system tracks when each JSON file was last modified
2. **Automatic Detection**: When a file is updated, the system detects the change
3. **Cache Invalidation**: The question cache for that subject is cleared
4. **Reload**: Questions are automatically reloaded from the updated file

### Benefits
- ✅ **No restart required**
- ✅ **Immediate availability** of new questions
- ✅ **Efficient**: Only reloads changed subjects
- ✅ **Safe**: Fallback to generated questions if file is corrupted

## 📈 Question Statistics

You can check question statistics for any subject:

```python
from question_database import QuestionDatabase

db = QuestionDatabase()
stats = db.get_subject_stats("maths")
print(f"Total maths questions: {stats['total_questions']}")
print(f"Topics: {stats['topics']}")
print(f"Year groups: {stats['year_groups']}")
print(f"Difficulties: {stats['difficulties']}")
```

## 🚨 Important Notes

### File Format Requirements
- **Must be valid JSON** - use a JSON validator if unsure
- **UTF-8 encoding** - for special characters and emojis
- **Array format** - questions must be in a JSON array `[]`

### Best Practices
1. **Backup your files** before making major changes
2. **Test questions** in the web interface after adding
3. **Use consistent topic names** (see list above)
4. **Include explanations** for all questions
5. **Balance difficulties** across year groups

### Error Handling
- If a JSON file is corrupted, the system falls back to generated questions
- Check the console output for error messages
- Invalid JSON will cause the file to be skipped

## 🔧 Troubleshooting

### Questions Not Appearing
1. **Check JSON syntax** - use a JSON validator
2. **Verify topic names** - must match exactly
3. **Check file encoding** - must be UTF-8
4. **Restart the application** if hot-reload isn't working

### File Not Found
1. **Check file path** - should be in `question_data/` folder
2. **Verify filename** - must match subject name exactly
3. **Create the file** if it doesn't exist

### Performance Issues
1. **Limit file size** - keep files under 1MB
2. **Optimize JSON** - remove unnecessary whitespace
3. **Use efficient structure** - avoid deeply nested objects

## 📋 Example Workflow

### Adding New Maths Questions

1. **Open the file**:
   ```bash
   notepad question_data/maths_questions.json
   ```

2. **Add questions**:
   ```json
   [
     {
       "topic": "place_value",
       "year_group": "Year 2",
       "difficulty": "Easy",
       "question": "What is the value of the ones digit in 67?",
       "options": ["6", "7", "60", "70"],
       "correct_answer": "7",
       "explanation": "In 67, the ones digit is 7."
     }
   ]
   ```

3. **Save and test**:
   - Save the file
   - Go to the web interface
   - Select Mathematics → Place Value → Year 2 → Easy
   - Your new question should appear!

## 🎉 Summary

This new system provides:
- **Easy management** with separate files per subject
- **No redeployment** required for question updates
- **Automatic reloading** when files change
- **Fallback system** to generated questions
- **Better organization** and maintainability

**You can now add questions without touching any code!** 🚀
