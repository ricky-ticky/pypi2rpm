#!/usr/bin/python
import os
from distutils.command.bdist_altrpm import bdist_altrpm
import urllib2
import simplejson
import tarfile
import subprocess
import sys

module_name=str(sys.argv[1])
path=os.getcwd()+os.sep+module_name

def prepare():
	#todo: read module name from getopt
	try :
		os.mkdir(path)
		os.chdir(path)
		return 1
	except:
		return 0

def get_url_and_version(module_name):
	"""JSON request to pypi and return direct url on tar file"""
	result = []
	try:
		link = 'http://pypi.python.org/pypi/'+module_name+'/json'
		r = urllib2.urlopen(link).read()
		for meta in simplejson.loads(r)["urls"]:
			if meta['packagetype'] == 'sdist':
				result.append(meta['url'])
				result.append(meta['filename'])
		result.append(simplejson.loads(r)["info"]['version'])
		return result
	except urllib2.HTTPError, e:
		print "HTTP Error:",e.code , link
	except urllib2.URLError, e:
		print "URL Error:",e.reason , url

def download_module_from_pypi(url,target):
	"""download archive from pypi"""	
	try:
		f = urllib2.urlopen(url)
		local_file = open(target, "w")
		local_file.write(f.read())
		local_file.close()
		return 1
	except urllib2.HTTPError, e:
		print "HTTP Error:",e.code , url
	except urllib2.URLError, e:
		print "URL Error:",e.reason , url

def untar_file(filename):
	tar = tarfile.open(filename)
	tar.extractall(path=".")
	tar.close()

def generate_spec_file(module_path,version):
	os.chdir(module_path+os.sep+module_name+"-"+version)
	if subprocess.call(["python", "setup.py", "bdist_rpm", "--spec-only", "-d", "."]):
		return 1

if prepare():
	url,filename,version = get_url_and_version(module_name)
	#if download_module_from_pypi(url, filename):
	#	untar_file(filename)
	#if generate_spec_file(path,version):
	#	print "Specfile done"
