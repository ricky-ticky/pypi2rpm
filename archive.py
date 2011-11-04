import urllib2
import simplejson


class pypi_package:
	
	def __init__(self,name):
		self.name = str(name)
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
	
	def get_sources_types(self):
		"""witch type of packages we have in pypi"""
		pass
	
	def get_version(self):
		"""witch version of package in pypi we have"""
		pass
	
	def get_package(self, url, target):
	        """get the package into target path or into current directory"""
		pass

	def test_me(self):
		print self.pypi

	def get_url_and_version(self):
		"""JSON request to pypi and return direct url on tar file"""
		self.result = []
		for meta in simplejson.loads(self.json_request)["urls"]:
			if meta['packagetype'] == 'sdist':
				self.result.append(meta['url'])
				self.result.append(meta['filename'])
		self.result.append(simplejson.loads(self.json_request)["info"]['version'])
		return self.result

	def download_from_pypi(self,target):
		"""download archive from pypi"""
		self.target = target
		self.url = self.get_url_and_version()
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
