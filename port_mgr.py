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
PORTS_FILE_NAME = "ports"
SCP_CMD = "scp "


def main():

    HOME_IP = urllib.urlopen("http://automation.whatismyip.com/n09230945.asp").read()
    # read in the config parameters
    config_parameters = simplejson.loads(file(CONFIG_FILE_NAME).read())
    ports = simplejson.loads(file(PORTS_FILE_NAME).read())

    #print config_parameters["server_ip"]
    #print config_parameters["port_base"]
    #print "stored home IP=%s, Current IP=%s" % (config_parameters["home_ip"], HOME_IP)
    #rewrite config file..
    # TCP server example\

    # read in port allocation
    if ports.__len__() == 0:
        print "nobody connected right now..."
    else:
        #print range(config_parameters["ports"].__len__())
        for entry in ports:
            print entry + ":"+ ports[entry]

    # start up the port allocation server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #have to change IP address...
    server_socket.bind((config_parameters["home_ip"], config_parameters["port_base"]))
    server_socket.listen(5)

    print "Server Waiting for client on port "+config_parameters["port_base"].__str__()

    while 1:
        client_socket, address = server_socket.accept()
        print "Connection from ", address
        while 1:
            rx = client_socket.recv(512).rstrip()
            try:
                data={}
                json = simplejson.loads(rx)
                if json["cmd"] == "port_request" :
                    print "allocating port to "+json["id"]
                    #print ports.has_key(json["id"])
                    port = config_parameters["port_base"]
                    while 1:
                        port=port+1
                        if ports.has_key(port.__str__()):
                            #print port.__str__() + " already taken"
                            if ports[port.__str__()] == json["id"]:
                                print "already allocated port "+ port.__str__()
                                break
                            else:
                                pass
                        else:
                            #print port.__str__() + " free!"
                            break
                    data["status"]="ok"
                    data["value"]=port
                    # update config file with current port allocation...
                    client_socket.send(simplejson.dumps(data))
                    ports[port]=json["id"]
                    f = file(PORTS_FILE_NAME,"w")
                    f.write(simplejson.dumps(ports))
                    f.close()
                elif json["cmd"] == "disconnect" :	                
                    # commented for testing
                    print "recieved disconnect.  removing "+json["id"]+" from ports list."
                    ports.__delitem__(json["id"])
                    f = file(PORTS_FILE_NAME,"w")
                    f.write(simplejson.dumps(ports))
                    f.close()
                    data["status"]="ok"
                    client_socket.send(simplejson.dumps(data))
                    break
                elif json["cmd"] == "show_ports" :
                    print "show_ports to "+json["id"]
                    client_socket.send(simplejson.dumps(ports))
                elif json["cmd"] == "exit" :	                
                    # commented for testing
                    data["status"]="ok"
                    client_socket.send(simplejson.dumps(data))
                    print "recieved exit, disconnecting "+json["id"]
                    break
                
                else:
                    print json["id"]+" sent: "+json["cmd"]
            except ValueError:
                data["error"]="Couldn't decode JSON string."
                print "ERROR: "+data["error"]
                client_socket.send(simplejson.dumps(data)+"\n")
        client_socket.close()
    return 0

if __name__ == '__main__':
    main()
