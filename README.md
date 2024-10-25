# winter.py
**Win**~~dows~~ **ter**~~minal~~ <br>
a proof-of-concept library enhancing the capabilities of the Windows terminal

# Installation

Download the file `winter.py` to the same directory as your program. Inside your program, write
```python
from winter import *
```
to load the library. You can now begin using all the classes and utilities defined within.

# Documentation

All documentation can be found in [the wiki](https://github.com/mk8-bruh/winter.py/wiki).

# Usage example

```python
from winter import *

program = Program(40, 15, "Hello World!", "escape")

class HelloWorld(ProgramState):
  def Enter(self, prev):
    window.Clear()
    Terminal.ResetStyle()
    Terminal.SetCursorPosition(1, 6)
    Terminal.Print(centerString("Hello world!!!", program.width))
    Terminal.Flush()
  def Keypress(self, key):
    Terminal.ResetStyle()
    Terminal.SetCursorPosition(1, 8)
    Terminal.Print(centerString(f"pressed key: {key}", program.width))
    Terminal.Flush()
  def Exit(self, next):
    Terminal.ResetStyle()
    Terminal.SetCursorPosition(1, 10)
    Terminal.Print(centerString(f"Goodbye!!!", program.width))
    Terminal.Flush()

program.Start(HelloWorld())
```

# Demos

## [ATM demo](https://github.com/mk8-bruh/winter.py/blob/main/atm-demo.py)

A simple interface mimicking an ATM that can deposit, withdraw and send money between multiple accounts. Use arrow keys to navigate the interface, `enter` to submit/proceed, `ctrl+z` to go back and `escape` to exit.
