import typer
from typing import Optional
from pathlib import Path
from webmix.discovery import discover_files
from webmix.structure import generate_repomix_output

app = typer.Typer()

@app.command()
def main(
    directory: Path = typer.Argument(..., help="The directory containing the website files"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path (default: stdout)")
):
    """
    Convert a local website directory into a single LLM-friendly Markdown file.
    """
    if not directory.exists():
        typer.echo(f"Error: Directory '{directory}' does not exist.", err=True)
        raise typer.Exit(code=1)

    files = discover_files(str(directory))
    
    # For now, we only have the structure generation part implemented
    result = generate_repomix_output(files)
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(result)
        typer.echo(f"Successfully wrote to {output}")
    else:
        typer.echo(result)

if __name__ == "__main__":
    app()
