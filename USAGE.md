# Quick Usage Guide

## 🆕 NEW: LangChain Agentic Workflow (Recommended)

The new LangChain-based system provides a structured 3-step workflow:

### Step 1: Extract Keywords
Automatically identifies critical keywords from job description

### Step 2: Calculate Match %
Gives you a detailed match score (0-100%) showing how well your resume aligns

### Step 3: Create Tailored Resume
Generates optimized PDF resume

### Run It:

**Manual input (recommended):**
```bash
python3 langchain_resume_agent.py "Niel Parekh New Resume.pdf"
```
Then paste job description and press Ctrl+D

**With URL:**
```bash
python3 langchain_resume_agent_url.py "JOB_URL" "Niel Parekh New Resume.pdf"
```

---

## 📊 Output Examples

### You'll see output like this:

```
STEP 1: Extracting Keywords from Job Description
============================================================

✓ Keywords Extracted:

  Technical Skills:
    • Python
    • Machine Learning
    • PyTorch
    • TensorFlow
    • AWS/GCP
    • Agentic AI
    • RAG Systems

  Soft Skills:
    • Leadership
    • Cross-functional collaboration
    • Problem solving

STEP 2: Calculating Resume Match Percentage
============================================================

✓ Overall Match: 87%

  Category Scores:
    • Technical Skills: 92%
    • Soft Skills: 85%
    • Experience: 88%
    • Qualifications: 80%

  Strengths:
    ✓ Strong AI/ML background with hands-on experience
    ✓ Proven track record with Agentic AI systems at Verizon
    ✓ Excellent education credentials (MS from UMass Amherst)
    ✓ Published research in relevant domains

  Gaps:
    ✗ Specific certification mentioned in job not present
    ✗ Limited mention of specific AWS services

  Recommendation: Excellent match overall. Emphasize your Agentic AI
  experience and RAG system implementation. Consider highlighting any
  AWS experience you have even if not explicitly mentioned.

STEP 3: Creating Tailored Resume
============================================================

✓ Tailored resume generated successfully
✓ Resume saved as PDF: tailored_resume_20260119_170530.pdf
✓ Markdown version saved: tailored_resume_20260119_170530.md
✓ Analysis report saved: resume_analysis_20260119_170530.json

WORKFLOW COMPLETE!
============================================================
Final Match Score: 87%
Resume ready for application: tailored_resume_20260119_170530.pdf
```

---

## 📁 Files Generated

1. **`tailored_resume_TIMESTAMP.pdf`** - Your optimized resume (submit this!)
2. **`tailored_resume_TIMESTAMP.md`** - Editable markdown version
3. **`resume_analysis_TIMESTAMP.json`** - Detailed analysis data

---

## 🔄 Original Version (Still Available)

If you prefer the original single-step version:

```bash
python3 resume_applier.py "JOB_URL" "Niel Parekh New Resume.pdf"
```

Or manual:
```bash
python3 resume_applier_manual.py "Niel Parekh New Resume.pdf"
```

---

## 💡 Which One Should You Use?

**Use LangChain Version (NEW) if you want:**
- ✅ Match percentage score
- ✅ Detailed keyword analysis
- ✅ Step-by-step transparency
- ✅ Gap analysis
- ✅ Better structure

**Use Original Version if you want:**
- ✅ Simpler, faster execution
- ✅ No need for detailed analysis
- ✅ Just want the tailored resume

---

## 🎯 Pro Tips

1. **Review the match score first** - If below 60%, consider if you're a good fit

2. **Check the gaps** - Prepare to address these in your cover letter or interview

3. **Use keyword insights** - Incorporate these naturally in your cover letter

4. **Save the analysis file** - Reference it when preparing for interviews

5. **Edit the markdown** - If you want to tweak anything, edit the .md file and regenerate PDF

---

## ⚡ Quick Install

```bash
cd /Users/nielparekh/Desktop/applier
pip install -r requirements.txt
```

That's it! Your `.env` file is already configured.
