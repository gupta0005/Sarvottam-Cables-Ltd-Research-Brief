"""Super Investing AI research agent using OpenRouter.

Usage:
    pip install -r requirements.txt
    set OPENROUTER_API_KEY=...
    python agent.py --ticker SRVCABLE --pack research_pack --output brief.md

The agent intentionally does not use web search. The assignment's test company is fictional,
and the research pack is treated as the scraped evidence set.
"""

import argparse
import os
import time
from pathlib import Path

SYSTEM_PROMPT = Path("system_prompt.md").read_text(encoding="utf-8")


def load_documents(pack_dir: str):
    docs = []
    for path in sorted(Path(pack_dir).glob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        docs.append((path.name, text))
    if not docs:
        raise ValueError(f"No markdown research documents found in {pack_dir}")
    return docs


def build_context(docs):
    blocks = []
    for filename, text in docs:
        blocks.append(f"\n===== DOCUMENT: {filename} =====\n{text}")
    return "".join(blocks)


def call_openrouter(prompt: str, model: str):
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("Install dependencies with: pip install -r requirements.txt") from exc

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set. Add your OpenRouter API key to the environment.")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "https://github.com/",
            "X-Title": "Super Investing AI Research Agent",
        },
    )

    last_error = None
    for attempt in range(4):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=3500,
            )
            content = response.choices[0].message.content
            if not content:
                raise RuntimeError("OpenRouter returned an empty response.")
            return content.strip()
        except Exception as exc:
            # Do not retry permanent billing/auth errors.
            if getattr(exc, "status_code", None) in (400, 401, 402, 403):
                raise
            last_error = exc
            if attempt == 3:
                raise
            wait = 2 ** attempt
            print(f"OpenRouter request failed. Retrying in {wait}s...")
            time.sleep(wait)

    raise RuntimeError("OpenRouter request failed.") from last_error


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--pack", default="research_pack")
    parser.add_argument("--model", default="openai/gpt-4o")
    parser.add_argument("--output", default="brief.md")
    args = parser.parse_args()

    docs = load_documents(args.pack)
    context = build_context(docs)

    user_prompt = f"""Research ticker: {args.ticker}\nAssume today is 23 September 2026.\n\nProduce the required one-page research brief using ONLY the evidence below.\n\n{context}"""
    full_prompt = SYSTEM_PROMPT + "\n\n" + user_prompt
    brief = call_openrouter(full_prompt, args.model)
    Path(args.output).write_text(brief + "\n", encoding="utf-8")
    print(brief)


if __name__ == "__main__":
    main()
