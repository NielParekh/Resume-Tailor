#!/usr/bin/env python3
"""
LangChain Resume Agent with URL support and Rich UI
"""

import sys
import requests
from bs4 import BeautifulSoup
from langchain_resume_agent_ui import LangChainResumeAgentUI, console


def fetch_job_description(url: str) -> str:
    """Fetch job description from URL"""
    console.print(f"\n[bold]Fetching job description from URL...[/bold]")
    console.print(f"[dim]{url}[/dim]\n")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        for script in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            script.decompose()

        job_content = None
        selectors = [
            {'class': 'job-description'},
            {'class': 'jobdescription'},
            {'id': 'job-description'},
            {'class': 'description'},
            {'role': 'main'},
        ]

        for selector in selectors:
            job_content = soup.find('div', selector) or soup.find('section', selector)
            if job_content:
                break

        if not job_content:
            job_content = soup.find('body') or soup

        text = job_content.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        if len(text) > 20000:
            text = text[:20000]

        console.print(f"[green]✓ Successfully fetched ({len(text)} characters)[/green]\n")
        return text

    except Exception as e:
        raise Exception(f"Failed to fetch job description: {str(e)}")


def main():
    if len(sys.argv) < 3:
        console.print("[red]Usage:[/red] python langchain_resume_agent_url_ui.py <job_url> <resume_file>")
        sys.exit(1)

    job_url = sys.argv[1]
    resume_path = sys.argv[2]

    try:
        job_description = fetch_job_description(job_url)
        agent = LangChainResumeAgentUI()
        agent.process(job_description, resume_path, job_url)
    except Exception as e:
        console.print(f"\n[red]Error:[/red] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
