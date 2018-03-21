# Tool to convert csv manifests into individual xml ready for ingest
# 
#
def findFileName(manifest):
	#finds the column which the filenames live in
	#Returns the column number if found
	#or returns -1 if not found
	foundFileName = 0
	for i, cell in enumerate(manifest[0]):
		if (cell=="File Name"):
			foundFileName = 1
			break
	if (foundFileName==1):
		return(i)
	else:
		return(-1)
	

def main():  

	#uses the csv reader module
	import csv
	
	#Open the manifest.csv file for reading		
	manifest = list(csv.reader(open("manifest.csv", "rt"), dialect="excel"))
	
	#Find out which column the FileNames are in
	fileColumn = findFileName(manifest)
	
	headerRow = 0
	
	if (fileColumn != -1):
		for i, row in enumerate(manifest):
			#work through each row of the manifest (skipping the headers), creating an xml manifest for each
			if (i != headerRow):
				
				#the filename for the xml needs to be the same as the object itself, but just with the extension changed
				jpgFilename = manifest[i][fileColumn]
				xmlFilename = jpgFilename[:-3]+"xml"
				
				#Extension change will only have worked if the original file had a three-letter extension, so just in case, throw up a warning if it didn't
				if (xmlFilename[-4:] != ".xml"):
					print("WARNING!  Check filename of [" + xmlFilename + "] Extension may be wrong, so will need to be fixed manually.")
				
				#create the xml file and give it the filename
				f = open(xmlFilename,"w+")
				
				#add xml header				
				f.write('<?xml version="1.0"?>\n<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:dnz="http://digitalnz.org/dummy" xmlns:schema="http://schema.org" xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#" xmlns:qsr="http://quakestudies.canterbury.ac.nz" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:dc="http://purl.org/dc/elements/1.1/">\n')
				
				
				for j, cell in enumerate(manifest[i]):
					#then within each row, work across the columns (skipping the filenames), and write the xml for that field 
					#also skip any empty cells (e.g. extra subject columns) or cells with null values
					if ((j != fileColumn) and (cell != "") and (cell != "<null>")):
						openTag = "  <" + manifest[headerRow][j] + ">"
						closeTag = "</" + manifest[headerRow][j] + ">\n"
						
						#Add field to the xml file
						f.write(openTag + cell + closeTag)
						
				#Add xml footer
				f.write("</rdf:RDF>")
				
				f.close()
	else:
		print("Couldn't find File Name column.  Check CSV.")
	
	
if __name__ == "__main__":
  main()
