## Graphs desired data.

from manipulate_data import Data_Manipulator
import matplotlib.pyplot as plt
import numpy as np

class EDF_Graph:
	def __init__(self, files_with_categs, filenames, categ_names):
		self.data_manipulator = Data_Manipulator()
		self.files_with_categs = files_with_categs
		self.filenames = filenames
		self.categ_names = categ_names
		self.manage_filenames_length()
		self.create_ax()
		self.create_settings()
	# Makes sure you aren't blasting matplotlib
	def manage_filenames_length(self):
		if len(self.filenames) > 10:
			self.filenames = self.filenames[:10]
			print('Number of files set to 10. We cannot accommodate more than 10 files.')
		if len(self.categ_names) > 5:
			self.categ_names = self.categ_names[:5]
			print('Number of categories set to 10. We cannot accommodate more than 5 categories.')
	# Get user to choose if they want a low pass, or subtracting a baseline
	def create_settings(self):
		if input("Set Low Pass? Y/N: ") != 'N':
			self.data_manipulator.get_low_pass_window_size()
		if input("Set Baseline? (Not recommended, still beta mode) Y/N: ") != 'N':
			self.data_manipulator.get_baseline(num_cols=len(self.filenames))
	# Makes a special tuple for snowflake matplotlib.
	def create_ax(self):
		self.ax = ()
		for i in range(len(self.categ_names)):
			name = self.categ_names[i]
			ax_append = ()
			for j in range(len(self.filenames)):
				ax_append = ax_append + (0,)
			self.ax = self.ax + (ax_append,)
	# For each piece of the matplotlib tuple, make a graph
	def run(self):
		fig, self.ax = plt.subplots(len(self.categ_names), len(self.filenames), figsize=(12, 10))
		fig.tight_layout()
		for i in range(len(self.categ_names)):
			for j in range(len(self.filenames)):
				title = self.filenames[j] + ": " + self.categ_names[i]
				x_data = self.files_with_categs[self.filenames[j]]['x']
				y_data = self.files_with_categs[self.filenames[j]]['categs'][self.categ_names[i]][0]
				try:
					self.graph(self.ax[i][j], x_data, y_data, i, title)
				except Exception as e:
					if len(self.filenames) == 1 and len(self.categ_names) > 1:
						self.graph(self.ax[i], x_data, y_data, i, title)
					elif len(self.categ_names) == 1 and len(self.filenames) > 1:
						self.graph(self.ax[j], x_data, y_data, i, title)
					elif len(self.categ_names) == 1 and len(self.filenames) == 1:
						self.graph(self.ax, x_data, y_data, i, title)
					else:
						print(e)
		plt.show()
	# Creates subplot. Elaboration below.
	def graph(self, sub_graph, x_data, y_data, categ, title):
		sub_graph.set_title(title)
		sub_graph.plot(x_data, y_data)
		if self.data_manipulator.subtract_baseline:
			try:
				baseline = self.files_with_categs[self.filenames[self.data_manipulator.baseline_index]]['categs'][self.categ_names[categ]][0]
				sub_graph.plot(x_data, y_data - baseline, color="green")
			except Exception as e:
				print(e)
		if self.data_manipulator.set_low_pass:
			convolved_data = self.data_manipulator.low_pass(y_data)
			sub_graph.plot(x_data, convolved_data, color="red")
