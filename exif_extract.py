#! /usr/bin/env python

import os
import fnmatch
import sys
import exifread
from optparse import OptionParser

parser = OptionParser()
usage = "usage: %prog [options] arg1 arg2"

parser.add_option("-i", "--indir", type="string",
                  help="input directory",
                  dest="indir", default=".")

parser.add_option("-o", "--odir", type="string",
                  help="output dir",
                  dest="odir",default=".")

options, arguments = parser.parse_args()


mimatches = []
for root, dirnames, filenames in os.walk(options.indir):
    for filename in fnmatch.filter(filenames,'*.JPG'):
        ifile = os.path.join(root, filename)
        f = open(ifile,'r')
        tags = exifread.process_file(f)
        print 'infile = %s, date created = %s' % (ifile,tags['EXIF DateTimeDigitized'])
