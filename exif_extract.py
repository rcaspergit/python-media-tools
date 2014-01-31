#! /usr/bin/env python

import os
import fnmatch
import sys
import exifread
import hashlib
from optparse import OptionParser

parser = OptionParser()
usage = "usage: %prog [options] arg1 arg2"

parser.add_option("-i", "--indir", type="string",
                  help="input directory",
                  dest="indir", default=".")

options, arguments = parser.parse_args()

def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()

mimatches = []
for root, dirnames, filenames in os.walk(options.indir):
    for filename in fnmatch.filter(filenames,'*.JPG'):
        ifile = os.path.join(root, filename)
        f = open(ifile,'r')
        tags = exifread.process_file(f)
        pichash = hashfile(open(ifile, 'rb'), hashlib.sha256())
        print 'infile = %s, date created = %s, hash = %s' % (ifile,tags['EXIF DateTimeDigitized'],pichash[:16])

