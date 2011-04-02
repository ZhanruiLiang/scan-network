#!/usr/bin/python2.7

import sys,os,getopt,time

version="2.0"
version_full="scan-network v."+version

' Copyleft by WebNuLL no any right reserved ;-)'

def usage():
        'Shows program usage and version, lists all options'

        print version_full+" for GNU/Linux. A simple local network scanner."
        print "Usage: scan-network [long GNU option] [option] from [option] to"
        print ""
        print " --from (-f) range of ip adresses to start, default is 1"
        print " --to (-t) range of ip adresses where to end, default is 254"
        print " --ip (-i) mask of adresses to scan, for example 192.168.1, default 192.168.1.*"
        print " --delay (-d) delay between pings, default is 1 second"
        print " --help this screen"

def main():
        'Main function'

        try:
                opts, args = getopt.getopt(sys.argv[1:], "d:i:f:t:h", ["from=", "to=", "help", "delay=", "ip="]) # output=

        except getopt.GetoptError, err:
                print "Error: "+str(err)+", Try --help for usage\n\n"
                # usage()
                sys.exit(2)

        x=100
        y=254
        ping_delay=0 # in seconds
        ip="192.168.1.*"

        for o, a in opts:
                if o in ("-h", "--help"):
                        usage()
                        sys.exit()
                if o in ("-f", "--from"):
                        try:
                                x=float(a)
                        except ValueError:
                                print "--from argument is taking only numeric values"
                                sys.exit(2);

                if o in ("-t", "--to"):
                        try:
                                y=float(a)
                        except ValueError:
                                print "--to argument is taking only numeric values"
                                sys.exit(2);

                if o in ("-d", "--delay"):
                        try:
                                ping_delay=float(a)
                        except ValueError:
                                print "--delay argument is taking only numeric values"
                                sys.exit(2);

                if o in ("-i", "--ip"):
                        ip=a

        if len(opts) == 0:
            print "scan-network for GNU/Linux,  See --help for usage"
            sys.exit()

        i=int(x)
        to=int(y)

        if (y-x) > 0:
                print "Adresses to scan: %1.0f" % (y-x)
                print "Ping "+ip.replace('*', "{"+str(x)+" to "+str(y)+"}")
                print "Delay: "+str(ping_delay)+"s"

                to=to+1

                while i != to:
                    # use system ping and return results
                    current_ip = ip.replace('*', str(i))
                    ResponseTime = do_one(current_ip, 100)


                    if ResponseTime == False:
                        print current_ip+" not responding, offline"
                    else:
                        print current_ip+" responds in "+str(ResponseTime)+"ms"
		    i=i+1

                    time.sleep(ping_delay)
        else:
                print "No ip range to scan, please select valid one with --from, --to and --ip"






def do_one (dest_addr, timeout):
    put,get = os.popen4 ("ping "+dest_addr+" -c 1")
    ResponseTime = False

    for line in get.readlines():
        # find line where is timing given
        if line.find("icmp_") > -1:
            Exp = line.split('=')
            # if response is valid
            if len(Exp) == 4:
                ResponseTime = Exp[3].replace(' ms\n', '')


    return ResponseTime
    
if __name__ == "__main__":
    main()
