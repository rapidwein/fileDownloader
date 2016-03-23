#!/usr/bin/python
#pyftpdlib FTP server

import logging
import pyftpdlib.authorizers
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.filesystems import UnixFilesystem

import os

def main():
  server_path = os.getcwd() + "/Server"
  try:
    os.stat(server_path)
  except:
    os.mkdir(server_path)
  try:
    authorizer = pyftpdlib.authorizers.UnixAuthorizer(rejected_users=["root"], require_valid_shell=True)
    authorizer.add_user("user","12345",server_path, perm='elradfmwM')
  except:
    authorizer = pyftpdlib.authorizers.DummyAuthorizer()
    authorizer.add_user("user","12345",server_path, perm='elradfmwM')
    authorizer.add_anonymous(server_path)
  
  handler = FTPHandler
  handler.authorizer = authorizer
  handler.abstracted_fs = UnixFilesystem
  handler.banner = "server ready"
  logging.basicConfig(filename='/var/log/fileDownloader.log', level=logging.DEBUG)
  address = ('localhost', 2121)
  server = FTPServer(address,handler)
  #server.max_cons = 256
  #server.max_cons_per_ip = 10
  server.serve_forever()

if __name__ == '__main__':
  main()
