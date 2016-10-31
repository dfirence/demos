#! /usr/bin/env python
# coding: utf-8


__version__ = '0.01'
__author__  = 'CAROS DIAZ | FOUNDSTONE IR GROUP'
__license__ = 'GNU General Public License version 2'


from collections import OrderedDict as OD
from tqdm import tqdm
import requests
import json
import time


def load_api():
	BASE = 'https://www.virustotal.com/vtapi/v2/'
	api  = OD()
	api['auth'] = OD()
	api['auth']['apikey'] = '' # <- YOUR VT PUBLIC API HERE!

	api['headers'] = OD()
	api['headers'] = { 'Accept-Encoding':'gzip, deflate', 'User-Agent':'PythonRequests' }

	api['urls'] = OD()
	api['urls']['retrieve'] = OD()
	api['urls']['retrieve']['reports'] = OD()
	api['urls']['retrieve']['reports']['domain'] = '{}{}'.format( BASE, 'domain/report' )
	api['urls']['retrieve']['reports']['file']   = '{}{}'.format( BASE, 'file/report' )
	api['urls']['retrieve']['reports']['url']    = '{}{}'.format( BASE, 'url/report' )
	api['urls']['retrieve']['reports']['ip']     = '{}{}'.format( BASE, 'ip-address/report' )

	api['urls']['submit'] = OD()
	api['urls']['submit']['comment']  = '{}{}'.format( BASE, 'comments/put' )
	api['urls']['submit']['rescan']   = '{}{}'.format( BASE, 'file/rescan' )
	api['urls']['submit']['scan']     = '{}{}'.format( BASE, 'file/scan' )
	api['urls']['submit']['url']      = '{}{}'.format( BASE, 'url/scan' )

	return api


def http_session():
        requests.packages.urllib3.disable_warnings()
        session = requests.Session()
        return session


def get_bulk_filescans( api, hashes ): # <- Prototype Function, needs memory optimization for scal with generators
	VTRES  = []
	bucket = []
	cycle  = 0
	batch  = 0
	for item in tqdm( hashes ):
		cycle += 1
		bucket.append( item )
		if cycle == 4:
			VTRES.append( get_batch_filescan( api, bucket ))
			bucket = []
			cycle  = 0
			batch  += 1
			if batch == 4:
				batch = 0
				time.sleep( 60 )
	return VTRES


def get_batch_filescan( api, hashes ):
	session   = http_session()
	vtparams  = { 'apikey':api['auth']['apikey'], 'resource':'{0},{1},{2},{3}'.format( hashes[0], hashes[1], hashes[2], hashes[3] ) }
	vtheaders = api['headers']

	try:
		http = session.get( api['urls']['retrieve']['reports']['file'], params=vtparams, headers=vtheaders )
		if http.status_code == 200:
			return json.loads( http.content )

		session.close()

	except Exception as http_error:
		print http_error


#def get_domainscan( api, domain ):
#	return


#def get_filesample( api, file ):
#	return


#def get_urlscan( api, url ):
#	return


#def get_ipscan( api, ip ):
#	return

#def make_comment( api, comment ):
#	return


#def scan_file( api, file ):
#	return


#def rescan_file( api, hash ):
#	return


#def scan_url( api, url ):
#	return
