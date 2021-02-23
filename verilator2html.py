#!/bin/env python3
import sys
import os
import argparse
import html
import re
import random

html_h = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
<meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Excel Bootstrap Table Filter</title>
  <link href="https://www.jqueryscript.net/css/jquerysctipttop.css" rel="stylesheet" type="text/css">
    <!-- Load jQuery -->
  <script src="https://code.jquery.com/jquery-1.12.4.min.js"></script>
  <!-- Load the plugin bundle. -->
  <script src="https://udif.github.io/verilator2html/dist/excel-bootstrap-table-filter-bundle.min.js"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" />
  <link rel="stylesheet" href="https://udif.github.io/verilator2html/dist/excel-bootstrap-table-filter-style.css" />
  <style>
  body {{ background-color:#fafafa;}}
  .container {{ margin:150px auto;}}
  </style>
</head>

<body>
<div class="jquery-script-clear"></div>
</div>
</div>
<div class="container">
  <div class="row">
    <div class="col-md-12">
      <table id="table" class="table table-bordered table-intel">
        <thead>
          <tr class="table-info">
            {}
          </tr>
        </thead>
        <tbody>
"""
html_t = """
        </tbody>
      </table>
    </div>
  </div>
</div>

<script>
  // Use the plugin once the DOM has been loaded.
  $(function () {
    // Apply the plugin 
    $('#table').excelTableFilter();
  });
</script>
</body>
</html>
"""
class log :
  def __init__(self, header, filter, split_func):
    self.header = header
    self.hdr_len = len(header)
    self.filter = filter
    self.split_func = split_func
    self.data = []

  def get_data(self, flog):
    for l in flog.readlines():
      if not re.search(self.filter, l):
        continue
      self.data.append((self.split_func(l) + [''] * self.hdr_len)[:self.hdr_len])

  def gen_data(self, rlines):
    l = len(self.data)
    for i in range(l, rlines):
      self.data.append([])
      for j in range(0, self.hdr_len):
        self.data[i].append(self.data[random.randrange(l)][j])

  def gen_html(self, fhtml):
    print(html_h.format("".join(["<th>"+i+"</th>" for i in self.header])), file=fhtml)
    for lp in self.data:
      lw = ''
      for w in lp:
        lw += '<td>{}</td>'.format(html.escape(w))
      print('<tr>{}</tr>'.format(lw), file=fhtml)
    print(html_t, file=fhtml)

conv_obj = {}
conv_obj['verilator'] = log(("Type", "File", "Line", "Col", "Message"), r'^%', lambda l: l.split(':'))
# spyglass is position based, in those position exactly (remove leading # below)
#ID       Rule                Alias               Severity    File                                                                                                                                         Line     Wt    Message
conv_obj['spyglass'] = log(('ID', 'Rule', 'Alias', 'Severity', 'File', 'Line', 'Wt', 'Message'), r'^\[', lambda l: [l[s:e].strip() for s,e in (lambda s: zip(s[:-1], s[1:]))([0, 9, 29, 49, 61, 202, 211, 217, 9999])])
conv_obj['gcc'] = log(("File", "Line", "Col", "Type", "Message"), r':.*:.*: (warning|error|note):', lambda l: [i.strip() for i in l.split(':')])

parser = argparse.ArgumentParser(description="Parse a logfile and creates a sortable/filterable/searchable HTML table.")
parser.add_argument('infile', metavar='<input file>', type=str, help="file to read, if '-', stdin is used")
parser.add_argument('outfile', metavar='<output file>', nargs='?', default='-', help="file to write, if '-' or no filename is given, stdout is used")
#parser.add_argument("-V", "--verbose", help="Be more verbose", action="store_true")
#parser.add_argument("-d", "--debug", help="debug flag", action='append', nargs="*")
parser.add_argument("-l", "--logtype", help="logfile type", choices=list(conv_obj.keys()))
parser.add_argument("-L", "--lines", type=int, help="limit output size to N lines")
parser.add_argument("-R", "--rlines", type=int, help="set output size to exactly N lines. randomize more lines from previous columns if needed (useful for debugging this program only))")
args = parser.parse_args()
 
def convert_any_log(flog, fhtml):
  c = conv_obj[args.logtype]
  c.get_data(flog)
  if args.lines:
    c.data = c.data[:args.lines]
  if args.rlines:
    if args.rlines <= len(c.data):
      c.data = c.data[:args.rlines]
    else:
      c.gen_data(args.rlines)
  c.gen_html(fhtml)

def convert_log(fhtml):
  if args.infile == "-":
    convert_any_log(sys.stdin, fhtml)
  else:
    with open(args.infile, "r") as flog:
      convert_any_log(flog, fhtml)

if args.outfile == "-":
  convert_log(sys.stdout)
else:
  with open(args.outfile, "w") as fhtml:
    convert_log(fhtml)
