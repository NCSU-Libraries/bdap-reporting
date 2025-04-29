from bs4 import BeautifulSoup,Tag
import sys,os,glob,re

# This parses the components
def parse_component(componentTitle, collectionTitle):
    # c element may be either series or file
    did = componentTitle.parent
    component = did.parent
    
    # Search for c elements under the top level c
    if component.find_all('c'):
        # Create a list of c tags, i.e. file or subseries, under series
        # This assumes there are no sub-series extents 
        listFileRecords =[]
        for sibling in did.next_siblings:
            if isinstance(sibling, Tag):
                listFileRecords.append(sibling)

        # Create a list of all the quantity tags
        listQuantity =[]
        for c in listFileRecords:
            for quantity in c.find_all('quantity'):
                listQuantity.append(quantity)
        
        # For each quantity tag, if its next sibling (unittype tag) has bytes/files/websites, add to list
        listKB = []
        listMB = []
        listGB = []
        listFiles =[]
        listWebsites = []
        for quantity in listQuantity:
            strQuantity = quantity.text
            # This assumes there will always be a unittype somewhere after quantity
            unittype = quantity.find_next_sibling("unittype")
            if re.search('[kK]ilobytes?', unittype.text):
                listKB.append(eval(strQuantity))
            if re.search('[mM]egabytes?', unittype.text):
                listMB.append(eval(strQuantity))
            if re.search('[gG]igabytes?', unittype.text):
                listGB.append(eval(strQuantity))
            # Looks for the word at the beginning of start to avoid "electronic file transfer"    
            if re.match('[fF]iles?', unittype.text):
                listFiles.append(eval(strQuantity))
            if re.search('[wW]ebsites?', unittype.text):
                listWebsites.append(eval(strQuantity))

        # Get a sum total of the lists
        totalKB = sum(listKB)
        totalMB = sum(listMB)
        totalGB = sum(listGB)
        seriesTotalFiles = sum(listFiles)
        seriesTotalWeb = sum(listWebsites)

        # Add up the lists of bytes, files, and websites to get grand totals
        seriesTotalMB = totalKB/1024+totalMB+totalGB*1024
        seriesResult = '"' + collectionTitle + '/' + componentTitle.text + '"' + ',' + str(round(seriesTotalMB)) + ',' + str(seriesTotalFiles) + ',' + str(seriesTotalWeb)
    else:
        # Solo file record means it's not in a series
        listSoloFileRecords =[]
        for soloFile in component:
            if isinstance(soloFile, Tag):
                listSoloFileRecords.append(soloFile)

        # Create a list of all the quantity tags
        listQuantity =[]
        for c in listSoloFileRecords:
            for quantity in c.find_all('quantity'):
                listQuantity.append(quantity)
        
        # For each quantity tag, if its next sibling (unittype tag) has bytes/files/websites, add to list
        listKB = []
        listMB = []
        listGB = []
        listFiles =[]
        listWebsites = []
        for quantity in listQuantity:
            strQuantity = quantity.text
            # This assumes there will always be a unittype somewhere after quantity
            unittype = quantity.find_next_sibling("unittype")
            if re.search('[kK]ilobytes?', unittype.text):
                listKB.append(eval(strQuantity))
            if re.search('[mM]egabytes?', unittype.text):
                listMB.append(eval(strQuantity))
            if re.search('[gG]igabytes?', unittype.text):
                listGB.append(eval(strQuantity))
            # Looks for the word at the beginning of start to avoid "electronic file transfer"    
            if re.match('[fF]iles?', unittype.text):
                listFiles.append(eval(strQuantity))
            if re.search('[wW]ebsites?', unittype.text):
                listWebsites.append(eval(strQuantity))    

        # Get a sum total of the lists
        totalKB = sum(listKB)
        totalMB = sum(listMB)
        totalGB = sum(listGB)
        seriesTotalFiles = sum(listFiles)
        seriesTotalWeb = sum(listWebsites)
                
        # Add up the lists of bytes, files, and websites to get grand totals
        seriesTotalMB = totalKB/1024+totalMB+totalGB*1024
        seriesResult = '"' + collectionTitle + '/' + componentTitle.text + '"' + ',' + str(round(seriesTotalMB)) + ',' + str(seriesTotalFiles) + ',' + str(seriesTotalWeb)

    return [seriesTotalMB,seriesTotalFiles,seriesTotalWeb,seriesResult]
    
# This parses the collection
def parse_collection(soup):

    collectionTotalSizeMB = 0
    collectionTotalFiles = 0
    collectionTotalWeb = 0
    x = soup.select_one('archdesc > did > unittitle')
    if x is not None:
        collectionTitle = x.text
    else:
        print("The EAD XML file may be empty.")
        sys.exit()
    seriesResultList = []
    
    # Get component titles
    componentTitles = soup.select('dsc > c > did >  unittitle')
    for componentTitle in componentTitles:
        seriesTotalMB, seriesTotalFiles, seriesTotalWeb, seriesResult = parse_component(componentTitle,collectionTitle)
        collectionTotalSizeMB = collectionTotalSizeMB + seriesTotalMB
        collectionTotalFiles = collectionTotalFiles + seriesTotalFiles
        collectionTotalWeb = collectionTotalWeb + seriesTotalWeb
        seriesResultList.append(seriesResult)
    
    print('"' + collectionTitle + '",' + str(round(collectionTotalSizeMB)) + ',' + str(collectionTotalFiles) + ',' + str(collectionTotalWeb))
    for seriesResult in seriesResultList:
        print(seriesResult)
        
    return [collectionTotalSizeMB,collectionTotalFiles, collectionTotalWeb]

# Main script
scriptName, path = sys.argv
parseOneEAD = path.endswith('.xml')

print("Title,MB,Files,Websites")

if parseOneEAD:
    with open(path, 'r', encoding="utf-8") as f:
        file = f.read()

    soup = BeautifulSoup(file, 'xml')
    parse_collection(soup)
else:
    collectionsTotalSizeMB = 0
    collectionsTotalFiles = 0
    collectionsTotalWeb = 0
    numberCollections = 0
    fileNameList = glob.glob(os.path.join(path,'*.xml'))

    if len(fileNameList) == 0:
        print("There were no XML files in this directory.")
        sys.exit()

    # Calling each XML file from path to directory
    for filename in fileNameList:
        with open(filename, 'r', encoding="utf-8") as f:
            file = f.read()

        soup = BeautifulSoup(file, 'xml')
        grandTotalSizeMB, grandTotalFiles, grandTotalWeb = parse_collection(soup)
        collectionsTotalSizeMB = collectionsTotalSizeMB + grandTotalSizeMB
        collectionsTotalFiles = collectionsTotalFiles + grandTotalFiles
        collectionsTotalWeb = collectionsTotalWeb + grandTotalWeb
        numberCollections = numberCollections + 1
    print('"Total for ' + str(numberCollections) + ' collections",' + str(round(collectionsTotalSizeMB)) + ',' + str(collectionsTotalFiles) + ',' + str(collectionsTotalWeb))