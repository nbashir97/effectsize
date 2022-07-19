* Cleaning raw NHANES data for testing effectsize in Python

use "{Insert path to}/nhanes_raw.dta", clear

* Age
generate age = ridageyr
replace age = . if(ridageyr < 20)

* Sex
generate sex = "Male" if(riagendr == 1)
replace sex = "Female" if(riagendr == 2)

* Ethnicity
generate ethnicity = "White" if(ridreth1 == 3)
replace ethnicity = "Black" if(ridreth1 == 4)
replace ethnicity = "Hispanic" if(ridreth1 == 1 | ridreth1 == 2)
replace ethnicity = "Other" if(ridreth1 == 5)

* Education
generate education = "Below" if(dmdeduc2 == 1 | dmdeduc2 == 2)
replace education = "High school" if(dmdeduc2 == 3 | dmdeduc2 == 4)
replace education = "College" if(dmdeduc2 == 5)

* BMI
generate BMI = bmxbmi

* Cholesterol
generate cholesterol = lbxtc

* Smoking status (0: non-smoker, 1: smoker)
generate smoking = 0 if(smq020 == 2 | smq040 == 3 )
replace smoking = 1 if(smq040 == 1 | smq040 == 2)

keep age-smoking wtmec2yr

foreach var of varlist age-smoking {
	drop if missing(`var')
}

save "{Insert path to}/nhanes_cleaned.dta", replace
