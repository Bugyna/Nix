# Nix-editor
Text editor made with python(3), tkinter and a bunch of other stuff

It can load and highlight a python file(~1200 lines) in an "instant". It takes around 0.5 seconds to highlight the whole file, but since it's multithreaded, there is no lag and the first few lines you see are highlighted very fast.

I added a clock for whatever reason I think it's kinda nice since windows doesn't really show you seconds and I also added temperature (it's random at first but it gets the current temperature(Stockholm) in max 10 minutes)

I started making this before I discovered how good Visual Studio Code actually is and I just kinda continued uprgrading it for fun. It's not perfect or even good but it's kinda usable; It has a syntax highlighter which basically supports Python and C (will add C++ support soon) it can save a file too so it does basically everything I need. I will have to add a Redo somehow though. It has a bunch of commands too, there's also some other themes besides the default dark (cake) one.

to get to the command line press Control+Space

todo:
- add functions to right-click pop-up window
- add more commands and their description and also refactor the parsing command because now it's somewhat sketchy and it can probably be done better
