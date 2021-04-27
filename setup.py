## Allows user to customize what data they wish to observe.

from const import *
import glob

class Setup:
	def __init__(self, params):
		self.params = params
		self.filenames = []
		self.categ_names = []
		self.categs = {}
		self.files_with_categs = {}
	# Self explanatory.
	def run(self):
		if self.params == None:
			self.get_files()
		else:
			self.file_list = [name + ".edf" for name in self.params]
		self.select_files()
		self.select_categs()
	# Responsible for getting all edf files.
	def get_files(self):
		pathname = "/Users/benfalken/Desktop/BigBrain/Data/"
		file_list = glob.glob(pathname + "*.edf")
		self.file_list = [filename[len(pathname):len(filename)] for filename in file_list]
	# Responsible for selecting specific edf files
	def select_files(self):
		select_files = input('Pick one or more files to analyze (1 to ' + str(len(self.file_list)) + '): ' + str(self.file_list) + ' Press return to complete, or "a" to copy everything. ')
		while True:
			if select_files == '':
				break
			if select_files == 'a':
				for name in self.file_list:
					self.filenames.append(name[:-4])
					self.files_with_categs[name[:-4]] = {}
				break
			try:
				index = int(select_files) - 1
				name = self.file_list[index]
				self.filenames.append(name[:-4])
				self.files_with_categs[name[:-4]] = {}
				del self.file_list[index]
				if len(self.file_list) == 0:
					break
			except:
				print('Your selection was invalid.')
			select_files = input('Pick one or more files to analyze (1 to ' + str(len(self.file_list)) + '): ' + str(self.file_list) + ' Press return to complete, or "a" to copy everything. ')
	# Responsible for getting the desired edf categories (brain regions).
	def select_categs(self):
		col = input('Which columns would you like to record? Select 1-' + str(len(ALL_CATEGS)) + '. (NOTE: Beta verision goes up to 5) Press return to end selection. ')
		while col != '':
			if col == '':
				break
			try:
				categ = ALL_CATEGS[int(col) -1]
				if categ not in self.categs:
					self.categs[categ] = []
					self.categ_names.append(categ)
			except:
				print('Your selection was invalid.')
			col = input('Which columns would you like to record? Select 1-' + str(len(ALL_CATEGS)) + '. (NOTE: Beta verision goes up to 5) Return to end selection. ')