splitter
========

Quick and dirty python script that will take IP ranges from a file and split them according to how many scanners you are going to use. 



Usage: ./splitter.py -f [file] -s [number of scanners]

The output file will be "split_ip_ranges.txt"

* Its not multi-threaded, so expect longer completion time with relatively large lists. 
