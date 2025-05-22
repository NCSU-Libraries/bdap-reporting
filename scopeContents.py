from bs4 import BeautifulSoup
import sys

scriptName, path = sys.argv

with open(path, "r") as file:
    html_content = file.read()
soup = BeautifulSoup(html_content, "lxml")

h2 = soup.find("h2", string="File formats")
table = h2.find_next("table")
tbody = table.find("tbody")

counts = []
names = []
for row in tbody.find_all('tr'):
    row_data = []
    cells = row.find_all('td')
    cell1 = cells[0]
    cell2 = cells[2]
    counts.append(cell2.text)
    # If the td tag is empty, that means the file is unidentified or a symlink
    # Refer to Unidentified and Errors section of report
    names.append(cell1.text) if cell1.text else names.append("unknown")

pairs = []
for count, name in zip(counts,names):
    pairs.append((str(count) + " " + str(name)))

if len(pairs) == 1:
    print("Included are " + (pairs)[0] + " files.")

if len(pairs) == 2:
    print("Included are " + pairs[0] + ' and ' + pairs[1] + " files.")

if len(pairs) > 2 and len(pairs) <= 5:
    pairComma = []
    for pair in pairs[:-1]:
        pairComma.append(pair + ",")
    pairCommaStrings = " ".join(pairComma)
    print("Included are " + pairCommaStrings + ' and', pairs[-1] + " files.")

if len(pairs) > 5:
    pairComma = []
    for pair in pairs[:5]:
        pairComma.append(pair + ",")
    pairCommaStrings = " ".join(pairComma)
    pairAdditionalInt = [int(x) for x in counts[5:]]
    sumAdditional = str(sum(pairAdditionalInt))
    print("Included are " + pairCommaStrings + " and " + sumAdditional + " additional files of various formats.")