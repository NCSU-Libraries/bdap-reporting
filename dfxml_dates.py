from bs4 import BeautifulSoup
import csv
from operator import attrgetter


with open("dfxml.xml", encoding="utf8") as fp:
    soup = BeautifulSoup(fp, features="xml")

fileobjects = soup.find_all('fileobject')
with open ('dfxml-dates.csv', 'w', newline='', encoding="utf8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["filename", "crtime","ctime", "mtime"])
    for fileobject in fileobjects:
        filename, crtime, ctime, mtime = attrgetter('filename', 'crtime', 'ctime', 'mtime')(fileobject)

        if all(item == None for item in (filename, crtime, ctime, mtime)):
            pass

        filenameText = getattr(filename, 'text', '')
        crtimeText = getattr(crtime, 'text', '')
        ctimeText = getattr(ctime, 'text', '')
        mtimeText = getattr(mtime, 'text', '')

        writer.writerow([filenameText, crtimeText, ctimeText, mtimeText])