#!/usr/bin/env python3
"""
LangChain-based Agentic Resume Applier
A multi-agent workflow for resume optimization
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT, TA_CENTER

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Load environment variables
load_dotenv()


class KeywordExtractorAgent:
    """Agent responsible for extracting keywords from job descriptions"""

    def __init__(self, llm):
        self.llm = llm
        self.parser = JsonOutputParser()

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert ATS (Applicant Tracking System) keyword analyzer.
Your job is to extract the most important keywords from job descriptions.

Extract:
1. Required technical skills
2. Required soft skills
3. Required qualifications
4. Important industry terms
5. Tools and technologies mentioned
6. Certifications or degrees required

Return ONLY a JSON object with this structure:
{{
    "technical_skills": ["skill1", "skill2", ...],
    "soft_skills": ["skill1", "skill2", ...],
    "qualifications": ["qual1", "qual2", ...],
    "tools_technologies": ["tool1", "tool2", ...],
    "certifications": ["cert1", "cert2", ...],
    "industry_terms": ["term1", "term2", ...]
}}"""),
            ("user", "Extract keywords from this job description:\n\n{job_description}")
        ])

        self.chain = self.prompt | self.llm | self.parser

    def extract(self, job_description: str) -> Dict:
        """Extract keywords from job description"""
        print("\n" + "="*60)
        print("STEP 1: Extracting Keywords from Job Description")
        print("="*60)

        result = self.chain.invoke({"job_description": job_description})

        # Display results
        print("\n✓ Keywords Extracted:")
        for category, keywords in result.items():
            if keywords:
                print(f"\n  {category.replace('_', ' ').title()}:")
                for kw in keywords:
                    print(f"    • {kw}")

        return result


class MatchScoreAgent:
    """Agent responsible for calculating resume-to-job match percentage"""

    def __init__(self, llm):
        self.llm = llm
        self.parser = JsonOutputParser()

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert resume analyzer specializing in ATS matching.

Analyze how well the candidate's resume matches the job description.

Consider:
1. Presence of required keywords
2. Relevant experience
3. Skills match
4. Qualifications match
5. Industry experience

Provide:
- Overall match percentage (0-100)
- Category-wise scores
- Strengths (what matches well)
- Gaps (what's missing)

Return ONLY a JSON object:
{{
    "overall_match_percentage": 85,
    "category_scores": {{
        "technical_skills": 90,
        "soft_skills": 80,
        "experience": 85,
        "qualifications": 75
    }},
    "strengths": ["strength1", "strength2", ...],
    "gaps": ["gap1", "gap2", ...],
    "recommendation": "Brief recommendation"
}}"""),
            ("user", """Job Description:
{job_description}

Candidate's Resume:
{resume}

Keywords from Job:
{keywords}

Analyze the match.""")
        ])

        self.chain = self.prompt | self.llm | self.parser

    def calculate_match(self, job_description: str, resume: str, keywords: Dict) -> Dict:
        """Calculate match percentage between resume and job"""
        print("\n" + "="*60)
        print("STEP 2: Calculating Resume Match Percentage")
        print("="*60)

        result = self.chain.invoke({
            "job_description": job_description,
            "resume": resume,
            "keywords": json.dumps(keywords, indent=2)
        })

        # Display results
        print(f"\n✓ Overall Match: {result['overall_match_percentage']}%")

        print("\n  Category Scores:")
        for category, score in result['category_scores'].items():
            print(f"    • {category.replace('_', ' ').title()}: {score}%")

        print("\n  Strengths:")
        for strength in result['strengths']:
            print(f"    ✓ {strength}")

        print("\n  Gaps:")
        for gap in result['gaps']:
            print(f"    ✗ {gap}")

        print(f"\n  Recommendation: {result['recommendation']}")

        return result


class ResumeTailoringAgent:
    """Agent responsible for creating optimized resume"""

    def __init__(self, llm):
        self.llm = llm
        self.parser = StrOutputParser()

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert resume writer and career consultant.

Create a professionally tailored resume that:
1. Incorporates keywords naturally from the job description
2. Highlights relevant experience and skills
3. Addresses identified gaps where truthful
4. Uses ATS-friendly formatting
5. Maintains truthfulness - NEVER fabricate experience

Use this standard format:

# [Full Name]
[Email] | [Phone] | [LinkedIn] | [Location]

## Professional Summary
[2-3 lines highlighting relevant experience and key strengths for this role]

## Experience

### [Job Title] - [Company Name]
*[Start Date - End Date]*

- [Achievement with quantifiable results relevant to target job]
- [Another relevant accomplishment]
- [Technical or leadership contribution]

[Repeat for each role]

## Education

### [Degree] - [University Name]
*[Graduation Date]*
[Relevant coursework if applicable]

## Technical Skills
**[Category]**: Skill1, Skill2, Skill3
[Repeat for different categories]

## Projects
[If relevant to the job, list significant projects]

## Certifications
[If applicable]

IMPORTANT:
- Use keywords from the job naturally
- Emphasize accomplishments that align with job requirements
- Keep all information truthful
- Format for ATS compatibility"""),
            ("user", """Create a tailored resume for this job.

Job Description:
{job_description}

Current Resume:
{resume}

Extracted Keywords:
{keywords}

Match Analysis:
{match_analysis}

Generate the complete tailored resume.""")
        ])

        self.chain = self.prompt | self.llm | self.parser

    def create_resume(self, job_description: str, resume: str,
                     keywords: Dict, match_analysis: Dict) -> str:
        """Create tailored resume"""
        print("\n" + "="*60)
        print("STEP 3: Creating Tailored Resume")
        print("="*60)

        result = self.chain.invoke({
            "job_description": job_description,
            "resume": resume,
            "keywords": json.dumps(keywords, indent=2),
            "match_analysis": json.dumps(match_analysis, indent=2)
        })

        print("\n✓ Tailored resume generated successfully")
        return result


class ResumePDFGenerator:
    """Utility class for generating PDF from resume text"""

    @staticmethod
    def convert_to_pdf(resume_text: str, output_path: str):
        """Convert resume text to professionally formatted PDF"""
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                              rightMargin=0.75*inch, leftMargin=0.75*inch,
                              topMargin=0.75*inch, bottomMargin=0.75*inch)

        story = []
        styles = getSampleStyleSheet()

        lines = resume_text.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                story.append(Spacer(1, 0.1*inch))
                continue

            # Headers
            if line.startswith('# '):
                content = line[2:]
                content = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', content)
                style = ParagraphStyle('CustomTitle', parent=styles['Heading1'],
                                     fontSize=16, spaceAfter=12, alignment=TA_CENTER)
                story.append(Paragraph(content, style))
            elif line.startswith('## '):
                content = line[3:]
                content = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', content)
                style = ParagraphStyle('CustomHeading', parent=styles['Heading2'],
                                     fontSize=14, spaceAfter=10)
                story.append(Paragraph(content, style))
            elif line.startswith('### '):
                content = line[4:]
                content = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', content)
                style = ParagraphStyle('CustomSubheading', parent=styles['Heading3'],
                                     fontSize=12, spaceAfter=8, bold=True)
                story.append(Paragraph(content, style))
            # Bullet points
            elif line.startswith('- ') or line.startswith('• '):
                content = line[2:]
                content = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', content)
                style = ParagraphStyle('Bullet', parent=styles['Normal'],
                                     leftIndent=20, bulletIndent=10)
                story.append(Paragraph('• ' + content, style))
            # Italic text
            elif line.startswith('*') and not line.startswith('**'):
                content = line[1:]
                content = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', content)
                story.append(Paragraph('<i>' + content + '</i>', styles['Normal']))
            else:
                # Regular paragraphs with bold support
                content = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', line)
                story.append(Paragraph(content, styles['Normal']))

        doc.build(story)


class LangChainResumeAgent:
    """Main orchestrator for the agentic resume workflow"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the multi-agent system"""
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found")

        # Initialize LLM
        self.llm = ChatAnthropic(
            model="claude-sonnet-4-5-20250929",
            anthropic_api_key=self.api_key,
            temperature=0.7
        )

        # Initialize agents
        self.keyword_agent = KeywordExtractorAgent(self.llm)
        self.match_agent = MatchScoreAgent(self.llm)
        self.tailor_agent = ResumeTailoringAgent(self.llm)
        self.pdf_generator = ResumePDFGenerator()

    def load_resume(self, resume_path: str) -> str:
        """Load resume from PDF or text file"""
        if resume_path.lower().endswith('.pdf'):
            reader = PdfReader(resume_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        else:
            with open(resume_path, 'r', encoding='utf-8') as f:
                return f.read()

    def process(self, job_description: str, resume_path: str,
                job_url: str = "Manual input") -> str:
        """Execute the complete agentic workflow"""
        print("\n" + "="*60)
        print("LANGCHAIN AGENTIC RESUME OPTIMIZER")
        print("="*60)

        # Load resume
        print(f"\nLoading resume from: {resume_path}")
        current_resume = self.load_resume(resume_path)

        # Step 1: Extract keywords
        keywords = self.keyword_agent.extract(job_description)

        # Step 2: Calculate match percentage
        match_analysis = self.match_agent.calculate_match(
            job_description, current_resume, keywords
        )

        # Step 3: Create tailored resume
        tailored_resume = self.tailor_agent.create_resume(
            job_description, current_resume, keywords, match_analysis
        )

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save PDF
        pdf_path = f"tailored_resume_{timestamp}.pdf"
        self.pdf_generator.convert_to_pdf(tailored_resume, pdf_path)
        print(f"\n✓ Resume saved as PDF: {pdf_path}")

        # Save markdown
        md_path = f"tailored_resume_{timestamp}.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(tailored_resume)
        print(f"✓ Markdown version saved: {md_path}")

        # Save analysis report
        report_path = f"resume_analysis_{timestamp}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump({
                'job_url': job_url,
                'timestamp': timestamp,
                'keywords': keywords,
                'match_analysis': match_analysis
            }, f, indent=2)
        print(f"✓ Analysis report saved: {report_path}")

        print("\n" + "="*60)
        print("WORKFLOW COMPLETE!")
        print("="*60)
        print(f"\nFinal Match Score: {match_analysis['overall_match_percentage']}%")
        print(f"Resume ready for application: {pdf_path}")

        return pdf_path


def main():
    """Main entry point"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python langchain_resume_agent.py <resume_file>")
        print("\nYou will be prompted to paste the job description.")
        sys.exit(1)

    resume_path = sys.argv[1]

    if not os.path.exists(resume_path):
        print(f"Error: Resume file not found: {resume_path}")
        sys.exit(1)

    print("Paste the job description below.")
    print("When finished, press Ctrl+D (Mac/Linux) or Ctrl+Z then Enter (Windows):")
    print("-" * 60)

    # Read multi-line input
    job_description_lines = []
    try:
        while True:
            line = input()
            job_description_lines.append(line)
    except EOFError:
        pass

    job_description = '\n'.join(job_description_lines)

    if not job_description.strip():
        print("\nError: No job description provided")
        sys.exit(1)

    # Optional job URL
    job_url = input("\nEnter job URL (optional, press Enter to skip): ").strip()
    if not job_url:
        job_url = "Manual input"

    try:
        agent = LangChainResumeAgent()
        agent.process(job_description, resume_path, job_url)
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
