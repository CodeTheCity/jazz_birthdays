# -*- coding:utf-8 -*-

import xml.etree.ElementTree as etree
import re
import datetime

input_file = "jazz_birthdays_manual_tidy2.xml"
#set the output file name for the 'good' data
#needs to be to a structured format - but dump to text for now
#clean_output = 'clean_out.csv'
clean_output = 'clean.xml'

#set the dirty output file where we'll dump the awkward lines
dirty_output = 'dirty_out.xml'

#open the clean output file
f2 = open(clean_output, 'w')
f2.write ("<musicians>"+ "\n")

#open the clean output file
f3 = open(dirty_output, 'w')
f3.write ('<?xml version="1.0" encoding="UTF-8"?>'+'\n')
f3.write ('<!DOCTYPE article PUBLIC "-//OASIS//DTD DocBook XML V4.1.2//EN" "http://www.oasis-open.org/docbook/xml/4.1.2/docbookx.dtd">'+'\n')
f3.write ('<article lang="">'+'\n')

#probably a better way of doing this - but set up a list of valide months to compare against (maybe move nearer to this code?)
month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August','September', 'October', 'November', 'December']
ref = ("january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december")

#initialise integer values for month and day
birth_day = 0
birth_month = 0
deceased = False
# First function: cleans out (invisible) ascii chars 132 and 160 from some lines which was causing problems
def remove_non_ascii_1(text): 
    return ''.join(i for i in text if ord(i)<128) #we need no characters below this normal pronting range

#Second Function - test_line() - split the line into words and return how many there are 
# (just used to spot 2-word lines which indicate a day / month line)

def test_line (text):
	words = text.split()
	num_words = len(words)
	#print "one " + str( words[0])
	#print "two " + str( words[1])
	return num_words

def muso_detail_split(text):

    # initialise so we can use it as a flag if fails below
    #worked = True 

  #split the line of text using commas as a delimiter
    muso_bits = text.split(',')

    try:  #try to convert the contents of the last item - to an integer. If it is 1928 or 1957 for example, it should work
        birth_year = int(muso_bits [-1])
        #Grab everything before the first comma - that seems to be a constant for the name location

        muso_name = muso_bits[0]

        #split that name into first, middle and surname to be returned individually - using the space as a delimiter
        # putting each into a list
        muso_name_list = muso_name.split(" ")
        muso_forname = muso_name_list[0] #choose the first item in the list - should be the forname
        muso_surname = muso_name_list[-1] # choose the last item as the last name
    
        #if there are more than 2 items in the list, assume that the second is a middle name
        if len (muso_name_list) > 2:
            muso_midname = muso_name_list[1]
        else:
            muso_midname = ""
        #chuck away the first item as we dealt with that as the names at lines 12 - 20 above
        
        #print muso_forname
        #print muso_surname

        muso_bits.remove(muso_bits[0])

        #chuck away the last item - it was the year of birth (line 24)
        muso_bits.remove(muso_bits[-1])

        #we should be left with the instruments
        instrm_list = list(muso_bits)
        #that's it all sorted - keep these remaining items as a list of instruments / roles which we'll return as a list
       ############
       # Needs to find and replace / in instrument list (e.g Campise entry)

        muso_obj = [muso_forname, muso_midname, muso_surname, birth_year, instrm_list]

    except ValueError:
    #  doesn't end with a single year we can't process it for now = write it out to the dirty file (and mark *** for future reference)
        f3.write("<para>" + str(birth_day) + " " + str(birth_month) + "</para>" +"\n")
        f3.write("<para>" + text + "</para>" +"\n")
        #f3.write(str(birth_day) + " " + str(birth_month) +"\n")
        #f3.write(text + "*** " +"\n")
        # return empty list
        muso_obj = []  
    
    return muso_obj

def create_date(d,m,y):

	date1 = datetime.date(y,m,d)
	return date1

def date_comp(dc):
    
    for month in ref:
        if dc in month:
            return ref.index(month) + 1

def find_death(line):
    line = line.strip()
    list1 = line.split(',')
    try:
        int_year = int(list1[1])
        #print(int_year)
    except:
        pass
    
    #print list[0]
    list1[0] = list1[0].replace(".", " ")   
    #print list[0] 
    d_m = list1[0].split(" ")
    d_m[0] = d_m[0].replace(".","").lower()

    int_month = date_comp(d_m[0])

    if int_month <10:
    	month = "0"+str(int_month)
    else:
    	month = str(int_month)
    
    int_day = d_m[-1]

    if int_day < 10:
    	day = "0"+str(int_day)
    else:
    	day = str(int_day)

    return str(int_year) + "-" + month + "-" + day

def write_record(intext):
	dob = create_date (birth_day, birth_month, muso_parts[3])
	f2.write ("<musician>"+ "\n")
	f2.write ("<fname>"+ muso_parts[0] + "</fname>" + "\n")
	if muso_parts[1] != "":
	    f2.write ("<mname>"+ muso_parts[1] + "</mname>" + "\n")
	f2.write ("<lname>"+ muso_parts[2] + "</lname>" + "\n")
	f2.write ("<dob>"+ str(dob) + "</dob>" + "\n")
	f2.write("<instruments>" + "\n")
	count = 0
	ins_len = len(muso_parts[4])
	for inst in muso_parts [4]:
	    f2.write ("<instrument>" + inst.strip() + "</instrument>" + "\n")
	f2.write("</instruments>"+"\n")
	f2.write("</musician>"+ "\n")

##################################
#    main code starts here       #
##################################

# grab the document as an xml object
tree = etree.parse(input_file)
root = tree.getroot()

for child in root:
	ignore_flag = False #used to identify elements with sub-elements <ulink> (ie Youtube links) as we don't want those
	dod =""
	for sub_child in child:
		if sub_child is not None: 
			# if there is a sub-elemnent (which can only be ulink) 
			# set the flag to true and do nothing more with that line
			ignore_flag = True

	if not ignore_flag: #so no sub elements - so we need to to more checks

		if child.text is not None: #not an empty <para/>
			line_text = child.text.encode('utf-8') #encode the text
			line_text = line_text.strip() # strip leading and trailing whitespace

			
			line_text = remove_non_ascii_1(line_text) # call the function to clean out ascii chars 132 and 160 from some lines
			nw = test_line (line_text)

			if nw ==2:
				#it can only be a date (as only they have two elements - day / month)
				words = line_text.split()
				tally = 0
				if words[1] in month_list:
					#take it that this is a date 

					# update the global vaiables with day and month * ordinal values*
					# We can use these to build up a datetime object for each musician's birth 
					# (taking the year from the muso's line below

					birth_day = int(words [0])
					birth_month = month_list.index(words[1]) +1
					
			else:
				#take it that it is a musician line (as we've excluded the day / month lines )
				# change this back to "(or"
				find_substr = "("
				if find_substr in line_text:
					f3.write("<para>" + str(birth_day) + " " + str(birth_month) + "</para>" +"\n")
					f3.write("<para>" + line_text + "</para>" +"\n")
				else:
					muso_parts = muso_detail_split (line_text)

					print muso_parts
					# returned as muso_forname, muso_midname, muso_surname, birth_year, instrm_list
					if len (muso_parts) > 0:
						
						write_record (muso_parts)



# f.close()
f2.write ("</musicians>"+ "\n")
f2.close()
f3.write('</article>')
f3.close()