from bs4 import BeautifulSoup
from rich.console import Console
from rich.theme import Theme
import sys
import re

ARGS = sys.argv[1:]

console = Console(highlight=False, theme=Theme({
    'red': '#f87474', 
    'green': '#6edf58',
    'blue': '#1363df',
}))
def error(err, err_type, line='std'):
    console.print(f"""[red]error[/red] in [blue]<{line}>[/blue]:
    returns that [red]error[/red] by [blue]{err_type} error [/blue] (
        "[green]{err}[/green]"
    )[red];[/red]""")
    quit()

def warning(warn):
    console.print(f"[blue]warning[/blue]: {warn}")

try:
    file_name = ARGS[0]
except IndexError:
    error('file name not found in specified arguments.', 'argument_specify')

if 'file_name' in globals():
    if file_name.split('.')[-1] not in (file_extensions:=['htm', 'html']):
        error(f'file extension not supportable for usage.\n\t use one of file extension in {file_extensions}', 'file_extension')
    
    try:
        FUNCTIONS = {
            "math"
        }
        with open(file_name) as f:
            content = f.read().strip()
            f.close()
        
        soup = BeautifulSoup(content, 'html.parser')

        for FUNCTION in FUNCTIONS:
            match FUNCTION:
                case "math":
                    math_tags = soup.find_all('math')

                    if math_tags:
                        for math_tag in math_tags:
                            if math_tag.get('op'):
                                op = math_tag.attrs["op"]
                                
                                if op not in (math_ops := ['+', '-', '*', '/', '//', '%', '**']):
                                    warning("your math tag's <op> attribute value doesnt in math operator list.")
                                else:
                                    res = op.join([math_tag.attrs[i] for i in list(math_tag.attrs) if i != "op"])
                                    
                                    try:
                                        soup.find(math_tag.name, attrs=math_tag.attrs).replaceWith(str(eval(res)))
                                    except SyntaxError:
                                        error(f"cannot do that operation: {res}", "op_error")
                            else:
                                warning("math tag's <op> attribute must to get a value.")

                    else:
                        continue
        with open(file_name, "w+") as f:
            f.write(soup.prettify())
            f.close()
    except FileNotFoundError:
        error(f'file with name {file_name} not found.', 'file_not_found')