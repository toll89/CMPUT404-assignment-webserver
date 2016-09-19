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
        
        def sendResponse( url, code, code_text, ctype, conn, location):
            statusline = "HTTP/1.1 %s %s\r\n" % (code, code_text)
            self.request.sendall(statusline)
            if ctype:
                self.request.sendall("Content-Type: %s\r\n" % ctype)
            if location:
                self.request.sendall("Location: %s\r\n" % location)
            if conn:
                self.request.sendall("Connection: %s\r\n" % conn)
            self.request.sendall("\r\n")
            if url:
                with open(url) as body:
                    self.request.sendall(body.read())
        
        if self.data:       
            parsed = self.data.splitlines()
            statusline = parsed[0]
            statusSplit = statusline.split()
            method, url, proto = statusline.split()
            root = os.path.dirname(os.path.realpath(__file__)) + "/www"
            if method == 'GET':
                
                #If using symbolic links, set URL to the real path.
                if "../" in url:
                    url = os.path.realpath(url)

                # Produce index
                if url == "/":
                    sendResponse("www" + url + "index.html", 
                            "200", "OK", "text/html", "close", None)
                
                elif os.path.isdir(root + url):
                    # If a directory without a trailing "/" is requested,
                    # redirect to same url with "/" appended.
                    if url[-1:] != "/":
                        location = "http://127.0.0.1:8080" + url + "/"
                        sendResponse(None, "301", "Redirection", "text/html", 
                                "close", location)

                    # Produce the index.html of the directory
                    else:
                        if os.path.isfile(root + url + "index.html"):
                            sendResponse("www" + url + "index.html", "200",
                                    "OK", "text/html", "close", None)

                # If we're given a filename directly, produce that file if it exists
                elif os.path.isfile(root + url):
                    if url[-4:] == ".css":
                        sendResponse("www" + url, "200", "OK", "text/css",
                                "close", None)
                    else:
                        sendResponse("www" + url, "200", "OK", "text/html",
                                "close", None)

                # No resource at requested path/file, or forbidden.
                else:
                    sendResponse(None, "404", "Not Found", "plain/text",
                        "close", None)
    

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
