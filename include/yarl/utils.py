from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table, box
from rich.panel import Panel

def scan_debug_table():
    debug_table = Table( show_edge=False,show_header=True, expand=False,
                             row_styles=["none", "dim"], box=box.SIMPLE )

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

    return debug_table

def scan_debug_panel(content):
    return Panel(content,
                     padding=(0, 2),
                     title="[b red]Errors found! during scanning",
                     border_style="red"
                )

def append_error(error):

    content = f'\nFile [yellow]{error["filename"]}[/yellow], line [b blue]{error["lineno"]}[/b blue]\n'

    if error["content"][-1] == "\n":
        error["content"] = error["content"][:-1]
    
    content += f'  {error["content"]}\n'
    
    idx_error = error["idx_error"]
    highlight_number = 0 if "invalid" in error["msg"] else len(error["content"])-idx_error
    point_out_error = " " * idx_error + "[b red]^" + ("~" * highlight_number)
    
    content += f'{point_out_error}\n'

    content += f'LexicalError: [/b red]{error["msg"]}\n'

    return content
