# winter.py
enhancing the capabilities of the Windows terminal

## Installation
Download the file `winter.py` to the same directory as your program. Inside your program, write
```python
from winter import *
```
to load the library. You can now begin using all the classes and utilities defined within.

## Usage

### Terminal class

#### Print calls and the buffer

```python
Terminal.Print(s, end = "")
```
print the text into the screen buffer
`s`: the text to print
`end`: the suffix, used for automatically inserting spaces or newlines (default: `""`)

```python
Terminal.EmptyBuffer()
```
clear the screen buffer

```python
Terminal.Flush()
```
print the buffer onto the screen

#### Escape sequences

```python
Terminal.Escape(s, inst = False, gen = False)
```
generate an escape sequence with a given code/parameters (for more insight check out the [wipedia page on ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code), for a comprehensive list check out [this cheatsheet](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797))
`s`: the escape code
`inst`: whether to execute the command instantaneously or add it to the buffer (default: `False`)
`gen`: whether to print the command or generate a string and return it (default: `False`)

*The* `inst` *and* `gen` *parameters apply for all other functions in this section*

```python
Terminal.Clear()
```
clear the contents of the screen (**not the buffer**)

```python
Terminal.SaveScreen()
```
save the current screen contents internally

```python
Terminal.LoadScreen()
```
load the saved screen contents back

### Input class

### Program class

### ProgramState class
