"""
PDF Generator Module
Generates professional PDF question papers from predicted paper data.
Uses ReportLab library for PDF creation.
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.colors import HexColor


def create_pdf(predicted_paper):
    """
    Generate a professionally formatted PDF exam paper from predicted questions.

    Args:
        predicted_paper: Dictionary with three sections:
            {
                "section_a": [list of short answer questions],
                "section_b": [list of medium answer questions],
                "section_c": [list of long answer questions]
            }

    Returns:
        str: Relative file path to the generated PDF (e.g., "static/generated/predicted_paper.pdf")

    Raises:
        Exception: If PDF generation fails
    """

    print("\n" + "="*60)
    print("📄 PDF GENERATION STARTED")
    print("="*60)

    # Step 1: Ensure output directory exists
    output_dir = os.path.join("static", "generated")
    os.makedirs(output_dir, exist_ok=True)
    print(f"✅ Output directory verified: {output_dir}")

    # Step 2: Define output file path
    filename = "predicted_paper.pdf"
    filepath = os.path.join(output_dir, filename)
    print(f"📁 PDF will be saved to: {filepath}")

    try:
        # Step 3: Create PDF document with A4 page size
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        print("✅ PDF document template created")

        # Step 4: Define custom styles for the document
        styles = getSampleStyleSheet()

        # Main title style
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=HexColor('#1a237e'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )

        # Subtitle style
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=HexColor('#424242'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica'
        )

        # Section heading style
        section_style = ParagraphStyle(
            'SectionHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=HexColor('#d32f2f'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold',
            borderPadding=10
        )

        # Question style
        question_style = ParagraphStyle(
            'Question',
            parent=styles['Normal'],
            fontSize=11,
            textColor=HexColor('#212121'),
            spaceAfter=14,
            leftIndent=20,
            fontName='Helvetica',
            leading=16
        )

        # Instructions style
        instructions_style = ParagraphStyle(
            'Instructions',
            parent=styles['Normal'],
            fontSize=10,
            textColor=HexColor('#424242'),
            spaceAfter=15,
            fontName='Helvetica-Oblique',
            leftIndent=10
        )

        print("✅ Custom styles configured")

        # Step 5: Build the PDF content
        story = []  # This will hold all PDF elements

        # Add title
        story.append(Paragraph("PREDICTED QUESTION PAPER", title_style))
        story.append(Spacer(1, 0.1*inch))

        # Add subtitle with generation date
        generation_date = datetime.now().strftime("%B %d, %Y")
        story.append(Paragraph(f"AI-Generated Exam Paper | {generation_date}", subtitle_style))
        story.append(Spacer(1, 0.2*inch))

        # Add instructions
        instructions = """
        <b>Instructions:</b><br/>
        • This paper is generated based on analysis of multiple previous year question papers.<br/>
        • Section C contains the most important questions (highest priority).<br/>
        • Focus your preparation on Section C first, then Section B, then Section A.<br/>
        • Time management is crucial during the actual exam.
        """
        story.append(Paragraph(instructions, instructions_style))
        story.append(Spacer(1, 0.3*inch))

        print("✅ Header and instructions added")

        # Step 6: Add SECTION C (Long Answer - Most Important)
        story.append(Paragraph("SECTION C — Long Answer Questions", section_style))
        story.append(Paragraph("<i>(Answer any THREE questions. Each question carries 10 marks.)</i>",
                             instructions_style))
        story.append(Spacer(1, 0.1*inch))

        section_c = predicted_paper.get('section_c', [])
        if section_c and len(section_c) > 0:
            for i, question in enumerate(section_c, 1):
                # Clean and format question text
                clean_question = question.strip()
                question_text = f"<b>{i}.</b> {clean_question}"
                story.append(Paragraph(question_text, question_style))
            print(f"✅ Section C added: {len(section_c)} questions")
        else:
            story.append(Paragraph("<i>No questions available for this section.</i>", instructions_style))
            print("⚠️ Section C: No questions available")

        story.append(Spacer(1, 0.3*inch))

        # Step 7: Add SECTION B (Medium Answer Questions)
        story.append(Paragraph("SECTION B — Medium Answer Questions", section_style))
        story.append(Paragraph("<i>(Answer any FIVE questions. Each question carries 6 marks.)</i>",
                             instructions_style))
        story.append(Spacer(1, 0.1*inch))

        section_b = predicted_paper.get('section_b', [])
        if section_b and len(section_b) > 0:
            for i, question in enumerate(section_b, 1):
                clean_question = question.strip()
                question_text = f"<b>{i}.</b> {clean_question}"
                story.append(Paragraph(question_text, question_style))
            print(f"✅ Section B added: {len(section_b)} questions")
        else:
            story.append(Paragraph("<i>No questions available for this section.</i>", instructions_style))
            print("⚠️ Section B: No questions available")

        story.append(Spacer(1, 0.3*inch))

        # Step 8: Add SECTION A (Short Answer Questions)
        story.append(Paragraph("SECTION A — Short Answer Questions", section_style))
        story.append(Paragraph("<i>(Answer any FIVE questions. Each question carries 4 marks.)</i>",
                             instructions_style))
        story.append(Spacer(1, 0.1*inch))

        section_a = predicted_paper.get('section_a', [])
        if section_a and len(section_a) > 0:
            for i, question in enumerate(section_a, 1):
                clean_question = question.strip()
                question_text = f"<b>{i}.</b> {clean_question}"
                story.append(Paragraph(question_text, question_style))
            print(f"✅ Section A added: {len(section_a)} questions")
        else:
            story.append(Paragraph("<i>No questions available for this section.</i>", instructions_style))
            print("⚠️ Section A: No questions available")

        # Step 9: Add footer
        story.append(Spacer(1, 0.5*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=HexColor('#757575'),
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique'
        )
        story.append(Paragraph("--- End of Question Paper ---", footer_style))
        story.append(Paragraph("Generated by PrepVision AI", footer_style))

        print("✅ All sections added to PDF")

        # Step 10: Build the PDF
        doc.build(story)
        print(f"✅ PDF successfully generated: {filepath}")

        # Step 11: Calculate total questions
        total_questions = len(section_a) + len(section_b) + len(section_c)
        print(f"📊 Total questions in PDF: {total_questions}")

        print("="*60)
        print("✅ PDF GENERATION COMPLETED SUCCESSFULLY")
        print("="*60 + "\n")

        # Return relative path for Flask to use
        return filepath

    except Exception as e:
        print(f"❌ ERROR during PDF generation: {str(e)}")
        raise Exception(f"Failed to generate PDF: {str(e)}")


# Testing function (runs only when this file is executed directly)
if __name__ == "__main__":
    print("\n" + "="*70)
    print("PDF GENERATOR MODULE - TEST RUN")
    print("="*70)

    # Sample predicted paper for testing
    test_paper = {
        "section_c": [
            "Explain the architecture of Convolutional Neural Networks (CNN) in detail with suitable diagrams.",
            "What is Natural Language Processing? Discuss various applications of NLP in real-world scenarios.",
            "Describe the working principle of Recurrent Neural Networks (RNN) and explain the vanishing gradient problem."
        ],
        "section_b": [
            "Differentiate between supervised learning and unsupervised learning with examples.",
            "Explain the concept of overfitting and underfitting in machine learning.",
            "What is transfer learning? How is it useful in deep learning applications?",
            "Describe the backpropagation algorithm used in neural networks.",
            "Explain the role of activation functions in neural networks."
        ],
        "section_a": [
            "Define artificial intelligence and machine learning.",
            "What is the difference between AI and ML?",
            "List the types of machine learning algorithms.",
            "What is a neural network?",
            "Define gradient descent optimization."
        ]
    }

    # Generate PDF
    try:
        pdf_path = create_pdf(test_paper)
        print(f"\n✅ TEST SUCCESSFUL!")
        print(f"📄 PDF saved at: {pdf_path}")
        print(f"🔗 You can open the file to verify the output.")
    except Exception as e:
        print(f"\n❌ TEST FAILED!")
        print(f"Error: {str(e)}")

    print("\n" + "="*70)


