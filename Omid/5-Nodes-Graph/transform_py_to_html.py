"""Take a python source code file as input and output its contents as HTML with syntax highlighting. 
This can be used to get syntax highlighting and line numbers to be displayed in JACK.
"""

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import autopep8
import argparse
import sys
import os

parser = argparse.ArgumentParser(
    prog="transform_py_to_html.py",
    description="""transform_py_to_html.py
    takes a python file as input and outputs a HTML file
    containing the python code with HTML formatting.
    By default the output is wrapped inside a collapsible HTML block.""")

parser.add_argument("-w", "--wrap", dest="wrap", action="store_true", help="Deprecated. This flag has no effect. Wrapping in a collapsible HTML block is now the default. Refer to -n, --nowrap to prevent this.")
parser.add_argument("-n", "--nowrap", dest="nowrap", action="store_true", help="If flag is set, only the python code is output without a collapsible HTML block around it.")
parser.add_argument("INPUT_FILE", type=str, help="Relative or absolute path to the input python file.")
parser.add_argument("-o", "--output", dest="OUTPUT_FILE", type=str, help="Relative or absolute path to the output HTML file. If omitted, output to STDOUT.", default=sys.stdout)

args = parser.parse_args()


with open(os.path.abspath(args.INPUT_FILE), "r") as f:
    code = f.read()

code = autopep8.fix_code(code, options={"indent_size": 2})

formatter = HtmlFormatter(
    full=False,
    linenos=True,
    noclasses=True,
    style="friendly"
)
highlighted_code = highlight(code, PythonLexer(), formatter)

# Line numbers and code are not aligned vertically, since they have different line heights.
# Fix this by adding line-height: 125% to the line number table.
# Do this by lazily adding the line height to the <pre> tag.
# There is only one <pre> tag before the class declaration of "linenodiv",
# therefore it should always affect the correct one.
highlighted_code = str(highlighted_code).replace(r'<div class="linenodiv"><pre>', r'<div class="linenodiv"><pre style="line-height: 125%;">' + "\n")

if args.wrap:
    print("Warning: The option -w, --wrap is deprecated. It is now the default behavior. Consult option -n, --nowrap to prevent wrapping the output in a collapsible HTML element.")

if not args.nowrap:
    highlighted_code = (
"""<details style="border-radius: 5px; display: inline-block; max-width: 100%; width: 100%;">
    <summary style="cursor: pointer; font-size: 16px; display: inline-block; padding: 10px 15px; background-color: #ccc; border-radius: 5px;">Toggle Code</summary>
    <div style="background-color: #f0f0f0; border-radius: 5px; margin-top: 5px; padding: 10px; max-width: 100%; max-height: 50vh; width: fit-content; overflow: auto;">
""" + 
highlighted_code + 
"""    </div>
</details>""")

out = args.OUTPUT_FILE

if type(args.OUTPUT_FILE) == str:
    if not os.path.exists(args.OUTPUT_FILE):
        os.makedirs(os.path.dirname(args.OUTPUT_FILE), exist_ok=True)
    out = open(args.OUTPUT_FILE, "w")

out.write(highlighted_code)
