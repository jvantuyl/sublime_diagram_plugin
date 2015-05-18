# Overview

This is a plugin that renders diagrams from your selection in Sublime Text 2
or 3.

By default, it binds the (Command / Alt)-M key and registers a command on the
Command Palette.  Simple select the text for your diagram and trigger the
command.  Multiselections are allowed.  Each diagram will be generated in a
uniquely named file.

If a diagram handler recognizes a diagram in the selection, it will render it
and pop it up in a detected viewer.  All files are created in such a way that
they will be cleaned up unless Sublime Text dies a particularly horrible death.

If you wish to override the viewer used, disable start-time sanity checks, or
change the default character set for diagram files, create a user version of
Diagram.sublime-settings file in the usual way.

## Install

To install from scratch, it's necessary to have:

* Java (download from java.sun.com)
* Graphviz (I recommend "homebrew" on the Mac)
* Sublime Text 2 or 3

To install, just put a checkout of this project into your Packages directory in
Sublime Text.


## Support

Operating Systems:  MacOS X, Linux, Windows (with default system viewer)
Diagram Types: PlantUML
Viewers (in order of preference):

* MacOS X Preview
* MacOS X QuickLook
* Eye of Gnome

Patches to support additional viewers or diagrams are welcome.

## Install Instructions

Check out the source directory or download and uncompress the source tarball.
Put this directoy in the Packages directory for your platform.

On Linux, it's sometimes "~/.config/sublime-text-2/Packages/".
On MacOS X, it's "~/Library/Application Support/Sublime Text 2/Packages/".

Sublime Text should detect the plugin and automatically load it.

The source is available via git at:

<https://github.com/jvantuyl/sublime_diagram_plugin.git>

Or as a tarball at:

<https://github.com/jvantuyl/sublime_diagram_plugin/tarball/master>

## Example Results

### Component Diagram 1
![component1](./samples/component1.png)

### Component Diagram 2
![component2](./samples/component2.png)

### State Diagram
![state1](./samples/state1.png)

## Thanks

Special thanks to all of those who have contributed code and feedback,
including:

* Tobias Bielohlawek (Syntax Highlighting Support)
* Julian Godesa (UX Feedback)
* Seán Labastille (Preview Support, Multi-Diagram Support)
* Kirk Strauser (Python 3 / SublimeText 3 Support)
* Stanislav Vitko (PlantUML Updates)
* Constantine ? (Windows Viewer, Charset Support, Various Other Fixes)
* Marcelo Da Cruz Pinto (Windows Viewer)
* Peter Ertel (PEP8 Cleanup, Windows Improvements)
* Juan Cabrera (Version Updates)
