import requests
from bs4 import BeautifulSoup
import csv

gages = ["323", "403", "312", "310", "322"]

for gage in gages:    
    url = "http://www.ladpw.org/wrd/precip/alert_rain/season_raindata.cfm?id=" + gage
    response = requests.get(url)
    code = response.content

    soup = BeautifulSoup(code, "lxml")
    table = soup.find('table', attrs={"border" : "1"})

    headers = [header.text for header in table.find_all('th')]
    headers = [w.replace('/', '') for w in headers]
    headers = [w.replace(' (in)', '') for w in headers]
    headers = [w.replace(' ', '') for w in headers]
    headers.append("id")
    list_of_rows = []
    for row in table.findAll('tr', attrs={'valign': None}):
        list_of_cells = []
        for cell in row.findAll('td'):
            text = cell.text.encode('latin-1')
            text = text.replace(chr(160), " ")
            list_of_cells.append(text.strip())
        list_of_cells.append(url[-3:])
        list_of_rows.append(list_of_cells)

    csvname = "data/rainfall_" + gage + ".csv"
    outfile = open(csvname, "w")
    writer = csv.writer(outfile, lineterminator ="\n")
    writer.writerow(headers)
    writer.writerows(list_of_rows)
print "done"
