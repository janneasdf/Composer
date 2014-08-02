import urllib
import urllib2
import re

def main():
  output_folder = "scraped_tabs/"
  
  top100_url = "http://www.ultimate-guitar.com/top/top100_pro.htm"
  
  response = urllib2.urlopen(top100_url)
  content = response.read()
  
  id_name_pairs = []
  pattern = """http://tabs.ultimate-guitar.com/.*/.*/.*.htm"""
  tab_page_urls = re.findall(pattern, content)
  for url in tab_page_urls:
    print url
    response = urllib2.urlopen(url)
    content = response.read()         # read tab dl page
    try:
      dl_link_pattern = r"""<input type='hidden' name='id' value='(?P<song_id>.*)' id="tab_id">"""
      id = re.search(dl_link_pattern, content).group('song_id')
      name_grab_pattern = r"http://tabs.ultimate-guitar.com/.*/.*/(?P<song_name>.*)_guitar_pro.htm"
      name = re.search(name_grab_pattern, url).group('song_name')
      #print id, name
      id_name_pairs.append((id, name))
    except:
      print "id / name grabbing failed, url:", url
  
  for id_name_pair in id_name_pairs:
    id, name = id_name_pair
    urllib.urlretrieve("http://tabs.ultimate-guitar.com/tabs/download?id=" + id, output_folder + name + ".gp5")
  
if __name__ == '__main__':
  main()