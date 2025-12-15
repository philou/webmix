import typer
from typing import Optional
from pathlib import Path
from webmix.discovery import discover_files
from webmix.structure import generate_webmix_output

app = typer.Typer()

def aggregate_website(directory_path: str) -> str:
    """
    Discover files in the directory and generate the aggregated Markdown output.
    """
    files = discover_files(directory_path)
    return generate_webmix_output(files, base_dir=directory_path)

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

    result = aggregate_website(str(directory))
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(result)
        typer.echo(f"Successfully wrote to {output}")
    else:
        typer.echo(result)

if __name__ == "__main__":
    app()
