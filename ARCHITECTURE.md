# LangChain Agentic Resume Optimizer - Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   USER INPUT                                 │
│  • Job Description (text or URL)                            │
│  • Current Resume (PDF)                                      │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│            LANGCHAIN ORCHESTRATOR                            │
│        (LangChainResumeAgent)                               │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │   AGENT WORKFLOW     │
        └──────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
    ▼              ▼              ▼
┌─────────┐  ┌──────────┐  ┌────────────┐
│ AGENT 1 │  │ AGENT 2  │  │  AGENT 3   │
│ Keyword │  │  Match   │  │  Resume    │
│Extractor│  │  Scorer  │  │  Tailor    │
└────┬────┘  └────┬─────┘  └─────┬──────┘
     │            │              │
     ▼            ▼              ▼
┌─────────┐  ┌──────────┐  ┌────────────┐
│Keywords │→ │Match %   │→ │ Tailored   │
│  JSON   │  │Analysis  │  │  Resume    │
└─────────┘  └──────────┘  └─────┬──────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │  PDF Generator  │
                         └────────┬────────┘
                                  │
                                  ▼
                    ┌──────────────────────────┐
                    │      OUTPUT FILES        │
                    │  • Resume PDF            │
                    │  • Resume Markdown       │
                    │  • Analysis JSON         │
                    └──────────────────────────┘
```

## Agent Details

### 🔍 Agent 1: Keyword Extractor
```
Input:  Job Description (text)
Process: Claude Sonnet 4.5 → Structured Extraction
Output: JSON with categorized keywords
{
  "technical_skills": [...],
  "soft_skills": [...],
  "qualifications": [...],
  "tools_technologies": [...],
  "certifications": [...],
  "industry_terms": [...]
}
```

### 📊 Agent 2: Match Scorer
```
Input:  Job Description + Current Resume + Keywords
Process: Claude Sonnet 4.5 → Comparative Analysis
Output: Match percentage + category breakdown
{
  "overall_match_percentage": 85,
  "category_scores": {
    "technical_skills": 90,
    "soft_skills": 80,
    "experience": 85,
    "qualifications": 75
  },
  "strengths": [...],
  "gaps": [...],
  "recommendation": "..."
}
```

### ✍️ Agent 3: Resume Tailor
```
Input:  Job Desc + Current Resume + Keywords + Match Analysis
Process: Claude Sonnet 4.5 → Resume Generation
Output: Optimized resume text (markdown format)

Uses standard professional format:
- Name & Contact
- Professional Summary
- Experience
- Education
- Skills
- Projects/Certifications
```

## Technology Stack

```
┌─────────────────────────────────────┐
│        Application Layer            │
│  • langchain_resume_agent.py       │
│  • Multi-agent orchestration        │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│         LangChain Layer             │
│  • ChatAnthropic (LLM)             │
│  • ChatPromptTemplate               │
│  • JsonOutputParser                 │
│  • StrOutputParser                  │
│  • RunnablePassthrough              │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│        AI Model Layer               │
│  Claude Sonnet 4.5                  │
│  (claude-sonnet-4-5-20250929)      │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│       Output Processing             │
│  • ReportLab (PDF generation)      │
│  • Markdown formatting              │
│  • JSON serialization               │
└─────────────────────────────────────┘
```

## Data Flow

```
1. INPUT STAGE
   User provides:
   ├─ Job description (text/URL)
   └─ Current resume (PDF)

2. EXTRACTION STAGE
   └─ PDF text extracted via PyPDF2

3. AGENT PROCESSING STAGE
   ├─ Agent 1: Extract keywords → keywords.json
   │   └─ Used by Agent 2
   ├─ Agent 2: Calculate match % → match_analysis.json
   │   └─ Used by Agent 3
   └─ Agent 3: Generate resume → resume_text.md
       └─ Used by PDF generator

4. OUTPUT STAGE
   ├─ PDF generation (ReportLab)
   ├─ Markdown file (direct write)
   └─ Analysis JSON (combined data)

5. COMPLETION
   User receives:
   ├─ tailored_resume_TIMESTAMP.pdf
   ├─ tailored_resume_TIMESTAMP.md
   └─ resume_analysis_TIMESTAMP.json
```

## Prompt Engineering

Each agent uses carefully crafted prompts:

### Agent 1 (Keyword Extractor)
- **System**: Expert ATS analyzer role
- **Task**: Extract and categorize keywords
- **Format**: Strict JSON schema
- **Focus**: ATS-relevant terms

### Agent 2 (Match Scorer)
- **System**: Resume analyzer specialist
- **Task**: Calculate match and identify gaps
- **Format**: Structured JSON with percentages
- **Focus**: Quantifiable metrics

### Agent 3 (Resume Tailor)
- **System**: Expert resume writer
- **Task**: Create ATS-optimized resume
- **Format**: Standard resume markdown
- **Focus**: Natural keyword incorporation

## Error Handling

```
┌─────────────────────────────┐
│  Potential Failure Points   │
└─────────────────────────────┘

1. API Rate Limits
   └─ Solution: Wait 60s, retry

2. PDF Extraction Failure
   └─ Solution: Fallback to text input

3. URL Fetch Failure
   └─ Solution: Manual job description input

4. JSON Parse Error
   └─ Solution: Retry with stricter prompt

5. PDF Generation Error
   └─ Solution: Still have markdown output
```

## Performance Characteristics

- **Latency**: ~30-60 seconds total
  - Keyword extraction: ~10s
  - Match scoring: ~15s
  - Resume generation: ~20s
  - PDF creation: ~5s

- **Token Usage**: ~15,000-20,000 tokens per run
  - Agent 1: ~3,000 tokens
  - Agent 2: ~5,000 tokens
  - Agent 3: ~10,000 tokens

- **Cost**: ~$0.10-0.15 per run (Claude Sonnet 4.5 pricing)

## Extensibility

The architecture supports easy extensions:

```
NEW AGENTS CAN BE ADDED:

┌──────────────────────────────┐
│  CoverLetterAgent           │
│  └─ Generate cover letter   │
└──────────────────────────────┘

┌──────────────────────────────┐
│  InterviewPrepAgent         │
│  └─ Generate Q&A prep       │
└──────────────────────────────┘

┌──────────────────────────────┐
│  SkillGapAgent              │
│  └─ Recommend courses       │
└──────────────────────────────┘
```

## Comparison: Old vs New Architecture

### Old (Monolithic)
```
Input → Single LLM Call → Output
• One-shot generation
• No intermediate visibility
• No match scoring
• Hard to extend
```

### New (Multi-Agent)
```
Input → Agent 1 → Agent 2 → Agent 3 → Output
• Step-by-step processing
• Visible intermediate results
• Match percentage included
• Easy to add new agents
• Better error handling
```

## Security Considerations

1. **API Key**: Stored in `.env`, never committed
2. **Data Privacy**: All processing via Anthropic API
3. **Local Storage**: Files only saved locally
4. **No Logging**: Sensitive data not logged
5. **HTTPS**: All API calls encrypted

## Dependencies Graph

```
langchain_resume_agent.py
├── langchain
│   ├── langchain-anthropic
│   │   └── anthropic
│   └── langchain-core
├── PyPDF2
├── reportlab
├── python-dotenv
└── json (stdlib)
```
