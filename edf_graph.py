## Graphs desired data.

import matplotlib.pyplot as plt
import numpy as np

class EDF_Graph:
	def __init__(self, files_with_categs, filenames, categ_names):
		self.files_with_categs = files_with_categs
		self.filenames = filenames
		self.categ_names = categ_names

		self.subtract_baseline = False
		self.set_low_pass = False
		self.window_size = 0

		self.create_ax()
		self.create_settings()
	def create_settings(self):
		if input("Set Low Pass? Y/N: ") != 'N':
			self.get_low_pass_window_size()
		if input("Set Baseline? Y/N: ") != 'N':
			self.get_baseline()
	# Creates subplot. Elaboration below.
	def get_low_pass_window_size(self):
		self.set_low_pass = True
		while True:
			try:
				size = int(input('What moving window size? '))
				if size >= 0:
					self.window_size = size
					break
				else:
					print('Invalid input.')
			except:
				print('Invalid input.') 
	def get_baseline(self):
		if self.window_size == 0:
			self.get_low_pass_window_size()
		self.subtract_baseline = True
		while True:
			try:
				self.baseline_index = int(input('Which column? '))
				break
			except:
				print('Invalid Input.') 
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
						#print(self.categ_names, self.filenames)
						print(e)
		plt.show()
	# Makes a special tuple for snowflake matplotlib.
	def create_ax(self):
		self.ax = ()
		for i in range(len(self.categ_names)):
			name = self.categ_names[i]
			ax_append = ()
			for j in range(len(self.filenames)):
				ax_append = ax_append + (0,)
			self.ax = self.ax + (ax_append,)
	def low_pass(self, data):
		convolved_data = np.zeros((data.size))
		for i in range(int(self.window_size/2), data.size - (int(self.window_size/2) + 1)):
			convolve_sum = 0
			for j in range(-1*int(self.window_size/2), int(self.window_size/2) + 1):
				convolve_sum += float(data[i+j])/self.window_size
			convolved_data[i] = convolve_sum
		convolved_data[0] = float(data[0])
		convolved_data[1] = np.sum(data[1:4])/3
		convolved_data[-1] = float(data[-1])
		convolved_data[-2] = np.sum(data[-3:])/3
		return convolved_data
	def graph(self, sub_graph, x_data, y_data, categ, title):
		sub_graph.set_title(title)
		sub_graph.plot(x_data, y_data)
		if self.subtract_baseline:
			try:
				#baseline = self.files_with_categs[self.filenames[self.baseline_index]]['categs'][self.categ_names[categ]]
				convolved_data = self.low_pass(y_data)
				#convolved_data = self.low_pass(y_data) #or self.files_with_categs[self.filenames[self.baseline_index]]['categs'][self.categ_names[i]]
				sub_graph.plot(x_data, y_data - convolved_data, color="green")
			except:
				print(title)
				print("BASELINE " + str(baseline.size))
				print("ACTUAL " + str(y_data.size))
				print("***")
		if self.set_low_pass:
			convolved_data = self.low_pass(y_data)
			sub_graph.plot(x_data, convolved_data, color="red")
