import sys
import os
import ftplib

argc = len(sys.argv)
argv = sys.argv
fname = argv[1]
fdir = argv[2]

try:
    os.stat(fdir)
except:
    os.mkdir(fdir)
ftp = ftplib.FTP()
ftp.connect("localhost",2121)
ftp.login()
file_name = fname.split('/')[-1]

try:
  os.stat(fdir+"/"+file_name)
except:
  file_dir = fname.rsplit('/',1)[0]
  ftp.cwd("./" + file_dir)
  print ftp.nlst()
  ftp.retrbinary("RETR " + file_name, open(fdir + "/" + file_name, 'wb').write)
ftp.quit()
