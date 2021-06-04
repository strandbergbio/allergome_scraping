from bs4 import BeautifulSoup
import csv, pdb, requests, time


class PalDat():
	BASE_URL = 'https://www.paldat.org/pub/'
	HEADERS = [
		'name', 'pollen unit', 'dispersal unit and peculiarities', 'size (pollen unit)', 
		'size of hydrated pollen (LM)', 'shortest polar axis in equatorial view (LM)', 
		'longest polar axis in equatorial view (LM)', 'shortest diameter in equatorial or polar view (LM)', 
		'longest diameter in equatorial or polar view (LM)', 'pollen class', 'polarity', 
		'P/E-ratio', 'shape', 'outline in polar view', 'dominant orientation (LM)', 
		'P/E-ratio (dry pollen)', 'shape (dry pollen)', 'outline in polar view (dry pollen)', 
		'infoldings (dry pollen)', 'aperture number', 'aperture type', 'aperture condition', 
		'aperture peculiarities', 'ornamentation LM', 'nexine', 'sexine', 'ornamentation SEM', 
		'suprasculpture SEM', 'tectum', 'infratectum', 'foot layer', 'endexine', 'intine', 
		'wall peculiarities', 'supratectal element', 'pollen coatings', 
		'reserves in cytoplasm', 'cell number', 'Ubisch bodies'
	]

	def __init__(self):
		self.data = []

	def fetch_species_data(self, filename):
		with open(filename, 'r') as csvfile:
			reader = csv.reader(csvfile)

			for row in reader:
				species_name = row[0]
				response = requests.get(self.url(species_name))
				html = response.text
				soup = BeautifulSoup(html, features="html5lib")

				species_info = {"name": species_name}

				# The behavior of the site is to redirect to paldat.org/search/A 
				# if the attempted URL doesn't resolve. Search for the species name
				# to see whether we actually hit or if we got redirected.
				if soup.find(text=species_name):
					heading = soup.find('h1', text="Shape, Size and Aperture")
					h1_tag = heading.parent
					current_tag = h1_tag.findNext('p')

					while True:
						current_tag = current_tag.findNext('span', class_="diag-label")
						if current_tag is None:
							break
						key = current_tag.text.replace(':', '').replace(u'\xa0', u' ')
						current_tag = current_tag.findNext('span', class_="diag-value")
						value = current_tag.text.replace(u'\xa0', u' ')
						species_info[key] = value

				self.data.append(species_info)
				time.sleep(0.5)

	def write_data(self, filepath):
		with open(filepath, 'w') as file:
			writer = csv.DictWriter(file, fieldnames=self.HEADERS)
			writer.writeheader()
			writer.writerows(self.data)

	# The search function weirdly doesn't allow for directly searching a species name, 
	# but putting the species name directly into the URL seems to work correctly.
	def url(self, species_name):
		return f'{self.BASE_URL}{species_name.replace(" ","_")}'


if __name__ == "__main__":
	paldat = PalDat()
	try:
		paldat.fetch_species_data("allergome_species_names.csv")
	finally:
		paldat.write_data("paldat_output.csv")

