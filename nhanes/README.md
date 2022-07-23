This directory contains the files used to create the use case examples on NHANES data:

1. **nhanes_examples.py:** script for running the analyses in order to create Table 2 and compute effect sizes
2. **nhanes_cleaned.dta:** the cleaned NHANES dataset used in nhanes_examples.py
3. **nhanes_raw.dta:** the raw NHANES data from the CDC website, imported as SAS XPT files (BMX_J, DEMO_J, SMQ_J, TCHOL_J) and then merged into a single Stata .dta file
4. **cleaning.do:** Stata do-file for creating nhanes_cleaned.dta (already had script written to do this, so this was simpler than writing new script for cleaning the data in Python)

Note in **nhanes_examples.py** and **cleaning.do** the path to the appropriate files must be specified at the start of the script
