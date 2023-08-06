# +
from IPython.core.magic import (magics_class, line_cell_magic, Magics)
from IPython.core import magic_arguments
from IPython.display import Javascript, clear_output, display, HTML

import string
import random

import html

import IPython
from IPython.core.hooks import clipboard_get
# -

from .diff_match_patch import diff_match_patch

@magics_class
class NbDiffMatchPatchMagic(Magics):
    def __init__(self, shell, cache_display_data=False):
        super(NbDiffMatchPatchMagic, self).__init__(shell)

    def output_view(self, output):
        """Display diff in a widget."""
        
        # TO DO - at the moment the HTML is not interpreted as such in the widget;
        # It is currently rendered as a string.
        display(output)
        output='<h1>sdsd\'dfd\'</h1><span>print(\'</span><del style="background:#ffe6e6;">h</del><ins style="background:#e6ffe6;">goodby</ins><span>e</span><del style="background:#ffe6e6;">llo</del><span>\')</span><ins style="background:#e6ffe6;">&para;<br></ins>'
        uid = 'nbcelldiff'+ ''.join([random.choice(string.hexdigits) for n in range(16)])
        output = html.escape(output)
        _output = f"""var nbcelldiff_w = document.createElement("div"); var nbcelldiff_out = document.createElement("div"); nbcelldiff_w.setAttribute("id", "{uid}");nbcelldiff_out.innerHTML = '{output}';nbcelldiff_w.appendChild(nbcelldiff_out);document.getElementsByTagName("head")[0].appendChild(nbcelldiff_w);$("#{uid}").dialog();"""
        display(_output)
        display(Javascript(_output))

    @line_cell_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument('--earlier', '-e', default=None, help='Compare with earlier selected cell')
    @magic_arguments.argument('--clipboard', '-c', action='store_true', help='Compare with contents of clipboard')
    @magic_arguments.argument('--previous', '-p', action='store_true', help='Compare with previously executed cell')
    @magic_arguments.argument('--compare', '-C', default=None, help='Comparetwo previously executed cells (comma separated, no space)')
    def diff_magic(self, line, cell=None):
        "Highlight code difference."
        args = magic_arguments.parse_argstring(self.diff_magic, line)
        
        differ = diff_match_patch()
        #return self.shell.user_ns
        diff = None
        
        if args.previous:
            diff = differ.diff_main(self.shell.user_ns['_ih'][-2], cell)
        elif args.clipboard:
            ip = IPython.get_ipython()
            diff = differ.diff_main(clipboard_get(ip), cell)
        elif args.earlier:
            # TO DO  - check that the index is valid
            diff = differ.diff_main(self.shell.user_ns['_ih'][int(args.earlier)], cell)
        elif args.compare:
            # TO DO  - check that the indexes are valid
            cells = args.compare.split(',')
            diff = differ.diff_main(self.shell.user_ns['_ih'][int(cells[0])], self.shell.user_ns['_ih'][int(cells[1])])

        if diff:
            display(HTML(differ.diff_prettyHtml(diff)))
            #self.output_view(differ.diff_prettyHtml(diff))

        #return self.shell.user_ns


