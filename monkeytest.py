'''
MonkeyTest -- test your hard drive read-write speed in Python
A simplistic script to show that such system programming
tasks are possible and convenient to be solved in Python

I haven't done any command-line arguments parsing, so
you should configure it using the constants below.

The file is being created, then written with random data, randomly read
and deleted, so the script doesn't waste your drive

(!) Be sure, that the file you point to is not smthng
    you need, cause it'll be overwritten during test

Runs on both Python3 and 2, despite that I prefer 3
Has been tested on 3.5 and 2.7 under ArchLinux
'''
from __future__ import division, print_function	# for compatability with py2

# change the constants below according to your needs
WRITE_MB = 128	        # total MBs written during test
WRITE_BLOCK_KB = 1024   # KBs in each write block
READ_BLOCK_B   = 512    # bytes in each read block (high values may lead to
						# invalid results because of system I/O scheduler
FILE = r'/home/thd/test' # file must be at drive under test

import os, sys
from random import shuffle
try:                    # if Python >= 3.3 use new high-res counter
    from time import perf_counter as time
except ImportError:     # else select highest available resolution counter
    if sys.platform[:3] == 'win':
        from time import clock as time
    else:
        from time import time


def write_test(file, block_size, blocks_count, show_progress=True):
    '''
    Tests write speed by writing random blocks, at total quantity
    of blocks_count, each at size of block_size bytes to disk.
    Function returns a list of write times in sec of each block.
    '''
    f = os.open(file, os.O_CREAT|os.O_WRONLY, 0o777) # low-level I/O
    
    took = []
    for i in range(blocks_count):
        if show_progress:
            # dirty trick to actually print progress on each iteration
            sys.stdout.write('\rWriting: {:.2f} %'.format(
                             (i+1)*100/blocks_count)  )
            sys.stdout.flush()
        buff = os.urandom(block_size)
        start = time()
        os.write(f, buff)
        os.fsync(f)	# force write to disk
        t = time() - start
        took.append(t)
        
    os.close(f)
    return took

def read_test(file, block_size, blocks_count, show_progress=True):
    '''
    Performs read speed test by reading random offset blocks from
    file, at maximum of blocks_count, each at size of block_size
    bytes until the End Of File reached.
    Returns a list of read times in sec of each block.
    '''
    f = os.open(file, os.O_RDONLY, 0o777) # low-level I/O
    # generate random read positions
    offsets = list(range(0, blocks_count*block_size, block_size))
    shuffle(offsets)

    took = []
    for i, offset in enumerate(offsets):
        if show_progress and i % int(WRITE_BLOCK_KB*1024/READ_BLOCK_B) == 0:
            # read is faster than write, so try to equalize print period
            sys.stdout.write('\rReading: {:.2f} %'.format(
                             (i+1)*100/blocks_count)  )
            sys.stdout.flush()
        start = time()
        os.lseek(f, offset, os.SEEK_SET) # set position
        buff = os.read(f, block_size) # read from position
        t = time() - start
        if not buff: break # if EOF reached
        took.append(t)
        
    os.close(f)
    return took
    

wr_blocks = int(WRITE_MB*1024/WRITE_BLOCK_KB)
rd_blocks = int(WRITE_MB*1024*1024/READ_BLOCK_B)

write_results = write_test(FILE, 1024*WRITE_BLOCK_KB, wr_blocks)
read_results = read_test(FILE, READ_BLOCK_B, rd_blocks)
    
os.remove(FILE)

result = ('\n\nWritten {} MB in {:.4f} s\nWrite speed is  {:.2f} MB/s'
          '\n  max: {max:.2f}, min: {min:.2f}\n'.format(
	     WRITE_MB, sum(write_results), WRITE_MB/sum(write_results),
             max = WRITE_BLOCK_KB/(1024*min(write_results)),
             min = WRITE_BLOCK_KB/(1024*max(write_results)) ))
result += ('\nRead {} x {} B blocks in {:.4f} s\nRead speed is  {:.2f} MB/s'
           '\n  max: {max:.2f}, min: {min:.2f}\n'.format(
             len(read_results), READ_BLOCK_B,
             sum(read_results), WRITE_MB/sum(read_results),
             max = READ_BLOCK_B/(1024*1024*min(read_results)),
             min = READ_BLOCK_B/(1024*1024*max(read_results)) ))
print(result)
print(r'''Brought to you by coding monkeys.
Eat bananas, drink coffee & enjoy!
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
# ASCII-art: used part of text-image @ http://www.ascii-art.de/ascii/mno/monkey.txt
# it seems that its original author is Mic Barendsz (mic aka miK)
# text-image is a bit old (1999) so I couldn't find a way to communicate with author
# if You're reading this and You're an author -- feel free to write me
