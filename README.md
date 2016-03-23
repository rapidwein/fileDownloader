# fileDownloader

Simple FTP server and a file downloader from the server

##Setup

Set up using:
python setup.py install

##File Server
Run Server as:

python server.py

##Client

Run client as:

python client.py <file_to_download> <destination_dir>

The file is downloaded in parallel by splitting it into 5 chunks.
part files are created when download is stopped in between.
When restarted the part files are merged and final file is obtained
