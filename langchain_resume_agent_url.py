#!/usr/bin/env python3
"""
LangChain Resume Agent with URL support
"""

import sys
import requests
from bs4 import BeautifulSoup
from langchain_resume_agent import LangChainResumeAgent


def fetch_job_description(url: str) -> str:
    """Fetch job description from URL"""
    print(f"Fetching job description from: {url}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove unnecessary elements
        for script in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            script.decompose()

        # Try to find job description
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

        # Limit to avoid rate limits
        if len(text) > 20000:
            text = text[:20000]

        print(f"Successfully fetched ({len(text)} characters)")
        return text

    except Exception as e:
        raise Exception(f"Failed to fetch job description: {str(e)}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python langchain_resume_agent_url.py <job_url> <resume_file>")
        sys.exit(1)

    job_url = sys.argv[1]
    resume_path = sys.argv[2]

    try:
        # Fetch job description
        job_description = fetch_job_description(job_url)

        # Run agent
        agent = LangChainResumeAgent()
        agent.process(job_description, resume_path, job_url)

    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
