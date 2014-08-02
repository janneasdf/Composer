import urllib
import urllib2
import re

def main():
	output_folder = "scraped_tabs/"
	
	top100_url = "http://www.ultimate-guitar.com/top/top100_pro.htm"
	
	response = urllib2.urlopen(top100_url)
	content = response.read()
	
	pattern = """a href="http://tabs.ultimate-guitar.com/.*/.*/.*.htm"""
	print pattern
	
	tab_page_urls = re.findall(pattern, content)
	for url in tab_page_urls:
		print url
		response = urllib2.urlopen(url)
		content = response.read()		# read tab dl page
		dl_link_pattern = """<input type='hidden' name='id' value='225441' id="tab_id">"""
		
	
	ids = ["1494962", "1494961"]
	for id in ids:
		urllib.urlretrieve("http://tabs.ultimate-guitar.com/tabs/download?id=" + id, output_folder + id + ".gp5")
	
if __name__ == '__main__':
	main()