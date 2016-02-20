# Badminton World Federation (BWF) Data

**NOT ALL DATA HAS BEEN OBTAINED YET**

Badminton World Federation (BWF) world ranking data available in csv format.
The data was scraped from the official BWF website and parsed using Pandas.
This repo will include data and analyses that I decide to conduct on the data.

All disciplines (as BWF calls them) are available.
Each discipline is separated into a directory and files are formatted as such:
`bwf_<discipline>_<year>w<week>.csv`.

## Details
There are 8 columns in each csv file. The first column is simply an index.

| Column              | Description                                                      |
|:--------------------|:-----------------------------------------------------------------|
| RANK                | The player's rank                                                |
| COUNTRY             | The player's representing country                                |
| PLAYER              | The player's name with their last name in uppercase              |
| CHANGE +/-          | Rank change for the current week                                 |
| WIN - LOSE          | Total number of wins and losses                                  |
| PRIZE MONEY         | Total prize money earned                                         |
| POINTS / TOURNAMENT | Number of ranking points earned and number of tournaments played |

## Notes
- All columns are directly from the table. No extra columns were added on my part.
- There is no data for 2015 week 3, so there are no rows in the corresponding csv.
- For each doubles category, the `PLAYER` column consists of both player's names
concatenated together. I didn't make an effort to split the names up.
