#! /usr/bin/env python
# coding: utf-8

# Playbook Sample :  	Demo Simple Technique of Rapid Triage
# Objective	  :	Find Malware in under 10 minutes

# Steps:		(1)  Dump Processes with Volatility = vol.py moddump -D < DUMPS FOLDER >
#			(2)  Calculate MD5 Hash the dumped Driver Modules
#			(3)  Reference MD5 Hash with Virustotal public api for context of malware


import sys
sys.path.append( '..' )

import cmds
import engine
import codecs
from cmds import load_dump_commands
from triage import virustotal as vt
from triage import hasher
from render import tables


__author__ = 'THE FOUNDSTONE IR GROUP'
__license__ = 'Creative Commons'


def load_playbook():
	D = {}
	D['plugin'] = cmds.load_dump_commands()
	D['files']  = []
	D['hashes'] = []
	D['vtapi']  = vt.load_api()
	return D


def run_playbook( mode='md5' ):
	''' Mode calculates the hashtype you want to use when querying VT API '''

	playbook = load_playbook()
	print '{}{}'.format( '\n', 'Dumping Active DRIVER from MEMORY' )

	engine.run_plugin( playbook['plugin'][1] ) 	# Run MODDUMP Volatility Plugin
	engine.time.sleep(1)

	path = playbook['plugin'][1][3]			# DUMPS DIR Path in Case Folder
	files =  cmds.os.listdir( path )

	for file in files:
		playbook['files'].append( cmds.os.path.join( path, file ))

	for file in playbook['files']:
		playbook['hashes'].append( hasher.hash_file( file, mode=mode ))

	create_hashes_file( playbook['plugin'][0][3], playbook['hashes'] )

	print '{}{}'.format( '[+] VT Querying for Hashes', '\n' )

	scans = vt.get_bulk_filescans( playbook['vtapi'], playbook['hashes'] )

	print tables.parse_vt_filescans( scans )

	return


def create_hashes_file( filepath, hashes ):
        outpath = cmds.os.path.join( filepath, 'hashes.text' )

        with codecs.open( outpath, 'wb', encoding='utf-8' ) as fp:
                for hash in hashes:
                        fp.write( hash + '\n' )
        return
