
''''
def strip_line(line):
	line = "  <para>1 January   </para>"
	sub_line = line[8:-8] # remove '  <para>'' at start and </para> at end
	sub_line.strip() # strip end whitespace
	#s = u'Good bye in Swedish is Hej d\xc3'
	print sub_line
	sub_line = sub_line.encode('ascii',errors='ignore')
	print sub_line
	return sub_line

for line in f:
	line = strip_line(line)
	print line
	print len(line)
	print ord(line[1])
	print ord(line[10])
	f3.write(line +"\n")
'''
