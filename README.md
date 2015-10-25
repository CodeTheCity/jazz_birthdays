jazz_birthdays
==============

A DB of jazz Musicians' birthdays.

Steps so far.
Converted original word doc to two trial formats using Libre Office:
 - XML
 - HTML 

- Used the XML file as the most neutral

- Tidied the file to remove the Jazz Birthdays and half a dozen erroneously-nested malformed <paras>

- Fixed 29 Jan, 5 March, 18 April, 2 May, 4 May, 14 May, 26 May, 1 June, 14 June, 18 June, 27 June, 2 Nov, 31 Oct, 4 Nov, 23 Nov, to remove extra text
Fixed 15 Oct (to October)

- Used global find and replace to correct handful of "(d " to "(d. " for consistency. 8 instances.

- Used global find and replace to correct approx 60 instances of "(Mmm" to "(d. Mmm" where obvioulsy missing "d."

- Removed a couple of empty year tags amongst Youtube line (e.g. <2012> )

- The programme choked on "Paul Ruhland, bass, arranger, leader, 1930 (d. July, 2013)") under 29 Feb - since 1930 was not a leap year.

- Manually fixed around 35 malformed death dates where commas used instead of "." e.g Ruby Braff, Glenn Miller

=============================================================================
#### Sunday 25 Oct 2015

Around version 7 of the extraction file got it working well enough to output all non-dead musicians out to XML which imported into the database.

We spent a few hours working on the dead musicians to try to get the death dates formatted correctly. 

We gave up and created process_the_dead.py which takes as input the output of first script, and allows any old text for death dates and writes that out as strings to DOD field.

We still have some queries in dirty_out2.xml which contain anomalies and "or" records where there are alternative dates for birth or death.

Sean Reilly has created a repo for the PHP / MySQL which he was working on [here](https://github.com/Surreily/CTC5-Jazz-Database)
