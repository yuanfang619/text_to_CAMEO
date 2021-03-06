"""
text_to_CAMEO.py

This program takes data in the text-oriented format of the ICEWS .tab files downloaded from DataVerse study 28075 and converts 
this to a more conventional data format using the CAMEO codes. The conversion process is described in detail in the file 
text_to_CAMEO_documentation.pdf. 

Repository for code: https://github.com/philip-schrodt/text_to_CAMEO

To run: python text_to_CAMEO.py
Requires:
	CAMEO_codefile.txt
	countrynames.txt
	agentnames.txt
	filenames.txt

SYSTEM REQUIREMENTS
This program has been successfully run under Mac OS 10.10; it is standard Python 2.6 so it should also run in Unix or Windows. 

PROVENANCE:
Programmer: Philip A. Schrodt
			Parus Analytics
			Charlottesville, VA 22901 U.S.A.
			http://eventdata.parusanalytics.com

Copyright (c) 2014	Philip A. Schrodt.	All rights reserved.

The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Report bugs to: schrodt735@gmail.com

REVISION HISTORY:
18-June-14:	Initial version
30-March-15: Modified to work with DataVerse filenames

----------------------------------------------------------------------------------
"""

import os,sys

# ======== global initializations ========= #

countryfile = "countrynames.txt"  # translates country names to ISO-3166-alpha-3 and COW numeric codes
agentfile = "agentnames.txt"  # translates 'sectors' text to CAMEO agent codes
outfile_prefix = "reduced.ICEWS."

"""
srccountry = {}  # ancillary dictionaries used to do frequency counts
tarcountry = {}
events = {}
"""

countrynames = {}
Missing_names = {}
sectornames = {}
sectorcounts = {}
Missing_sectors = {}

datefield = 1
evtfield = 6
srcfield = 4
tarfield = 10
srcagtfield = 3
taragtfield = 9
goldscorefield = 7

# ordered list of CAMEO agent codes to extract for the agent field: see documentation
agentcodes = ['GOV','MIL','REB','OPP', 'PTY', 'COP','JUD','SPY','IGO','MED','EDU','BUS','CRM','CVL','---']

# ============ function definitions ================ #

def do_count(thedict, fieldindex):
	if field[fieldindex] in thedict:
		thedict[field[fieldindex]]  += 1
	else:
		thedict[field[fieldindex]]  = 1 

def do_sub_count(thedict, phrase):
	if phrase in thedict:
		thedict[phrase]  += 1
	else:
		thedict[phrase]  = 1 

def get_country_code(phrase):
	if phrase in countrynames:
		return countrynames[phrase]
	else:
#	    print 'Missing:',phrase
		do_sub_count(Missing_names, phrase)
		return '' 

def get_sector_code(phrase):
	if phrase in sectornames:
		return sectornames[phrase]
	else:
#		print 'Missing:',phrase
		do_sub_count(Missing_sectors, phrase)
		return '' 
		
def reduce_sectors():
#	print agentlist
	for code in agentcodes:
		if code in agentlist:
			return code
	return 'OTH'

def print_sorted_dict(thedict):
	print "\n",
	d_view = sorted( ((v,k) for k,v in thedict.iteritems()), reverse=True)
	for v,k in d_view:
		print v,k

# ============ main program =============== #

#try: 
#	fin = open(CAMEO_codefile,'r') 
#except IOError:
#	print "\aError: Could not find the event code file", CAMEO_codefile
#	sys.exit()	

#caseno = 1
#line = fin.readline()
#while len(line) > 0:
#	if line.startswith('LABEL'):
#		part = line[line.find(' ')+1:].partition(' ')
#		CAMEO_eventcodes[part[2][:-1]] = part[0][:-1]
#		print CAMEO_eventcodes[part[2][:-1]]
#		caseno += 1
#	if caseno > 32: break   # debugging exit 		
#	line = fin.readline()
	
#fin.close()
#for k,v in CAMEO_eventcodes.iteritems(): print v,k
#sys.exit()


try: 
	fin = open(countryfile,'r') 
except IOError:
	print "\aError: Could not find the country names file", countryfile
	sys.exit()	

line = fin.readline()
while len(line) > 0:
	part = line.split('\t')
	countrynames[part[0]] = (part[1],part[2][:-1])
	line = fin.readline()
	
fin.close()
#for k,v in countrynames.iteritems(): print v,k
#sys.exit()


try: 
	fin = open(agentfile,'r') 
except IOError:
	print "\aError: Could not find the agents file", agentfile
	sys.exit()	

line = fin.readline()
while len(line) > 0:
	part = line.split('\t')
	sectornames[part[0]] = part[1]
	line = fin.readline()
	
fin.close()
#for k,v in sectornames.iteritems(): print v,k
#sys.exit()


directory = os.getcwd()
filelist = []
for path, subdirs, files in os.walk(directory): # get list of ICEWS files based on .tab extension
    for name in files:
        if name.endswith((".tab")):
            filelist.append(os.path.join(path,name)) 

for filename in filelist:
	try: 
		fin = open(filename,'r')
                filename = filename.rsplit('/') # get filename from filepath 
                filename = filename[-1]
                print 'Reading',filename
	except IOError:
		print "\aError: Could not find the input file", infile
		sys.exit()	
	fout = open(outfile_prefix+filename[:12]+'txt','w')

	line = fin.readline()  # skip header
	line = fin.readline()
	caseno = 1
	while len(line) > 0:
                line = line.replace('\t\t','\tNULL\t') # replace missing field with 'NULL' 
                line = line.replace('\t\t','\tNULL\t') # in case there are two missing fields in a row
                line = line.replace('\t\t','\tNULL\t') # in case there are  missing fields in a row
		field = line.split('\t')
	#	for ka in range(len(field)): print ka, field[ka]
		outlist = [field[datefield]]	

	#	do_count(srccountry, srcfield)
	#	do_count(tarcountry, tarfield)
                if field[srcfield] in countrynames:
                    outlist.extend(get_country_code(field[srcfield]))
                else:
                    outlist.append('---')
                    outlist.append('000')
		subfields = field[srcagtfield].split(',')
		if subfields:
			agentlist = []
			for phrase in subfields:
				do_sub_count(sectorcounts, phrase)
				agentlist.append(get_sector_code(phrase))
		outlist.append(reduce_sectors())
                
                if field[tarfield] in countrynames:
		    outlist.extend(get_country_code(field[tarfield]))
                else:
                    outlist.append('---')
                    outlist.append('000')
		subfields = field[taragtfield].split(',')
		if subfields:
			agentlist = []
			for phrase in subfields:
				do_sub_count(sectorcounts, phrase)
				agentlist.append(get_sector_code(phrase))
		outlist.append(reduce_sectors())
		
	#	do_count(events, evtfield)  # debug: checks distribution of events
		camcode = field[evtfield].strip()
		outlist.append(camcode)
		outlist.append(field[goldscorefield])
		if camcode[0] == '2':  # determine the quad code
			quad = '4'
		elif camcode[0] == '0':
			if camcode[1] < '6':
				quad = '1'
			else:
				quad = '2'
		else:
			if camcode[1] < '5':
				quad = '3'
			else:
				quad = '4'
		outlist.append(quad)
	
	#	print outlist
		#if '---' not in outlist:
		fout.write('\t'.join(outlist)+'\n')
		caseno += 1
	#	if caseno > 16: sys.exit()   # debugging exit 		
		line = fin.readline()

	fin.close()
	fout.close()

	#filename = fdir.readline().strip()

"""
print_sorted_dict(events)   # code for printing frequencies 
print_sorted_dict(srccountry)
print_sorted_dict(tarcountry)
"""

"""
# code for printing sector frequencies 
print "\n",
d_view = sorted( ((v,k) for k,v in sectorcounts.iteritems()), reverse=True)
total = 0
for v,k in d_view:
	total += v
print "Total sector codes:",total
for v,k in d_view:
	print v,v*10000/total, k, 
	if k in sectornames:
		print sectornames[k]
	else: print '---'
	if v*10000/total < 1:  # stop printing when the proportion is less than 0.01%
		break
	

print "=== MISSING PHRASES ====",  # code of printing missing phrases
#print_sorted_dict(Missing_eventcodes)
#print_sorted_dict(Missing_names)
print_sorted_dict(Missing_sectors)
"""
#fdir.close()
print "Finished"

