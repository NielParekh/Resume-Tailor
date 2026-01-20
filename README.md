# LangChain Agentic Resume Optimizer

An intelligent 4-agent AI system that optimizes your resume for specific job applications using LangChain and Claude Sonnet 4.5.

## Quick Start

```bash
# 1. Install dependencies (one-time)
pip install -r requirements.txt

# 2. Run with beautiful UI (recommended!)
python3 langchain_resume_agent_ui.py "Niel Parekh New Resume.pdf"

# 3. Paste job description and press Ctrl+D
```

## Features

✅ **Extract Keywords** - AI identifies critical keywords from job descriptions
✅ **Calculate Match %** - Get detailed 0-100% match score with category breakdown
✅ **Generate Resume PDF** - Creates professionally formatted, ATS-optimized resume
✅ **Recruiter Evaluation** - Senior technical recruiter assesses your candidacy
✅ **Interview Prep Insights** - Get talking points and salary leverage analysis
✅ **Beautiful UI** - Real-time progress bars and color-coded results

---

## How It Works

### 4-Agent Workflow

```
Job Description → Agent 1 → Agent 2 → Agent 3 → Agent 4 → Output
                  Keywords   Match %   Resume    Recruiter
```

#### Agent 1: Keyword Extractor
Identifies technical skills, soft skills, qualifications, tools, and certifications from the job description.

**Output**: JSON with categorized keywords
```json
{
  "technical_skills": ["Python", "Machine Learning", "AWS"],
  "soft_skills": ["Leadership", "Communication"],
  "tools_technologies": ["Docker", "Kubernetes"],
  "certifications": ["AWS Certified"],
  "industry_terms": ["Agile", "CI/CD"]
}
```

#### Agent 2: Match Scorer
Calculates how well your resume matches the job with detailed percentage breakdown.

**Output**: Match percentage with category scores
```json
{
  "overall_match_percentage": 87,
  "category_scores": {
    "technical_skills": 92,
    "soft_skills": 85,
    "experience": 88,
    "qualifications": 80
  },
  "strengths": ["Strong AI/ML background", "Proven leadership"],
  "gaps": ["Missing specific certification"],
  "recommendation": "Excellent match! Emphasize..."
}
```

#### Agent 3: Resume Tailor
Creates an optimized resume that naturally incorporates keywords and highlights relevant experience.

**Output**: Professional resume in markdown and PDF formats

#### Agent 4: Recruiter Evaluator
A senior technical recruiter evaluates your candidacy from a hiring perspective.

**Output**: Interview insights and salary leverage
```json
{
  "candidacy_score": 85,
  "likelihood_to_proceed": "High",
  "interview_readiness": {
    "technical_prep": "Strong",
    "behavioral_prep": "Moderate",
    "cultural_fit": "Strong"
  },
  "competitive_advantages": ["Unique AI experience", "Strong education"],
  "potential_concerns": ["Limited cloud experience"],
  "key_talking_points": ["Agentic AI system at Verizon", "Published research"],
  "salary_leverage": "High - strong technical skills",
  "interview_prep_focus": ["Behavioral questions", "Cloud architecture"]
}
```

---

## Output Files

You get **3 files** for each job application:

1. **`tailored_resume_TIMESTAMP.pdf`** ← Submit this!
2. **`tailored_resume_TIMESTAMP.md`** ← Editable version
3. **`resume_analysis_TIMESTAMP.json`** ← Full analysis with recruiter evaluation

---

## Usage Examples

### With Beautiful UI (Recommended)
```bash
python3 langchain_resume_agent_ui.py "Niel Parekh New Resume.pdf"
```

**What you'll see:**
```
╭───────────────────────────────────────────────────╮
│  LangChain Agentic Resume Optimizer              │
│  4-Agent AI Workflow with Recruiter Evaluation   │
╰───────────────────────────────────────────────────╯

⠋ Agent 1: Extracting keywords... ████████░░ 80%

╭──────────── 📋 Extracted Keywords ─────────────╮
│ Category          │ Keywords                   │
├───────────────────┼────────────────────────────┤
│ Technical Skills  │ Python, ML, AWS, Docker... │
│ Soft Skills      │ Leadership, Communication...│
╰────────────────────────────────────────────────╯

╭────── Overall Match Score ──────╮
│ 🎉 87% Excellent Match!        │
╰─────────────────────────────────╯

👔 Senior Recruiter Evaluation
🌟 85/100 - Likelihood: High

💬 Key Interview Talking Points:
  1. Agentic AI system implementation at Verizon
  2. Published research in ML/AI domains
  3. Cross-functional leadership experience

╭──────────────── 🎉 Success ────────────────╮
│ ✓ 4-Agent Process Complete!               │
│                                            │
│ Resume Match Score: 87%                    │
│ Candidacy Score: 85/100                    │
│ Likelihood to Proceed: High                │
│                                            │
│ Files generated:                           │
│   • PDF Resume: tailored_resume.pdf       │
│   • Markdown: tailored_resume.md          │
│   • Full Analysis: resume_analysis.json   │
╰────────────────────────────────────────────╯
```

### Without UI
```bash
python3 langchain_resume_agent.py "Niel Parekh New Resume.pdf"
```

### With Job URL
```bash
python3 langchain_resume_agent_url_ui.py "https://..." "Niel Parekh New Resume.pdf"
```

---

## Understanding Match Scores

| Score | Meaning | Action |
|-------|---------|--------|
| **85-100%** | Excellent fit! | Apply with confidence |
| **70-84%** | Good fit | Emphasize relevant skills |
| **60-69%** | Moderate fit | Highlight transferable experience |
| **Below 60%** | Lower fit | Consider if it's the right opportunity |

---

## Technical Architecture

### Technology Stack

- **LangChain** - Multi-agent orchestration framework
- **Claude Sonnet 4.5** - AI model (`claude-sonnet-4-5-20250929`)
- **Rich** - Beautiful terminal UI with progress bars
- **ReportLab** - Professional PDF generation
- **PyPDF2** - PDF reading and text extraction
- **Python-dotenv** - Environment variable management

### System Architecture

```
┌─────────────────────────────────────────┐
│           USER INPUT                     │
│  • Job Description (text or URL)        │
│  • Current Resume (PDF)                  │
└──────────────┬──────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│      LANGCHAIN ORCHESTRATOR              │
└──────────────┬───────────────────────────┘
               │
        ┌──────┴──────┬──────┬──────┐
        ▼             ▼      ▼      ▼
    ┌────────┐  ┌─────────┐ ┌─────────┐ ┌──────────┐
    │Agent 1 │→ │Agent 2  │→│Agent 3  │→│Agent 4   │
    │Keyword │  │Match %  │ │Resume   │ │Recruiter │
    └────────┘  └─────────┘ └─────────┘ └──────────┘
        │            │           │            │
        ▼            ▼           ▼            ▼
    Keywords → Match Analysis → Resume → Evaluation
                                   │
                                   ▼
                            ┌──────────────┐
                            │ PDF Generator│
                            └──────┬───────┘
                                   │
                                   ▼
                        ┌───────────────────┐
                        │  OUTPUT FILES     │
                        │  • Resume PDF     │
                        │  • Markdown       │
                        │  • Analysis JSON  │
                        └───────────────────┘
```

### Prompt Engineering

Each agent uses carefully crafted prompts with specific personas and output formats:

**Temperature**: 0.7 (balanced creativity and consistency)

#### Agent 1: Keyword Extractor Prompt
```
System: You are an expert ATS (Applicant Tracking System) keyword analyzer.
Your job is to extract the most important keywords from job descriptions.

Extract:
1. Required technical skills
2. Required soft skills
3. Required qualifications
4. Important industry terms
5. Tools and technologies mentioned
6. Certifications or degrees required

Return ONLY a JSON object with this structure:
{
    "technical_skills": ["skill1", "skill2", ...],
    "soft_skills": ["skill1", "skill2", ...],
    "qualifications": ["qual1", "qual2", ...],
    "tools_technologies": ["tool1", "tool2", ...],
    "certifications": ["cert1", "cert2", ...],
    "industry_terms": ["term1", "term2", ...]
}

User: Extract keywords from this job description:
{job_description}
```

#### Agent 2: Match Scorer Prompt
```
System: You are an expert resume analyzer specializing in ATS matching.

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
{
    "overall_match_percentage": 85,
    "category_scores": {
        "technical_skills": 90,
        "soft_skills": 80,
        "experience": 85,
        "qualifications": 75
    },
    "strengths": ["strength1", "strength2", ...],
    "gaps": ["gap1", "gap2", ...],
    "recommendation": "Brief recommendation"
}

User: Analyze this resume against the job:
Job Description: {job_description}
Resume: {resume}
Keywords: {keywords}
```

#### Agent 3: Resume Tailor Prompt
```
System: You are an expert resume writer and career consultant.

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
[2-3 lines highlighting relevant experience]

## Experience
### [Job Title] - [Company Name]
*[Start Date - End Date]*
- [Achievement with quantifiable results]
- [Another accomplishment]

## Education
### [Degree] - [University Name]

## Technical Skills
**[Category]**: Skill1, Skill2, Skill3

IMPORTANT:
- Use keywords naturally
- Emphasize accomplishments aligned with job
- Keep all information truthful
- Format for ATS compatibility

User: Create a tailored resume for this job.
Job: {job_description}
Current Resume: {resume}
Keywords: {keywords}
Match Analysis: {match_analysis}
```

#### Agent 4: Recruiter Evaluator Prompt
```
System: You are a senior technical recruiter with 15+ years of experience hiring
for top tech companies.

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
{
    "candidacy_score": 85,
    "likelihood_to_proceed": "High/Medium/Low",
    "interview_readiness": {
        "technical_prep": "Strong/Moderate/Weak",
        "behavioral_prep": "Strong/Moderate/Weak",
        "cultural_fit": "Strong/Moderate/Weak"
    },
    "competitive_advantages": ["advantage1", "advantage2", ...],
    "potential_concerns": ["concern1", "concern2", ...],
    "key_talking_points": ["point1", "point2", ...],
    "salary_leverage": "High/Medium/Low with explanation",
    "interview_prep_focus": ["area1", "area2", ...],
    "recruiter_notes": "Honest assessment and recommendations"
}

User: Evaluate this candidate's profile for the role.
Job: {job_description}
Tailored Resume: {tailored_resume}
Match Analysis: {match_analysis}
```

---

## Customization

### Modify Agent Prompts

Edit the system prompts in the agent classes to customize behavior:

```python
# Change Agent 1 to extract additional categories
self.prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert ATS keyword analyzer.

Extract:
1. Required technical skills
2. Required soft skills
...
8. Your new category here
""")
])
```

### Adjust Match Scoring Criteria

Modify `MatchScoreAgent` to weight categories differently:

```python
("system", """Consider:
1. Presence of required keywords (40% weight)
2. Relevant experience (30% weight)
3. Skills match (20% weight)
4. Qualifications match (10% weight)
""")
```

### Change Resume Format

Edit `ResumeTailoringAgent` prompt to use different structure or styling.

---

## Tips & Best Practices

### Before Applying
1. **Review the match score** - If below 60%, consider gaining more relevant experience
2. **Read the gaps carefully** - Prepare to address these in your cover letter
3. **Check recruiter evaluation** - Focus interview prep on suggested areas

### Using the Output
1. **Submit the PDF resume** - It's ATS-optimized and professionally formatted
2. **Use keywords in cover letter** - Reference extracted keywords naturally
3. **Save the analysis file** - Review before interviews for talking points
4. **Leverage recruiter insights** - Use competitive advantages in negotiations

### Interview Preparation
1. **Key talking points** - Prepare stories around these topics
2. **Potential concerns** - Have responses ready to address gaps
3. **Interview prep focus** - Study these areas before the interview
4. **Salary leverage** - Use this insight for negotiation strategy

---

## Performance

- **Total Time**: ~30-60 seconds per run
  - Agent 1 (Keywords): ~10s
  - Agent 2 (Match): ~15s
  - Agent 3 (Resume): ~20s
  - Agent 4 (Recruiter): ~15s
  - PDF Generation: ~5s

- **Token Usage**: ~20,000-25,000 tokens per run
- **Cost**: ~$0.15-0.20 per run (Claude Sonnet 4.5 pricing)

---

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
Your `.env` file should already be configured. If not, create one:
```bash
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

### "Rate limit error"
Wait 1-2 minutes between runs. Anthropic has rate limits on API calls.

### "Failed to fetch job description from URL"
Use manual mode and paste the job description directly:
```bash
python3 langchain_resume_agent_ui.py "Niel Parekh New Resume.pdf"
```

### "PDF generation error"
The markdown version is still saved. You can convert it manually or fix any formatting issues.

### No UI showing up
Make sure you're running the `_ui` version:
```bash
python3 langchain_resume_agent_ui.py "Niel Parekh New Resume.pdf"  # ← With UI
python3 langchain_resume_agent.py "Niel Parekh New Resume.pdf"     # ← Without UI
```

---

## Privacy & Security

- **API Key**: Stored in `.env`, excluded from git
- **Data Processing**: All processing via Anthropic's API
- **Local Storage**: Files saved only on your machine
- **No Logging**: Sensitive data not logged
- **HTTPS**: All API calls encrypted

---

## Beautiful UI Features

The UI version (`langchain_resume_agent_ui.py`) provides a stunning visual experience:

### UI Features
- ✨ **Real-time Progress Bars** - See each agent's progress with spinners
- 🎯 **Agent Status Tracking** - Know exactly which agent is running
- 📊 **Visual Match Scores** - Color-coded progress bars for all categories
- 📋 **Formatted Tables** - Beautiful keyword and score displays
- 🎉 **Color-Coded Output** - Green for success, red for gaps, yellow for warnings
- ⏱️ **Time Tracking** - See how long each step takes

### Color Coding System
- **Green** (85-100%): Excellent match 🎉
- **Yellow** (70-84%): Good match 👍
- **Orange** (60-69%): Moderate match ⚠️
- **Red** (<60%): Low match ❌

### Visual Progress Indicators
Each agent shows:
- ⠋ Spinner animation while working
- █ Progress bar filling up (e.g., `████████░░ 80%`)
- ⏱️ Time elapsed
- ✓ Green checkmark when complete

### UI vs Non-UI Comparison

**Without UI:**
```
STEP 1: Extracting Keywords
✓ Keywords Extracted
  Technical Skills: Python, ML...
```

**With UI:**
```
⠋ Agent 1: Extracting keywords... ████████████░░ 80% 0:00:08

╭──────────── 📋 Extracted Keywords ─────────────╮
│ Technical Skills  │ Python, ML, AWS, Docker... │
│ Soft Skills      │ Leadership, Communication...│
╰──────────────────────────────────────────────────╯
```

### Technical Implementation
Built with [Rich](https://github.com/Textualize/rich) library:
- Progress bars with spinners
- Formatted tables with borders
- Colored panels and text
- Live updates during execution
- Cross-platform support (Windows, Mac, Linux)
- Adapts to terminal width (dark/light mode compatible)

---

## Files in This Project

```
applier/
├── langchain_resume_agent_ui.py       ← Main app with UI ⭐
├── langchain_resume_agent.py          ← Main app without UI
├── langchain_resume_agent_url_ui.py   ← URL support with UI
├── langchain_resume_agent_url.py      ← URL support without UI
├── test_ui.py                         ← UI demo
├── requirements.txt                   ← Dependencies
├── README.md                          ← This comprehensive guide
├── .env                               ← API key (not in git)
└── .gitignore                         ← Protects sensitive files
```

---

## Requirements

All dependencies are in `requirements.txt`:

```
anthropic>=0.18.0
requests>=2.31.0
beautifulsoup4>=4.12.0
python-dotenv>=1.0.0
PyPDF2>=3.0.0
reportlab>=4.0.0
markdown>=3.5.0
langchain>=0.1.0
langchain-anthropic>=0.1.0
langchain-core>=0.1.0
rich>=13.0.0
```

Install with:
```bash
pip install -r requirements.txt
```

---

## Why the 4th Agent (Recruiter) Matters

### Before Agent 4:
- ❌ You only knew if your resume matched
- ❌ No insight into hiring likelihood
- ❌ No preparation guidance
- ❌ No understanding of competitive position

### With Agent 4:
- ✅ Know your competitive position
- ✅ Understand interview likelihood (High/Medium/Low)
- ✅ Get specific prep recommendations
- ✅ Identify salary negotiation leverage
- ✅ Address concerns proactively
- ✅ Receive honest recruiter feedback

### Key Use Cases

**1. Reality Check**
- Is this role worth applying to?
- What are my actual chances?
- Should I invest time in this application?

**2. Interview Preparation**
- What should I focus on studying?
- What are my strongest talking points?
- How should I frame my experience?

**3. Salary Negotiation**
- What's my leverage in negotiations?
- How should I position myself?
- What's my competitive advantage?

**4. Self-Improvement**
- What gaps should I address long-term?
- How can I strengthen my profile?
- What skills should I develop next?

---

## Future Extensions

The architecture supports easy addition of new agents:

- **CoverLetterAgent** - Generate tailored cover letters
- **InterviewPrepAgent** - Create interview Q&A prep
- **SkillGapAgent** - Recommend courses to fill gaps
- **LinkedInAgent** - Optimize LinkedIn profile
- **NetworkingAgent** - Suggest people to connect with

---

## License

MIT License - Free to use and modify

---

## Credits

Built with:
- [LangChain](https://github.com/langchain-ai/langchain) - Agent orchestration
- [Anthropic Claude](https://www.anthropic.com/claude) - AI model
- [Rich](https://github.com/Textualize/rich) - Terminal UI

---

## Quick Reference

```bash
# Installation
pip install -r requirements.txt

# Run with UI (recommended)
python3 langchain_resume_agent_ui.py "Niel Parekh New Resume.pdf"

# Run without UI
python3 langchain_resume_agent.py "Niel Parekh New Resume.pdf"

# With URL
python3 langchain_resume_agent_url_ui.py "JOB_URL" "Resume.pdf"

# Test UI
python3 test_ui.py
```

**That's it! Good luck with your applications! 🚀**
