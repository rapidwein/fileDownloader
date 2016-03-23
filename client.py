import sys
import os
import ftplib
from urlgrabber.grabber import URLGrabber
import glob
import multiprocessing

def chunk_get(process_no,dest_dir,file_url, file_size):
  file_name = file_url.split('/')[-1]
  url = "ftp://localhost:2121/" + file_url
  file_path = dest_dir + file_name+".part"+str(process_no)
  file_dir = file_url.rsplit('/',1)[0]
  try:
    if(os.path.isfile(file_path) == False):
      raise Exception('')
    else:
      g = URLGrabber(reget="simple")
      start_byte = os.stat(file_path).st_size
      if start_byte < process_no*file_size/5:
	if process_no == 4:
	  end_byte = file_size
	else:
	  end_byte = process_no*file_size/5
	file_temp_path = file_path + ".tmp"
	local_file = g.urlgrab(url,filename=file_temp_path,range=(start_byte,end_byte), retry=0)
	file(file_path,'ab').write(file(file_temp_path,'rb').read())
	os.remove(file_temp_path)
  except:
    g = URLGrabber(reget="simple")
    start_byte = (process_no)*file_size/5
    if process_no == 4:
      end_byte = file_size
    else:
      end_byte = start_byte + file_size/5
    local_file = g.urlgrab(url,filename=file_path,range=(start_byte,end_byte), retry=0)

def main():
  argc = len(sys.argv)
  argv = sys.argv
  fname = argv[1]
  fdir = argv[2]

  #create destination directory if it is not found
  try:
      os.stat(fdir)
  except:
      os.mkdir(fdir)

  #find file size in ftp server
  ftp = ftplib.FTP()
  ftp.connect("localhost",2121)
  ftp.login()
  ftp.voidcmd('TYPE I')
  fsize = ftp.size(fname)
  ftp.quit()
  file_name = fname.split('/')[-1]
  
  processes = []

  #spawn multiple processes to run in parallel
  for x in range(5):
    process = multiprocessing.Process(target=chunk_get, args=(x, fdir, fname,fsize))
    processes.append(process)
    process.start()
  #wait for all processes to end
  for p in processes:
    p.join()

  file_path = fdir+file_name

  #merge all part files
  if os.path.isfile(file_path) == False:
    for x in range(5):
      file_part_path = fdir+file_name+".part"+str(x)
      try:
	#raise exception is part file is missing
	if(os.path.isfile(file_part_path) == False):
	  raise Exception('')
	else:
	  if x==0:
	    file(file_path,'wb').write(file(file_part_path,'rb').read())
	  else:
	    file(file_path,'ab').write(file(file_part_path,'rb').read())
	  os.remove(file_part_path)
      except:
	print "part file missing"

if __name__ == "__main__":
  main()
