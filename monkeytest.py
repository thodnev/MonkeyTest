'''
MonkeyTest -- test your hard drive write speed in Python
A simplistic script to show that such system programming
tasks are possible and convenient to be solved in Python

I haven't done any command-line arguments parsing, so
you should configure it using the constants below.

The file is being created, then written and deleted, so
the script doesn't waste your drive

(!) Be sure, that the file you point to is not smthng
    you need, cause it'll be overwritten during test

Runs on both Python3 and 2, despite that I prefer 3
Has been tested on 3.5 and 2.7 under ArchLinux
'''
from __future__ import division, print_function	# for compatability with py2

# change the constants below according to your needs
WRITE_MB = 128	        # total MBs written during test
WRITE_BLOCK_KB = 1024   # KBs in each write block
FILE = '/home/thd/test' # file must be at drive under test

from time import time
import os, sys

f = os.open(FILE, os.O_CREAT|os.O_WRONLY, 0o777) # low-level I/O
blocks = int(WRITE_MB*1024/WRITE_BLOCK_KB)
took = []
for i in range(blocks):
    # dirty trick to actually print progress on each iteration
    sys.stdout.write('\rWorking: {:.2f} %'.format((i+1)*100/blocks))
    sys.stdout.flush()
    buff = os.urandom(1024*WRITE_BLOCK_KB)
    start = time()
    os.write(f, buff)
    os.fsync(f)	# force write to disk
    t = time() - start
    took.append(t)

os.close(f)
os.remove(FILE)
result = ('\n\nWritten {} MB in {:.4f} s\nWrite speed is  {:.2f} MB/s'
          '\n  max: {max:.2f}, min:{min:.2f}\n'.format(
	     WRITE_MB, sum(took), WRITE_MB/sum(took),
             max = WRITE_BLOCK_KB/(1024*min(took)),
             min = WRITE_BLOCK_KB/(1024*max(took)) ))
print(result)
print(r'''Brought to you by coding monkeys. Eat bananas, drink coffee & enjoy!
                 _
               ,//)
               ) /
              / /
        _,^^,/ /
       (G,66<_/
       _/\_,_)    _
      / _    \  ,' )
     / /"\    \/  ,_\
  __(,/   >  e ) / (_\.oO
  \_ /   (   -,_/    \_/
    U     \_, _)
           (  /
            >/
           (.oO
''')
