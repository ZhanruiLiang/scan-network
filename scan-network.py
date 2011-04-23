#!/usr/bin/python2.7

import sys,os,getopt,time
from threading import Thread
from IPy import IP

version="2.1"
version_full="scan-network v."+version
Action="range_scan" # Default action

x=100
y=254
ping_delay=0 # in seconds
ip="192.168.1.*"

' Copyleft by WebNuLL no any right reserved ;-)'

def usage():
        'Shows program usage and version, lists all options'

        print version_full+" for GNU/Linux. A simple local network scanner."
        print "Usage: scan-network [long GNU option] [option] from [option] to"
        print ""
        print " --from (-f) range of ip adresses to start, default is 1"
        print " --to (-t) range of ip adresses where to end, default is 254"
        print " --ip (-i) mask of adresses to scan, for example 192.168.1, default 192.168.1.*"
        print " --delay (-d) delay between pings, default is 0 second"
        print " --load-file (-l) scan ip adresses listed in file"
        print " --stdin (-s) grab list of ip adresses from stdin"
        print " --help this screen"

class PingThread(Thread):
    def __init__(self,Adress):
        Thread.__init__(self) # initialize thread

        # variables
        self.Adress = Adress
        self.Status = -1

    def run(self):
        put,get = os.popen4 ("ping "+self.Adress+" -c 1")
        ResponseTime = False

        for line in get.readlines():
            # find line where is timing given
            if line.find("icmp_") > -1:
                Exp = line.split('=')
                # if response is valid
                if len(Exp) == 4:
                    self.Status = Exp[3].replace(' ms\n', '')
def main():
        'Main function'
        global Action, x, y, ping_delay, ip

        try:
                opts, args = getopt.getopt(sys.argv[1:], "sl:d:i:f:t:h", ["from=", "to=", "help", "delay=", "ip=", "stdin", "load-file="]) # output=

        except getopt.GetoptError, err:
                print "Error: "+str(err)+", Try --help for usage\n\n"
                # usage()
                sys.exit(2)

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
                if o in ("-l", "--load-file"):
                        Action="file_scan"
                        FileToScan = a
                if o in ("-s", "--stdin"):
                        Action="stdin_scan"

        if len(opts) == 0:
            print "scan-network for GNU/Linux,  See --help for usage"
            sys.exit()

        if Action == "range_scan":
            doRangeScan()
        elif Action == "file_scan":
            if os.access(FileToScan, os.R_OK):
                FileHandler = open(FileToScan, "r")
                doListScan(FileHandler.read())
                FileHandler.close()
            else:
                print "Cannot open input file "+FileToScan

        elif Action=="stdin_scan":
            import select
            if select.select([sys.stdin,],[],[],0.0)[0]:
                Adresses = sys.stdin.read()
                doListScan(Adresses)
            else:
                print "STDIN is empty"

def doListScan(inputList):
    ListOfHosts = list()
    Lines = inputList.split("\n")

    for Line in Lines: # Line == IP Adress or list of ip adresses seperated by comma ","
        Multiples = Line.split(',')

        for IPAdress in Multiples:
            try:
                IP(IPAdress)
            except ValueError:
                continue
            else:
                Ping = PingThread(IPAdress)
                ListOfHosts.append(Ping)
                Ping.start()

    for Host in ListOfHosts:
       Host.join()
       if Host.Status == -1:
          print Host.Adress+" not responding, offline"
       else:
          print Host.Adress+" responds in "+str(Host.Status)+"ms"

       time.sleep(ping_delay)

def doRangeScan():
        global x, y, ping_delay, ip
        i=int(x)
        to=int(y)
        ListOfHosts = list()

        if (y-x) > 0:
            to=to+1
            while i != to:
                # use system ping and return results
                current_ip = ip.replace('*', str(i))
                # Single ping thread
                Ping = PingThread(current_ip)
                i=i+1
                # Append it to list of pinged hosts
                ListOfHosts.append(Ping)
                Ping.start()
                
            print "Adresses to scan: %1.0f" % (y-x)
            print "Ping "+ip.replace('*', "{"+str(int(x))+"-"+str(int(y))+"}")
            print "Delay: "+str(ping_delay)+"s"

            for Host in ListOfHosts:
                Host.join()
                if Host.Status == -1:
                   print Host.Adress+" not responding, offline"
                else:
                    print Host.Adress+" responds in "+str(Host.Status)+"ms"

                time.sleep(ping_delay)
        else:
            print "No ip range to scan, please select valid one with --from, --to and --ip"

    
if __name__ == "__main__":
    main()
