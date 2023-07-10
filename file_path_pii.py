import re, os, csv

piilist = []
with open("/regex/file_path_regex.txt", "r") as piidoc:
    piilist = (piidoc.read().splitlines())

filepathlist = []
for dirpath, dirnames, filenames in os.walk("/logical"):
    for file in filenames:
        filepathlist.append(os.path.join(dirpath, file))

resultlist = []
for stringpattern in piilist:
    regex = re.compile(stringpattern)
    for f in filepathlist:
        result = re.search(regex, f)
        if not result == None:
            for x in zip([result.string], [result.group()]):
                resultlist.append(x)
            with open('/reports/file_path_pii.csv', mode='w') as result_file:
                writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row in resultlist:
                    writer.writerow(row)