
# 1)  A genome of n pieces, that we will divide into c distinct jobs similar on a high level to the SAND tool of Chris/Mike
#
# 2)  We would like to determine which of m PacBio reads (database) correspond to genome pieces in subset c using a computational kernel.  For now, assume each comparison takes 0.00001 seconds and generates 20 bytes of input with probability 0.001.  So the expected runtime is n/c * m * 0.00001
#
# 3)  In theory we can divide the Pacbio database also into d distinct pieces.  The algorithm gets a bit wacky in the general case, but my new student Shenglong (co-advised by Danny Chen) is working on a conference paper where this is possible.  Let me know if it helps.
#
# As for the genome of n pieces, please use this (see link in the lower right corner):
# https://www.vectorbase.org/organisms/anopheles-gambiae/pimperena-s-form/agams1

import os
import shutil
import sys

from weaver.stack import WeaverNests
from weaver.util import Stash

CONTIGS = './Anopheles-gambiae-S-Pimperena_CONTIGS_AgamS1.fa'
PACBIOR = './Mosquito.FilteredPacBioSubreads.58Cells.130905.fastq'

N = 25
C = N
M = 1

def nstdir(path):
    return os.path.join(CurrentNest().work_dir, path)

shutil.copyfile(os.path.join(os.path.dirname(os.path.abspath(CurrentScript().path)), "genome-split.py"), nstdir("genome-split.py"))
shutil.copyfile(os.path.join(os.path.dirname(os.path.abspath(CurrentScript().path)), "bio-kernel.py"), nstdir("bio-kernel.py"))

os.link(CONTIGS, nstdir(os.path.basename(CONTIGS)))
CONTIGS = nstdir(os.path.basename(CONTIGS))
os.link(PACBIOR, nstdir(os.path.basename(PACBIOR)))
PACBIOR = nstdir(os.path.basename(PACBIOR))

splitter = ShellFunction('''
script="$1"
shift
python2 "$script" "$@"
''', cmd_format = "{EXE} {ARG}")
inputs = [nstdir('genome-split.py'), CONTIGS]
GENOME_SPLITS = [nstdir("genome.%08d" % i) for i in range(N)]
arguments = [nstdir('genome-split.py'), CONTIGS]
arguments.extend(GENOME_SPLITS)
splitter(inputs = inputs, arguments = arguments, outputs = GENOME_SPLITS)

kernel = ShellFunction('''
script="$1"
shift
out="$1"
shift
python2 "$script" "$@" > "$out"
''', cmd_format = "{EXE} {ARG}")
for c in range(C):
    genomes = GENOME_SPLITS[c::C]
    inputs = [nstdir('bio-kernel.py'), PACBIOR]
    inputs.extend(genomes)
    outputs = [nstdir(("%08d.out" % c))]
    arguments = [nstdir('bio-kernel.py'), outputs[0], PACBIOR]
    arguments.extend(genomes)
    kernel(inputs = inputs, outputs = outputs, arguments = arguments)

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
