# RetroDev

My assembler for tinkering with older computer systems. Right now this assembler
only supports 6502 but likely other targets in the future. I'd like it to be
easy to maintain and have good support for target systems.

# Installation

* Clone down the git repo
```bash
git clone https://github.com/KennethWilke/RetroDev
```
* Install dependencies
```bash
pip install -r requirements.txt
```

# Usage

So far the usage is very basic, the assembler takes two arguments, an input source file and an output file.

```bash
python retrodev.py examples/appleii/charloop.asm charloop.dsk
```
