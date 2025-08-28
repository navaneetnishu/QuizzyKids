from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        # Subtitle style
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.darkgreen
        )
        
        # Question style
        self.question_style = ParagraphStyle(
            'Question',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            spaceBefore=15,
            leftIndent=20,
            textColor=colors.black
        )
        
        # Option style
        self.option_style = ParagraphStyle(
            'Option',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=5,
            leftIndent=40,
            textColor=colors.black
        )
        
        # Answer style
        self.answer_style = ParagraphStyle(
            'Answer',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=10,
            leftIndent=20,
            textColor=colors.darkred,
            backColor=colors.lightyellow
        )
        
        # Explanation style
        self.explanation_style = ParagraphStyle(
            'Explanation',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=15,
            leftIndent=20,
            textColor=colors.darkblue,
            fontName='Helvetica-Oblique'
        )

    def generate_worksheet(self, questions, subject, topic, year_group, difficulty, output_path):
        """Generate a printable worksheet PDF"""
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Header
        title = Paragraph(f"Mathematics Worksheet", self.title_style)
        story.append(title)
        
        subtitle = Paragraph(f"{subject.title()} - {topic.replace('_', ' ').title()}", self.subtitle_style)
        story.append(subtitle)
        
        # Worksheet info
        info_text = f"Year Group: {year_group} | Difficulty: {difficulty} | Questions: {len(questions)}"
        info_para = Paragraph(info_text, self.styles['Normal'])
        story.append(info_para)
        story.append(Spacer(1, 20))
        
        # Instructions
        instructions = Paragraph(
            "Instructions: Circle the correct answer for each question below.",
            self.styles['Normal']
        )
        story.append(instructions)
        story.append(Spacer(1, 20))
        
        # Questions
        for i, question in enumerate(questions, 1):
            # Question text
            question_text = f"<b>Question {i}:</b> {question['question']}"
            question_para = Paragraph(question_text, self.question_style)
            story.append(question_para)
            
            # Options
            for j, option in enumerate(question['options']):
                option_text = f"<b>{chr(65 + j)}.</b> {option}"
                option_para = Paragraph(option_text, self.option_style)
                story.append(option_para)
            
            story.append(Spacer(1, 10))
        
        # Footer
        story.append(Spacer(1, 30))
        footer = Paragraph(
            f"Generated on: {self._get_current_date()} | UK Curriculum Aligned",
            self.styles['Normal']
        )
        story.append(footer)
        
        # Build PDF
        doc.build(story)

    def generate_answer_key(self, questions, subject, topic, year_group, difficulty, output_path):
        """Generate an answer key PDF"""
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Header
        title = Paragraph(f"Answer Key", self.title_style)
        story.append(title)
        
        subtitle = Paragraph(f"{subject.title()} - {topic.replace('_', ' ').title()}", self.subtitle_style)
        story.append(subtitle)
        
        # Worksheet info
        info_text = f"Year Group: {year_group} | Difficulty: {difficulty} | Questions: {len(questions)}"
        info_para = Paragraph(info_text, self.styles['Normal'])
        story.append(info_para)
        story.append(Spacer(1, 20))
        
        # Answer table
        answer_data = [['Question', 'Correct Answer', 'Explanation']]
        
        for i, question in enumerate(questions, 1):
            # Find the letter of the correct answer
            correct_index = question['options'].index(question['correct_answer'])
            correct_letter = chr(65 + correct_index)
            
            answer_data.append([
                f"Question {i}",
                f"{correct_letter}. {question['correct_answer']}",
                question['explanation']
            ])
        
        # Create table
        table = Table(answer_data, colWidths=[1*inch, 2*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige, colors.white])
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Summary
        summary_text = f"Total Questions: {len(questions)} | Subject: {subject.title()} | Topic: {topic.replace('_', ' ').title()}"
        summary_para = Paragraph(summary_text, self.styles['Normal'])
        story.append(summary_para)
        
        # Footer
        story.append(Spacer(1, 20))
        footer = Paragraph(
            f"Answer Key Generated on: {self._get_current_date()} | UK Curriculum Aligned",
            self.styles['Normal']
        )
        story.append(footer)
        
        # Build PDF
        doc.build(story)

    def _get_current_date(self):
        """Get current date in a formatted string"""
        from datetime import datetime
        return datetime.now().strftime("%B %d, %Y")

    def generate_preview_worksheet(self, questions, subject, topic, year_group, difficulty):
        """Generate a preview worksheet (returns HTML for web display)"""
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
            <h1 style="text-align: center; color: #2c3e50; margin-bottom: 10px;">Mathematics Worksheet</h1>
            <h2 style="text-align: center; color: #27ae60; margin-bottom: 20px;">{subject.title()} - {topic.replace('_', ' ').title()}</h2>
            
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                <p><strong>Year Group:</strong> {year_group} | <strong>Difficulty:</strong> {difficulty} | <strong>Questions:</strong> {len(questions)}</p>
            </div>
            
            <div style="background-color: #e8f4fd; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                <p><strong>Instructions:</strong> Circle the correct answer for each question below.</p>
            </div>
        """
        
        for i, question in enumerate(questions, 1):
            html_content += f"""
            <div style="margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px;">
                <p style="font-weight: bold; margin-bottom: 10px;">Question {i}: {question['question']}</p>
            """
            
            for j, option in enumerate(question['options']):
                html_content += f"""
                <p style="margin-left: 20px; margin-bottom: 5px;">{chr(65 + j)}. {option}</p>
                """
            
            html_content += "</div>"
        
        html_content += f"""
            <div style="margin-top: 30px; padding: 15px; background-color: #f8f9fa; border-radius: 5px;">
                <p style="text-align: center; color: #666;">Generated on: {self._get_current_date()} | UK Curriculum Aligned</p>
            </div>
        </div>
        """
        
        return html_content

    def generate_preview_answer_key(self, questions, subject, topic, year_group, difficulty):
        """Generate a preview answer key (returns HTML for web display)"""
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
            <h1 style="text-align: center; color: #2c3e50; margin-bottom: 10px;">Answer Key</h1>
            <h2 style="text-align: center; color: #27ae60; margin-bottom: 20px;">{subject.title()} - {topic.replace('_', ' ').title()}</h2>
            
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                <p><strong>Year Group:</strong> {year_group} | <strong>Difficulty:</strong> {difficulty} | <strong>Questions:</strong> {len(questions)}</p>
            </div>
            
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                <thead>
                    <tr style="background-color: #34495e; color: white;">
                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Question</th>
                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Correct Answer</th>
                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Explanation</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for i, question in enumerate(questions, 1):
            # Find the letter of the correct answer
            correct_index = question['options'].index(question['correct_answer'])
            correct_letter = chr(65 + correct_index)
            
            row_color = "#f8f9fa" if i % 2 == 0 else "white"
            
            html_content += f"""
                <tr style="background-color: {row_color};">
                    <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">Question {i}</td>
                    <td style="padding: 12px; border: 1px solid #ddd; color: #e74c3c; font-weight: bold;">{correct_letter}. {question['correct_answer']}</td>
                    <td style="padding: 12px; border: 1px solid #ddd;">{question['explanation']}</td>
                </tr>
            """
        
        html_content += f"""
                </tbody>
            </table>
            
            <div style="margin-top: 20px; padding: 15px; background-color: #f8f9fa; border-radius: 5px;">
                <p style="text-align: center; color: #666;">Answer Key Generated on: {self._get_current_date()} | UK Curriculum Aligned</p>
            </div>
        </div>
        """
        
        return html_content
