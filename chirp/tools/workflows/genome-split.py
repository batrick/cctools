#!/usr/bin/env python2

# 1)  A genome of n pieces, that we will divide into c distinct jobs similar on a high level to the SAND tool of Chris/Mike

import contextlib
import mmap
import re
import sys

genome = sys.argv[1]
output = [open(path, 'w') for path in sys.argv[2:]]

#n = int(sys.argv[2])
#prefix = sys.argv[3]
#
#outputs = []
#for i in range(n):
#    outputs.append(open("%s.%08d" % (prefix, i), 'w'))

delim = re.compile(r'>[^>]+')

with open(genome, 'r') as f:
    with contextlib.closing(mmap.mmap(f.fileno(), 0, mmap.MAP_SHARED, mmap.PROT_READ)) as mapping:
        j = 0
        for match in delim.finditer(mapping):
            output[j].write(match.group(0))
            j = (j+1)%len(output)
