## Graphs desired data.

import matplotlib.pyplot as plt

class EDF_Graph:
	def __init__(self, files_with_categs, filenames, categ_names):
		self.files_with_categs = files_with_categs
		self.filenames = filenames
		self.categ_names = categ_names
		self.create_ax()
	# Creates subplot. Elaboration below.
	def run(self):
		fig1, self.ax = plt.subplots(len(self.categ_names), len(self.filenames))
		for i in range(len(self.categ_names)):
			for j in range(len(self.filenames)):
				print(i, j)
				try:
					# Removes axes, plots data for each EDF file and sub-category.
					self.ax[i][j].set_title(self.filenames[j] + ": " + self.categ_names[i])
					self.ax[i][j].axis('off')
					self.ax[i][j].plot(self.files_with_categs[self.filenames[j]]['x'], self.files_with_categs[self.filenames[j]]['categs'][self.categ_names[i]])
				except Exception as e:
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