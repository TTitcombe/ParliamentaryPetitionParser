# ParliamentaryPetitionParser
A handy code wrapper to retrieve and parse data from the [UK Parliamentary Petitions website](https://petition.parliament.uk/).

This code will, eventually, accept petition numbers, names, or urls.
The data collected and parsed from the petition can be saved in a time-separated manner to allow analysis of the petition's evolution over time,
for the rare occurrences when petitions take off.

## Requirements
This repo is written for Python 3. Python 2 compatibility is not guaranteed.
See requirements.txt for a list of python packages this code depends on.

## How To Use
*This repo is in the early stages of development*
1. Clone this repo and install the required packages.
2. Find out the petition number of the petition for which you would like to collect data
3. Find the path to the directory to which you would like data to be saved, *relative to the top-level* **ParliamentaryPetitionParser** *directory*. This defaults to **data/**.
4. In the **ParliamentaryPetitionParser** directory, run `python -m src.ppp --petition_number=NUM --output_dir=DIR`, 
where NUM is the petition number and DIR is the save directory.
5. Check your output directory location. You will have two file: **constituency** and **country**, which
are prefixed by year_month_day_hour_minute_ and suffixed by the petition number.

You can also set **ParliamentrayPetitionParser** to collect data every X minutes. To do this, run
`python -m src.ppp --petition_number=NUM --output_dir=DIR --frequency=X`
