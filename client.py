#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       client.py
#       
#       Copyright 2012 matt User <matt@ubuntu>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import socket, simplejson, subprocess, sys

def main(args):
    
    if args.__len__() < 2 :
	print "not enough arguments"
    else:
	#TCP client example
	tx={}
	p = subprocess.Popen(["uname", "-snrmpio"],stdout=subprocess.PIPE)
	tx["id"] = p.communicate()[0].rstrip()
	
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect(("192.168.220.211", 40000))
	tx["cmd"]=args[1]
	client_socket.send(simplejson.dumps(tx))
	while 1:
	    rx = client_socket.recv(512)
	    try:		
		data = simplejson.loads(rx)
		print data["status"]
		print data["value"]
		break
	    except ValueError:
		print rx
		break
	tx["cmd"]="exit"
	client_socket.send(simplejson.dumps(tx))
    return 0

if __name__ == '__main__':
    main(sys.argv)
