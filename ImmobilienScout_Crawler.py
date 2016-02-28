import urllib.request
from bs4 import BeautifulSoup
import re
import csv

url = 'http://www.immobilienscout24.de/Suche/S-T/P-1/Wohnung-Miete/Hamburg/Hamburg?pagerReporting=true'
data = []
page_i = 0
while True:
    page_i += 1
    url = 'http://www.immobilienscout24.de/Suche/S-T/P-{}/Wohnung-Miete/Hamburg/Hamburg?pagerReporting=true'.format(page_i)
    page_content = urllib.request.urlopen(url)
    soup = BeautifulSoup(page_content, "lxml")
    page_content.close()
    page_results = soup.findAll("div", { "class": "resultlist_criteria resultlist_gt_2_criteria"})
    for result in page_results:
        result_values = result.findAll("dd", {"class" : "value font-semibold"})
        data.append([float(re.sub('[^0-9,]','', val.string.strip().replace(",","."))) for val in result_values])
    print('{}. page'.format(page_i))
with open('immo_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['price', 'size', 'rooms'])
    for i in range(len(data)):
        writer.writerow(data[i])

