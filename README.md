jazz_birthdays
==============

A DB of jazz Musicians' birthdays.

Steps so far.
Converted original word doc to two trial formats using Libre Office:
 - XML
 - HTML 

Used the XML file as the most neutral

Tidied the file to remove the Jazz Birthdays and half a dozen erroneously-nested malformed <paras>

Fixed 29 Jan, 5 March, 18 April, 2 May, 4 May, 14 May, 26 May, 1 June, 14 June, 18 June, 27 June, 2 Nov, 31 Oct, 4 Nov, 23 Nov, to remove extra text
Fixed 15 Oct (to October)

Used global find and replace to correct handful of "(d " to "(d. " for consistency. 8 instances.

Used global find and replace to correct approx 60 instances of "(Mmm" to "(d. Mmm" where obvioulsy missing "d."

Removed a couple of empty year tags amongst Youtube line (e.g. <2012> )

The programme choked on "Paul Ruhland, bass, arranger, leader, 1930 (d. July, 2013)") under 29 Feb - since 1930 was not a leap year.

Manually fixed around 35 malformed death dates where commas used instead of "." e.g Ruby Braff, Glenn Miller
