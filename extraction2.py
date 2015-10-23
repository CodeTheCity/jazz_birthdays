# -*- coding:utf-8 -*-

import xml.etree.ElementTree as etree
import re

#set the output file name for the 'good' data
#needs to be to a structured format - but dump to text for now
#clean_output = 'clean_out.csv'
clean_output = 'clean.txt'

#set the dirty output file where we'll dump the awkward lines
dirty_output = 'dirty_out.txt'

#open the clean output file
f2 = open(clean_output, 'w')

#open the clean output file
f3 = open(dirty_output, 'w')

#probably a better way of doing this - but set up a list of valide months to compare against (maybe move nearer to this code?)
month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August','September', 'October', 'November', 'December']

#initialise integer values for month and day
birth_day = 0
birth_month = 0

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

#Third Function - we start to split up the line which contains musician details

def muso_detail_split(text):
	deceased = False

  # test if deceased first
  	deceased = re.search ("\(d\.(.*)\)", text)
 	if deceased:
 		pass
 		print "here"
        #do something here

#ident from here
	else:
	  #split the line of text using commas as a delimiter
	  muso_bits = text.split(',')
	  
	  #Grab everything before the first comma - that seems to be a constant for the name location
	  muso_name = muso_bits[0]
	  
	  #split that name into first, middle and surname to be returned individually - using the space as a delimiter
	  # putting each into a list
	  muso_name_list = muso_name.split(" ")
	  muso_forname = muso_name_list[0] #choose the first item in the list - should be the forname
	  muso_surname = muso_name_list[-1] # choose the last item as the last name


	  if len (muso_name_list) > 2: #if there are more than 2 items in the list, assume that the second is a middle name
	    muso_midname = muso_name_list[1]
	  else:
	    muso_midname = ""

	    #back to the list which we created from the passed in text
	  try:  #try to convert the contents of the last item - to an integer. If it is 1928 or 1957 for example, it should work
	    birth_year = int(muso_bits [-1])
	    
	    #ditch the name and the birth year
	    muso_bits.pop(0) #chuck away the first item as we dealt with that as the names at lines 12 - 20 above
	    muso_bits.pop(-1) #chuck away the last item - it was the year of birth (line 24)

	    #we should be left with the instruments
	    instrm_list = list(muso_bits)
	    #that's it all sorted - keep these remaining items as a list of instruments / roles which we'll return as a list

	  except ValueError:
	    #  doesn't end with a single year 
	    
	    print text
	    print "did not work"
	    worked = False
	    #need to work out what to do with these!!

	    if worked:
	 	#put all the values to be returned here
	  		muso_obj = [muso_forname, muso_midname, muso_surname, birth_year, instrm_list]
	  		return muso_obj

  		#return "1"



##################################
#    main code starts here       #
##################################

# grab the document as an xml object
tree = etree.parse('jazz_birthdays.xml')
root = tree.getroot()

for child in root:
	ignore_flag = False #used to identify elements with sub-elements <ulink> (ie Youtube links) as we don't want those
	for sub_child in child:
		if sub_child is not None:
			ignore_flag = True

	if not ignore_flag: #so no sub elements
		if child.text is not None: #not an empty <para/>
			line_text = child.text.encode('utf-8') #encode the text
			line_text = line_text.strip()

			
			line_text = remove_non_ascii_1(line_text) # cleans out ascii chars 132 and 160 from some lines
			nw = test_line (line_text)

			if nw ==2:
				#it can only be a date (as only they have two elements - day / month)
				words = line_text.split()
				tally = 0
				if words[1] in month_list:
					#take it that this is a date 

					#update the global vaiables with day and month * ordinal values*
					#                                              
					birth_day = int(words [0])
					birth_month = month_list.index(words[1]) +1
					
			else:
				#take it that it is a musician line (as we've excluded the day / month lines )
				find_substr = "(or"
				if find_substr in line_text:
					f3.write(str(birth_day) + " " + str(birth_month) +"\n")
					f3.write(line_text +"\n")
				else:
				
					muso_parts = muso_detail_split (line_text)
					f2.write (str(birth_day) + " " + str(birth_month) +"\n")
					for part in muso_parts:

						f2.write (part)
					#print muso_parts
					#for part in muso_parts:
					#	print part
					

			#f3.write(line_text +"\n")
		#print len(child)



# f.close()
f2.close()
f3.close()
