import os.path
from multiprocessing import Pool
import sys
import time
from itertools import groupby
from operator import itemgetter
import re
from pprint import pprint

pattern = re.compile('[\W_]+')

def map_words(inp):
    ''' Split each line into words, yield each word and '1' as the key-value pair '''
    for line in inp:
        for word in line.split(' '):
            yield pattern.sub('', word.strip()), 1

def reduce_word_counts(inp):
    ''' Reduce key-value pairs to sum() '''
    for key, group in groupby(inp, key=itemgetter(0)):
        yield key, sum([count for word, count in group])

def process_file(name):
    ''' Process one file'''
    with open(name, 'r') as inp:
        return name, sorted(reduce_word_counts(sorted(map_words(inp))), key=itemgetter(1))

def process_files_parallel(arg, dirname, names):
    ''' Process each file in parallel via Poll.map() '''
    pool=Pool()
    results=pool.map(process_file, [os.path.join(dirname,name) for name in names])
    pprint(results)

def process_files(arg, dirname, names):
    ''' Process each file in via map() '''
    results=map(process_file, [os.path.join(dirname,name) for name in names])
    pprint(results)

if __name__ == '__main__':
    ''' Benchmark parallel vs non-parallel approach '''
    
    start=time.time()
    os.path.walk('input/', process_files, None)
    print "process_files()", time.time()-start
    
    start=time.time()
    os.path.walk('input/', process_files_parallel, None)
    print "process_files_parallel()", time.time()-start
