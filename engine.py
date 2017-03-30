#! /usr/bin/env python
# coding: utf-8


__version__ = '0.03'
__author__  = 'CARLOS DIAZ | FOUNDSTONE IR GROUP'
__license__ = 'GNU General Public License version 2'


import cmds
import time
import subprocess
import multiprocessing as mp

from os import devnull
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor


def run_imageinfo( syntax ):
	start = time.time()
	memorypath    = syntax[2]
	imageinfopath = syntax[5].split('=')[1]
	print '\n[-] Inspecting Memory Image Information of: {}'.format( memorypath )
	print '[-] Image Information Output to be created: {}'.format( imageinfopath )
	with open( devnull, 'w' ) as FNULL:
		subprocess.call( syntax, stdout=FNULL )
	end = time.time()
	print '[+] Ends Imageinfo: {:.2f}'.format( end - start )
	return imageinfopath


def run_plugin( plugin ):
	start = time.time()
	print '[-] Start {}'.format( plugin[1] )
	with open( devnull, 'w' ) as FNULL:
		subprocess.call( plugin, stdout=FNULL )

	#end = '[+] Ends   {0:<20}: {:.2f}s'.format( plugin[1], time.time() - start )
	end = '{:.2f}s'.format( time.time() - start )
	print '[+] Ends  {:25}--> {}'.format( plugin[1], end )
	return


def run_concurrently( queue ):
	start = time.time()
	cpus  = mp.cpu_count()
	qsize = queue.qsize()
	procs = []
	with ProcessPoolExecutor( cpus ) as executor:
		for n in xrange( qsize ):
			proc = mp.Process( target=run_plugin, args=( queue.get(),) )
			procs.append( proc )
			proc.start()
			time.sleep( 0.05 )
		for proc in procs:
			proc.join()
			time.sleep( 0.05 )
	#end = '[+] Ends  {:30} {}: {:.2f}s'.format( 'Concurrency of', qsize, 'tasks',time.time() - start)
	t = '{:.2f}s'.format( time.time() - start )
	end = '[+] Ends  Concurrent {} Tasks'.format( qsize )

	print '{:35}--> {}{}{}{}'.format(end, t, '\n', '-' * 48, '\n' )
	#print '{}{}{}{}'.format( end, '\n', '-' * 48, '\n' )
	return
