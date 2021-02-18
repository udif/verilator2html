#!/bin/env python3
import sys
import os

if len(sys.argv) != 3:
    print("""
Usage: {} <Verilator logfile> <HTML output file>
logfile may be replaced with '-' to take input from stdin instead
""".format(sys.argv[0]))
    sys.exit()

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
  body { background-color:#fafafa;}
  .container { margin:150px auto;}
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
            <th>Type</th>
            <th>File</th>
            <th>Line</th>
            <th>Col</th>
            <th>Message</th>
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
def convert_log(flog, fhtml):
  print(html_h, file=fhtml)
  for l in flog.readlines():
    if not l.startswith('%'):
      continue
    lw = ''
    for w in l.split(':', 4):
      lw += '<td>{}</td>'.format(w)
    print('<tr>{}</tr>'.format(lw), file=fhtml)
  print(html_t, file=fhtml)

with open(sys.argv[2], "w") as fhtml:
  if sys.argv[1] == "-":
    convert_log(sys.stdin, fhtml)
  else:
    with open(sys.argv[1], "r") as flog:
      convert_log(flog, fhtml)


