## Allows user to customize what data they wish to observe.

from const import *
import glob

class Setup:
	def __init__(self):
		self.filenames = []
		self.categ_names = []
		self.categs = {}
		self.files_with_categs = {}
	# Self explanatory.
	def run(self):
		self.get_files()
		self.get_categs()
	# Responsible for getting all desired edf files.
	def get_files(self):
		pathname = "YourPath/ProjectFolder/Data"
		file_list = glob.glob(univ_path + "*.edf")
		file_list = [filename[len(pathname):len(filename)] for filename in file_list]

		select_files = input('Pick one or more files to analyze (1 to ' + str(len(file_list)) + '): ' + str(file_list) + ' Return to complete. ')

		while select_files != '':
			if select_files == '':
				break
			try:
				index = int(select_files) - 1
				name = file_list[index]
				self.filenames.append(name[:-4])
				self.files_with_categs[name[:-4]] = {}
				del file_list[index]
				if len(file_list) == 0:
					break
			except:
				print('Your selection was invalid.')
			select_files = input('Pick one or more files to analyze (1 to ' + str(len(file_list)) + '): ' + str(file_list) + ' Return to complete. ')
	# Responsible for getting the desired edf categories (brain regions).
	def get_categs(self):
		col = input('Which columns would you like to record? Select 1-' + str(len(ALL_CATEGS)) + '. Return to end selection. ')
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
			col = input('Which columns would you like to record? Select 1-' + str(len(ALL_CATEGS)) + '. Return to end selection. ')
