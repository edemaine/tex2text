#!/usr/bin/python
import optparse, os, re, sys

def tex2text(x, options):
  if not hasattr(options, 'bibcite'): options.bibcite = {}
  x = re.sub(r'\n%.*', r'', x)
  x = re.sub(r'%.*', r'', x)
  x = re.sub(r'^\s+', r'', x, re.MULTILINE)
  x = re.sub(r'\n\n+', r'<P>', x)
  x = re.sub(r'\s+', r' ', x)
  x = re.sub(r'<P>', r'\n\n', x)
  #x = re.sub(r'\\cite\{([^{}]*)\}', r'[\1]', x)
  def biblookup(match):
    bib = [b.strip() for b in match.group(1).split(',')]
    bib = [options.bibcite.get(b, b) for b in bib]
    return '[%s]' % ', '.join(bib)
  x = re.sub(r'\\cite\s*\{([^{}]*)\}', biblookup, x)
  x = re.sub(r'\\(xxx|label)\s*\{([^{}]*)\}', '', x)
  x = re.sub(r'\\url\s*\{([^{}]*)\}', r'\1', x)
  x = re.sub(r'\\item\s*', '\n* ', x)  ## bullets are *s
  x = re.sub(r'\\(begin|end){(normal)?(itemize|enumerate|description|center)}\s*', '\n', x)
  x = re.sub(r'\\noindent\s*', '', x)
  x = re.sub(r'\\vspace\s*\*?\s*{[^{}]*}', '', x)
  x = re.sub(r'\\iffull\s*(.*?)\\fi', '', x, re.DOTALL)
  x = re.sub(r'\\footnote\s*{(.*?)}', r'[\1]', x, re.DOTALL)
  if options.markdown:
    x = re.sub(r'\\textbf\s*{([^{}]*)}', r'**\1**', x)
    x = re.sub(r'{\\bf\s+([^{}]*)}', r'**\1**', x)
    x = re.sub(r'\\(?:emph|textit)\s+{([^{}]*)}', r'*\1*', x)
    x = re.sub(r'\\(?:texttt|ttt)\s+{([^{}]*)}', r'`\1`', x)
    x = re.sub(r'---', r'&mdash;', x)
    x = re.sub(r'~', r'&nbsp;', x)
    x = re.sub(r'``', r'&ldquo;', x)
    x = re.sub(r"''", r'&rdquo;', x)
    x = re.sub(r'`', r'&lsquo;', x)
    x = re.sub(r"'", r'&rsquo;', x)
  else:
    def dash(match):
      if len(match.group(0)) == 3:
        return '--'
      else:
        return '-'
    x = re.sub(r'---?', dash, x)
  if options.math:
    x = re.sub(r'\$\$?|\\[]()[]', options.math, x)
  else:
    x = re.sub(r'(\\left|\\right)\s*', '', x)
    x = re.sub(r'\\infty\s*', r'infinity', x)
    x = re.sub(r'\s*\\times\s*', r' x ', x)
    x = re.sub(r'\\[cl]?dots\s*', r'...', x)
    x = re.sub(r'\s*\\leq?\s+', r' <= ', x)
    x = re.sub(r'\s*\\geq?\s+', r' >= ', x)
    x = re.sub(r'\s*\\neq?\s+', r' != ', x)
    x = re.sub(r'\$\\leq?\$', r'<=', x)
    x = re.sub(r'\$\\geq?\$', r'>=', x)
    x = re.sub(r'\$\\neq?\$', r'!=', x)
    x = re.sub(r'\\ell', r'l', x)
    x = re.sub(r'~|\\,', r' ', x)
    x = re.sub(r'\\tilde\s+([^{}])', r'\1~', x)
    x = re.sub(r'[$\\]', r'', x)
  x = re.sub(r"``|''", r'"', x)
  return x

def extract_abstract(x):
  match = re.search(r'\\begin\s*\{abstract\}\s*(.*?)\s*\\end\s*\{abstract\}', x, re.DOTALL)
  if not match:
    raise 'could not find abstract'
  return match.group(1)

def tex2text_file(filename, options):
  try:
    f = open(filename, 'r')
  except IOError:
    filename += '.tex'
    f = open(filename, 'r')
  x = f.read()
  f.close()
  if options.abstract:
    x = extract_abstract(x)
  bibcite = {}
  try:
    f = open(os.path.splitext(filename)[0] + '.aux', 'r')
    aux = f.read()
    f.close()
    for match in re.finditer(r'\\bibcite\{([^{}]*)\}\{([^{}]*)\}', aux):
      bibcite[match.group(1)] = match.group(2)
  except IOError:
    pass
  options.bibcite = bibcite
  return tex2text(x, options)

optparser = optparse.OptionParser(
  usage = '%prog [options] [filename]')
optparser.add_option('-a', '--abstract',
  action = 'store_true', dest = 'abstract', default = False,
  help = 'search for LaTeX abstract and just convert that')
optparser.add_option('-d', '--markdown',
  action = 'store_true', dest = 'markdown', default = False,
  help = 'enable Markdown formatting')
optparser.add_option('-m', '--math',
  action = 'store', dest = 'math', default = None, metavar = '$',
  help = 'preserve LaTeX math with specified delimeter e.g. $')
optparser.add_option('-g', '--gradescope',
  action = 'store_true', dest = 'gradescope', default = False,
  help = 'Gradescope mode: -d -m $$')

def main():
  options, filenames = optparser.parse_args()
  if options.gradescope:
    options.markdown = True
    options.math = '$$'
  if filenames:
    for filename in filenames:
      print('--- %s' % filename)
      print(tex2text_file(filename, options))
  else:
    tty = os.isatty(sys.stdin.fileno())
    if tty: print('[reading text from stdin; specify --help for help]')
    x = sys.stdin.read()
    if options.abstract:
      x = extract_abstract(x)
    if tty: print('----------------------')
    print(tex2text(x, options))

if __name__ == '__main__': main()
