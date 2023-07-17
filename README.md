<div align="center">

# YARL - Yet Another Regular Language
</div>

## Instalation

It is recommended to build a virtual environment before installing dependencies for this project as it can reconfigure environment variables.

```bash
$ virtualenv env
$ source env/bin/activate
```

or 

```bash
$ ./env/Scripts/Activate.ps1
```

According the OS you're currently using.

After this, install YARL in developer mode with as it can have some changes later

```bash
$ python setup.py develop
```

## Use

If you're placed in the main folder try running the next command to see if YARL was successfully installed:

```bash
$ python .\src.\main.py .\samples\parser\simple_sample.yarl --debug
```

This will get you in prompt the Lexemes and Tokens scanned in a debug table as following

<div align="center">

![Scanning](https://cdn.discordapp.com/attachments/886256698640171008/1130594115386617856/image.png)

</div>


The proper Abstract Syntax Tree will also be printed and saved in [/output](https://github.com/RayverAimar/yarl/tree/master/output) folder:

```bash
$ python .\src.\main.py .\samples\parser\simple_sample.yarl --debug

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