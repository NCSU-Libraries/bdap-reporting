import re, os, csv

piilist = []
with open("rlist.txt", "r") as piidoc:
    piilist = (piidoc.read().splitlines())
#print(piilist)

filepathlist = []
for dirpath, dirnames, filenames in os.walk("/logical"):
    for file in filenames:
        filepathlist.append(os.path.join(dirpath, file))
#print(filepathlist)

resultlist = []
for stringpattern in piilist:
    regex = re.compile(stringpattern)
    for f in filepathlist:
        result = re.findall(regex, f)
        if not result == []:
            # print(f,",".join(result))
            resulttuples = f,",".join(result)
            # print(resulttuples)
            resultlist.insert(1,resulttuples)
            print(resultlist)
            with open('file_path_pii.csv', mode='w') as result_file:
                writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row in resultlist:
                    writer.writerow(row)             
