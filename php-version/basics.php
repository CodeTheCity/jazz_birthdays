<?php
// a train hacking experiment
// starting with the source material, and a similar approach to the python project
// can I knock this into shape while sitting on a train in one big stretch

// input file was first 'fixed' by a lot of sublime text regexp jiggery pokery
// input file was then hand tweaked in many places to fix things like "Ju1y"



$forecast_input_file ="source_tidy_sm_extra.xml";
$output = 'sm_output.xml';
$discardedoutput = 'sm_output_discards.xml';

$day = 1;
$month = "January";
$year = "1900";

$buffer = "<musicians>\n";
$discardedlines = "";
// Establish our input data file exists...
if (file_exists($forecast_input_file)) {
    //echo "The file $filename exists";
} else {
    echo "FAILED : Data File Unavailable";
    exit();
}

// Open our file
$lines = file($forecast_input_file);

// Loop through each line

foreach ($lines as $line_num => $line) {
 // limit things for testing...
 if (  $line_num < 10000){
 	// we use this later to flag lines where we don't trust the data
 	$errorline = FALSE;
 	$dateswitch = FALSE;
 	$dob = FALSE;
 	$dod = FALSE;
 	$fullname = FALSE;
 	$firstname = FALSE;
 	$lastname = FALSE;
 	$middlenames = FALSE;
 	$talent = FALSE;
 	$talentxml = FALSE;
 	$musician = FALSE;
	// remove whitespace from our line
	$line = trim($line);
	$line = RemoveBS($line);
	// show the line quickly
//	echo "<h1>#".$line_num."</h1>";
//	echo "<p>Line #<b>{$line_num}</b> : //" . ($line) . "//</p>\n";

	// blow it up around the commas as these are about the most useful delimiter we have
	// we'll do most of our work on this - but we might return to $line too
	$parts = explode(",",$line);

	// how many elements do we have? This is useful to identify date lines, as each day has a date header
	$part_count = count($parts);

	//echo "<p>elements: ".$part_count."</p>";

    if ($part_count === 1){
		// if we have only one element we don't have an artist, but we might have a date.
		//echo "<h3>NOT AN ARTIST</h3>";
		// so it MIGHT be a date... let's check.

		$datelineparts = explode(" ",$parts[0]);
		//print_r($datelineparts);
		//echo count($datelineparts);
		if (count($datelineparts) === 2){
			//echo "<hr /><h1>LOOKS LIKE I'M A DATE ".$datelineparts[0]." / ".$datelineparts[1]."</h1>";

			// so we set the global day / month for date construction for other rows.
			$day = $datelineparts[0];
			$month = $datelineparts[1];
			$dateswitch = TRUE;

				$discardedlines = $discardedlines . $line . "\n";

		} else {

				$errorline = true;
				$discardedlines = $discardedlines . $line . "\n";
			//echo "<p>IGNORE ME I'm NOTHING</p>";
		}
    } elseif ($part_count === 2) {
 		// these ones are troubling as they may or may not have anything useful.
 		// likely to only have a name or a name / year pair with no instruments
 		// TODO we should simply write the whole line to the 'dunno.txt' file.
 		//echo "<p>IGNORE ME too - 2</p>";
    } else {
     	// any other length we have to assume is a legit artist entry
	//	echo "<p><b>PROBABLY AN ARTIST</b></p>";

		// the format is messy at the end of the line.
		// let's check the last element and see if it's a birth year:

     	//echo "<p> Name? <b>".$parts[0]."</b></p>";

     	// if last segment has a ) character this is likely the date of death
     	// so we need to keep looking for year of birth

		// so if we have a ) we treat it as a date of death
		if (strpos($parts[$part_count-1], ')') !== FALSE){

	     	//	echo "<p> YOB? <b>".$parts[$part_count-3]."</b></p>";
	     	//	echo "<p> RAW DOD ? <b>".$parts[$part_count-2]."</b></p>";
	     	//	echo "<p> RAW DOD ? <b>".$parts[$part_count-1]."</b></p>";

			// we need to strip some garbage from the string
			// neater ways to do this, but this is clear
     		$rawdod = $parts[$part_count-2] . " " . $parts[$part_count-1];
     		$cleandod = str_replace("(d. ","",$rawdod);
     		$cleandod = str_replace("(","",$cleandod);
     		$cleandod = str_replace(")","",$cleandod);
     		$cleandod = str_replace("?","",$cleandod);
     		$cleandod = str_replace(".","",$cleandod);

			//echo "<p>cleanDOD : <b>".$cleandod."</b></p>";

     		// finally we have a gotcha hanging around
     		// some entries have a date in brackets that is an alternative
     		// birth year. insane!
			if (strpos($cleandod, 'or') !== FALSE){
				//echo "<p> Danger wil robinson - this is an alternative birthday!!</p>";
				// so we set the error flag
				$errorline = true;
			} else {
				// so we can now set a date of death. awesome.
				$deathdate = new DateTime($cleandod);
				$dod = date_format($deathdate, 'Y-m-d ');
				//echo "<p>DOD : <b>".$dod."</b></p>";

				// and we *might* be able to set a date of birth if the next entry looks like a year

				$yob_poss = intval(trim($parts[$part_count-3]));
				if (is_int($yob_poss)){
					// so this looks like it's a year. hurrah
					// let's construct a date of birth from this

					$birthdate = new DateTime($day.' '.$month.' '.$yob_poss);
					$dob = date_format($birthdate, 'Y-m-d ');
 					//echo "<p> YOB?  <b>".date_format($birthdate, 'Y-m-d ')."</b></p>";
				}


			}
		// otherwise we assume the jazzer is still alive and well
		// and take this last value as the year of birth
		}	else {
			// we already know the day and month
			// so we want to construct a date with the year we just found
			// and we know that DOD is unset as this jazz fiend is alive
			// or so unknown that no one noticed that they died :(

			// first check that this can be treated as an integer
			$yob_poss = intval(trim($parts[$part_count-1]));
			if (is_int($yob_poss)){
				if ($yob_poss>1000 ){

					$birthdate = new DateTime($day.' '.$month.' '.$yob_poss);

					$dob = date_format($birthdate, 'Y-m-d ');
				}
			}
 			//echo "<p> YOB?  <b>".date_format($birthdate, 'Y-m-d ')."</b></p>";
 			//echo "<p> DOD?  <b>alive</b></p>";

		}

     }

     // OK. Deep breath. That's the date stuff dealt with.
     // So now we need to get a name...

     $fullname = $parts[0];

     // That was easy. Awesome.
     // hold on though - we need to do some more don't we...
     // we need first , sur, middle

     $namebits = explode(" ",$fullname);
     $namebits_count = count($namebits);

     $firstname = trim($namebits[0]);
     $lastname = trim($namebits[$namebits_count-1]);

     // so we have first and last
     // now for a dirty cheat to make the middle name
     // blank out the bits we already have
     $namebits[0] = "";
     $namebits[$namebits_count-1] = "";

     // and then implode the array again

     $middlenames = trim(implode(" ", $namebits));


     //$middlenames = $namebits[-1];

     // now for talent
     // ok - if we have a dod we want to kill the last 3 parts
     // if we don't have a dod we just want to kill the last
     // oh - and we want to kill the first.

     $newparts = $parts;
     $newparts[0] = "";
     $newparts[-1] = "";
     //echo $dod;
     if($dod ){
     	//echo $newparts[$part_count-2];
     	//echo $newparts[$part_count-3];
	     $newparts[$part_count-2] = "";
	     $newparts[$part_count-3] = "";
     }

	foreach ($newparts as $part) {
     	if (intval($part)<1 && strlen($part)>0){
     		$talent = $talent . ',' . $part;
     		$talentxml = $talentxml .  "   <instrument>".trim($part)."</instrument>\n";
     	}
     }


     // TODO
     // complete the actual output element instead of this dodgy dump to screen nonsense
     // train hacking ftw!
    if (!$errorline){
    	if (!$dateswitch){


$musician = $musician . " <musician>\n";
$musician = $musician .  "  <fullname>".$fullname."</fullname>\n";
$musician = $musician .  "  <fname>".$firstname."</fname>\n";
$musician = $musician .  "  <middlename>".$middlenames."</middlename>\n";
$musician = $musician .  "  <lname>".$lastname."</lname>\n";
$musician = $musician .  "  <dob>".trim($dob)."</dob>\n";
$musician = $musician .  "  <dod>".trim($dod)."</dod>\n";
$musician = $musician .  "  <instruments>\n";
$musician = $musician .  $talentxml;
$musician = $musician .  "  </instruments>\n";
$musician = $musician .  " </musician>\n";

echo "<musicians>\n";
echo $musician;
echo "</musicians>\n";

$buffer = $buffer . $musician;
 		//	echo "<p> FULL NAME  <b>".$fullname."</b></p>";
 		//	echo "<p> TALENT  <b>".$talent."</b></p>";
 		//	echo "<p> DOB  <b>".$dob."</b></p>";
 		//	echo "<p> DOD  <b>".$dod."</b></p>";
 		}
 	}
//	$datepart = forecast_date($line);


   }
}

$buffer = $buffer . "</musicians>";
file_put_contents($output, $buffer);


file_put_contents($discardedoutput, $discardedlines);
//echo "done";

/*

	CLEVER STUFF DOWN THERE

*/
// just grabbed from https://stackoverflow.com/questions/1189007/removing-strange-characters-from-php-string
	// pretty brutal approach but works
function RemoveBS($Str) {
  $StrArr = str_split($Str); $NewStr = '';
  foreach ($StrArr as $Char) {
    $CharNo = ord($Char);
    if ($CharNo == 163) { $NewStr .= $Char; continue; } // keep £
    if ($CharNo > 31 && $CharNo < 127) {
      $NewStr .= $Char;
    }
  }
  return $NewStr;
}

/*

END */