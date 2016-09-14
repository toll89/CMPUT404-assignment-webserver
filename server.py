#  coding: utf-8 
import SocketServer
import os

# Copyright 2016 Jarrett Toll
# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Jarrett Toll
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        if self.data:       
            parsed = self.data.splitlines()
            statusline = parsed[0]
            statusSplit = statusline.split()
            method, url, proto = statusline.split()
        
            if method == 'GET':
                #Don't allow users to view previous directories. Only makes sense
                #for malicious code.
                if "../" in url:
                    self.request.sendall("HTTP/1.1 404 Not Found\n")
                    self.request.sendall("Content-Type: plain/text\n")
                    self.request.sendall("Connection: close\n")

                # Produce index
                elif url == "/":
                    self.request.sendall("HTTP/1.1 200 OK\n")
                    self.request.sendall("Content-Type: text/html\n")
                    self.request.sendall("Connection: close\n")
                    self.request.sendall("\n")
                    with open("www" + url + "index.html") as body:
                        self.request.sendall(body.read())
                
                elif os.path.isdir("www" + url):
                    # If a directory without a trailing "/" is requested,
                    # redirect to same url with "/" appended.
                    if url[-1:] != "/":
                        self.request.sendall("HTTP/1.1 301 Redirection\n")
                        self.request.sendall("Content-Type: text/html\n")
                        self.request.sendall("Location: http://127.0.0.1:8080" + url + "/\n")
                        self.request.sendall("Connection: close\n")

                    # Produce the index.html of the directory
                    else:
                        if os.path.isfile("www" + url + "index.html"):
                            self.request.sendall("HTTP/1.1 200 OK\n")
                            self.request.sendall("Content-Type: text/html\n")
                            self.request.sendall("\n")
                            with open("www" + url + "index.html") as body:
                                self.request.sendall(body.read())
                # If we're given a filename directly, produce that file if it exists
                elif os.path.isfile("www" + url):
                    self.request.sendall("HTTP/1.1 200 OK\n")
                    if url[-4:] == ".css":
                        self.request.sendall("Content-Type: text/css\n")
                    else:
                        self.request.sendall("Content-Type: text/html\n")
                    self.request.sendall("Connection: close\n")
                    self.request.sendall("\n")
                    with open("www" + url) as body:
                        self.request.sendall(body.read())
                # No resource at requested path/file, or forbidden.
                else:
                    self.request.sendall("HTTP/1.1 404 Not Found\n")
                    self.request.sendall("Content-Type: plain/text\n")
                    self.request.sendall("Connection: close\n")
    

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
