Overview
========

This is a plugin that renders diagrams from your selection in Sublime Text 2.

By default, it binds the (Command / Alt)-M key and registers a command on the
Command Palette.  Simple select the text for your diagram and trigger the
command.  Multiselections are allowed.

If a diagram handler recognizes a diagram in the selection, it will render it
and pop it up in a detected viewer.  All files are created in such a way that
they will be cleaned up unless Sublime Text dies a particularly horrible death.


Support
=======

Operating Systems:  MacOS X, Linux
Diagram Types: PlantUML
Viewers (in order of preference): MacOS X QuickLook, Eye of Gnome

Patches for additional support welcome.


Install Instructions
====================

Check out the source directory or download and uncompress the source tarball.
Put this directoy in the Packages directory for your platform.

On Linux, it's sometimes "~/.config/sublime-text-2/Packages/".
On MacOS X, it's "~/Library/Application Support/Sublime Text 2/Packages/".

Sublime Text should detect the plugin and automatically load it.

The source is available via git at:

https://github.com/jvantuyl/sublime_diagram_plugin.git

Or as a tarball at:

https://github.com/jvantuyl/sublime_diagram_plugin/tarball/master
