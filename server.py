#!/usr/bin/python
#Arguments:
#"file_to_download" - file to download from ftp server
#"destination_dir" - destination directory in local fs

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os
def main():
  authorizer = DummyAuthorizer()
  authorizer.add_user("user","12345",".", perm='elradfmwM')
  authorizer.add_anonymous(os.getcwd())
  
  handler = FTPHandler
  handler.authorizer = authorizer
  handler.banner = "server ready"
  address = ('localhost', 2121)
  server = FTPServer(address,handler)
  server.max_cons = 256
  server.max_cons_per_ip = 5
  server.serve_forever()

if __name__ == '__main__':
  main()
