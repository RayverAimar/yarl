from yarl.scanner import Scanner

import typer

from pathlib import Path

def file_exists(path: str):
    file_path = Path(path)

    if not file_path.exists():
        raise typer.BadParameter(f"Input file not found: {path}")
    
    return file_path

def main(debug: bool = False, file_path:str = typer.Argument("./samples/sample.txt", 
                                        help="Input file with source code", 
                                        callback=file_exists)):
    if debug:
        scanner = Scanner()
        scanner.scan(file_path)

if __name__ == "__main__":
    typer.run(main)