from bs4 import BeautifulSoup
import csv

with open("allergome_pollen_search.html") as file:
	html = file.read()
	soup = BeautifulSoup(html, features="html5lib")

	rows = soup.findAll('table')[5].findAll('tr')
	names_unflat = [row.findAll('i') for row in rows]
	names_flat = {str(name).replace('<i>','').replace('</i>', '') for names in names_unflat for name in names}
	names_species_only = sorted([name for name in names_flat if len(name.split()) == 2])

	with open("allergome_species_names.csv", 'w') as csvfile:
		writer = csv.writer(csvfile)
		for name in names_species_only:
			writer.writerow([name])