# Password Generator

A password generator with a dark UI built with Python and tkinter. Lets you customize what goes into the password and shows you how strong it is.

## Features

- dark themed UI
- adjustable length (6 to 64 characters)
- toggle uppercase, lowercase, numbers, symbols
- strength meter (weak / medium / strong)
- one-click copy to clipboard
- history of last 20 generated passwords

## How to run

Install the dependency:
```bash
pip install pyperclip
```

Run it:
```bash
python main.py
```

## Usage

- drag the slider to set the password length
- check/uncheck what character types to include
- hit Generate to get a new password
- click Copy to copy it to your clipboard
- click Show History to see previously generated ones and copy from there too
