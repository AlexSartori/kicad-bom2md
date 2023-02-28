# KiCad BOM2Md

Plugin for KiCAD to generate a Bill of Materials formatted as a Markdown table.

## Fields selection

When the window with all the available fields pops up, you can:

- **Remove a field**: just delete that line
- **Rename a field**: by appending to the line a colon and the new name, like so `old-name:new-name`
- **Sort the field**: the columns will be generated in the order in which they appear in the window, just move the lines up and down

## Installation

To add a new plugin in KiCad (V6.0, at least), go to `Tools` > `Generate Bill of Materials...` and click on the `+` in the window that pops up. Select the Python script provided in this repo and it will be added to the list.

### Dependencies

Ensure that in KiCad's plugin folder (`~/.local/share/kicad/6.0/plugins/` in my case) the `kicad_netlist_reader.py` module is present. In case it's not, you can install it with pip:

```bash
pip install --user kicad_netlist_reader
```

Also, for the user interface you'll need Tkinter, if it's not already installed:

```bash
sudo apt-get install python3-tk # Ubuntu/Debian
sudo dnf install python3-tkinter # Fedora
brew install python-tk # MacOS
```