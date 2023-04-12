from yarl.consolehandler import ConsoleHandler
from yarl.scanner import Scanner

import typer

from pathlib import Path

def file_exists(path: str):
    file_path = Path(path)

    if not file_path.exists():
        raise typer.BadParameter(f"Input file not found: {path}")
    
    return file_path

def main(debug: bool = True, file_path:str = typer.Argument("./samples/sample.yarl", 
                                        help="Input file with source code", 
                                        callback=file_exists)):
    console_handler = ConsoleHandler()

    if debug:
        console_handler.print_title()

        scanner = Scanner()
        tokens, errors = scanner.scan(file_path)

        if errors:
            console_handler.scan_debug_panel(errors, file_path)
        else:
            console_handler.scan_debug_table(tokens)

        console_handler.console.print(f'\nFinishing scanning with [b red]{len(errors)}[/b red] errors\n', justify="center")


if __name__ == "__main__":
    typer.run(main)