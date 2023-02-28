#
# Python script to generate a BOM from a KiCad netlist, prompting the user for the wanted fields
#

"""
    @package
    Output: Markdown

    From the window that pops up, remove the unwanted fields and sort/rename those you want.

    Command line:
    python "bom2md.py" "%I" "%O.md"
"""

import sys
import tkinter as tk
from tkinter import scrolledtext
from typing import List

try:
    import kicad_netlist_reader
except ModuleNotFoundError:
    print("Please ensure that the 'kicad_netlist_reader' module is present in this script's directory")
    exit(-1)


# Custon type aliases
Net = kicad_netlist_reader.netlist
Component = kicad_netlist_reader.comp


def get_components(net: Net) -> List[Component]:
    ''' Return the subset of comonents that should show up in the BOM based on blacklists '''
    return net.getInterestingComponents()

def get_components_fields(net: Net, components: List[Component]) -> List[str]:
    compfields = net.gatherComponentFieldUnion(components)
    partfields = net.gatherLibPartFieldUnion()
    return partfields.union(compfields) - set(['Reference'])


def prompt_columns_filter(cols: List[str]) -> List[str]:
    ''' Prompt the user with the list of available BOM fields'''

    def btn_callback(res: List[str]):
        res += txt.get("1.0", "end-1c").split('\n')
        win.destroy()

    result = []
    win = tk.Tk()
    win.title("BOM Fields Configuration")
    win.geometry('600x400')

    l1 = tk.Label(win, text="Fields to show in BOM:", font=("Sans", 16))
    l1.pack()
    l2 = tk.Label(win, text="Delete, reorder, and rename the desired columns.", font=("Sans", 10))
    l2.pack()
    l3 = tk.Label(win, text="To rename a field, use the \"OldName:NewName\" format", font=("Sans", 10))
    l3.pack()

    txt = scrolledtext.ScrolledText(win, wrap=tk.WORD, width=40, height=15)
    txt.pack()
    txt.insert(tk.END, '\n'.join(cols))

    btn = tk.Button(win, text="Generate BOM", command=lambda: btn_callback(result))
    btn.pack()

    tk.mainloop()
    return result


def rename_cols(cols: List[str]) -> dict[str, str]:
    ''' Check if a column needs to be renamed. Return a dictionary with a mapping. '''
    res = {}

    for c in cols:
        if ':' in c:
            a, b = c.split(':')
            res[a] = b
        else:
            res[c] = c
    
    return res


def main():
    if len(sys.argv) != 3:
        print("Usage:", __file__, "<netlist.xml> <output.md>", file=sys.stderr)
        sys.exit(1)
    
    input_netlist: Net = kicad_netlist_reader.netlist(sys.argv[1])
    output_md = open(sys.argv[2], 'w', encoding='utf-8')

    components = get_components(input_netlist)
    grouped_components = input_netlist.groupComponents(components)
    print("Loaded list of %d components" % len(components))

    all_columns = get_components_fields(input_netlist, components)
    cols_selection = prompt_columns_filter(all_columns)
    cols_name_map = rename_cols(cols_selection)

    output_md.write("|Q.ty|References|%s|\n" % '|'.join(cols_name_map.values()))
    output_md.write("%s|\n" % ('|---'*(2 + len(cols_selection))))

    for group in grouped_components:
        refs = [c.getRef() for c in group]
        cols = [input_netlist.getGroupField(group, f) for f in cols_name_map.keys()]

        output_md.write(
            "%d|%s|%s\n" % (
            len(refs), ','.join(refs), '|'.join(cols)
        ))
    
    output_md.close()


if __name__ == '__main__':
    main()