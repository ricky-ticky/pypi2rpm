import urllib2
import simplejson
import tarfile
import sys
import subprocess
import os

class pypackage:
	
	def __init__(self,name,path="/tmp"):
		"""you need to setup name of pypi package and path, if you don't whant to use defaults /tmp"""
		self.name = str(name)
		self.path = path
		self.json_request = self.get_json_req()

	def get_name(self):
		"""Print a module name"""
		print self.name

	def generate_url(self):
		"""Generate an URL to module JSON api"""
		self.json_url = 'http://pypi.python.org/pypi/'+self.name+'/json'
		return self.json_url
        
	def get_json_req(self):
		"""make json query to pypi"""
		self.json_link = self.generate_url()
		try:
			self.r = urllib2.urlopen(self.json_link).read()
			return self.r
		except urllib2.HTTPError, e:
			print "HTTP Error:",e.code , self.json_link
		except urllib2.URLError, e:
			print "URL Error:",e.reason , self.json_url
	
	def get_source_types(self):
		"""return a list of package archives, we have in pypi"""
		self.result = []
		for meta in simplejson.loads(self.json_request)["urls"]:
			if meta['packagetype'] == 'sdist':
				self.result.append(meta['filename'])
		return self.result

	def get_version(self):
		"""witch version of package in pypi we have"""
		return simplejson.loads(self.json_request)["info"]['version']
	
	def get_most_freq_archive_url(self):
		"""get the url of package archive. if there more than one archive, get tar archive"""
		self.result = []
		for meta in simplejson.loads(self.json_request)["urls"]:
			if len(meta) == 1 and meta['packagetype'] == 'sdist':
				self.result = meta['url']
			elif len(meta) > 1: 
				if meta['packagetype'] == 'sdist' and meta['filename'].find("tar") > -1:
					self.result = meta['url']
		return self.result

	def get_most_freq_archive_filename(self):
		self.result1 = []
		for meta in simplejson.loads(self.json_request)["urls"]:
			if len(meta) == 1 and meta['packagetype'] == 'sdist':
				self.result1 = meta['filaname']
			elif len(meta) > 1: 
				if meta['packagetype'] == 'sdist' and meta['filename'].find("tar") > -1:
					self.result1 = meta['filename']
		return self.result1

	def download(self):
		"""get archive from pypi"""
		self.filename = self.get_most_freq_archive_filename()
		self.url = self.get_most_freq_archive_url()
		self.filepath = self.path + "/" + self.filename
		try:
			self.f = urllib2.urlopen(self.url)
			self.pypackage_file = open(self.filepath, "w")
			self.pypackage_file.write(self.f.read())
			self.pypackage_file.close()
			return 1
		except urllib2.HTTPError, e:
			print "HTTP Error:",e.code , self.url
		except urllib2.URLError, e:
			print "URL Error:",e.reason , self.url
        
	def extract(self):
		"""extract archive into path. if there is no archive, download it"""
		try:
			self.tar = tarfile.open(self.filepath)
			self.archroot = tar.getnames()[0]
			self.tar.extractall(path=self.path)
		except :
			if self.download():
				self.tar = tarfile.open(self.filepath)
				self.archroot = self.tar.getnames()[0]
				self.tar.extractall(path=self.path)
			else:
				sys.exit(1)
		finally:
			self.tar.close()
			#os.rm(self.filepath)
	
	def make_specfile(self):
		"""generate a specfile for python package"""
		#TODO: get workdir from args if package already downloaded and extracted
		self.workdir=(self.path + "/" + self.archroot)
		os.chdir(self.workdir)
		subprocess.call(["python", "setup.py", "bdist_rpm", "--spec-only", "-d", "."])
		#TODO: change to bdist_altrpm
