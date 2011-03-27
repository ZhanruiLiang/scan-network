#!/usr/bin/python2.7
#-*- coding: utf-8 -*-
import ping, getopt, sys, os, socket

version="1.0"
version_full="scan-network v."+version

def usage():
	'Shows program usage and version, lists all options'

	print version_full+" for GNU/Linux. A simple local network scanner."
	print "Usage: scan-network [long GNU option] [option] from [option] to"
	print ""
	print " --from range of ip adresses to start"
	print " --to range of ip adresses where to end"
	print " --ip mask of adresses to scan, for example 192.168.1, default 192.168.1"
	print " --help this screen"

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "ft:h", ["from=", "to=", "help", "delay=", "ip="]) # output=

	except getopt.GetoptError, err:
		print "Error: "+str(err)+", Try --help for usage\n\n"
		# usage()
		sys.exit(2)

	x=0
	y=0
	ip="192.168.1"
	ping_delay=1 # in seconds

	for o, a in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit()
		if o == "--from":
			try:
				x=float(a)
			except ValueError:
				print "--from argument is taking only numeric values"
				sys.exit(2);

		if o == "--to":
			try:
				y=float(a)
			except ValueError:
				print "--to argument is taking only numeric values"
				sys.exit(2);

		if o == "--delay":
			try:
				ping_delay=float(a)
			except ValueError:
				print "--delay argument is taking only numeric values"
				sys.exit(2);

		if o == "--ip":
			ip=a

	i=int(x)
	to=int(y)

	if (y-x) > 0:
		print "Adresses to scan: %1.0f" % (y-x)
		print "Ping "+ip+".{%1.0f to %1.0f}" % (x,y)
		print "Delay: "+str(ping_delay)

		to=to+1

		while i != to:
			try:
				respond_time = ping.do_one(ip+"."+str(i), float(ping_delay))

				if respond_time == None:
					print ip+"."+str(i)+" not responding, offline"
				else:
					print ip+"."+str(i)+" responds in "+str(respond_time)
			except socket.gaierror, e:
				print "Ping failed. (socket error: '%s')" % e[1]

			i=i+1
 
	else:
		print "There are no adresses to scan, please input valid arguments for help type `scan-network --help`"
	

if __name__ == "__main__":
    main()
