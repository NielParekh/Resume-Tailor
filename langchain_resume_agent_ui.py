#!/usr/bin/env python3
"""
LangChain-based Agentic Resume Applier with Rich UI
A multi-agent workflow with beautiful progress visualization
"""

import os
import json
import re
import time
import hashlib
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

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich import box

# Load environment variables
load_dotenv()

console = Console()


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
        result = self.chain.invoke({"job_description": job_description})
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
        result = self.chain.invoke({
            "job_description": job_description,
            "resume": resume,
            "keywords": json.dumps(keywords, indent=2)
        })
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
        result = self.chain.invoke({
            "job_description": job_description,
            "resume": resume,
            "keywords": json.dumps(keywords, indent=2),
            "match_analysis": json.dumps(match_analysis, indent=2)
        })
        return result


class RecruiterEvaluationAgent:
    """Agent acting as a senior technical recruiter to evaluate candidacy"""

    def __init__(self, llm):
        self.llm = llm
        self.parser = JsonOutputParser()

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a senior technical recruiter with 15+ years of experience hiring for top tech companies.

Your role is to evaluate the candidate's profile and provide honest hiring insights.

Evaluate:
1. Overall candidacy strength (0-100)
2. Interview readiness
3. Competitive positioning
4. Red flags or concerns
5. Interview talking points
6. Salary negotiation leverage
7. Areas to prepare for interviews

Be honest and constructive. Provide actionable feedback.

Return ONLY a JSON object:
{{
    "candidacy_score": 85,
    "likelihood_to_proceed": "High/Medium/Low",
    "interview_readiness": {{
        "technical_prep": "Strong/Moderate/Weak",
        "behavioral_prep": "Strong/Moderate/Weak",
        "cultural_fit": "Strong/Moderate/Weak"
    }},
    "competitive_advantages": ["advantage1", "advantage2", ...],
    "potential_concerns": ["concern1", "concern2", ...],
    "key_talking_points": ["point1", "point2", ...],
    "salary_leverage": "High/Medium/Low with explanation",
    "interview_prep_focus": ["area1", "area2", ...],
    "recruiter_notes": "Honest assessment and recommendations"
}}"""),
            ("user", """Evaluate this candidate's profile for the role.

Job Description:
{job_description}

Tailored Resume:
{tailored_resume}

Match Analysis:
{match_analysis}

Provide your honest recruiter evaluation.""")
        ])

        self.chain = self.prompt | self.llm | self.parser

    def evaluate_candidacy(self, job_description: str, tailored_resume: str,
                          match_analysis: Dict) -> Dict:
        """Evaluate candidate from recruiter perspective"""
        result = self.chain.invoke({
            "job_description": job_description,
            "tailored_resume": tailored_resume,
            "match_analysis": json.dumps(match_analysis, indent=2)
        })
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
            elif line.startswith('- ') or line.startswith('• '):
                content = line[2:]
                content = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', content)
                style = ParagraphStyle('Bullet', parent=styles['Normal'],
                                     leftIndent=20, bulletIndent=10)
                story.append(Paragraph('• ' + content, style))
            elif line.startswith('*') and not line.startswith('**'):
                content = line[1:]
                content = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', content)
                story.append(Paragraph('<i>' + content + '</i>', styles['Normal']))
            else:
                content = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', line)
                story.append(Paragraph(content, styles['Normal']))

        doc.build(story)


class ResumeCache:
    """Cache for parsed resume content to avoid re-parsing on every run"""

    _cache: Dict[str, str] = {}  # Maps file hash to parsed content
    _path_hash_map: Dict[str, str] = {}  # Maps file path to hash for quick lookup

    @classmethod
    def _get_file_hash(cls, file_path: str) -> str:
        """Generate hash based on file path and modification time"""
        mtime = os.path.getmtime(file_path)
        return hashlib.md5(f"{file_path}:{mtime}".encode()).hexdigest()

    @classmethod
    def get(cls, file_path: str) -> Optional[str]:
        """Get cached resume content if available and file hasn't changed"""
        if not os.path.exists(file_path):
            return None

        current_hash = cls._get_file_hash(file_path)
        cached_hash = cls._path_hash_map.get(file_path)

        if cached_hash == current_hash and current_hash in cls._cache:
            return cls._cache[current_hash]
        return None

    @classmethod
    def set(cls, file_path: str, content: str) -> None:
        """Cache parsed resume content"""
        file_hash = cls._get_file_hash(file_path)
        cls._cache[file_hash] = content
        cls._path_hash_map[file_path] = file_hash

    @classmethod
    def clear(cls) -> None:
        """Clear all cached content"""
        cls._cache.clear()
        cls._path_hash_map.clear()


class LangChainResumeAgentUI:
    """Main orchestrator with Rich UI for the agentic resume workflow"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the multi-agent system"""
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found")

        self.llm = ChatAnthropic(
            model="claude-sonnet-4-5-20250929",
            anthropic_api_key=self.api_key,
            temperature=0.7
        )

        self.keyword_agent = KeywordExtractorAgent(self.llm)
        self.match_agent = MatchScoreAgent(self.llm)
        self.tailor_agent = ResumeTailoringAgent(self.llm)
        self.recruiter_agent = RecruiterEvaluationAgent(self.llm)
        self.pdf_generator = ResumePDFGenerator()
        self.resume_cache = ResumeCache

    def load_resume(self, resume_path: str) -> str:
        """Load resume from PDF or text file, using cache if available"""
        # Check cache first
        cached_content = self.resume_cache.get(resume_path)
        if cached_content is not None:
            return cached_content

        # Parse the resume
        if resume_path.lower().endswith('.pdf'):
            reader = PdfReader(resume_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            content = text.strip()
        else:
            with open(resume_path, 'r', encoding='utf-8') as f:
                content = f.read()

        # Cache the parsed content
        self.resume_cache.set(resume_path, content)
        return content

    def display_keywords(self, keywords: Dict):
        """Display extracted keywords in a nice table"""
        table = Table(title="📋 Extracted Keywords", box=box.ROUNDED, show_header=True, header_style="bold magenta")
        table.add_column("Category", style="cyan", no_wrap=True)
        table.add_column("Keywords", style="white")

        for category, kw_list in keywords.items():
            if kw_list:
                category_name = category.replace('_', ' ').title()
                keywords_str = ", ".join(kw_list[:5])  # Show first 5
                if len(kw_list) > 5:
                    keywords_str += f" (+{len(kw_list)-5} more)"
                table.add_row(category_name, keywords_str)

        console.print(table)
        console.print()

    def display_match_score(self, match_analysis: Dict):
        """Display match score with visual bars"""
        score = match_analysis['overall_match_percentage']

        # Overall score panel
        if score >= 85:
            color = "green"
            emoji = "🎉"
            status = "Excellent Match!"
        elif score >= 70:
            color = "yellow"
            emoji = "👍"
            status = "Good Match"
        elif score >= 60:
            color = "orange"
            emoji = "⚠️"
            status = "Moderate Match"
        else:
            color = "red"
            emoji = "❌"
            status = "Low Match"

        score_text = Text()
        score_text.append(f"{emoji} {score}% ", style=f"bold {color}")
        score_text.append(status, style=f"{color}")

        console.print(Panel(score_text, title="Overall Match Score", border_style=color))
        console.print()

        # Category scores
        table = Table(title="📊 Category Breakdown", box=box.ROUNDED)
        table.add_column("Category", style="cyan")
        table.add_column("Score", justify="right", style="magenta")
        table.add_column("Progress", width=30)

        for category, score in match_analysis['category_scores'].items():
            category_name = category.replace('_', ' ').title()
            bar_length = int(score / 100 * 20)
            bar = "█" * bar_length + "░" * (20 - bar_length)

            if score >= 80:
                bar_color = "green"
            elif score >= 60:
                bar_color = "yellow"
            else:
                bar_color = "red"

            table.add_row(
                category_name,
                f"{score}%",
                Text(bar, style=bar_color)
            )

        console.print(table)
        console.print()

        # Strengths
        if match_analysis['strengths']:
            console.print("[bold green]✓ Strengths:[/bold green]")
            for strength in match_analysis['strengths'][:3]:
                console.print(f"  • {strength}", style="green")
            console.print()

        # Gaps
        if match_analysis['gaps']:
            console.print("[bold red]✗ Gaps:[/bold red]")
            for gap in match_analysis['gaps'][:3]:
                console.print(f"  • {gap}", style="red")
            console.print()

        # Recommendation
        console.print(Panel(match_analysis['recommendation'], title="💡 Recommendation", border_style="blue"))
        console.print()

    def display_recruiter_evaluation(self, evaluation: Dict):
        """Display recruiter evaluation in a professional format"""
        score = evaluation['candidacy_score']
        likelihood = evaluation['likelihood_to_proceed']

        # Candidacy score panel
        if score >= 80:
            color = "green"
            emoji = "🌟"
        elif score >= 60:
            color = "yellow"
            emoji = "👍"
        else:
            color = "red"
            emoji = "⚠️"

        score_text = Text()
        score_text.append(f"{emoji} {score}/100 ", style=f"bold {color}")
        score_text.append(f"Likelihood: {likelihood}", style=color)

        console.print(Panel(score_text, title="👔 Senior Recruiter Evaluation", border_style=color))
        console.print()

        # Interview readiness
        table = Table(title="🎯 Interview Readiness", box=box.ROUNDED)
        table.add_column("Area", style="cyan")
        table.add_column("Assessment", style="white")

        for area, assessment in evaluation['interview_readiness'].items():
            area_name = area.replace('_', ' ').title()
            if assessment == "Strong":
                assessment_color = "green"
            elif assessment == "Moderate":
                assessment_color = "yellow"
            else:
                assessment_color = "red"

            table.add_row(area_name, Text(assessment, style=assessment_color))

        console.print(table)
        console.print()

        # Competitive advantages
        if evaluation['competitive_advantages']:
            console.print("[bold green]💪 Competitive Advantages:[/bold green]")
            for advantage in evaluation['competitive_advantages']:
                console.print(f"  • {advantage}", style="green")
            console.print()

        # Potential concerns
        if evaluation['potential_concerns']:
            console.print("[bold red]⚠️  Potential Concerns:[/bold red]")
            for concern in evaluation['potential_concerns']:
                console.print(f"  • {concern}", style="red")
            console.print()

        # Key talking points
        if evaluation['key_talking_points']:
            console.print("[bold blue]💬 Key Interview Talking Points:[/bold blue]")
            for i, point in enumerate(evaluation['key_talking_points'][:5], 1):
                console.print(f"  {i}. {point}", style="blue")
            console.print()

        # Salary leverage
        console.print(Panel(
            f"[bold]Salary Leverage:[/bold] {evaluation['salary_leverage']}",
            title="💰 Negotiation Position",
            border_style="yellow"
        ))
        console.print()

        # Interview prep focus
        if evaluation['interview_prep_focus']:
            console.print("[bold magenta]📚 Interview Prep Focus Areas:[/bold magenta]")
            for area in evaluation['interview_prep_focus']:
                console.print(f"  • {area}", style="magenta")
            console.print()

        # Recruiter notes
        console.print(Panel(
            evaluation['recruiter_notes'],
            title="📝 Recruiter's Honest Assessment",
            border_style="cyan"
        ))
        console.print()

    def process(self, job_description: str, resume_path: str, job_url: str = "Manual input") -> str:
        """Execute the complete agentic workflow with UI"""

        # Header
        console.print()
        console.print(Panel.fit(
            "[bold cyan]LangChain Agentic Resume Optimizer[/bold cyan]\n"
            "[dim]4-Agent AI Workflow with Senior Recruiter Evaluation[/dim]",
            border_style="cyan"
        ))
        console.print()

        # Load resume (uses cache if already parsed)
        console.print("[bold]Loading resume...[/bold]", style="dim")
        cached = self.resume_cache.get(resume_path) is not None
        current_resume = self.load_resume(resume_path)
        if cached:
            console.print(f"✓ Resume loaded from cache: [cyan]{os.path.basename(resume_path)}[/cyan]")
        else:
            console.print(f"✓ Resume parsed and cached: [cyan]{os.path.basename(resume_path)}[/cyan]")
        console.print()

        # Progress tracking
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console,
        ) as progress:

            # Step 1: Extract keywords
            task1 = progress.add_task("[cyan]Agent 1: Extracting keywords...", total=100)
            progress.update(task1, advance=20)

            keywords = self.keyword_agent.extract(job_description)

            progress.update(task1, advance=80, description="[green]✓ Agent 1: Keywords extracted")
            console.print()

            self.display_keywords(keywords)

            # Step 2: Calculate match
            task2 = progress.add_task("[yellow]Agent 2: Calculating match score...", total=100)
            progress.update(task2, advance=20)

            match_analysis = self.match_agent.calculate_match(
                job_description, current_resume, keywords
            )

            progress.update(task2, advance=80, description="[green]✓ Agent 2: Match score calculated")
            console.print()

            self.display_match_score(match_analysis)

            # Step 3: Create resume
            task3 = progress.add_task("[magenta]Agent 3: Generating tailored resume...", total=100)
            progress.update(task3, advance=20)

            tailored_resume = self.tailor_agent.create_resume(
                job_description, current_resume, keywords, match_analysis
            )

            progress.update(task3, advance=60)

            # Save files
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            pdf_path = f"tailored_resume_{timestamp}.pdf"
            self.pdf_generator.convert_to_pdf(tailored_resume, pdf_path)

            md_path = f"tailored_resume_{timestamp}.md"
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(tailored_resume)

            report_path = f"resume_analysis_{timestamp}.json"
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'job_url': job_url,
                    'timestamp': timestamp,
                    'keywords': keywords,
                    'match_analysis': match_analysis
                }, f, indent=2)

            progress.update(task3, advance=20, description="[green]✓ Agent 3: Resume generated and saved")

            # Step 4: Recruiter evaluation
            task4 = progress.add_task("[yellow]Agent 4: Senior recruiter evaluating candidacy...", total=100)
            progress.update(task4, advance=20)

            recruiter_evaluation = self.recruiter_agent.evaluate_candidacy(
                job_description, tailored_resume, match_analysis
            )

            progress.update(task4, advance=80, description="[green]✓ Agent 4: Recruiter evaluation complete")

        console.print()

        self.display_recruiter_evaluation(recruiter_evaluation)

        # Update report with recruiter evaluation
        with open(report_path, 'r', encoding='utf-8') as f:
            full_report = json.load(f)
        full_report['recruiter_evaluation'] = recruiter_evaluation
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(full_report, f, indent=2)

        # Summary
        console.print(Panel(
            f"[bold green]✓ 4-Agent Process Complete![/bold green]\n\n"
            f"[cyan]Resume Match Score:[/cyan] [bold]{match_analysis['overall_match_percentage']}%[/bold]\n"
            f"[cyan]Candidacy Score:[/cyan] [bold]{recruiter_evaluation['candidacy_score']}/100[/bold]\n"
            f"[cyan]Likelihood to Proceed:[/cyan] [bold]{recruiter_evaluation['likelihood_to_proceed']}[/bold]\n\n"
            f"[dim]Files generated:[/dim]\n"
            f"  • PDF Resume: [cyan]{pdf_path}[/cyan]\n"
            f"  • Markdown: [dim]{md_path}[/dim]\n"
            f"  • Full Analysis: [dim]{report_path}[/dim]",
            title="🎉 Success",
            border_style="green"
        ))

        return pdf_path


def main():
    """Main entry point"""
    import sys

    if len(sys.argv) < 2:
        console.print("[red]Usage:[/red] python langchain_resume_agent_ui.py <resume_file>")
        console.print("\nYou will be prompted to paste the job description.")
        sys.exit(1)

    resume_path = sys.argv[1]

    if not os.path.exists(resume_path):
        console.print(f"[red]Error:[/red] Resume file not found: {resume_path}")
        sys.exit(1)

    console.print("\n[bold]Paste the job description below.[/bold]")
    console.print("[dim]When finished, press Ctrl+D (Mac/Linux) or Ctrl+Z then Enter (Windows):[/dim]")
    console.print("─" * 60)

    job_description_lines = []
    try:
        while True:
            line = input()
            job_description_lines.append(line)
    except EOFError:
        pass

    job_description = '\n'.join(job_description_lines)

    if not job_description.strip():
        console.print("\n[red]Error:[/red] No job description provided")
        sys.exit(1)

    job_url = input("\nEnter job URL (optional, press Enter to skip): ").strip()
    if not job_url:
        job_url = "Manual input"

    try:
        agent = LangChainResumeAgentUI()
        agent.process(job_description, resume_path, job_url)
    except Exception as e:
        console.print(f"\n[red]Error:[/red] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
