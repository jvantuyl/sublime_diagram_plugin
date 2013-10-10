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

If you wish to override the viewer used, create a user version of
Diagram.sublime-settings file in the usual way.

# new feature
## support i18n
You can edit this .wsd file for chinese, and it can render well:

    @startuml
    title <<顺序图>> 这是一个顺序图的说明


    skinparam backgroundColor #EEEBDC 
    actor 使用者
    participant "頭等艙" as A 
    participant "第二類" as B 
    participant "最後一堂課" as 別的東西

    使用者 -> A: 完成這項工作 
    activate A
    A -> B: 創建請求
    activate B
    B -> 別的東西: 創建請求 
    activate 別的東西
    別的東西 --> B: 這項工作完成 
    destroy 別的東西
    B --> A: 請求創建 
    deactivate B
    A --> 使用者: 做完 
    deactivate A 

    @enduml

## support subtitle
Just like the code above, with a title `<<subname>>`, you can get a fixed name with 'sourcefilename-subname.png' instead of the random name with template file.

# Install

To install from scratch, it's necessary to have:

* Java (download from java.sun.com)
* Graphviz (I recommend "homebrew" on the Mac)
* Sublime Text 2 or 3

To install, just put a checkout of this project into your Packages directory in
Sublime Text.


# Support

Operating Systems:  MacOS X, Linux
Diagram Types: PlantUML
Viewers (in order of preference):

* MacOS X Preview
* MacOS X QuickLook
* Eye of Gnome

Patches to support additional viewers or diagrams are welcome.

# Install Instructions

Check out the source directory or download and uncompress the source tarball.
Put this directoy in the Packages directory for your platform.

On Linux, it's sometimes "~/.config/sublime-text-2/Packages/".
On MacOS X, it's "~/Library/Application Support/Sublime Text 2/Packages/".

Sublime Text should detect the plugin and automatically load it.

The source is available via git at:

https://github.com/jvantuyl/sublime_diagram_plugin.git

Or as a tarball at:

https://github.com/jvantuyl/sublime_diagram_plugin/tarball/master

# Thanks

Special thanks to all of those who have contributed code and feedback,
including:

* Tobias Bielohlawek (Syntax Highlighting Support)
* Julian Godesa (UX feedback)
* Seán Labastille (Preview support, multi-diagram support)
* Kirk Strauser (Python 3 / SublimeText 3 Support)
* Stanislav Vitko (PlantUML updates)
