<div align="center">

# YARL - Yet Another Regular Language
</div>

## Installation

### System dependencies

YARL renders the AST using [Graphviz](https://graphviz.org). Install the binary first — without it, `python src/main.py` will crash with `FileNotFoundError: 'dot'` after parsing.

```bash
# macOS
brew install graphviz

# Debian / Ubuntu
sudo apt-get install graphviz

# Windows
choco install graphviz
```

### Python environment

```bash
# Linux / macOS
$ python3 -m venv env
$ source env/bin/activate

# Windows (PowerShell)
$ python -m venv env
$ .\env\Scripts\Activate.ps1
```

Then install the Python dependencies and YARL in editable mode:

```bash
$ pip install -r requirements.txt
$ python setup.py develop
```

## Use

From the project root, run the compiler against any sample to verify the install:

```bash
# Linux / macOS
$ python src/main.py samples/parser/simple_sample.yarl --debug

# Windows (PowerShell)
$ python .\src\main.py .\samples\parser\simple_sample.yarl --debug
```

This will print the Lexemes and Tokens scanned in a debug table as following

<div align="center">

![Scanning](https://cdn.discordapp.com/attachments/886256698640171008/1130599147519606906/image.png)

</div>


The proper Abstract Syntax Tree will also be printed and saved in [/output](https://github.com/RayverAimar/yarl/tree/master/output) folder:

```bash
$ python .\src\main.py .\samples\parser\simple_sample.yarl --debug

Program
└── DEF_STATEMENT
    ├── def
    ├── add
    ├── (
    ├── TYPED_VAR
    │   ├── a
    │   ├── :
    │   └── int
    ├── ,
    ├── TYPED_VAR
    │   ├── b
    │   ├── :
    │   └── int
    ├── )
    ├── :
    └── BLOCK
        ├── STATEMENT
        │   ├── EXPR
        │   │   └── result
        │   ├── =
        │   └── EXPR
        │       ├── a
        │       ├── +
        │       └── b
        └── STATEMENT
            ├── return
            └── result

--> Accepted Program
```

Its proper AST image will be the following:

<div align="center">

![AST](https://cdn.discordapp.com/attachments/886256698640171008/1130593455396114483/Abstract_Syntax_Tree.png)

</div>

## Recovery Technique

The Recursive Descent Parser has a proper method to recover from error, the current technique used is known as Panic Mode, so if you create a program with fails, the parser will force the parsing to be finished despite the errors as the following example.

```bash
$ python .\src\main.py .\samples\parser\simple_fail_sample.yarl --debug
...
Program
├── DEF_STATEMENT
│   ├── def
│   ├── add
│   ├── ERROR
│   └── BLOCK
│       ├── STATEMENT
│       │   ├── EXPR
│       │   │   └── result
│       │   ├── =
│       │   └── EXPR
│       │       └── a
│       ├── ERROR
│       └── STATEMENT
│           ├── return
│           └── result
└── DEF_STATEMENT
    ├── def
    ├── substraction
    ├── (
    ├── TYPED_VAR
    │   ├── a
    │   ├── :
    │   └── int
    ├── )
    ├── :
    └── BLOCK
        └── ERROR
```
And the errors will be forced to be displayed:

<div align="center">

![Errors](https://cdn.discordapp.com/attachments/886256698640171008/1130597183205421186/image.png)

</div>

And the respective AST will be the following

<div align="center">

![AST_Error](https://media.discordapp.net/attachments/886256698640171008/1130597569735692439/Abstract_Syntax_Tree.png)

</div>

You can try with your own examples and try if they are a correct program according to this modified Chocopy Grammar.