### IMPORTS             ###
    ## Dependencies         ##
from docifyPLUS import (
    document
)
from lambdaChaining import (
    b       # binding lambda
)
    ## Dependencies         ##
from tkinter import (
    Tk,
    Frame,
    Button,
    Widget
)
from collections.abc import (
    Iterable
)
### IMPORTS             ###
### CONSTANTS           ###
lmbda = type(lambda _: _)
### CONSTANTS           ###
### UTILITY             ###
def grid(w: Widget, p: None or Iterable=None, **k: "Standard tkinter **opts"):
    """Allows for ease of griding widgets"""
    w.grid(column=p[0], row=p[1], **k) if p else w.grid(**k)
def _bind(master, action, binding): master.bind(
    binding,
    action
)
def bind_enter(master: Tk or Frame, action: lmbda): _bind(
    master,
    action,
    '<Enter>'
)
def bind_leave(master: Tk or Frame, action: lmbda): _bind(
    master,
    action,
    '<Leave>'
)
change_bg = lambda master, c: master.config(background=c)

document(bind_enter, "For binding a command to <Enter> for a widget")
document(bind_leave, "For binding a command to <Leave> for a widget")
document(change_bg, "For changing the background of a widget")
### UTILITY             ###
### BUTTONS             ###
class Buttons(object):
    """
    Class to access all Tkinter Template Buttons
    """

    class ButtonCommands(object):
        def add_cmd(self, cmd: "Command"): self.config(command=cmd)

            
        @staticmethod
        def _hover(inst):
            bind_ent, bind_leav = inst.colors
            bg = bind_leav if bind_leav != 'origin' else inst.cget('background') 
            bind_enter(
                inst,
                lambda *args: change_bg(inst, bind_ent)
            )
            bind_leave(
                inst,
                lambda *args: change_bg(inst, bg)
            )

        document(add_cmd, "For adding commands to buttons")
    class Big(Button, ButtonCommands):
        """
        Class to create a Big Button in tkinter.
        
        In order to add options not listed in the init,
        one must use the config method
        """
        def __init__(self,
            master:         Tk or Frame,
            text:           "Text to appear on Button",
            bind_ent:       "Button background color upon entering"='azure',
            bind_leav:      "Button background color upon leaving"='origin',
            height:         "Any Integer; Self-explanitory"=1,
            width:          "Any Integer; Self-explanitory"=20,
            relief:         "How the button looks on the window"='flat',
            borderwidth:    "Any Integer; Self-explanitory"=0,
            font:           "Format: (Font-family, Font-size)"=('Papyrus', 40)
            ):
            ## Init ##
            Button.__init__(self,
                master,
                text=text,
                height=height, width=width,
                relief=relief,
                borderwidth=borderwidth,
                font=font
            )
            self.colors = (bind_ent, bind_leav)
            ## Init ##
            ## Bindings ##
            self._hover(self)
            ## Bindings ##
    class Back(Big):
        def __init__(self,
            master:         Tk or Frame,
            dest:           f"{Tk or Frame } Destination to go upon clicking back button",
            text:           "Text to appear on Button"="Back",
            bind_ent:       "Button background color upon entering"='azure',
            bind_leav:      "Button background color upon leaving"='origin',
            height:         "Any Integer; Self-explanitory"=1,
            width:          "Any Integer; Self-explanitory"=20,
            relief:         "How the button looks on the window"='flat',
            borderwidth:    "Any Integer; Self-explanitory"=0,
            font:           "Format: (Font-family, Font-size)"=('Papyrus', 40)
            ):
            ## Init             ##
            Buttons.Big.__init__(self,
                master,
                text=text,
                height=height, width=width,
                relief=relief,
                borderwidth=borderwidth,
                font=font
            )
            self.dest = dest
            self.master = master
            self.add_cmd(
                lambda: b(
                    self.master.grid_forget(), lambda _: b(
                        grid(self.dest, (0, 0))
                    )
                )
            )
            ## Init             ##
    class Small(Button, ButtonCommands):
        """
        Class to create a Big Button in tkinter.
        
        In order to add options not listed in the init,
        one must use the config method
        """
        def __init__(self,
            master:         Tk or Frame,
            text:           "Text to appear on Button",
            bind_ent:       "Button background color upon entering"='azure',
            bind_leav:      "Button background color upon leaving"='origin',
            height:         "Any Integer; Self-explanitory"=1,
            width:          "Any Integer; Self-explanitory"=10,
            relief:         "How the button looks on the window"='flat',
            borderwidth:    "Any Integer; Self-explanitory"=0,
            font:           "Format: (Font-family, Font-size)"=('Papyrus', 20)
            ):
            ## Init ##
            Button.__init__(self,
                master,
                text=text,
                height=height, width=width,
                relief=relief,
                borderwidth=borderwidth,
                font=font
            )
            self.colors = (bind_ent, bind_leav)
            ## Init ##
            ## Bindings ##
            self._hover(self)
            ## Bindings ##
### BUTTONS             ###
root = Tk()
Buttons.Big(root, "LLJW").grid(row=0,column=0)
root.mainloop()