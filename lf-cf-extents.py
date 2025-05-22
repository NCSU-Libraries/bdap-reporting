# To run the script: `python3 lf-extents.py XML_FILE CONTAINER_PROFILES_FILE`

from bs4 import BeautifulSoup
import re, sys

# EAD3 XML should be exported from ArchivesSpace (lib.ncsu.edu served up XML doesn't have container tags?)
scriptName, xml, profiles = sys.argv

with open(xml, "r") as eadXML:
    xml_content = eadXML.read()
soup = BeautifulSoup(xml_content, "xml")

# Find all container tags
containers = soup.find_all('container')

# Convert the list of container profiles exported from ASpace into a dictionary
# Key/value pairs are container profile name (altrender tag) and dimension used for LF extent
d = {}
with open(profiles, 'r') as file:
    for line in file:
        noBrackets = (re.sub(r"\[.*?\]", " ", line))
        noBracketsFormatted = noBrackets.replace('"', '').replace("\n", "").replace("extent measured by ", "").split("   ")
        key, value = noBracketsFormatted[0], noBracketsFormatted[1]
        d[key] = value

containersWithIDs = []
containerIDs = []
uniqueContainerIDs =[]
linearInches = []
cubicInches = []
containersNoProfile = []

for container in containers:
    # Create list of container tags that have a containerid attribute, i.e. barcode
    # Child containers don't have containerid
    if container.get('containerid') is not None:
        containersWithIDs.append(container)
# Create list of containers with unique containerid attributes
for containerWithID in containersWithIDs:
    containerID = containerWithID.get('containerid')
    containerIDs.append(containerID)
    for containerID in containerIDs:      
        if containerID not in uniqueContainerIDs:
            uniqueContainerIDs.append(containerID)
        # Get container profile name containing d x h x w
        # Some containers don't have profile and we'll have to use localtype for conversion later
            if containerWithID.get('altrender') is not None:
                # If the name doesn't have d x h x w, this will break
                altrender = containerWithID.get('altrender').split(' x ')
                depth = re.search(r"(?<=\().*[^d$]", altrender[-3]).group()
                height = re.search(r"^(.*)[^h]", altrender[-2]).group()
                width = re.search(r"^(.*)[^w\)]", altrender[-1]).group()
                # Match altrender tag text with dictionary key
                for key, value in d.items():
                    if containerWithID.get('altrender') in key:
                        if value == "width":
                            linearInches.append(float(width))
                        if value == "height:":
                            linearInches.append(float(height))
                cubicInches.append(float(depth)*float(height)*float(width))
            # If there's no container profile name (altrender tag), then add container to new list
            else:
                containersNoProfile.append(containerWithID)

totalLinearInches = sum(linearInches)
totalCubicInches = sum(cubicInches)
print("This collection measures " + str(round(totalLinearInches/12, 2)) + " linear feet and " + str(round(totalCubicInches/1728, 2)) + " cubic feet.")

if len(containersNoProfile) > 0:
    print("\nThese containers don't have profiles:")
    for container in containersNoProfile:
        print(container.get("containerid"))