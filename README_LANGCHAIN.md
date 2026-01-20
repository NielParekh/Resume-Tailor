# LangChain Agentic Resume Optimizer

An intelligent multi-agent AI system built with LangChain that optimizes your resume for specific job applications.

## 🤖 Agentic Workflow

The application uses three specialized AI agents working together:

### 1. **Keyword Extractor Agent**
- Extracts important keywords from job descriptions
- Categorizes: technical skills, soft skills, tools, certifications, qualifications
- Provides structured keyword analysis

### 2. **Match Score Agent**
- Calculates resume-to-job match percentage (0-100%)
- Provides category-wise breakdown
- Identifies strengths and gaps
- Gives actionable recommendations

### 3. **Resume Tailoring Agent**
- Creates ATS-optimized resume in standard format
- Naturally incorporates keywords
- Highlights relevant experience
- Maintains truthfulness (never fabricates)

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Setup API Key

Your `.env` file is already configured with your Anthropic API key.

### Usage

#### Option 1: Manual Job Description Input (Recommended)

```bash
python3 langchain_resume_agent.py "Niel Parekh New Resume.pdf"
```

Then paste the job description when prompted and press `Ctrl+D`.

#### Option 2: Job URL

```bash
python3 langchain_resume_agent_url.py "JOB_URL" "Niel Parekh New Resume.pdf"
```

## 📊 Output

The workflow produces:

1. **Tailored Resume PDF** (`tailored_resume_YYYYMMDD_HHMMSS.pdf`)
   - Professionally formatted
   - ATS-optimized
   - Ready to submit

2. **Markdown Version** (`tailored_resume_YYYYMMDD_HHMMSS.md`)
   - Easy to edit
   - Human-readable format

3. **Analysis Report** (`resume_analysis_YYYYMMDD_HHMMSS.json`)
   - Extracted keywords
   - Match percentage breakdown
   - Strengths and gaps analysis

## 🎯 Workflow Steps

When you run the agent, you'll see:

```
LANGCHAIN AGENTIC RESUME OPTIMIZER
============================================================

STEP 1: Extracting Keywords from Job Description
✓ Keywords Extracted:
  Technical Skills:
    • Python
    • Machine Learning
    • AWS
  [...]

STEP 2: Calculating Resume Match Percentage
✓ Overall Match: 85%
  Category Scores:
    • Technical Skills: 90%
    • Soft Skills: 80%
    • Experience: 85%
    • Qualifications: 75%

  Strengths:
    ✓ Strong ML background
    ✓ Relevant cloud experience

  Gaps:
    ✗ Missing specific certification

  Recommendation: [...]

STEP 3: Creating Tailored Resume
✓ Tailored resume generated successfully
✓ Resume saved as PDF: tailored_resume_20260119_170530.pdf
✓ Markdown version saved: tailored_resume_20260119_170530.md
✓ Analysis report saved: resume_analysis_20260119_170530.json

WORKFLOW COMPLETE!
Final Match Score: 85%
Resume ready for application: tailored_resume_20260119_170530.pdf
```

## 🔧 Technical Details

### Architecture

- **Framework**: LangChain with Anthropic Claude Sonnet 4.5
- **Agent Pattern**: Multi-agent sequential workflow
- **Output Parser**: Structured JSON for analysis, text for resume
- **PDF Generation**: ReportLab with professional formatting

### Features

✅ **Multi-Agent System**: Three specialized agents for different tasks
✅ **Structured Output**: JSON-based keyword and score analysis
✅ **Match Percentage**: Quantified resume-job alignment
✅ **ATS Optimization**: Industry-standard formatting
✅ **Truthful Tailoring**: Never fabricates experience
✅ **Professional PDF**: Clean, readable output

## 📝 Example

### Input
- Job: "Senior AI Engineer at Microsoft"
- Your resume: "Niel Parekh New Resume.pdf"

### Output
1. Keywords extracted: Python, ML, Azure, Agentic AI, etc.
2. Match score: 87%
3. Tailored PDF resume highlighting relevant experience

## 🆚 Comparison with Previous Version

| Feature | Previous | LangChain Version |
|---------|----------|-------------------|
| Architecture | Single monolithic script | Multi-agent workflow |
| Keyword extraction | Combined with analysis | Dedicated agent |
| Match scoring | Not provided | **Detailed percentage breakdown** |
| Workflow visibility | Limited | **Step-by-step progress** |
| Extensibility | Hard to modify | Easy to add new agents |
| Output structure | Basic | **Structured JSON + PDF** |

## 🛠️ Customization

You can easily customize the agents:

### Modify Keyword Categories
Edit `KeywordExtractorAgent.prompt` to add/remove categories

### Adjust Match Scoring
Edit `MatchScoreAgent.prompt` to change scoring criteria

### Change Resume Format
Edit `ResumeTailoringAgent.prompt` to modify resume structure

## 📦 Dependencies

- `langchain`: Agent orchestration framework
- `langchain-anthropic`: Claude integration
- `anthropic`: Claude API
- `reportlab`: PDF generation
- `PyPDF2`: PDF reading
- `beautifulsoup4`: Web scraping (for URL mode)
- `python-dotenv`: Environment management

## 🎓 How It Works

1. **Keyword Extraction**: Agent analyzes job description using Claude to identify critical keywords and requirements

2. **Match Analysis**: Agent compares resume against job requirements, calculating match percentages and identifying gaps

3. **Resume Tailoring**: Agent creates optimized resume incorporating keywords naturally while highlighting relevant experience

4. **PDF Generation**: Converts markdown resume to professional PDF format

## 💡 Tips

1. **For best results**: Paste the complete job description including requirements and responsibilities

2. **Match scores above 75%**: Strong fit, resume should perform well in ATS

3. **Match scores 60-75%**: Moderate fit, consider emphasizing transferable skills

4. **Match scores below 60%**: May want to focus on other opportunities or gain more relevant experience

5. **Review the gaps**: Use identified gaps to prepare for interview questions

## 🔒 Privacy

- All processing happens via Anthropic's API
- No data stored beyond local files
- Resume and job data sent to Claude for processing
- Generated files remain on your machine only

## 🐛 Troubleshooting

**Rate limit errors**: Wait 1-2 minutes between runs

**URL fetching fails**: Use manual mode and paste job description

**PDF formatting issues**: Check markdown output and adjust if needed

## 📄 License

MIT License - Free to use and modify
