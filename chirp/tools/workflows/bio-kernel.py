#!/usr/bin/env python2

from __future__ import print_function

import contextlib
import datetime
import mmap
import os
import random
import re
import sys
import time
usleep = lambda us: time.sleep(us/1000000.0)

readdb = sys.argv[1]
genomes = sys.argv[2:]

#1)  A genome of n pieces, that we will divide into c distinct jobs similar on a high level to the SAND tool of Chris/Mike
#
#2)  We would like to determine which of m PacBio reads (database) correspond
# to genome pieces in subset c using a computational kernel.  For now, assume
# each comparison takes 0.00001 seconds and generates 20 bytes of input with
# probability 0.001.  So the expected runtime is n/c * m * 0.00001

def contigs(genome):
    delim = re.compile(r'>[^>]+')
    with open(genome, 'r') as f:
        with contextlib.closing(mmap.mmap(f.fileno(), 0, mmap.MAP_SHARED, mmap.PROT_READ)) as mapping:
            for match in delim.finditer(mapping):
                yield match.group(0)

def chunks(infile, size = 2**20):
    count = 0
    last_print = 0
    last_size = 2**20
    while True:
        chunk = infile.read(size)
        if chunk:
            count += len(chunk)
            if (count-last_print) >= last_size:
                print("[%s] Processed %fGB." % (str(datetime.datetime.now()), count/2.**30), file = sys.stderr)
                last_print = count
                last_size *= 2
                if last_size > 2**30:
                    last_size = 2**30
            yield chunk
        else:
            break

def reads(readdb):
    delim = re.compile(r'@[^@]+(?=@|\Z)')
    with open(readdb, 'r') as f:
        # No large mmap available on CRC :(
        overlap = ""
        for chunk in chunks(f):
            chunk = overlap+chunk
            overlapi = 0
            for match in delim.finditer(chunk):
                yield match.group(0)
                overlapi = match.end()
            overlap = chunk[overlapi:]

def cmp(contig, read):
    #usleep(100)
    if random.randint(0, 1000-1) == 0:
        print("".join("{0:02x}".format(ord(c)) for c in os.urandom(10)))

c = []
for genome in genomes:
    for contig in contigs(genome):
        c.append(contig)
print("[%s] Using %d contigs with total length %d." % (str(datetime.datetime.now()), len(c), sum(len(s) for s in c)), file = sys.stderr)

for read in reads(readdb):
    for contig in c:
        cmp(contig, read)
