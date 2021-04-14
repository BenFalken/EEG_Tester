## Reads all the data files to check if they exist. Converts to CSV so data can be analyzed.

from const import *
from setup import Setup
from edf_graph import EDF_Graph
import numpy as np
import mne, csv, os

class EDF_Reader:
	def __init__(self):
		eeg_setup = Setup()
		eeg_setup.run()

		self.categs = eeg_setup.categs 
		self.categ_names = eeg_setup.categ_names
		self.files_with_categs = eeg_setup.files_with_categs
		self.filenames = eeg_setup.filenames
	# Runs, then conditionally graphs.
	def run(self):
		self.process_files()
		graph = input('Graph data? Y/N: ')
		if graph == 'Y':
			grapher = EDF_Graph(self.files_with_categs, self.filenames, self.categ_names)
			grapher.run()
	# Proceeses all files. Elaboration below.
	def process_files(self):
		for name in self.filenames:
			# Checks if CSV exists; if not, it creates one.
			if not os.path.exists(name + '.csv'):
				edf = mne.io.read_raw_edf(name + '.edf')
				header = ','.join(edf.ch_names)
				np.savetxt(name + '.csv', edf.get_data().T, delimiter=',', header=header)

			file = open(name + '.csv')
			reader = csv.reader(file)

			counter = 0

			# Iterates by row to collect desired data.
			for row in reader:
				if counter%STEP == 0:
					for categ_name in self.categ_names:
						self.categs[categ_name].append(row[ALL_CATEGS.index(categ_name)])
				counter += 1

			# Creates an independent variable. This varies by EDF file.
			x = np.arange(0, len(self.categs[self.categ_names[0]]))

			# Converts recorded data to numpy files for usability later on.
			for categ_name in self.categ_names:
				self.categs[categ_name] = np.array(self.categs[categ_name])

			# Sets the full database with your dependent and independent variables.
			self.files_with_categs[name] = {
				'categs': self.categs, 
				'x': x
			}

			# Clears the existing data and resets for the next file.
			categ_placeholder = {}
			for name in self.categ_names:
				categ_placeholder[name] = []
			self.categs = categ_placeholder