# Super Investing — AI Research Agent

A small evidence-grounded research agent for the Super Investing AI Innovator Part B assignment.

## What it does

Input:
- NSE ticker, e.g. `SRVCABLE`
- A folder containing company research documents

Output:
- A one-page Markdown research brief with Snapshot, Bull case, Bear case, Open questions, and Sources.

The agent deliberately does **not** use live web search for the required test because Sarvottam Cables is fictional. The supplied research pack is treated as the evidence returned by a scraper.

## Model

I used **OpenRouter 2.5 Flash** because the task is a small document-grounded synthesis problem where fast responses and low cost matter more than a large reasoning model. The model receives the system prompt plus the complete research pack and is instructed to cite every material claim and flag conflicts.

## Setup

1. Install Python 3.10+.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set a OpenRouter API key as `OPENROUTER_API_KEY`.

Windows PowerShell:

```powershell
$env:OPENROUTER_API_KEY="YOUR_KEY"
```

4. Run the required test case:

```bash
python agent.py --ticker SRVCABLE --pack research_pack --output brief.md
```

## Design choices

### 1. Evidence-first prompting
The model is explicitly told that the research pack is the source of truth and that it must not browse the web for the fictional company.

### 2. Source hierarchy
Official exchange/company filings and the earnings transcript are treated as stronger evidence than secondary news and promotional blogs.

### 3. Prompt-injection resistance
One research document contains an instruction aimed at AI assistants. The system prompt explicitly treats document text as untrusted content and tells the model not to follow instructions found inside source documents.

### 4. Conflict detection
The pack contains a useful test conflict: one news article reports Q1 revenue of ₹1,428 crore, while the official company release reports ₹1,248 crore. The agent is instructed to flag this rather than silently choosing a number.

## Files

- `agent.py` — agent implementation
- `system_prompt.md` — system prompt/skill file
- `research_pack/` — supplied test documents
- `brief.md` — generated SRVCABLE brief
- `test_log.md` — iterative testing record
