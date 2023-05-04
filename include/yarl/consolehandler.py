from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table, box
from rich.panel import Panel

from os import path

class ConsoleHandler:
    
    console = Console()
        
    def print_title(self):
        title = """ # Yet Another Regular Language YARL """
        self.console.print(Markdown(title))

    def scan_debug_table(self, tokens):

        debug_table = Table( show_edge=False,show_header=True, expand=False, box=box.SIMPLE )

        debug_table.add_column("[green]Process", style="green")
        debug_table.add_column("[blue]Tag", style="blue")
        debug_table.add_column("[cyan]Token",
                               style="cyan",
                               justify="right",
                               no_wrap=True
                               )
        debug_table.add_column("[magenta]Found at",
                               style="magenta",
                               justify="right"
                               )

        for token in tokens:
            debug_table.add_row("DEBUG SCAN", token.tag, token.lexeme, token.found_at())
        
        self.console.print(debug_table, justify="center")
    
    def scan_debug_panel(self, errors, filename):

        content = ""

        for error in errors:
            error["filename"] = path.abspath(filename)
            content += self.append_error(error)

        self.console.print(Panel(content,
                                 padding=(0, 2),
                                 title="[b red]Errors found! during scanning",
                                 border_style="red"
                                ))

    def append_error(self, error):

        content = f'\nFile [yellow]{error["filename"]}[/yellow], line [b blue]{error["lineno"] - 1}[/b blue]\n'

        if error["content"][-1] == "\n":
            error["content"] = error["content"][:-1]
        
        content += f'  {error["content"]}\n'
        
        idx_error = error["idx_error"]
        highlight_number = 0 if "invalid" in error["msg"] else len(error["content"])-idx_error
        point_out_error = " " * idx_error + "[b red]^" + ("~" * highlight_number)
        
        content += f'  {point_out_error}\n'

        content += f'LexicalError: [/b red]{error["msg"]}\n'

        return content
