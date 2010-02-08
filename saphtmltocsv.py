#!/usr/bin/python

import sys
import re

def removeHtmlEntities( str ):
	entities = { "&#32;": " ", "&amp;": "&" }
	
	newStr = str
	for entity in entities:
		newStr = newStr.replace( entity, entities[entity] )
	
	return newStr

if len(sys.argv) < 3:
	sys.exit( "Please provide an input and output file name" )

# open the file and process the lines
inputfile = sys.argv[1]
outputfile = sys.argv[2]
rowOpen = False
values = []
output = open( outputfile, 'w' )
fileLines = 0
dataLines = 0

for line in open(inputfile,'r'):
	
	#does the line start with <tr>?
	
	#print line
	fileLines = fileLines+1
	print 'Processing line: ' + str(fileLines)
	
	if line.startswith( "<tr>" ):
		rowOpen = True
		print "opening a line!"	
	elif line.startswith( "</tr>" ):
		rowOpen = False
		print "closing a line, writing data to output file"
		dataLines = dataLines+1

		# turn the list into a nice comma-separated string
		towrite = ''		
		for value in values:
			towrite = towrite + '"' + removeHtmlEntities(value) + '",'

		print 'writing line: ' + towrite
		output.write( towrite + '\n' )			
		
		# reinitialize the list and line string
		values = []

	else:
		# we are processing a row, so the next few lines should be <td> tags with data
		if rowOpen:
			if line.startswith( "<td" ):
				print 'processing line with data'
				# extract the value with a regular expression
				matches = re.search( '<td.*>(.*)<\/td>', line )
				if matches:
					# there should only ever be one match
					print 'data matched: ' + matches.group(1)
					data = matches.group(1)
					values.append( data )
				else:
					# empty line, but we still need to leave the placeholder
					values.append( '' )
			else:
				print 'Ignoring line!'
	
	# a
	#print line	

print 'lines processed: ' + str(fileLines)
print 'rows processed: ' + str(dataLines)