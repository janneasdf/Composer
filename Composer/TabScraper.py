import urllib
import urllib2

def main():
	output_folder = "scraped_tabs/"
	
	top100_url = "http://www.ultimate-guitar.com/top/top100_pro.htm"
	
	response = urllib2.urlopen(top100_url)
	content = response.read()
	
	
	ids = ["1494962", "1494961"]
	for id in ids:
		urllib.urlretrieve("http://tabs.ultimate-guitar.com/tabs/download?id=" + id, output_folder + id + ".gp5")
	
if __name__ == '__main__':
	main()