#! /usr/bin/env python
# coding: utf-8


__version__ = '0.2'
__author__  = 'CARLOS DIAZ | FOUNDSTONE IR GROUP'
__license__ = 'GNU General Public License version 2'


import argparse as AG
import codecs
import os
import re

from collections import OrderedDict as OD



def show_folders():
	ROOTDIRS = [
			( 'VADS', 'Dump VADS from PIDS' )		,
			( 'DUMPS', 'Dump PIDS, DLLS, etc.' )		,
			( 'BULKEX', 'Dump BulkExtractor Output' )	,
			( 'PLUGINS', 'Dump Volatility Plugins Output' )	,
			( 'STRINGS', 'Dump Strings Utility Output' )	,
			( 'TIMELINES', 'Dump Body Format Output' )	,
			( 'PROFILING', 'Dump Special Profiling Items' )	,
			( 'YARASCANS', 'Dump Yarascan Output' )
		]

	underline = '_' * 70
	headline  = '%10s %s' % ( '', 'Case Structure for Memory Analysis')

	print '{}{}{}{}{}'.format( '\n', underline, '\n', headline, '\n' )
	for e in sorted( ROOTDIRS ):
		print '%20s  :  %s' % ( e[0], e[1] )

	print '{}{}'.format( '\n', underline )
	return

def create_case_directories():
	D = OD()
	D['VADS']	= 'VADS'
	D['DUMPS']	= 'DUMPS'
	D['BULKEX']	= 'BULKEX'
	D['STRINGS']	= 'STRINGS'
	D['PLUGINS']	= 'PLUGINS'
	D['PROFILING']	= 'PROFILING'
	D['YARASCANS']	= 'YARASCANS'
	D['TIMELINES']	= 'TIMELINES'

	for i, folder in enumerate( D ):
		os.makedirs( folder )
	return

def create_case_subfolders():
	D = OD()
	D['DUMPS'] 	= ''
	D['BULKEX'] 	= ''
	D['TIMELINES'] 	= ''

	DUMPS     = [ 'PIDS', 'DLLS', 'EVTX', 'REGISTRY' ]
	BULKEX    = [ 'PCAP', 'URLS', 'EMAIL' ]
	TIMELINES = [ 'MASTER' ]

	PATH = {
		'DUMPS' : os.path.join( os.getcwd(), 'DUMPS') 	,
		'BULKEX' : os.path.join( os.getcwd(), 'BULKEX')	,
		'TIMELINES' : os.path.join(os.getcwd(), 'TIMELINES'),
		}

	D['DUMPS']  = [ os.path.join( PATH['DUMPS'], fp ) for fp in DUMPS ]
	D['BULKEX'] = [ os.path.join( PATH['BULKEX'], fp ) for fp in BULKEX ]
	D['TIMELINES'] = [ os.path.join( PATH['TIMELINES'], fp) for fp in TIMELINES ]

	for i, items in enumerate( D ):
		for subfolder in D[ items ]:
			os.makedirs( subfolder )
	return


def load_regex():
	RGX = [
	re.compile( r'Profile.*?:\s.*?,' ),
	re.compile( r'KDBG\s:\s.*?L' ),
	re.compile( r'DTB\s:\s.*?L' )
	]
	return RGX


def find_markers( imageinfoFile ):
	cwd = os.path.abspath( imageinfoFile )
	res = []
	RGX = load_regex()
	with codecs.open( cwd, 'r', encoding='utf-8' ) as fp:
		for line in fp.readlines():
			for n in range( 3 ):
				M = RGX[ n ].search( line )
				if M:
					res.append( M.group().replace('L','') )
	return res


def create_config( results, memfile=None ):
	if memfile:
		mf = os.path.join( os.getcwd(), memfile )
		cf = os.path.join( os.getcwd(), 'volatilityrc' )
		R  = [
		'[DEFAULT]',
		'PROFILE = {}'.format( results[0].split()[2].replace( ',' , '' )),
		'LOCATION = file://{}'.format( mf ),
		results[1].replace( ':' , ' = ' ),
		results[2].replace( ':' , ' = ' )
		]

		with codecs.open( cf, 'wb', encoding='utf-8' ) as fp:
			for setting in R:
				fp.write( setting + '\n' )
		return


def main():
	P = AG.ArgumentParser()

	P.add_argument( '-c', action='store_true', help=' Create Case Folders' )
	P.add_argument( '-f', action='store', help=' Path of Imageinfo Plugin Output' )
	P.add_argument( '-m', action='store', help=' Path of Memory Sample File' )
	args = P.parse_args()

	if args.c:
		create_case_directories()
		create_case_subfolders()
		show_folders()
	elif args.f and args.m:
		create_config( find_markers(args.f), memfile=args.m )

	return

if __name__ == '__main__':
	main()
