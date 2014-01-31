#! /usr/bin/env python

import os
import fnmatch
import sys
from optparse import OptionParser

parser = OptionParser()
usage = "usage: %prog [options] arg1 arg2"

parser.add_option("-i", "--indir", type="string",
                  help="input directory",
                  dest="indir", default=".")

parser.add_option("-o", "--odir", type="string",
                  help="output dir",
                  dest="odir",default=".")

parser.add_option("-t", "--tdir", type="string",
                  help="temp dir",
                  dest="tdir",default=".")

options, arguments = parser.parse_args()


commandstring = '''cvlc -q  '%s' --sout "#transcode{vcodec=VP80,vb=2000,scale=0,acodec=vorb,ab=128,channels=2,samplerate=44100}:std{access=file,mux=webm,dst='%s'}" vlc://quit''' 


mvcmd = '''sudo mv "%s"  "%s"''' 

import pdb

## pdb.set_trace()

matches = []
for root, dirnames, filenames in os.walk(options.indir):
    for filename in fnmatch.filter(filenames,'*.MPG'):
        ifile = os.path.join(root, filename)
        newfilename = filename.split('.')[0] + '.mp4'
        tfile = options.tdir + '/' + newfilename
        print commandstring % (ifile,tfile)
        os.system(commandstring % (ifile,tfile))
        ofile = options.odir + '/' + newfilename
        print mvcmd % (tfile,ofile)
	os.system(mvcmd % (tfile,ofile))

