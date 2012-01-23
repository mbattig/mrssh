#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       port_mgr.py
#       
#       Copyright 2012 Matt Battig <matt.battig@gmail.com>
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

import simplejson, subprocess, urllib, socket

BASE_DIR = "/home/matt/dev/mrssh"
CONFIG_FILE_NAME = "config"
SCP_CMD = "scp "


def main():

    HOME_IP = urllib.urlopen("http://automation.whatismyip.com/n09230945.asp").read()
    # read in the config parameters
    config_parameters = simplejson.loads(file(CONFIG_FILE_NAME).read())

    #print config_parameters["server_ip"]
    #print config_parameters["port_base"]
    #print "stored home IP=%s, Current IP=%s" % (config_parameters["home_ip"], HOME_IP)
    #rewrite config file..
    # TCP server example\

    # read in port allocation
    if config_parameters["ports"].__len__() == 0:
        print "nobody connected right now..."
    else:
        #print range(config_parameters["ports"].__len__())
        for entry in config_parameters["ports"]:
            print entry + ":"+ config_parameters["ports"][entry]

    # start up the port allocation server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", config_parameters["port_base"]))
    server_socket.listen(5)

    print "Server Waiting for client on port "+config_parameters["port_base"].__str__()

    while 1:
        client_socket, address = server_socket.accept()
        print "Request from ", address
        while 1:
            rx = simplejson.loads(client_socket.recv(512))
            if rx["cmd"] == "port_request":
                print "allocating port..."
                port = config_parameters["port_base"]
                while 1:
                    port=port+1
                    if config_parameters["ports"].has_key(port.__str__()):
                        #print port.__str__() + " already taken"
                        pass
                    else:
                        #print port.__str__() + " free!"
                        break
                data={}
                data["port"]=port
                # update config file with current port allocation...

                client_socket.send(simplejson.dumps(data))
            elif rx["cmd"] == "exit" :
                
                # commented for testing
                client_socket.close()
                print "recieved exit command disconnecting..."
            else:
                print "recieved "+rx["cmd"]

    return 0

if __name__ == '__main__':
    main()
