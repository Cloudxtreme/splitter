#!/usr/bin/env python


from libnmap.process import *
from libnmap.parser import *
import argparse
from time import sleep 

#Reads the file and the number of scanners from the cmd line
parser = argparse.ArgumentParser(description='Take a list of ip ranges as input. Conduct an nmap list scan.\n Then divide up the number of addresses by scanners needed', usage='splitter.py -f file -s number of scanners')
parser.add_argument('-f', help="Specify a file of ip ranges")
parser.add_argument('-s', help="Specify the number of scanners", type=int)


args = parser.parse_args()
fileOfRanges = args.f
numOfScanners = args.s
ipRanges = []
addresses = []

f = open(fileOfRanges, 'r')
r = open('split_ip_ranges.txt','a')

#load the ip ranges into a list
for line in f.readlines():
  ipRanges.append(line)

f.close()


#Run an nmap List scan for each range in the list. The format can be any format accepted by nmap. 
for ipRange in ipRanges:
  nmapWorker = NmapProcess(ipRange,options="-sL")
  nmapWorker.run_background()
  while nmapWorker.is_running():
    print "List scan of range " + ipRange + "is " + str(nmapWorker.progress) + " % " + "complete \n"
    sleep(1)

  results = NmapParser.parse(nmapWorker.stdout)
  for host in results.hosts:
    addresses.append(host.address)


scanner_group_size = (len(addresses)/numOfScanners)
remainder = (len(addresses)%numOfScanners)

#List of lists for each scanner needed
dividedIPs = [[]for scanners in range(numOfScanners)]
#Populate the dividedIPs list with ip's 
for groupID in range(numOfScanners):
  for ip in range(scanner_group_size): 
    dividedIPs[groupID].append(addresses.pop())
#Write the IP's out to a file. 
if remainder > 0:
  try:
    dividedIPs[-1].append(addresses.pop())
  except:
    pass

  for groupID in range(numOfScanners):
    r.write("\n" + "Scanner " + str(groupID+1) + "\n\n")
    for ip in range(scanner_group_size):
      r.write(dividedIPs[groupID][ip] + "\n")
  try:
    r.write(dividedIPs[-1][-1] + "\n")
  except:
    pass
else:
  for groupID in range(numOfScanners):
    r.write("\n" + "Scanner " + str(groupID+1) + "\n\n")
    for ip in range(scanner_group_size):
      r.write(dividedIPs[groupID][ip] + "\n")

r.close()
