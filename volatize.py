#! /usr/bin/env python
# coding: utf-8

import argparse as AG
import volcase
import engine

from playbook import vtdumps
from playbook import vtmods

__version__ = '0.02'
__author__  = 'CARLOS DIAZ | FOUNDSTONE IR GROUP'
__license__ = 'GNU General Public License version 2'

def display(memoryprofile):
	print '''
Volatility Foundation (c) - An Advanced Memory Forensics Framework
__________________________________________________________________

Program Name	:	Volatize.py
Program Author	:	@dfirence  | The Foundstone IR Group
Program Purpose :	Volatility Automation Tool via CLI
Program GitHub	:	http://bit.ly/2eSI72J
__________________________________________________________________

'''
	print '\t\t[!] Parsing Memory Profile: %s\n\n' % memoryprofile['vol']
	return


def parse_imageinfo(memoryFilePath):
	syntax = engine.cmds.set_imageinfo( memoryFilePath )
	return engine.run_imageinfo( syntax )


def parse_memory(mode='text'):
	tasks    = engine.cmds.load_tasks( mode=mode )
	memory   = engine.cmds.validate_memory_profile()
	platform = engine.cmds.set_plugins_profile( memory )
	queue    = engine.cmds.set_plugins_queue( platform, tasks )

	display(memory)
	for plugin in queue:
		engine.run_concurrently( queue[ plugin ] )
	return


def parse_memory_body_output():
	tasks  = engine.cmds.load_tasks( mode='body' )
	memory = engine.cmds.validate_memory_profile()
	queue  = engine.cmds.set_plugins_body_queue( tasks )

	display( memory )
	engine.run_concurrently( queue )
	return


def main():
	P = AG.ArgumentParser()

	Subparser = P.add_subparsers( dest='mode', help=' Execute volatize in different modes' )

	Playbook  = Subparser.add_parser( 'playbook', help=' Run Digital Playbooks as Scripts under Playbook Folder' )
	Playbook.add_argument( '-vtd', '--vtdumps', action='store_true', help=' Run VTDUMPS.py:  Dump PIDS, Hash PIDS, Query Hashes in VT' )
	Playbook.add_argument( '-vtm', '--vtmods', action='store_true', help=' Run VTMODS.py: Dump MODS, Hash MODS, Query Hashes in VT' )

	Parsemem  = Subparser.add_parser( 'parsemem', help=' Parse Memory Sample' )
	Parsemem.add_argument( '-a', '--auto'     , action='store_true', help=' Run in Auto Mode. Use with "--memory" flag' )
	Parsemem.add_argument( '-c', '--create'   , action='store_true', help=' Create VolatilityRC File' )
	Parsemem.add_argument( '-f', '--file'     , action='store'     , help=' Path for Imageinfo File' )
	Parsemem.add_argument( '-i', '--imageinfo', action='store_true', help=' Run Imageinfo Plugin on Memory Sample.  Use with "--memory" flag' )
	Parsemem.add_argument( '-m', '--memory'   , action='store'     , help=' Path for Memory Sample' )
	Parsemem.add_argument( '-o', '--output'   , action='store'     , help=' Save output from "--parse" flag:  Body file format' )
	Parsemem.add_argument( '-p', '--parse'    , action='store_true', help=' Run All Plugins on Memory Sample.  Used after creating the "setup"')
	Parsemem.add_argument( '-s', '--setup'    , action='store_true', help=' Setup the Analysis Environment ONLY')

	args = P.parse_args()

	if args.mode == 'playbook':
		if args.vtdumps:
			vtdumps.run_playbook()
		elif args.vtmods:
			vtmods.run_playbook()


        elif args.mode == 'parsemem':
                if args.auto and args.memory:
                        imageinfo = parse_imageinfo( args.memory )
                        volcase.create_case_directories()
                        volcase.create_case_subfolders()
                        volcase.create_config( volcase.find_markers( imageinfo ), memfile=args.memory )
                        volcase.show_folders()
                        parse_memory()

		elif args.create and args.file and args.memory:
			print '{}{}{}'.format( '\n' * 1, '\n[+] Created VolatilityRC Configfile', '\n[+] Created VOLCASE Directories\n' )
			volcase.create_directories()
			volcase.create_config( volcase.find_markers( imageinfo ), memfile=args.memory )

		elif args.create and args.imageinfo and args.memory:
			parse_imageinfo( args.memory )

		elif args.setup and args.memory:
			imageinfo = parse_imageinfo( args.memory )
			volcase.create_case_directories()
			volcase.create_case_subfolders()
			volcase.create_config( volcase.find_markers( imageinfo ), memfile=args.memory )
			volcase.show_folders()

		elif args.parse:
			if args.output == 'body':
				parse_memory_body_output()
			else:
				parse_memory()

if __name__ == '__main__':
	main()
