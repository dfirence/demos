#! /usr/bin/env python
# coding: utf-8
# Creative Commons Credits:  www.programiz.com/python-programming/examples/hash-file


__version__ = '0.01'
__author__  = 'CARLOS DIAZ | FOUNDSTONE IR GROUP'
__license__ = 'GNU General Public License version 2'


import hashlib
import argparse as AG


def hash_file( filename, mode=None ):
	if mode == 'md5':
		hash = md5( filename )

	elif mode == 'sha1':
		hash = sha1( filename )

	elif mode == 'sha256':
		hash = sha256( filename )
	return  hash



def md5( filename ):
	md5 = hashlib.md5()
	with open( filename, 'rb' ) as fp:
		chunk = 0
		while chunk != b'':
			chunk = fp.read( 1024 )
			md5.update( chunk )
	return md5.hexdigest()



def sha1( filename ):
	sha1 = hashlib.sha1()
	with open( filename, 'rb' ) as fp:
		chunk = 0
		while chunk != b'':
			chunk = fp.read( 1024 )
			sha1.update( chunk )
	return sha1.hexdigest()



def sha256( filename ):
	sha256 = hashlib.sha256()
	with open( filename, 'rb' ) as fp:
		chunk = 0
		while chunk != b'':
			chunk = fp.read( 1024 )
			sha256.update( chunk )
	return sha256.hexdigest()


# Add the Recurse Directory Function on V.02 Here


def main():
	P = AG.ArgumentParser()
	P.add_argument( '-f', '--file', action='store', help=' File to be hashed' )
	P.add_argument( '-md5', action='store_true', help=' Create MD5 of file'   )
	P.add_argument( '-sha1', action='store_true', help=' Create SHA1 of file' )
	P.add_argument( '-sha256', action='store_true', help=' Create SHA256 of file' )

	args = P.parse_args()

	if args.file:
		if args.md5:
			print '{}:\t{}'.format( args.file, hash_file( args.file, mode='md5' ))

		elif args.sha1:
			print '{}:\t{}'.format( args.file, hash_file( args.file, mode='sha1' ))

		elif args.sha256:
			print '{}:\t{}'.format( args.file, hash_file( args.file, mode='sha256' ))

if __name__ == '__main__':
	main()
