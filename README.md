# LangChain Agentic Resume Optimizer 🤖

An intelligent multi-agent AI system that optimizes your resume for specific job applications.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run with beautiful UI (recommended!)
python3 langchain_resume_agent_ui.py "Niel Parekh New Resume.pdf"

# Or run without UI
python3 langchain_resume_agent.py "Niel Parekh New Resume.pdf"
```

Then paste the job description and press `Ctrl+D`.

## 🎨 NEW: Beautiful UI Version

The UI version features:
- ✨ Real-time progress bars
- 📊 Visual match score displays
- 🎯 Color-coded categories
- ⏱️ Time tracking per agent

See [UI_VERSION.md](UI_VERSION.md) for details!

## Features

✅ **Extract Keywords** - AI identifies critical keywords from job descriptions
✅ **Calculate Match %** - Get detailed 0-100% match score with category breakdown
✅ **Generate Resume PDF** - Creates professionally formatted, ATS-optimized resume
✅ **Recruiter Evaluation** - Senior technical recruiter assesses your candidacy 🆕
✅ **Interview Prep Insights** - Get talking points and salary leverage analysis 🆕
✅ **Multi-Agent System** - Four specialized LangChain agents working together

## Documentation

- **[START_HERE.md](START_HERE.md)** - Quick start guide (read this first!)
- **[AGENT4_RECRUITER.md](AGENT4_RECRUITER.md)** - 🆕 4th Agent: Recruiter evaluation
- **[PROMPTS.md](PROMPTS.md)** - All AI agent prompts and customization guide
- **[UI_VERSION.md](UI_VERSION.md)** - Beautiful UI features
- **[USAGE.md](USAGE.md)** - Detailed usage examples
- **[README_LANGCHAIN.md](README_LANGCHAIN.md)** - Complete documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture

## How It Works

### Step 1: Keyword Extraction
Identifies technical skills, soft skills, qualifications, tools, and certifications from the job description.

### Step 2: Match Scoring
Calculates how well your resume matches the job with detailed percentage breakdown and identifies strengths/gaps.

### Step 3: Resume Generation
Creates an optimized resume that naturally incorporates keywords and highlights relevant experience.

### Step 4: Recruiter Evaluation 🆕
A senior technical recruiter evaluates your candidacy, providing interview likelihood, talking points, salary leverage, and honest hiring insights.

## Output

You get three files for each job:
1. `tailored_resume_TIMESTAMP.pdf` - Submit this!
2. `tailored_resume_TIMESTAMP.md` - Editable version
3. `resume_analysis_TIMESTAMP.json` - Full analysis data

## Built With

- **LangChain** - Agent orchestration
- **Claude Sonnet 4.5** - AI model
- **Rich** - Beautiful terminal UI
- **ReportLab** - PDF generation
- **PyPDF2** - PDF reading

## License

MIT
