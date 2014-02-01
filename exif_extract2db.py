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

parser.add_option("-o", "--odir", type="string",
                  help="output dir",
                  dest="odir",default=".")

parser.add_option("-u", "--user", type="string",
                  help="database user",
                  dest="user",default="user")

parser.add_option("-d", "--dbase", type="string",
                  help="database dir",
                  dest="dbase",default="yourdb")

parser.add_option("-p", "--passwd", type="string",
                  help="db password",
                  dest="dbpass",default="yourpassword")

parser.add_option("-s", "--server", type="string",
                  help="db host",
                  dest="dbhost",default="localhost")


options, arguments = parser.parse_args()

def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()


import MySQLdb

db = MySQLdb.connect(host=options.dbhost, # your host, usually localhost
                     user=options.user, # your username
                      passwd=options.dbpass, # your password
                      db=options.dbase) # name of the data base
cur = db.cursor() 

insert_cmd = '''INSERT INTO pic_tbl ( pic_path,pic_author,pic_hash,pic_date)
                       VALUES
                       ( "%s","%s","%s","%s"); '''
commit_counter = 0
mimatches = []
for root, dirnames, filenames in os.walk(options.indir):
    for filename in fnmatch.filter(filenames,'*.jpg') + fnmatch.filter(filenames,'*.JPG'):
        ifile = os.path.join(root, filename)
        print ifile
        f = open(ifile,'r')
        picdate = '0-0-0 00:00:00'
        try:
           tags = exifread.process_file(f)
           if 'EXIF DateTimeDigitized' in tags.keys():
               picdate = tags['EXIF DateTimeDigitized']
               tmp = '%s' % picdate
               split_tmp = tmp.split()
               gg = split_tmp[0].replace(':','-')
               picdate = gg + '\t ' + split_tmp[1]
        except:
              print '%s  had an error' % ifile
        pichash = hashfile(open(ifile, 'rb'), hashlib.sha256())
        the_cmd = insert_cmd % (root,filename,pichash,picdate)
        commit_counter = commit_counter +1
        cur.execute(the_cmd)
        if (commit_counter > 100) :
             db.commit()
             commit_counter = 0

db.commit()
cur.close()
db.close()

