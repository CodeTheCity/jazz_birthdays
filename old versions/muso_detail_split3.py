

def muso_detail_split(text):

    # initialise so we can use it as a flag if fails below
    worked = True 

  #split the line of text using commas as a delimiter
    muso_bits = text.split(',')
    
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

    #back to the list which we created from the passed in text
    try:  #try to convert the contents of the last item - to an integer. If it is 1928 or 1957 for example, it should work
        birth_year = int(muso_bits [-1])
    
        #chuck away the first item as we dealt with that as the names at lines 12 - 20 above
        #muso_bits.pop[0]
        muso_bits.remove(muso_bits[0])

        #chuck away the last item - it was the year of birth (line 24)
        muso_bits.remove(muso_bits[-1])

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
        print muso_forname
        print muso_midname
        print muso_surname
        print birth_year
        print instrm_list


        muso_obj = [muso_forname, muso_midname, muso_surname, birth_year, instrm_list]
    

    else:
        muso_obj = []
  
    return muso_obj

#line_text = 'Ronnell Bright, piano, 1930'
#line_text = 'Johnny Coles, trumpet, 1926 (d. Dec 21, 1997)'
#line_text = 'Ron Collier, composer, arranger, leader 1930 (d. Oct 22, 2003)'
#line_text = 'Pete Fountain, clarinet, 1930'
#line_text = 'Laszlo Gardony, piano, 1956'
#line_text = 'Jerry Gray, composer, arranger, leader, 1915 (d. Aug. 10, 1976)'
#line_text = 'Corky Hale, harp, piano, keyboards, flute, vocal, 1936'
#line_text = 'Johnny Hartman, vocal, 1923 (or 7/13) (d. Sept 15, 1983)'
#line_text = 'John Heard, bass, 1938'
#line_text = 'Duffy Jackson, drums, piano, bass, vibes, vocal, director, 1953'
#line_text = 'John Klemmer, saxophones, flute, keyboards, percussion vocal, 1946'
#line_text = 'Sakari Kukko, tenor and soprano sax, 1953'
#line_text = 'Bob McChesney, trombone'
#line_text = 'Dick Robertson, vocal, 1903 (or July 4, 1910) (d. 1979)'
#line_text = 'Michel Ruppli, discographer, 1934'
#line_text = '(Dr.) Lonnie Smith, organ, piano, keyboards, 1942'
#line_text = 'Tommy Tedesco, guitar, 1930 (d. Nov. 10, 1997)'
#line_text = 'Melissa Walker, vocal, 1964'

birth_day = 3
birth_month = 10

muso_detail_split (line_text)