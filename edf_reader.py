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
	# If record is set to true, files will be selected to be imported. Otherwise, takes files from database and processes them.
	def run(self):
		if not self.should_record:
			self.collect_relevant_files()
			self.decide_network_or_graph()
		else:
			self.add_relevant_files_to_database()
	# Collects all data and then allows user to parse through what they want.
	def collect_relevant_files(self):
		self.storage = EDF_Store(files_with_categs={}, filenames=[], categ_names=[])
		self.storage.fetch_data()
		self.eeg_setup = Setup(params=self.storage.test_user_ids)
		self.eeg_setup.run()
	# Collects the files users want to record, then records them.
	def add_relevant_files_to_database(self):
		self.eeg_setup = Setup(params=None)
		self.eeg_setup.run()
		self.process_files()
		self.storage = EDF_Store(self.eeg_setup.files_with_categs, self.eeg_setup.filenames, self.eeg_setup.categ_names)
		self.storage.record_data()
	# If user wishes to graph, the grapher is run. Otherwise, the network is run.
	def decide_network_or_graph(self):
		self.process_firebase_files()
		graph = input('Graph data (g) or process in network? (n) ')
		if graph == 'g':
			grapher = EDF_Graph(self.eeg_setup.files_with_categs, self.eeg_setup.filenames, self.eeg_setup.categ_names)
			grapher.run()
		else:
			network = EDF_Network(self.eeg_setup.files_with_categs, self.eeg_setup.filenames)
			network.run()
	# Selects/converts particular files for graph/network
	def process_firebase_files(self,):
		for i in range(len(self.storage.test_user_ids)):
			user_id = self.storage.test_user_ids[i]
			if user_id in self.eeg_setup.filenames:
				user = self.storage.test_users[i]
				for categ_name in self.eeg_setup.categ_names:
					user_data_by_categ = list(user[str(categ_name)].items())
					user_data_by_categ = sorted(user_data_by_categ, key=lambda x: int(x[0]))
					user_data_by_categ = [item[1] for item in user_data_by_categ]
					self.eeg_setup.categs[categ_name].append(user_data_by_categ)
				self.add_data(user_id)
			self.reset_vars()
	def add_data(self, name):
		# Creates an independent variable. This varies by EDF file.
		x = np.arange(0, len(self.eeg_setup.categs[self.eeg_setup.categ_names[0]][0]))
		# Converts recorded data to numpy files for usability later on.
		for categ_name in self.eeg_setup.categ_names:
			self.eeg_setup.categs[categ_name] = np.array(self.eeg_setup.categs[categ_name])	
		# Sets the full database with your dependent and independent variables.
		self.eeg_setup.files_with_categs[name] = {
			'categs': self.eeg_setup.categs, 
			'x': x
		}
	# Clears the existing data and resets for the next file.
	def reset_vars(self):
		categ_placeholder = {}
		for name in self.eeg_setup.categ_names:
			categ_placeholder[name] = []
		self.eeg_setup.categs = categ_placeholder
	# Proceeses all files. Elaboration below.
	def process_files(self):
		for name in self.eeg_setup.filenames:
			# Checks if CSV exists; if not, it creates one.
			if not os.path.exists('Data/' + name + '.csv'):
				edf = mne.io.read_raw_edf('Data/' + name + '.edf')
				header = ','.join(edf.ch_names)
				np.savetxt('Data/' + name + '.csv', edf.get_data().T, delimiter=',', header=header)
			file = open('Data/' + name + '.csv')
			reader = csv.reader(file)
			# Iterates by row to collect desired data.
			counter = 0
			for row in reader:
				if counter%STEP == 0 and counter > 0:
					for categ_name in self.eeg_setup.categ_names:
						self.eeg_setup.categs[categ_name].append(float(row[ALL_CATEGS.index(categ_name)]))
				counter += 1
			self.add_data(name)
			self.reset_vars()