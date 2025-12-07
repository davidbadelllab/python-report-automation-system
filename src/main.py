"""
Main entry point for Report Automation System
"""
import click
from rich.console import Console
from pathlib import Path

console = Console()


@click.group()
def cli():
    """Python Report Automation System - CLI Interface"""
    pass


@cli.command()
@click.option('--report', required=True, help='Report name to generate')
@click.option('--date', default=None, help='Date for the report (YYYY-MM-DD)')
@click.option('--output', default='./output', help='Output directory')
def generate(report: str, date: str, output: str):
    """Generate a specific report"""
    console.print(f"[bold green]Generating report:[/bold green] {report}")
    console.print(f"[bold blue]Date:[/bold blue] {date or 'today'}")
    console.print(f"[bold yellow]Output:[/bold yellow] {output}")

    # Import here to avoid circular imports
    from src.core.config import settings
    from src.generators.excel_generator import ExcelGenerator

    generator = ExcelGenerator()
    result = generator.generate_report(report, date, output)

    console.print(f"[bold green]✓ Report generated successfully:[/bold green] {result}")


@cli.command()
@click.option('--job', required=True, help='Job ID to run')
def run_job(job: str):
    """Run a scheduled job manually"""
    console.print(f"[bold green]Running job:[/bold green] {job}")

    from src.schedulers.jobs import execute_job

    result = execute_job(job)
    console.print(f"[bold green]✓ Job completed:[/bold green] {result}")


@cli.command()
def list_jobs():
    """List all configured jobs"""
    console.print("[bold cyan]Configured Jobs:[/bold cyan]")

    jobs = [
        {"id": "daily_sales", "schedule": "Daily at 09:00", "status": "Active"},
        {"id": "weekly_kpi", "schedule": "Monday at 08:00", "status": "Active"},
        {"id": "monthly_summary", "schedule": "1st of month at 07:00", "status": "Active"},
    ]

    for job in jobs:
        console.print(f"  • {job['id']} - {job['schedule']} [{job['status']}]")


@cli.command()
@click.option('--lines', default=50, help='Number of log lines to display')
def logs(lines: int):
    """Display recent logs"""
    console.print(f"[bold cyan]Last {lines} log entries:[/bold cyan]")

    log_file = Path("./output/logs/app.log")
    if log_file.exists():
        with open(log_file) as f:
            log_lines = f.readlines()[-lines:]
            for line in log_lines:
                console.print(line.strip())
    else:
        console.print("[yellow]No logs found[/yellow]")


if __name__ == "__main__":
    cli()
