import csv
from bs4 import BeautifulSoup
import requests

def get_title(title_links):
    title = ''
    for t in title_links:
        if 'Senate Bill' in t.text or 'House Resolution' in t.text:
            title = t.text
    return title


def parse_link (soup, link):
    try: 
        divs = soup.find_all('div', class_='RollCalls-Vote-Senate')
        title_links = soup.find_all('div', class_='Column-OneFourth')[0].find_all('a')  
    except: 
        print ('cannot parse link {}, please make sure it is the correct page'.format(link))
    title = get_title(title_links)
    if not title:
        title = link.replace('\n', '')
    report = []
    for d in divs:
        entry = {}
        entry['vote'] = d.span.text.replace('\n', '')
        d.span.clear()
        entry['senator'] = d.text.strip('\t').strip('\n').strip('\r').strip(' ')
        report.append(entry)
    
    with open('output_files/{0}.csv'.format(title.replace(' ', '_').replace('/', '_')), 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow([title, ''])
        field_names = ['senator', 'vote']
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        for row in report:
            writer.writerow(row)

def read_links():
    with open('links.txt', 'r') as links_file:
        for line in links_file:
            r = requests.get(
                line
            )
            soup = BeautifulSoup(r.text, "html.parser")
            parse_link(soup, line)


if __name__ == "__main__":
    # execute only if run as a script
    read_links()
