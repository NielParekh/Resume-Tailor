# LangChain Agentic Resume Optimizer

AI-powered 4-agent system that optimizes resumes for specific job applications using LangChain and Claude Sonnet 4.5.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run with UI (recommended)
python3 langchain_resume_agent_ui.py "YourResume.pdf"

# Paste job description and press Ctrl+D
```

## Features

- **Extract Keywords** - Identifies critical ATS keywords from job descriptions
- **Match Scoring** - 0-100% match score with category breakdown
- **Generate Resume PDF** - ATS-optimized, professionally formatted
- **Recruiter Evaluation** - Real hiring insights and interview prep
- **Beautiful UI** - Real-time progress bars and color-coded results

---

## How It Works

```
Job Description → [Agent 1: Keywords] → [Agent 2: Match %] → [Agent 3: Resume] → [Agent 4: Recruiter] → Output
```

**Agent 1: Keyword Extractor** - Identifies technical skills, soft skills, qualifications, tools, and certifications

**Agent 2: Match Scorer** - Calculates 0-100% match score with category breakdown and identifies strengths/gaps

**Agent 3: Resume Tailor** - Creates ATS-optimized resume with natural keyword incorporation

**Agent 4: Recruiter Evaluator** - Provides hiring insights, interview prep, and salary leverage analysis

---

## Output Files

Three files generated per run:
1. **`tailored_resume_TIMESTAMP.pdf`** - Submit this
2. **`tailored_resume_TIMESTAMP.md`** - Editable version
3. **`resume_analysis_TIMESTAMP.json`** - Full analysis with recruiter insights

## Usage

```bash
# With UI (recommended)
python3 langchain_resume_agent_ui.py "YourResume.pdf"

# Without UI
python3 langchain_resume_agent.py "YourResume.pdf"

# With job URL
python3 langchain_resume_agent_url_ui.py "JOB_URL" "YourResume.pdf"
```

## Match Score Guide

| Score | Meaning | Recommendation |
|-------|---------|----------------|
| 85-100% | Excellent | Apply with confidence |
| 70-84% | Good | Emphasize relevant skills |
| 60-69% | Moderate | Highlight transferable experience |
| <60% | Low | Consider skill gap |

---

## Technical Stack

- **LangChain** - Multi-agent orchestration
- **Claude Sonnet 4.5** - AI model
- **Rich** - Terminal UI with progress bars
- **ReportLab** - PDF generation
- **PyPDF2** - PDF text extraction

## Agent Details

All agents use **temperature 0.7** for balanced creativity and consistency.

**Agent 1: Keywords** - Extracts technical skills, soft skills, qualifications, tools, certifications, industry terms

**Agent 2: Match Scorer** - Returns overall match % (0-100), category scores, strengths, gaps, and recommendations

**Agent 3: Resume Tailor** - Creates ATS-optimized resume using extracted keywords and match analysis

**Agent 4: Recruiter** - Provides candidacy score, interview likelihood (High/Medium/Low), prep focus areas, and salary leverage

---

## Customization

Edit agent prompts in the Python files to customize behavior:
- Modify categories in `KeywordExtractorAgent`
- Adjust scoring weights in `MatchScoreAgent`
- Change resume format in `ResumeTailoringAgent`
- Customize evaluation criteria in `RecruiterAgent`

## Performance

- **Time**: 30-60 seconds per run
- **Cost**: ~$0.15-0.20 per run (Claude Sonnet 4.5)

---

## Troubleshooting

**API Key Error**: Create `.env` file with `ANTHROPIC_API_KEY=your_key_here`

**Rate Limit**: Wait 1-2 minutes between runs

**URL Fetch Failed**: Use manual mode and paste job description

**No UI**: Ensure running `_ui.py` version

## Files

```
applier/
├── langchain_resume_agent_ui.py       ← Main (with UI)
├── langchain_resume_agent.py          ← Main (no UI)
├── langchain_resume_agent_url_ui.py   ← URL support (UI)
├── langchain_resume_agent_url.py      ← URL support (no UI)
├── requirements.txt
├── README.md
├── .env                               ← API key (git ignored)
└── .gitignore
```

## Why 4 Agents?

**Agent 4 (Recruiter) provides**:
- Interview likelihood assessment (High/Medium/Low)
- Prep recommendations and talking points
- Salary negotiation leverage
- Competitive positioning insights

## License

MIT License

---

Built with [LangChain](https://github.com/langchain-ai/langchain), [Claude](https://www.anthropic.com/claude), and [Rich](https://github.com/Textualize/rich)
