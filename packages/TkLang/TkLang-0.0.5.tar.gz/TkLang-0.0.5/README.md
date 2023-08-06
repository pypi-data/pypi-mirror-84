
# TkLang
##### *Allows one to parse .tk files*

### Instillation
    python -m pip install TkLang

### Usage
    import tklang as tkl
    content = tkl.load("your_tk_file.tk")

## Example(s)

### _TkLang Code_
    <src>
        <button id="LLJ" height="1" width="20">LLJ</button>
        <button id="LLJW">LLJW</button>
    </src>
> Note that the <src\> tag is arbitrary and may be replaced with what ever name you desire; however, it is required. Omitting the src tag will cause issues with parser
### _Python Code_
    import tklang as tkl
    import tkinter as tk
    t = tkl.load("test.tk")

    root = t['master']
    b1 = t['LLJ']

    b1.grid(row=0, column=0)

    root.mainloop()

> Note that the 'master' key in the 't' dictionary is auto-definned and the root/master for all widgets in that TKL File


### Features
    load(src: file_name) -> dict

#

### Changelog

#### 0.0.1 ~ ~ 11/5/2020 10:01
Initial Unstable Release

#### 0.0.2 ~ ~ 11/5/2020 10:03
Added README.md File

#### 0.0.3 ~ ~ 11/5/2020 10:30
Added README.md File

#### 0.0.4 ~ ~ 11/5/2020 10:43
Added setup.py & instillation_requires

filemodes -> file-modes

#### 0.0.5 ~ ~ 11/5/2019 10:47
Updated changelog

#### 1.0.0 ~ ~ [PLANNED]
Initial Stable Release