#!/usr/bin/env python3
"""Quick UI demo to show the Rich interface"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.text import Text
from rich import box
import time

console = Console()

# Header
console.print()
console.print(Panel.fit(
    "[bold cyan]LangChain Agentic Resume Optimizer[/bold cyan]\n"
    "[dim]UI Demo[/dim]",
    border_style="cyan"
))
console.print()

# Demo progress
with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    console=console,
) as progress:

    task = progress.add_task("[cyan]Agent 1: Extracting keywords...", total=100)
    for i in range(100):
        progress.update(task, advance=1)
        time.sleep(0.02)

    progress.update(task, description="[green]✓ Agent 1: Keywords extracted")

console.print()

# Keywords table
table = Table(title="📋 Extracted Keywords", box=box.ROUNDED)
table.add_column("Category", style="cyan")
table.add_column("Keywords", style="white")
table.add_row("Technical Skills", "Python, Machine Learning, AWS, Docker")
table.add_row("Soft Skills", "Leadership, Communication, Problem Solving")
console.print(table)
console.print()

# Match score
score = 87
if score >= 85:
    color = "green"
    emoji = "🎉"
    status = "Excellent Match!"
else:
    color = "yellow"
    emoji = "👍"
    status = "Good Match"

score_text = Text()
score_text.append(f"{emoji} {score}% ", style=f"bold {color}")
score_text.append(status, style=f"{color}")

console.print(Panel(score_text, title="Overall Match Score", border_style=color))
console.print()

# Category breakdown
table2 = Table(title="📊 Category Breakdown", box=box.ROUNDED)
table2.add_column("Category", style="cyan")
table2.add_column("Score", justify="right", style="magenta")
table2.add_column("Progress", width=30)

categories = {
    "Technical Skills": 92,
    "Soft Skills": 85,
    "Experience": 88,
    "Qualifications": 80
}

for category, score in categories.items():
    bar_length = int(score / 100 * 20)
    bar = "█" * bar_length + "░" * (20 - bar_length)

    if score >= 80:
        bar_color = "green"
    else:
        bar_color = "yellow"

    table2.add_row(category, f"{score}%", Text(bar, style=bar_color))

console.print(table2)
console.print()

# Final
console.print(Panel(
    "[bold green]✓ This is what the UI looks like![/bold green]\n\n"
    "[cyan]Features:[/cyan]\n"
    "  • Animated progress bars ⠋\n"
    "  • Color-coded scores 📊\n"
    "  • Beautiful tables 📋\n"
    "  • Visual feedback ✨",
    title="🎨 UI Demo Complete",
    border_style="green"
))
