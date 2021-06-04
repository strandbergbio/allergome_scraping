import matplotlib.pyplot as plt
import pandas as pd
import csv, pdb

# count_overall data taken manually by using the 
# Combined Search tool on the PalDat website
data = {
	'<10 µm': [0,10],
	'11-15 µm': [0,89],
	'16-20 µm': [0,279],
	'21-25 µm': [0,523],
	'26-30 µm': [0,478],
	'31-35 µm': [0,339],
	'36-40 µm': [0,261],
	'41-50 µm': [0,247],
	'51-100 µm': [0,247],
	'>100 µm': [0,4]
}
counts = pd.DataFrame.from_dict(
	data,
	orient='index',
	columns=['Allergic','Overall']
)

with open('paldat_output.csv') as csvfile:
	reader = csv.DictReader(csvfile) 

	for row in reader:
		size_ranges = row['size of hydrated pollen (LM)'].split(', ')
		for size_range in size_ranges:
			try:
				counts.loc[size_range]['Allergic'] += 1
			except KeyError:
				pass

percentages = (100 * counts) / counts.sum(axis=0)

plt.figure()
percentages.plot.barh()
plt.xlabel("Percent of samples")
plt.ylabel("Size of hydrated pollen")
plt.tight_layout()
plt.savefig('allergic_vs_overall_pollen_plot.png')
