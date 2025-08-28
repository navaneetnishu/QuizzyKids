<<<<<<< HEAD
# 🎓 Kids Practice PDF Generator

A comprehensive PDF multiple-choice question generator designed specifically for UK curriculum students in Years 1-6. This application creates printable worksheets and answer keys for various subjects with age-appropriate difficulty levels.

## 🌟 Features

### 📚 Subjects Covered
- **Mathematics** (Fully Implemented)
  - Number: Place Value
  - Number: Addition & Subtraction
  - Number: Multiplication & Division
  - Number: Fractions, Decimals & Percentages
  - Ratio & Proportion
  - Algebra
  - Measurement
  - Geometry: Properties of Shape
  - Geometry: Position & Direction
  - Statistics

- **Other Subjects** (Placeholder Structure Ready)
  - Science
  - Computing
  - History
  - Geography

### 🎯 Key Features
- **UK Curriculum Aligned**: Questions follow the National Curriculum for England
- **Age-Appropriate Difficulty**: Easy, Medium, and Hard levels for each year group
- **Printable PDFs**: Professional worksheet and answer key generation
- **Interactive Preview**: Preview questions before generating PDFs
- **Kid-Friendly Interface**: Colorful, engaging design with emojis
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd KidsPracticePDF
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## 📖 Usage Guide

### Creating a Worksheet

1. **Select Subject**: Choose from Mathematics (other subjects coming soon)
2. **Choose Topic**: Pick a specific topic within the subject
3. **Set Year Group**: Select Year 1-6 based on student age
4. **Choose Difficulty**: Easy 🌱, Medium 🌿, or Hard 🌳
5. **Set Question Count**: 5-50 questions per worksheet
6. **Preview or Generate**: 
   - Click "👀 Preview Questions" to see questions first
   - Click "📄 Generate PDF" to create printable worksheets

### Download Options

- **📄 Download Worksheet**: Student-friendly PDF with questions
- **🔑 Download Answer Key**: Teacher/parent answer key with explanations

## 🏗️ Project Structure

```
KidsPracticePDF/
├── app.py                 # Main Flask application
├── question_bank.py       # Question generation logic
├── pdf_generator.py       # PDF creation utilities
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── templates/
    └── index.html        # Main web interface
```

## 🔧 Technical Details

### Backend (Python/Flask)
- **Flask**: Web framework for the application
- **ReportLab**: PDF generation library
- **Question Bank**: Comprehensive question database with UK curriculum alignment

### Frontend (HTML/CSS/JavaScript)
- **Responsive Design**: Works on all device sizes
- **Modern UI**: Kid-friendly interface with animations
- **Interactive Features**: Real-time preview and validation

### PDF Generation
- **Professional Layout**: Clean, printable worksheets
- **Answer Keys**: Detailed explanations for each question
- **UK Curriculum Branding**: Official curriculum alignment

## 📊 Question Types by Year Group

### Year 1-2
- Numbers up to 100
- Basic addition/subtraction
- Simple shapes and patterns
- Basic measurement concepts

### Year 3-4
- Numbers up to 1000
- Multiplication tables (2-12)
- Fractions and decimals
- Coordinates and position

### Year 5-6
- Numbers up to 10,000
- Complex operations
- Algebra and equations
- Advanced geometry and statistics

## 🎨 Customization

### Adding New Questions
Edit `question_bank.py` to add new question types:

```python
def _generate_new_topic_questions(self, year_group, difficulty, num_questions):
    # Add your question generation logic here
    pass
```

### Modifying PDF Layout
Edit `pdf_generator.py` to customize PDF appearance:

```python
def generate_worksheet(self, questions, subject, topic, year_group, difficulty, output_path):
    # Modify PDF generation logic here
    pass
```

### Styling Changes
Edit `templates/index.html` to modify the web interface appearance.

## 🔮 Future Enhancements

### Planned Features
- [ ] Science questions (Biology, Chemistry, Physics)
- [ ] Computing questions (Programming, Digital Literacy)
- [ ] History questions (British and World History)
- [ ] Geography questions (Physical and Human Geography)
- [ ] Question image support
- [ ] Multiple worksheet formats
- [ ] Student progress tracking
- [ ] Teacher dashboard

### Contributing
1. Fork the repository
2. Create a feature branch
3. Add your enhancements
4. Submit a pull request

## 📝 License

This project is designed for educational use. Please ensure compliance with UK curriculum guidelines when using in educational settings.

## 🤝 Support

For questions or support:
- Check the documentation above
- Review the code comments
- Create an issue for bugs or feature requests

## 🎯 Educational Use

This application is designed to support:
- **Teachers**: Create differentiated worksheets for their classes
- **Parents**: Provide additional practice for their children
- **Tutors**: Generate targeted practice materials
- **Students**: Access age-appropriate learning materials

---

**Made with ❤️ for UK Education**
=======
# QuizzyKids
PDF MCQ generator
>>>>>>> 5b8aa329595ca25d13a6c1acc2852a984c984ff5
