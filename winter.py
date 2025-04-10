'''

MIT License

Copyright (c) 2024 Matus Kordos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

from __future__ import annotations
from math import floor, ceil
from time import perf_counter as timer
from msvcrt import kbhit, getch
from re import finditer
from traceback import format_exc

def centerString(s: str, width: int, pad: str = ' '):
    ls = len(s)
    for m in finditer('\x1b.*?\0', s):
        ls -= len(m.group(0))
    if ls > width:
        return s[floor((ls - width) / 2):][:width]
    elif ls < width:
        return pad[0] * floor((width - ls) / 2) + s + pad[0] * ceil((width - ls) / 2)
    else:
        return s

class Terminal:
    buffer = ""

    @staticmethod
    def Print(s = '', end = ''):
        Terminal.buffer += s + end
    
    @staticmethod
    def EmptyBuffer():
        Terminal.buffer = ""

    @staticmethod
    def Flush():
        print(Terminal.buffer)
        Terminal.EmptyBuffer()

    @staticmethod
    def Escape(s: str, inst = False, gen = False):
        if gen:
            return f"\x1b[{s}\0"
        elif inst:
            print(end=f"\x1b[{s}")
        else:
            Terminal.Print(f"\x1b[{s}")

    @staticmethod
    def Clear(**kwargs):
        return Terminal.Escape("2J", **kwargs)
    
    @staticmethod
    def SaveScreen(**kwargs):
        return Terminal.Escape("?47h", **kwargs)
    
    @staticmethod
    def LoadScreen(**kwargs):
        return Terminal.Escape("?47l", **kwargs)

    @staticmethod
    def GetCursorPosition():
        Terminal.Escape("6n", True)
        x = y = ''
        if getch() == b'\x1b' and getch() == b'[':
            c = getch()
            while c != b';':
                y += c.decode()
                c = getch()
            c = getch()
            while c != b'R':
                x += c.decode()
                c = getch()
            return (int(x), int(y))

    @staticmethod
    def HomeCursor(**kwargs):
        return Terminal.Escape("H", **kwargs)

    @staticmethod
    def SetCursorPosition(x: int, y: int, **kwargs):
        return Terminal.Escape(f"{y + 1};{x + 1}H", **kwargs)
    
    @staticmethod
    def SaveCursorPosition(**kwargs):
        return Terminal.Escape(" 7", **kwargs)
    
    @staticmethod
    def LoadCursorPosition(**kwargs):
        return Terminal.Escape(" 8", **kwargs)

    @staticmethod
    def HideCursor(**kwargs):
        return Terminal.Escape("?25l", **kwargs)
    
    @staticmethod
    def ShowCursor(**kwargs):
        return Terminal.Escape("?25h", **kwargs)

    style = {
        "bold": ("1", "22"),
        "dim": ("2", "22"),
        "italic": ("3", "23"),
        "underline": ("4", "24"),
        "blink": ("5", "25"),
        "invert": ("7", "27"),
        "hidden": ("8", "28"),
        "strikethrough": ("9", "29"),
    }

    colors = {
        "black": ("30", "40"),
        "red": ("31", "41"),
        "green": ("32", "42"),
        "yellow": ("33", "43"),
        "blue": ("34", "44"),
        "magenta": ("35", "45"),
        "cyan": ("36", "46"),
        "white": ("37", "47"),
        "default": ("39", "49")
    }

    @staticmethod
    def EnableStyle(*args, **kwargs):
        return Terminal.Escape(f"{';'.join([Terminal.style.get(arg, ('',''))[0] for arg in args])}m", **kwargs)

    @staticmethod
    def DisableStyle(*args, **kwargs):
        return Terminal.Escape(f"{';'.join([Terminal.style.get(arg, ('',''))[1] for arg in args])}m", **kwargs)
    
    @staticmethod
    def SetColor(c: str, **kwargs):
        return Terminal.Escape(f"{Terminal.colors.get(c, ('',''))[0]}m", **kwargs)
    
    @staticmethod
    def ResetColor(**kwargs):
        return Terminal.SetColor("default", **kwargs)

    @staticmethod
    def SetBackground(c: str, **kwargs):
        return Terminal.Escape(f"{Terminal.colors.get(c, ('',''))[1]}m", **kwargs)
    
    @staticmethod
    def ResetBackground(**kwargs):
        return Terminal.SetBackground("default", **kwargs)

    @staticmethod
    def ResetStyle(**kwargs):
        return Terminal.Escape("0m", **kwargs)

class Input:
    keycodes = {
        b' ': 'space',
        b'\r': 'enter',
        b'\t': 'tab',
        b'\x1b': 'escape',
        b'\x08': 'backspace',
        b'\xe0': {
            b'\x47': 'home',
            b'\x48': 'up',
            b'\x49': 'pageup',
            b'\x4b': 'left',
            b'\x4c': 'center', # numpad 5
            b'\x4d': 'right',
            b'\x4f': 'end',
            b'\x50': 'down',
            b'\x51': 'pagedown',
            b'\x52': 'insert',
            b'\x53': 'delete',
            b'\x85': 'f11',
            b'\x86': 'f12'
        },
        b'\x00': {
            b'\x3b': 'f1',
            b'\x3c': 'f2',
            b'\x3d': 'f3',
            b'\x3e': 'f4',
            b'\x3f': 'f5',
            b'\x40': 'f6',
            b'\x41': 'f7',
            b'\x42': 'f8',
            b'\x43': 'f9',
            b'\x44': 'f10',
            b'\x48': 'up',
            b'\x4b': 'left',
            b'\x4c': 'center', # numpad 5
            b'\x4d': 'right',
            b'\x50': 'down',
        },
        b'\x01': 'ctrl+a',
        b'\x02': 'ctrl+b',
        b'\x03': 'ctrl+c',
        b'\x04': 'ctrl+d',
        b'\x05': 'ctrl+e',
        b'\x06': 'ctrl+f',
        b'\x07': 'ctrl+g',
        # \x08 = ctrl+h = backspace
        # \x09 = ctrl+i = \t
        # \x0a = ctrl+j = \n
        b'\x0b': 'ctrl+k',
        b'\x0c': 'ctrl+l',
        # \x0d = ctrl+m = \r
        b'\x0e': 'ctrl+n',
        b'\x0f': 'ctrl+o',
        b'\x10': 'ctrl+p',
        b'\x11': 'ctrl+q',
        b'\x12': 'ctrl+r',
        b'\x13': 'ctrl+s',
        b'\x14': 'ctrl+t',
        b'\x15': 'ctrl+u',
        b'\x16': 'ctrl+v',
        b'\x17': 'ctrl+w',
        b'\x18': 'ctrl+x',
        b'\x19': 'ctrl+y',
        b'\x1a': 'ctrl+z'
    }

    @staticmethod
    def HasKeypress():
        return kbhit()

    @staticmethod
    def GetKeypress(codes: dict[bytes] = keycodes):
        if kbhit():
            ch = getch()
            k = codes.get(ch)
            if type(k) == dict:
                return Input.GetKeypress(k)
            else:
                return k or ch.decode()

class ProgramState:
    def Enter(self, prev: ProgramState, *args, **kwargs):
        pass
    def Update(self, dt: float):
        pass
    def Keypress(self, key: str):
        pass
    def Exit(self, next: ProgramState):
        pass

class Program:
    # state machine
    currentState: ProgramState = None
    exit = False
    deltaTime: float = 0
    def __init__(self, width: int, height: int, name: str = None, killKey = "escape"):
        self.width, self.height = width, height
        self.name = name
        self.killKey = killKey
    def SwitchState(self, state: ProgramState, *args, **kwargs):
        if isinstance(state, ProgramState):
            prev = None
            if self.currentState:
                self.currentState.Exit(state)
                prev = self.currentState
            self.currentState = state
            self.currentState.Enter(prev, *args, **kwargs)
        else:
            raise TypeError("All states must inherit from ProgramState")
    def Run(self, state: ProgramState, *args, **kwargs):
        Terminal.Escape("=7l")
        Terminal.HideCursor()
        Terminal.Flush()
        self.Clear()
        self.SwitchState(state, *args, **kwargs)
        lastT = timer()
        try:
            while not self.exit:
                while Input.HasKeypress():
                    key = Input.GetKeypress()
                    if key == self.killKey:
                        self.Exit()
                    elif self.currentState:
                        self.currentState.Keypress(key)
                self.deltaTime = timer() - lastT
                lastT = timer()
                if self.currentState:
                    self.currentState.Update(self.deltaTime)
            if self.currentState:
                self.currentState.Exit(None)
            Terminal.ResetStyle()
            Terminal.SetCursorPosition(0, self.height + 1)
            Terminal.ShowCursor()
            Terminal.Flush()
        except Exception:
            Terminal.ResetStyle()
            Terminal.SetCursorPosition(0, self.height + 1)
            Terminal.ShowCursor()
            Terminal.Flush()
            print(format_exc())
            
    def Exit(self):
        self.exit = True
    
    # graphics
    def Clear(self):
        Terminal.Clear()
        Terminal.ResetStyle()
        Terminal.HomeCursor()
        Terminal.Print(("╔" + centerString(f" {self.name} " if self.name else "", self.width, "═") + "╗\n") + ("║" + " " * self.width + "║\n") * self.height + ("╚" + "═" * self.width + "╝"), end="")
        Terminal.Flush()
