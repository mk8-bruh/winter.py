# winter.py
enhancing the capabilities of the Windows terminal

# Installation

Download the file `winter.py` to the same directory as your program. Inside your program, write
```python
from winter import *
```
to load the library. You can now begin using all the classes and utilities defined within.

# Usage

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

# Documentation

## Terminal class

### Print calls and the buffer

#### Terminal.Print
```python
Terminal.Print(s, end = "")
```
print the text into the screen buffer
* `s`: the text to print
* `end`: the suffix, used for automatically inserting spaces or newlines (default: `""`)

#### Terminal.EmptyBuffer
```python
Terminal.EmptyBuffer()
```
clear the screen buffer

#### Terminal.Flush
```python
Terminal.Flush()
```
print the buffer onto the screen

### General escape sequences

#### Terminal.Escape
```python
Terminal.Escape(s, inst = False, gen = False)
```
generate an escape sequence with a given code/parameters (for more insight check out the [wipedia page on ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code), for a comprehensive list check out [this cheatsheet](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797))
* `s`: the escape code
* `inst`: whether to execute the command instantaneously or add it to the buffer (default: `False`)
* `gen`: whether to print the command or generate a string and return it (default: `False`)

> *The* `inst` *and* `gen` *parameters apply for all the rest of the functions below*

#### Terminal.Clear
```python
Terminal.Clear()
```
clear the contents of the screen (**not the buffer**)

#### Terminal.SaveScreen
```python
Terminal.SaveScreen()
```
save the current screen contents internally

#### Terminal.LoadScreen
```python
Terminal.LoadScreen()
```
load the saved screen contents back

### Cursor control

#### Terminal.GetCursorPosition
```python
(x, y) = Terminal.GetCursorPosition()
```
reports the current cursor position (starting in the top-left corner)
* `x`: column (from left to right)
* `y`: row (from top to bottom)

#### Terminal.HomeCursor
```python
Terminal.HomeCursor()
```
move cursor to `(0, 0)`

#### Terminal.SetCursorPosition
```python
Terminal.SetCursorPosition(x, y)
```
move the cursor to `(x, y)`

#### Terminal.SaveCursorPosition
```python
Terminal.SaveCursorPosition()
```
save the cursor position internally

#### Terminal.LoadCursorPosition
```python
Terminal.LoadCursorPosition()
```
loads the saved cursor position

#### Terminal.HideCursor
```python
Terminal.HideCursor()
```
make the cursor invisible

#### Terminal.ShowCursor
```python
Terminal.ShowCursor()
```
re-enable cursor visibility

### Styling and colors

#### Available colors

* `black`
* `red`
* `green`
* `yellow`
* `blue`
* `magenta`
* `cyan`
* `white`
* `default`

(again, the appearance might vary between different terminals)

#### Terminal.SetColor
```python
Terminal.SetColor(c)
```
set the text color of future print operations to the given color
* `c`: the name of the color

#### Terminal.ResetColor
```python
Terminal.ResetColor()
```
set the text color back to default

#### Terminal.SetBackground
```python
Terminal.SetBackground(c)
```
set the background color of future print operations to the given color
* `c`: the name of the color

> *This will only affect the background of the text printed after this call, not the color of the entire background!*

#### Terminal.ResetBackground
```python
Terminal.ResetBackground()
```
reset the bakcground color back to default

#### Terminal.ResetColor
```python
Terminal.ResetColor()
```
set the text color back to default

#### Available styles

* `bold`
* `dim`
* `italic`
* `underline`
* `blink`
* `invert`
* `hidden`
* `strikethrough`

(the appearance of these styles might vary between terminals)

#### Terminal.EnableStyle
```python
Terminal.EnableStyle(...)
```
enable the given style(s)
* `...`: the style(s)

#### Terminal.DisableStyle
```python
Terminal.DisableStyle(...)
```
disable the given style(s)
* `...`: the style(s)

#### Terminal.ResetStyle
```python
Terminal.ResetStyle()
```
resets the entire style, _**including text and background color**_

## Input class

### Available key-codes

The module supports all keyboard letters, capital letters (passed as `A`, not `shift+a`), numbers (doesn't differentiate between alpha and numpad) and special characters, along with the following special keys/combinations:
| keyboard key | name |
| :---: | :---: |
| space | `space` |
| enter/return | `enter` |
| tabulator | `tab` |
| escape | `escape` |
| backspace | `backspace` |
| up arrow | `up` |
| down arrow | `down` |
| left arrow | `left` |
| right arrow | `right` |
| delete | `delete` |
| insert | `insert` |
| home | `home` |
| end | `end` |
| page up | `pageup` |
| page down | `pagedown` |
| f1 - f10 | `f1` - `f10` |
| control-a - control-z\* | `ctrl+a` - `ctrl+z` |

\**control-i, control-j and control-m are not available due to representing tab, enter and newline*

### Checking functions

#### Input.HasKeypress
```python
Input.HasKeypress()
```
checks if there has been a keypress which was not yet processed

#### Input.GetKeypress
```python
key = Input.GetKeypress()
```
returns the next keypress in the buffer (**WARNING** - this is a blocking call; if used without checking `Input.HasKeypress`, the program will stop and wait until the user presses a key)
* `key`: the name of the key that was pressed

## ProgramState class

A base class for all screens/scenes in the program. Every class representing a different screen has to inherit from this class.

### Callbacks

These are callbacks to be overridden by your custom state class. _**Make sure to always include all the compulsory parameters**_ in your custom callback, otherwise a `TypeError` will be raised, as these parameters are always passed by the program.

#### ProgramState.Enter
```python
state.Enter(self, prev, *args, **kwargs)
```
triggered when the state is turned active with `program.SwitchState()`
* `prev`: the previous active state of the program (will be `None` when the program has just started)
* `*args`, `**kwargs`: the optional arguments passed to the `SwitchState` call

#### ProgramState.Update
```python
state.Update(self, dt)
```
called continually in the smallest intervals possible
* `dt`: the time since the last `Update` call ([perf_counter](https://docs.python.org/3/library/time.html#time.perf_counter) is used as the timer function)

#### ProgramState.Keypress
```python
state.Keypress(self, key)
```
triggered when a key is pressed while this state is active
* `key`: the name of the key that was pressed

#### ProgramState.Exit
```python
state.Exit(self, next)
```
called when this state is made inactive due to a `SwitchState` call
* `next`: the next active state (will be `None` when exiting the program)

## Program class

The class for running and managing your custom `ProgramState`s.

### Creating a program

Create a new `Program` instance with the constructor
```python
program = Program(width, height, name = None, killKey = "escape")
```
* `width`: the width of the "window"
* `height`: the height of the "window"
* `name`: the title, displayed in the center of the top border (default: `None`)
* `killKey`: a key which automatically terminates the program (default: `"escape"`)
* `program`: the resultant `Program` instance

### Properties

These are used internally or for debugging. **Do not overwrite these values manually**.

#### program.currentState
```python
program.currentState: ProgramState
```
the currently active `ProgramState` instance

#### program.exit
```python
program.exit: bool
```
whether the program shout exit upon finishing the next update

#### program.deltaTime
```python
program.deltaTime: float
```
the time between the last two `Update`s (passed as `dt` into `ProgramState.Update`)

### Functions

#### program.Run
```python
program.Run(state, *args, **kwargs)
```
start the program with a given state
* `state`: the first active `ProgramState`
* `*args`, `**kwargs`: optional arguments to pass to `state.Enter`

#### program.SwitchState
```python
program.SwitchState(state, *args **kwargs)
```
deactivate the current state and set `state` as the new active state
* `state`: the new active state
* `*args`, `**kwargs`: optional arguments for `state.Enter`

#### program.Clear
```python
program.Clear()
```
clear the contents of the "window" and redraw it

#### program.Exit
```python
program.Exit()
```
finish the current `Update` cycle and terminate the program

# Demos

## [ATM demo](https://github.com/mk8-bruh/winter.py/blob/main/atm-demo.py)

A simple interface mimicking an ATM that can deposit, withdraw and send money between multiple accounts. Use arrow keys to navigate the interface, `enter` to submit/proceed, `ctrl+z` to go back and `escape` to exit.
