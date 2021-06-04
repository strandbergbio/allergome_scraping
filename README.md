# Allergome and PalDat scraping scripts

This is a series of scripts and files for determining the size distribution of allergenic pollen relative to pollen overall.

The first step pulls information from the [Allergome database](http://www.allergome.org/). I saved a file from the output of the search term "pollen" per 4 Jun 2021 (`allergome_pollen_search.html`) and extracted the set of species names (using `allergome_search_scraper.py` and saved in `allergome_species_names.csv`.)

Then that list is used to pull data from [PalDat](https://www.paldat.org/) about the size of pollen particles for a given species, using `paldat_scraper.py` and saved to `paldat_output.csv`. Finally, `plotting.py` is used to generate a chart of the relative size distribution and output to `plot.png`.


## Dependencies

This project uses [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), which can be installed by running `pip install beautifulsoup4`.
