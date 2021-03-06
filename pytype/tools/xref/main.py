#!/usr/bin/env python

"""Generate cross references from a project."""

from __future__ import print_function

import signal
import sys

from pytype import utils
from pytype.pytd.parse import node

# pytype: disable=import-error
# (b/119682838)
from pytype.tools.xref import debug
from pytype.tools.xref import indexer
from pytype.tools.xref import output
from pytype.tools.xref import parse_args
# pytype: enable=import-error


def main():
  try:
    args, kythe_args, options = parse_args.parse_args(sys.argv[1:])
  except utils.UsageError as e:
    print(str(e), file=sys.stderr)
    sys.exit(1)

  node.SetCheckPreconditions(options.check_preconditions)

  if options.timeout is not None:
    signal.alarm(options.timeout)

  try:
    ix = indexer.process_file(options, kythe_args=kythe_args)
  except indexer.PytypeError as e:
    print(e.args[0], file=sys.stderr)
    sys.exit(1)

  if args.debug:
    debug.show_index(ix)
  else:
    output.output_kythe_graph(ix)


if __name__ == "__main__":
  sys.exit(main())
