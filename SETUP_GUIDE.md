# 🚀 Quick Setup Guide

## Prerequisites
- Python 3.7 or higher installed
- Internet connection (for first-time dependency installation)

## Installation Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
**Option A: Using Python directly**
```bash
python app.py
```

**Option B: Using the batch file (Windows)**
```bash
start_app.bat
```

### 3. Access the Application
Open your web browser and go to:
```
http://localhost:5000
```

## 🎯 Quick Test

Run the test script to verify everything works:
```bash
python test_app.py
```

## 📚 How to Use

1. **Select Subject**: Choose Mathematics (other subjects coming soon)
2. **Choose Topic**: Pick from 10 different maths topics
3. **Set Year Group**: Year 1-6 based on student age
4. **Choose Difficulty**: Easy 🌱, Medium 🌿, or Hard 🌳
5. **Set Question Count**: 5-50 questions
6. **Preview or Generate**: 
   - Click "👀 Preview Questions" to see questions first
   - Click "📄 Generate PDF" to create printable worksheets

## 📄 Output Files

- **Worksheet PDF**: Student-friendly questions
- **Answer Key PDF**: Teacher/parent answers with explanations

## 🛠️ Troubleshooting

### Common Issues

**Import Error: No module named 'reportlab'**
```bash
pip install reportlab==4.0.4
```

**Flask not found**
```bash
pip install Flask
```

**Port already in use**
- Change the port in `app.py` line 122
- Or stop other applications using port 5000

### Getting Help

1. Check the full README.md for detailed documentation
2. Run `python test_app.py` to verify installation
3. Check the console output for error messages

## 🎓 Educational Use

This application is designed for:
- **Teachers**: Create differentiated worksheets
- **Parents**: Provide additional practice
- **Tutors**: Generate targeted materials
- **Students**: Access age-appropriate content

---

**Ready to create amazing worksheets! 🎉**
