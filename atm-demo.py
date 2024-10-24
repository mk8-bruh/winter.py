'''

A SIMPLE DEMONSTRATION OF THE winter LIBRARY - A BANK ATM INTERFACE

CONTROLS:
[ARROWS] | navigate
[ENTER ] | submit/proceed
[CTRL+Z] | go back
[ESCAPE] | exit

'''

from winter import *

class Account:
    all = []
    @staticmethod
    def Exists(name):
        for account in Account.all:
            if account.name == name:
                return True
    @staticmethod
    def Find(name):
        for account in Account.all:
            if account.name == name:
                return account
    @staticmethod
    def Register(name, pin, confirmPIN):
        if pin != confirmPIN:
            return "PIN unconfirmed"
        if Account.Exists(name):
            return "An account with this name already exists"
        Account.all.append(Account(name, pin))
        return f"Successfully registered {Terminal.EnableStyle('bold', gen = True) + Terminal.SetColor('cyan', gen = True)}{name}{Terminal.ResetStyle(gen = True)}"
    @staticmethod
    def Remove(account, confirm):
        if account in Account.all:
            if confirm:
                Account.all.remove(account)
                return f"Successfully removed {Terminal.EnableStyle('bold', gen = True) + Terminal.SetColor('cyan', gen = True)}{account.name}{Terminal.ResetStyle(gen = True)}"
            else:
                return "Operation cancelled"
        else:
            return "Account not registered"
    
    def __init__(self, name, pin, balance = 0):
        self.name = name
        self.pin = pin
        self.balance = balance
    def Deposit(self, sum):
        self.balance += sum
        return f"Successfully deposited {Terminal.EnableStyle('bold', gen = True) + Terminal.SetColor('green', gen = True)}{sum}{Terminal.ResetStyle(gen = True)}"
    def Withdraw(self, sum):
        if self.balance >= sum:
            self.balance -= sum
            return f"Successfully withdrawn {Terminal.EnableStyle('bold', gen = True) + Terminal.SetColor('green', gen = True)}{sum}{Terminal.ResetStyle(gen = True)}"
        else:
            return "Withdrawn sum exceeds the balance"
    def Send(self, recipient, sum):
        if recipient == self.name:
            return "Cannot send money to self"
        if Account.Exists(recipient):
            if self.balance >= sum:
                self.balance -= sum
                Account.Find(recipient).balance += sum
                return f"Successfully sent {Terminal.EnableStyle('bold', gen = True) + Terminal.SetColor('green', gen = True)}{sum}{Terminal.ResetStyle(gen = True)} to {Terminal.EnableStyle('bold', gen = True) + Terminal.SetColor('cyan', gen = True)}{recipient}{Terminal.ResetStyle(gen = True)}"
            else:
                return "Sent sum exceeds the balance"
        return "Recipient not found"

window = Program(40, 15, "Winter Bank ATM", killKey = "escape")

# generic scene classes

class Message(ProgramState):
    def __init__(self, message = "Something went wrong...\nPress [ESC] to exit", nextScreen = None):
        self.message = message
        self.nextScreen = nextScreen
    def Enter(self, prev):
        window.Clear()
        Terminal.ResetStyle()
        for (i, l) in zip(range(self.message.count('\n') + 1), self.message.split('\n')):
            Terminal.SetCursorPosition(1, 8 - ceil(self.message.count('\n') / 2) + i)
            Terminal.Print(centerString(l, window.width))
        Terminal.Flush()
    def Keypress(self, key):
        if key == "enter":
            if self.nextScreen:
                window.SwitchState(self.nextScreen)

class MenuItem:
    def __init__(self, name = "", action = None):
        self.name = name
        self.action = action
    def Select(self):
        if self.action:
            self.action(self)

class Menu(ProgramState):
    def __init__(self, header = "", items = [], decorator = Terminal.EnableStyle('bold', gen = True) + Terminal.SetColor('yellow', gen = True)):
        self.header = header
        self.items = items
        self.decorator = decorator
        self.selected = 0
    def Enter(self, prev):
        window.Clear()
        Terminal.ResetStyle()
        lineCount = self.header.count('\n') + 1
        for (i, l) in zip(range(lineCount), self.header.split('\n')):
            Terminal.SetCursorPosition(1, 2 + i)
            Terminal.Print(centerString(l, window.width))
        for (i, v) in zip(range(len(self.items)), self.items):
            Terminal.SetCursorPosition(1, 3 + lineCount + i)
            Terminal.Print(centerString(f"{self.decorator if i == self.selected else ''}{v.name}{Terminal.ResetStyle(gen = True)}", window.width))
        Terminal.Flush()
    def Keypress(self, key):
        Terminal.ResetStyle()
        lineCount = self.header.count('\n') + 1
        if 0 <= self.selected < len(self.items):
            Terminal.SetCursorPosition(1, 3 + lineCount + self.selected)
            Terminal.Print(centerString(self.items[self.selected].name, window.width))
            if key == "enter":
                self.items[self.selected].Select()
                return
        if key == "up":
            if self.selected - 1 >= 0:
                self.selected -= 1
        elif key == "down":
            if self.selected + 1 < len(self.items):
                self.selected += 1
        for (i, v) in zip(range(len(self.items)), self.items):
            Terminal.SetCursorPosition(1, 3 + lineCount + i)
            Terminal.Print(centerString(f"{self.decorator if i == self.selected else ''}{v.name}{Terminal.ResetStyle(gen = True)}", window.width))
        Terminal.Flush()

class DialogValue:
    def __init__(self, name, type = "int", values = None, value = None, validate = lambda x: True, encrypt = lambda x: x):
        self.name = name
        self.type = type
        self.values = values
        self.value = value if value else (0 if self.values else "")
        self.validate = validate
        self.encrypt = encrypt
    def IsValid(self):
        if self.values:
            return self.validate(type(self.value) == int and self.value in range(len(self.values)))
        else:
            s = self.value
            try:
                if self.type == "int":
                    return self.validate(int(self.value))
                elif self.type == "float":
                    return self.validate(float(self.value))
                elif self.type == "bool":
                    return s.lower() in ("true", "false", "yes", "no")
                elif self.type == "string":
                    return self.validate(self.value)
            except ValueError:
                pass
            return False
    def Convert(self):
        if self.IsValid():
            if self.values:
                s = self.values[self.value]
            else:
                s = self.value
            try:
                if self.type == "int":
                    return int(s)
                elif self.type == "float":
                    return float(s)
                elif self.type == "bool":
                    return True if s.lower() in ("true", "yes") else False if s.lower() in ("false", "no") else None
                elif self.type == "string":
                    return s
            except ValueError:
                pass
        return None

class Dialog(ProgramState):
    def __init__(self, operation, header = "", params = [DialogValue("Continue?", "bool", ("Yes", "No"))], nextScreen = None, decorator = Terminal.EnableStyle("bold", gen = True) + Terminal.SetColor("yellow", gen = True)):
        self.operation = operation
        self.header = header
        self.values = params
        self.selected = 0
        self.nextScreen = nextScreen
        self.decorator = decorator
    def Enter(self, prev):
        self.prev = prev
        window.Clear()
        Terminal.ResetStyle()
        lineCount = self.header.count('\n') + 1
        for (i, l) in zip(range(lineCount), self.header.split('\n')):
            Terminal.SetCursorPosition(1, 2 + i)
            Terminal.Print(centerString(l, window.width))
        for (i, v) in zip(range(len(self.values)), self.values):
            Terminal.SetCursorPosition(1, 3 + lineCount + i)
            Terminal.Print(centerString(f"{self.decorator if i == self.selected else ''}{v.name}{Terminal.ResetStyle(gen = True)}: {'< ' if v.values and v.value > 0 else ''}{v.values[v.value] if v.values else v.encrypt(v.value)}{' >' if v.values and v.value < len(v.values) - 1 else ''}", window.width))
        Terminal.Flush()
    def Keypress(self, key):
        Terminal.ResetStyle()
        lineCount = self.header.count('\n') + 1
        if 0 <= self.selected < len(self.values):
            v = self.values[self.selected]
            Terminal.SetCursorPosition(1, 3 + lineCount + self.selected)
            Terminal.Print(centerString(f"{v.name}: {'< ' if v.values and v.value > 0 else ''}{v.values[v.value] if v.values else v.encrypt(v.value)}{' >' if v.values and v.value < len(v.values) - 1 else ''}", window.width))
            if key == "left":
                if v.values and v.value - 1 >= 0:
                    v.value -= 1
            elif key == "right":
                if v.values and v.value + 1 < len(v.values):
                    v.value += 1
            elif key == "backspace":
                if v.type != "bool" and not v.values:
                    v.value = v.value[:-1]
            elif not key in ("up", "down", "enter") and not v.values:
                if key == "space":
                    key = " "
                pv = v.value
                v.value += key
                if not v.IsValid():
                    v.value = pv
        if key == "up":
            if self.selected > 0:
                self.selected -= 1
        elif key == "down":
            if self.selected < len(self.values) - 1:
                self.selected += 1
        elif key == "enter":
            valid = True
            for v in self.values:
                if not v.IsValid():
                    valid = False
            if valid:
                window.SwitchState(Message(self.operation(*(v.Convert() for v in self.values)), self.nextScreen))
                return
        elif key == "ctrl+z" and self.prev:
            window.SwitchState(self.prev)
            return
        for (i, v) in zip(range(len(self.values)), self.values):
            Terminal.SetCursorPosition(1, 3 + lineCount + i)
            Terminal.Print(centerString(f"{self.decorator if i == self.selected else ''}{v.name}{Terminal.ResetStyle(gen = True)}: {'< ' if v.values and v.value > 0 else ''}{v.values[v.value] if v.values else v.encrypt(v.value)}{' >' if v.values and v.value < len(v.values) - 1 else ''}", window.width))
        Terminal.Flush()

# screens

class StartScreen(Menu):
    def __init__(self):
        super().__init__(f"Welcome to {Terminal.EnableStyle('bold', gen = True) + Terminal.SetColor('cyan', gen = True)}Winter Bank{Terminal.ResetStyle(gen = True)}", [])
    def Enter(self, prev):
        self.items = []
        for i in range(len(Account.all)):
            account = Account.all[i]
            self.items.append(MenuItem(account.name, lambda i: window.SwitchState(PINScreen(Account.Find(i.name)))))
        self.items += [MenuItem("<register>", lambda *_: window.SwitchState(Dialog(Account.Register, "Register an account", [
            DialogValue("name", "string"),
            DialogValue("PIN", "int", validate = lambda p: p < 10**4, encrypt = lambda p: " ".join(f"{"*" * len(p):_<4}")),
            DialogValue("confirm PIN", "int", validate = lambda p: p < 10**4, encrypt = lambda p: " ".join(f"{"*" * len(p):_<4}"))
        ], self)))]
        super().Enter(prev)

class PINScreen(ProgramState):
    def __init__(self, account, attempts = 3):
        self.pin = ""
        self.account = account
        self.correct = str(account.pin)
        self.attemptsLeft = attempts
    def Enter(self, prev):
        self.prev = prev
        window.Clear()
        Terminal.ResetStyle()
        Terminal.SetCursorPosition(1, 7)
        Terminal.Print(centerString(f"Enter PIN for {Terminal.EnableStyle('bold', gen = True) + Terminal.SetColor('cyan', gen = True)}{self.account.name}{Terminal.ResetStyle(gen = True)}:", window.width))
        Terminal.SetCursorPosition(1, 8)
        Terminal.Print(centerString(" ".join("_" * len(self.correct)), window.width))
        Terminal.SetCursorPosition(1, 9)
        Terminal.Print(centerString(f"({self.attemptsLeft} attempt{'s' if self.attemptsLeft != 1 else ''} remaining)", window.width))
        Terminal.Flush()
    def Keypress(self, key):
        if key in "0123456789":
            if len(self.pin) < len(self.correct):
                self.pin += key
        elif key == "backspace":
            if len(self.pin) > 0:
                self.pin = self.pin[:-1]
        elif key == "enter":
            if len(self.pin) >= len(self.correct):
                if self.pin == self.correct:
                    window.SwitchState(AccountScreen(self.account))
                    return
                else:
                    self.attemptsLeft -= 1
                    if self.attemptsLeft <= 0:
                        window.SwitchState(Message("You entered the wrong PIN too many times", StartScreen()))
                    else:
                        Terminal.SetCursorPosition(1, 9)
                        Terminal.Print(centerString(f"({self.attemptsLeft} attempt{'s' if self.attemptsLeft != 1 else ''} remaining)", window.width))
                self.pin = ""
        elif key == "ctrl+z" and self.prev:
            window.SwitchState(self.prev)
            return
        Terminal.ResetStyle()
        Terminal.SetCursorPosition(1, 8)
        Terminal.Print(centerString(" ".join("*" * len(self.pin) + "_" * (len(self.correct) - len(self.pin))), window.width))
        Terminal.Flush()

class AccountScreen(Menu):
    def __init__(self, account):
        self.account = account
        super().__init__(f"Logged in as {Terminal.EnableStyle('bold', gen = True) + Terminal.SetColor('cyan', gen = True)}{self.account.name}{Terminal.ResetStyle(gen = True)}\nBalance: {Terminal.EnableStyle('bold', gen = True) + Terminal.SetColor('green', gen = True)}{self.account.balance}{Terminal.ResetStyle(gen = True)}",
        [
            MenuItem("deposit",  lambda *_: window.SwitchState(Dialog(self.account.Deposit,  "Deposit",  [DialogValue("amount", "float")], self))),
            MenuItem("withdraw", lambda *_: window.SwitchState(Dialog(self.account.Withdraw, "Withdraw", [DialogValue("amount", "float")], self))),
            MenuItem("send",     lambda *_: window.SwitchState(Dialog(self.account.Send,     "Send",     [DialogValue("recipient", "string"), DialogValue("amount", "float")], self))),
            MenuItem("logout",   lambda *_: window.SwitchState(StartScreen())),
            MenuItem("remove",   lambda *_: window.SwitchState(Dialog(lambda c: Account.Remove(self.account, c), "Remove", nextScreen = self)))
        ])
    def Enter(self, prev):
        if not self.account in Account.all:
            window.SwitchState(StartScreen())
        else:
            super().Enter(prev)

window.Run(StartScreen())
