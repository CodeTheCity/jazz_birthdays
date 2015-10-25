words=['5', 'March']
month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August','September', 'October', 'November', 'December']
birth_month = month_list.index(words[1]) +1

print "day = " + str(words[0])
print "month = " + str (birth_month)