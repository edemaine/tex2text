# tex2text

**tex2text** is a simple converter from LaTeX to ASCII text, Unicode text,
or Markdown.
It's not intended to be perfect &mdash; the output likely requires some human
editing &mdash; but rather to save a lot of the manual work in conversion.
It also doesn't support much LaTeX &mdash;
feel free to add features via pull requests!
But it has nonetheless served me well for two purposes:

1. Converting a paper's abstract into text for uploading to a submission server
   (see `-a` option).
2. Converting an exam into Markdown for e.g. Gradescope's online assignments
   (see `-q` option).

## Usage

tex2text is a command-line tool.  You need Python (2 or 3) installed.
Then you can run it as follows:
```
python tex2text.py [options] filename.tex
```

Available options:

```
  -h, --help        show this help message and exit
  -a, --abstract    search for LaTeX abstract and just convert that
  -d, --markdown    enable Markdown formatting (implies -u)
  -u, --unicode     enable Unicode characters (beyond ASCII)
  -m $, --math=$    preserve LaTeX math with specified delimeter e.g. $
  -g, --gradescope  Gradescope mode, equivalent to -d -m $$
```
