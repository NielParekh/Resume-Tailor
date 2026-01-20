# 🚀 Resume Applier - Start Here

## What You Have

You now have TWO versions of the resume optimizer:

### ⭐ **NEW: LangChain Agentic AI (Recommended)**
Multi-agent workflow with 3 clear steps:
1. Extract keywords from job
2. Calculate match percentage
3. Generate tailored resume PDF

### 📄 **Original: Simple Version**
Single-step resume generation

---

## Quick Start (3 Steps)

### 1️⃣ Open Terminal
```bash
cd /Users/nielparekh/Desktop/applier
```

### 2️⃣ Install Dependencies (one time only)
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Agent
```bash
python3 langchain_resume_agent.py "Niel Parekh New Resume.pdf"
```

Then:
- Paste the job description
- Press `Ctrl+D` when done
- Watch the magic happen!

---

## What You'll See

```
LANGCHAIN AGENTIC RESUME OPTIMIZER
============================================================

STEP 1: Extracting Keywords from Job Description
✓ Keywords Extracted:
  Technical Skills: Python, ML, AWS...
  Soft Skills: Leadership, Communication...

STEP 2: Calculating Resume Match Percentage
✓ Overall Match: 87%
  Category Scores:
    • Technical Skills: 92%
    • Soft Skills: 85%
  Strengths: Strong ML background...
  Gaps: Missing certification X...

STEP 3: Creating Tailored Resume
✓ Resume saved as PDF: tailored_resume_20260119_170530.pdf

WORKFLOW COMPLETE!
Final Match Score: 87%
```

---

## You Get 3 Files

1. **`tailored_resume_TIMESTAMP.pdf`** ← Submit this one!
2. **`tailored_resume_TIMESTAMP.md`** ← Edit if needed
3. **`resume_analysis_TIMESTAMP.json`** ← Full analysis data

---

## 📚 Documentation

- **[USAGE.md](USAGE.md)** - Detailed usage examples
- **[README_LANGCHAIN.md](README_LANGCHAIN.md)** - Full LangChain docs
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture
- **[SETUP.md](SETUP.md)** - Setup instructions

---

## 💡 Key Features

✅ **Match Percentage** - Know how well you fit (0-100%)
✅ **Keyword Analysis** - See what matters most
✅ **Gap Identification** - Know what you're missing
✅ **Professional PDF** - Ready to submit
✅ **ATS Optimized** - Passes applicant tracking systems
✅ **100% Truthful** - Never fabricates experience

---

## 🎯 Example Workflow

```bash
# 1. Navigate to folder
cd /Users/nielparekh/Desktop/applier

# 2. Run the agent
python3 langchain_resume_agent.py "Niel Parekh New Resume.pdf"

# 3. Paste job description (copy from company website)
[Paste here...]
[Press Ctrl+D]

# 4. Optionally enter job URL
Enter job URL: https://...

# 5. Done! Check your files
✓ tailored_resume_20260119_170530.pdf
```

---

## Alternative Usage

### With URL (auto-fetch job description)
```bash
python3 langchain_resume_agent_url.py "JOB_URL" "Niel Parekh New Resume.pdf"
```

### Original Simple Version
```bash
python3 resume_applier.py "JOB_URL" "Niel Parekh New Resume.pdf"
```

---

## 🆘 Troubleshooting

**"ANTHROPIC_API_KEY not found"**
→ Your `.env` file is already set up, this shouldn't happen

**"Rate limit error"**
→ Wait 2 minutes and try again

**"Failed to fetch job description"**
→ Use manual mode and paste job description

**"PDF generation error"**
→ Check the markdown file, it will still have your resume

---

## 🎓 Understanding Match Scores

- **85-100%**: Excellent fit! Apply with confidence
- **70-84%**: Good fit, emphasize relevant skills
- **60-69%**: Moderate fit, highlight transferable experience
- **Below 60%**: Consider if it's the right opportunity

---

## 🔑 Pro Tips

1. **Read the gaps** - Prepare to address them in interviews
2. **Use keywords in cover letter** - Reference the extracted keywords
3. **Save the analysis** - Review before interviews
4. **Customize further** - Edit the markdown if needed
5. **Track applications** - Keep all analysis files organized

---

## 📁 Project Structure

```
applier/
├── langchain_resume_agent.py       ← Main LangChain version
├── langchain_resume_agent_url.py   ← With URL support
├── resume_applier.py               ← Original version
├── resume_applier_manual.py        ← Original manual mode
├── Niel Parekh New Resume.pdf      ← Your resume
├── .env                            ← API key (configured)
├── requirements.txt                ← Dependencies
└── [Documentation files]
```

---

## 🎉 Ready to Apply?

1. Find a job you're interested in
2. Copy the job description
3. Run: `python3 langchain_resume_agent.py "Niel Parekh New Resume.pdf"`
4. Paste the job description
5. Submit the generated PDF!

---

## Need Help?

- Check [USAGE.md](USAGE.md) for detailed examples
- Read [README_LANGCHAIN.md](README_LANGCHAIN.md) for full documentation
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for technical details

---

## What Makes This Special?

This isn't just a resume tool - it's an **agentic AI system**:

- 🤖 **3 Specialized Agents** working together
- 🎯 **Quantified Match Score** - know your fit
- 📊 **Structured Analysis** - clear insights
- 🔄 **Multi-Step Workflow** - transparent process
- 🏗️ **LangChain Framework** - industry-standard AI architecture

**Good luck with your applications! 🚀**
