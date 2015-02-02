#!/usr/bin/env python

import sys
import retrodev

if len(sys.argv) < 3:
    print 'Usage: {0} <source file> <output file>'.format(sys.argv[0])
    sys.exit(1)

output_state = retrodev.parse_source_file(sys.argv[1])

output_state['write'](output_state, sys.argv[2])
