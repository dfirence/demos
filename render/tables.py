#! /usr/bin/env pyton
#code: utf-8

__version__ = '0.01'
__author__  = 'CARLOS DIAZ | FOUNDSTONE IR GROUP'
__license__ = 'GNU General Public License version 2'


from tabulate import tabulate


def parse_vt_filescans( apiresults ):
	VTRES   = []
	COLUMNS = [ 'Index', 'Source', 'ScanDate', 'Hash', 'Verdict' ]
	counter = 0

	for scan in apiresults:
		for item in scan:
			counter += 1
			if item['response_code'] == 0:
				VTRES.append([ counter, 'VirusTotal', '---', item['resource'].upper(), '---' ])

			elif item['response_code'] == 1:
				VTRES.append([ counter, 'VirusTotal', item['scan_date'], item['resource'].upper(), '{}/{}'.format( item['positives'], item['total'] ) ])

	TABLE = tabulate( VTRES, headers=COLUMNS )
	return TABLE
