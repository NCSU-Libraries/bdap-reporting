# Born-Digital Reporting Scripts

This repository contains scripts used during born-digital processing at NC State University Libraries.

1. Clone the repository: `git clone https://github.com/ShellyYBlack/born-digital-reporting.git` Alternatively, you can also click the green <> Code button and download a ZIP of the files.
1. Change to the born-digital-reporting directory: `cd born-digital-reporting`
1. Build the image: `docker build -t bd-reports .`

## Calculate Extents (bd-extent-calculator.py)

This script calculates the total extent in MB, files, and websites from the quantity and unittype tags in EAD3 XML finding aids. It provides the totals for the entire collection and each series, as well as all the collections. 

1. To download all finding aids, run: `docker run -v $PWD/EAD-XML:/EAD-XML/ -it bd-reports bash -c "wget https://www.lib.ncsu.edu/findingaids/ead.txt ; cd /EAD-XML ; bash /src/download-EAD.sh"` 
To download a single finding aid, run: `docker run -v $PWD/EAD-XML:/EAD-XML/ -it bd-reports bash -c "cd /EAD-XML ; wget -O mc00467.xml https://www.lib.ncsu.edu/findingaids/mc00467/ead"`
1. Calculate extents by replacing path to directory and running: `python3 bd-reports.py /EAD-XML > /EAD-XML/output.csv`

### Tips

- If you want to run the script on a single EAD XML file instead of a directory, in step 4, replace /EAD-XML with your file path.
- If you only need to view the results in the terminal, in step 4, you can remove the `>` operator and what follows it.
- This script works on EAD3 records that use \<c\> elements, rather than \<cxx\>. It was also written for records that do not have the id or level attributes in \<c\> elements.

## Find PII in File Paths (file_path_pii.py)

Identify file paths that may contain PII based on a list of regular expressions. The script will search for the regex in file names or directory names. However, if a directory is empty, it will not be included.

1. Edit rlist.txt to contain strings or regular expressions you want to search for.
1. Run the script `docker run -v $PWD:/src/born-digital-reporting -it bd-reports bash -c "python3 file_path_pii.py"`
1. Open file_path_pii.csv to view the results. The first column shows the file paths and the second column shows the match.

## Extract Dates from DFXML (dfxml_dates.py)

This script creates a CSV with the filename, mtime, and ctime for each <fileobject> element in a [DFXML file](https://github.com/dfxml-working-group/dfxml_python).

1. Copy your DFXML to the /born-digital-reporting directory.
1. Run the script: `docker run -v $PWD:/src/born-digital-reporting -it bd-reports bash -c "python3 dfxml-dates.py"`
1. Open dfxml-dates.csv in Excel and sort the columns to find the earliest date.