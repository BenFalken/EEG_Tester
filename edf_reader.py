## Reads all the data files to check if they exist. Converts to CSV so data can be analyzed.

from const import *
from setup import Setup
from edf_graph import EDF_Graph
from edf_store import EDF_Store
from edf_network import EDF_Network
import numpy as np
import mne, csv, os

class EDF_Reader:
	def __init__(self, should_record):
		self.should_record = should_record
	# Runs, then conditionally graphs.
	def run(self):
		if not self.should_record:
			storage = EDF_Store(files_with_categs={}, filenames=[], categ_names=[])
			storage.fetch_data()
			eeg_setup = Setup(params=storage.test_user_ids)
			eeg_setup.run()
			self.record_eeg_setup_data(categs=eeg_setup.categs, categ_names=eeg_setup.categ_names, files_with_categs=eeg_setup.files_with_categs, filenames=eeg_setup.filenames)
			graph = input('Graph data? Y/N: ')
			if graph == 'Y':
				self.process_firebase_files_for_graph(storage.test_users, storage.test_user_ids)
				grapher = EDF_Graph(self.files_with_categs, self.filenames, self.categ_names)
				grapher.run()
			else:
				self.process_firebase_files_for_network(storage.test_users, storage.test_user_ids)
				network = EDF_Network(self.sifted_test_users, self.sifted_test_user_ids)
				network.run()
		else:
			eeg_setup = Setup(params=None)
			eeg_setup.run()
			self.record_eeg_setup_data(categs=eeg_setup.categs, categ_names=eeg_setup.categ_names, files_with_categs=eeg_setup.files_with_categs, filenames=eeg_setup.filenames)
			self.process_files()
			storage = EDF_Store(self.files_with_categs, self.filenames, self.categ_names)
			storage.run()
	def record_eeg_setup_data(self, categs, categ_names, files_with_categs, filenames):
		self.categs = categs 
		self.categ_names = categ_names
		self.files_with_categs = files_with_categs
		self.filenames = filenames
	def process_firebase_files_for_network(self, test_users, test_user_ids):
		self.sifted_test_users = []
		self.sifted_test_user_ids = []
		for i in range(len(test_user_ids)):
			user_id = test_user_ids[i]
			if user_id in self.filenames:
				user = test_users[i]
				self.sifted_test_user_ids.append(user_id)
				self.sifted_test_users.append(user)
	def process_firebase_files_for_graph(self, test_users, test_user_ids):
		for i in range(len(test_user_ids)):
			user_id = test_user_ids[i]
			if user_id in self.filenames:
				user = test_users[i]
				for categ_name in self.categ_names:
					user_data_by_categ = list(user[str(categ_name)].items())
					user_data_by_categ = sorted(user_data_by_categ, key=lambda x: int(x[0]))
					user_data_by_categ = [item[1] for item in user_data_by_categ]
					self.categs[categ_name].append(user_data_by_categ)
				x = np.arange(0, len(self.categs[self.categ_names[0]][0]))
				for categ_name in self.categ_names:
					self.categs[categ_name] = np.array(self.categs[categ_name])
				self.files_with_categs[user_id] = {
					'categs': self.categs, 
					'x': x
				}
			# Clears the existing data and resets for the next file.
			categ_placeholder = {}
			for name in self.categ_names:
				categ_placeholder[name] = []
			self.categs = categ_placeholder
	# Proceeses all files. Elaboration below.
	def process_files(self):
		#print(self.filenames)
		for name in self.filenames:
			# Checks if CSV exists; if not, it creates one.
			if not os.path.exists('Data/' + name + '.csv'):
				edf = mne.io.read_raw_edf('Data/' + name + '.edf')
				header = ','.join(edf.ch_names)
				np.savetxt('Data/' + name + '.csv', edf.get_data().T, delimiter=',', header=header)

			file = open('Data/' + name + '.csv')
			reader = csv.reader(file)

			counter = 0

			# Iterates by row to collect desired data.
			for row in reader:
				if counter%STEP == 0 and counter > 0:
					for categ_name in self.categ_names:
						self.categs[categ_name].append(float(row[ALL_CATEGS.index(categ_name)]))
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