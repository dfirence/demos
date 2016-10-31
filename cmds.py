#! /bin/bash/env python
# coding: utf-8


__version__ = '0.02'
__author__  = 'CARLOS DIAZ | FOUNDSTONE IR GROUP'
__license__ = 'GNU General Public License version 2'


import os
from copy import deepcopy
from Queue import Queue as Q
from collections import OrderedDict as OD



def load_commands():
	cmd = OD()
	out = [ 'body', 'xlsx', 'json', 'text' ]

	plugins = [
		['vol.py', 'amcache']				,
		['vol.py', 'apihooks']				,
 		['vol.py', 'atoms']				,
 		['vol.py', 'atomscan']				,
 		['vol.py', 'auditpol']				,
		['vol.py', 'bigpools']				,
 		['vol.py', 'bioskbd']				,
 		['vol.py', 'cachedump']				,
 		['vol.py', 'callbacks']				,
 		['vol.py', 'clipboard', '--verbose']		,
 		['vol.py', 'cmdscan', '--verbose']		,
 		['vol.py', 'connections']			,
 		['vol.py', 'connscan']				,
 		['vol.py', 'consoles', '--verbose']		,
 		['vol.py', 'dlllist']				,
 		['vol.py', 'driverirp']				,
 		['vol.py', 'drivermodule']			,
 		['vol.py', 'driverscan', '--verbose']		,
 		['vol.py', 'editbox']				,
 		['vol.py', 'envars']				,
 		['vol.py', 'eventhooks']			,
 		['vol.py', 'filescan', '--verbose']		,
 		['vol.py', 'gahti']				,
 		['vol.py', 'gditimers']				,
 		['vol.py', 'gdt']				,
 		['vol.py', 'getservicesids']			,
 		['vol.py', 'getsids']				,
 		['vol.py', 'handles', '--silent']		,
 		['vol.py', 'hashdump']				,
 		['vol.py', 'hivelist']				,
 		['vol.py', 'hivescan']				,
 		['vol.py', 'idt']				,
 		['vol.py', 'iehistory', '--verbose']		,
		['vol.py', 'imageinfo']				,
 		['vol.py', 'joblinks']				,
 		['vol.py', 'ldrmodules', '--verbose']		,
 		['vol.py', 'lsadump']				,
 		['vol.py', 'malfind']				,
 		['vol.py', 'malfind']				,
 		['vol.py', 'mbrparser']				,
 		['vol.py', 'messagehooks']			,
 		['vol.py', 'mftparser', '--verbose']		,
 		['vol.py', 'modscan']				,
 		['vol.py', 'modscan']				,
 		['vol.py', 'modules']				,
 		['vol.py', 'mutantscan']			,
 		['vol.py', 'netscan']				,
 		['vol.py', 'netscan']				,
 		['vol.py', 'notepad']				,
 		['vol.py', 'objtypescan']			,
 		['vol.py', 'pooltracker']			,
 		['vol.py', 'privs']				,
 		['vol.py', 'pslist', '-P']			,
 		['vol.py', 'psscan']				,
 		['vol.py', 'pstree']				,
 		['vol.py', 'psxview', '--apply-rules']		,
 		['vol.py', 'sessions']				,
 		['vol.py', 'shellbags']				,
 		['vol.py', 'shimcache', '--verbose']		,
 		['vol.py', 'shutdowntime']			,
 		['vol.py', 'sockets']				,
 		['vol.py', 'sockscan']				,
 		['vol.py', 'ssdt']				,
 		['vol.py', 'svcscan', '--verbose']		,
 		['vol.py', 'symlinkscan']			,
		['vol.py', 'timeliner']				,
 		['vol.py', 'thrdscan']				,
 		['vol.py', 'threads']				,
 		['vol.py', 'unloadedmodules', '--verbose']	,
 		['vol.py', 'userassist']			,
 		['vol.py', 'userhandles']
		]

        for output in out:
                cmd[ output ] = OD()
                for cmdline in plugins:
                        cmd[ output ][ cmdline[1] ] = cmdline
        return cmd


def load_dump_commands():
	bulkex  = os.path.join( os.getcwd(), 'BULKEX' )
	dumps   = os.path.join( os.getcwd(), 'DUMPS' )
	pids	= os.path.join( dumps,  'PIDS' )
	pcap	= os.path.join( bulkex, 'PCAP' )
	email	= os.path.join( bulkex, 'EMAIL')

	plugins = [
		['vol.py', 'procdump', '-D', pids]		,
		['bulk_extractor', '-E', 'net', '-o', pcap]	,
		['bulk_extractor', '-E', 'email', '-o', email]	,
		]

	return plugins


def set_output( cmdlist, mode=None ):
	outpath = os.path.join( os.getcwd(), 'PLUGINS' )
	outflag = '--output={} --output-file={}/{}.{}' 

	if mode == 'body':
		cmdline = set_body_output( cmdlist )
		outpath = os.path.join( os.getcwd(), 'TIMELINES' )
	elif mode == None or mode == 'text':
		cmdline = cmdlist['text']

	elif mode == 'xlsx':
		cmdline = cmdlist['xlsx']

	elif mode == 'json':
		cmdline = cmdlist['json']

	else:
		print '[+] Error: Requested Mode not supported'
		return

	for key, value in cmdline.iteritems():
		syntax = outflag.format(mode, outpath, key, mode).split()
		value.extend( syntax )

	return cmdline


def set_body_output( cmdlist ):
        holder  = OD()
        cmdline = cmdlist['body']
        plugins = [
                'mftparser'		,
                'usnparser'		,
                'shellbags'		,
                'timeliner'		,
                'chromecookies'		,
                'chromedownloadchains'	,
                'chromedownloads'	,
                'chromehistory'		,
                'chromevisits'		,
                'chromesearchterms'	,
                'firefoxcookies'	,
                'firefoxdownloads'	,
                'firefoxhistory'
                ]

        for key in cmdline:
                if key in plugins:
                        holder[ key ] = cmdline[ key ]
        cmdline = holder
        return cmdline


def load_tasks( mode=None ):
	if mode == 'body':
		tasks = set_output( load_commands(), mode='body' )

	elif mode == None or mode == 'text':
		tasks = set_output( load_commands(), mode='text' )

	elif mode == 'xlsx':
		tasks = set_output( load_commands(), mode='xlsx' )

	elif mode == 'json':
		tasks = set_output( load_commands(), mode='json' )

	return tasks


def set_plugins_body_queue( tasks ):
	queue = Q()
	for cmd in tasks.itervalues():
		queue.put( cmd )
	return queue


def set_plugins_queue( phases, tasks ):
        ph    = xrange( 0, len( phases.keys() ))
        queue = OD()
        for n in ph:
                queue[ str(n) ] = Q()
                for item in phases[ str(n) ]:
                        if item in tasks:
                                queue[ str(n) ].put( tasks[item] )
        return queue


def set_plugins_profile( platform ):
	OS = OD()
	OS['x86'] = OD()
	OS['x64'] = OD()
	OS['x86']['0'] = [
		'sockets'	,
 		'notepad'	,
 		'idt'		,
 		'pslist'	,
		'gdt'		,
		'sockscan'	,
		'connections'	,
		'connscan'	,
		'malfind'	,
		'modscan'
		]

	OS['x86']['1'] = [
		'unloadedmodules',
		'psxview'	,
		'sessions'	,
		'modules'	,
		'pooltracker'	,
		'hivescan'	,
		'hivelist'	,
		'privs'		,
		'dlllist'
		]

	OS['x86']['2'] = [
		'psscan'	,
		'driverscan'	,
 		'drivermodule'	,
 		'symlinkscan'	,
 		'ssdt'		,
 		'auditpol'	,
 		'mutantscan'	,
		'consoles'	,
		'cmdscan'	,
		'ldrmodules'
		]

	OS['x86']['3'] = [
 		'thrdscan'	,
 		'atomscan'	,
 		'mbrparser'	,
 		'messagehooks'	,
 		'netscan'	,
 		'shimcache'	,
 		'atoms'		,
		'editbox'
		]

	OS['x86']['4'] = [
		'envars'	,
		'shutdowntime'	,
		'cachedump'	,
		'hashdump'	,
 		'threads'	,
 		'eventhooks'	,
 		'userassist'	,
		'joblinks'
		]

	OS['x86']['5'] = [
 		'gditimers'	,
 		'gahti'		,
		'userhandles'	,
		'clipboard'	,
		'getsids'	,
		'filescan'
		]

	OS['x86']['6'] = [
		'kdbgscan'	,
		'callbacks'	,
		'handles'	,
		'objtypescan'
		]

	OS['x86']['7'] = [
		'vadinfo'	,
		'mftparser'	,
		'amcache'	,
		'shellbags'
		]

	OS['x86']['8'] = [
		'iehistory'	,
		'svcscan'	,
		'getservicesids',
		]

	OS['x64'] = deepcopy( OS['x86'] )

	return generate_exclusions( platform, OS )


def generate_exclusions( platform, OS ):
	excluded = load_profiles_exclusion()
	platform = platform['vol']

	if 'x86' in platform:
                if 'XPSP' in platform and platform in excluded['OS']['x86']:
			OS = set_plugins_exclusion( 'XPx86', OS['x86'] )

		elif '2003SP' in platform and platform in excluded['OS']['x86']:
			OS = set_plugins_exclusion( '2K3x86', OS['x86'] )

                elif platform in excluded['OS']['x86']:
                        OS = set_plugins_exclusion( 'x86',  OS['x86'] )
                else:
                        OS = OS['x86']

        elif 'x64' in platform:
                if platform in excluded['OS']['x64']:
                        OS = set_plugins_exclusion( 'x64', OS['x64'] )
                else:
                        OS = OS['x64']
	return OS


def set_plugins_exclusion( platform, plugins ):
	exclusion = load_plugins_exclusion()
	if platform == 'XPx86' or platform == '2K3x86':
		exclusion = exclusion['OS']['x86']['WinXPSP2x86']

	elif platform == 'x64':
		exclusion = exclusion['OS']['x64']['Win7SP1x64']

	elif platform == 'x86':
		exclusion = exclusion['OS']['x86']['Win7SP0x86']

	for excluded in exclusion:
		for k,v in plugins.iteritems():
			if excluded in v:
				v.remove( excluded )
	return plugins


def load_plugins_exclusion():
        exclusions = OD()
	exclusions['OS']	= OD()
	exclusions['OS']['x64'] = OD()
	exclusions['OS']['x86'] = OD()

        exclusions['OS']['x64']['Win7SP1x64']  = [ 'connections','connscan', 'sockscan', 'sockets', 'notepad', 'idt', 'gdt' ]
	exclusions['OS']['x86']['Win7SP0x86']  = [ 'connscan', 'sockscan', 'sockets', 'notepad', 'connections' ]
	exclusions['OS']['x86']['WinXPSP2x86'] = [ 'netscan','pooltracker' ]
        return exclusions


def load_profiles_exclusion():
	exclusions = OD()
	exclusions['OS']	= OD()
	exclusions['OS']['x64'] = OD()
	exclusions['OS']['x86'] = OD()

	exclusions['OS']['x64'] = [ 'Win7SP1x64', 'Win2008R2SP1x64_632B36E0', 'Win2008R2SP0x64', 'Win7SP1x64_632B36E0', 'Win2008R2SP1x64', 'Win7SP0x64','Win2012R2x64_54B5A1C6' ]
	exclusions['OS']['x86'] = [ 'Win7SP0x86', 'Win7SP1x86', 'Win7SP1x86_BBA98F40', 'WinXPSP2x86', 'WinXPSP3x86', 'VistaSP1x86', 'Win2008SP1x86',
				    'Win2003SP0x86', 'Win2003SP1x86', 'Win2003SP2x86','Win2008SP2x86', 'VistaSP2x86' ]
	return exclusions


def load_memory_profile( profile=None ):
	profiles = OD()

	profiles['win'] = [
			'VistaSP0x64',
 			'VistaSP1x64',
 			'VistaSP2x64',
 			'Win10x64',
 			'Win10x64_1AC738FB',
 			'Win10x64_DD08DD42',
 			'Win2003SP1x64',
 			'Win2003SP2x64',
 			'Win2008R2SP0x64',
 			'Win2008R2SP1x64',
 			'Win2008R2SP1x64_632B36E0',
 			'Win2008SP1x64',
 			'Win2008SP2x64',
 			'Win2012R2x64',
 			'Win2012R2x64_54B5A1C6',
 			'Win2012x64',
 			'Win7SP0x64',
 			'Win7SP1x64',
 			'Win7SP1x64_632B36E0',
 			'Win81U1x64',
 			'Win8SP0x64',
 			'Win8SP1x64',
 			'Win8SP1x64_54B5A1C6',
 			'WinXPSP1x64',
 			'WinXPSP2x64',
			'VistaSP0x86',
 			'VistaSP1x86',
 			'VistaSP2x86',
 			'Win10x86',
 			'Win10x86_44B89EEA',
 			'Win10x86_9619274A',
 			'Win2003SP0x86',
 			'Win2003SP1x86',
 			'Win2003SP2x86',
 			'Win2008SP1x86',
 			'Win2008SP2x86',
 			'Win7SP0x86',
 			'Win7SP1x86',
 			'Win7SP1x86_BBA98F40',
 			'Win81U1x86',
 			'Win8SP0x86',
 			'Win8SP1x86',
 			'WinXPSP2x86',
 			'WinXPSP3x86'
			]
	if profile == None:
		return '[+] Error on Input Type:  You must provide a memory profile'

	elif profile in profiles['win']:
		return profile

	elif profile not in profiles['win']:
		return '[+] Error on Memory Profile:  Profile does not match supported types'


def validate_memory_profile():
	import re
	regex = re.compile( r'PROFILE.*' )

	with open( 'volatilityrc', 'r' ) as fp:
		for line in fp.readlines():
			match = regex.search( line )
			if match:
				result = match.group().split('=')[1].replace(' ', '')

	profile = OD()
	profile['vol']  = load_memory_profile( profile=result )
	profile['arch'] = ''

	if 'x86' in profile['vol']:
		profile['arch'] = 'x86'

	elif 'x64' in profile['vol']:
		profile['arch'] = 'x64'

	return profile


def set_imageinfo( memoryFilePath ):
	path = r'{}'.format( memoryFilePath )
	path = os.path.abspath( path )
	try:
		if os.access( path, os.F_OK):
			if  os.access( path, os.R_OK ):
				cwd 	  = os.getcwd()
				imageinfo = [ 'vol.py', '-f', '{}'.format( path ), 'imageinfo',	 \
										'--output=text', \
										'--output-file={}'.format( os.path.join( cwd, 'imageinfo.text' ))]
				return imageinfo
			else:
				print '\n[!] Error File Permissions: No Read Access for {}\n'.format( path )
		else:
			print '\n[!] Error FilePath:  Does not exist {}\n'.format( path )

	except Exception as set_imageinfo_error:
		print '[!] EXCEPTION ERROR:  < set_imageinfo > function'
		print set_imageinfo_error
