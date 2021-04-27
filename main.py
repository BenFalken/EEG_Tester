## Main file, my guys

from edf_reader import EDF_Reader

if __name__ == "__main__":
	record_or_run = input('Import files to database (a) or Examine files from database? (b)? ')
	if record_or_run == 'a':
		reader = EDF_Reader(should_record=True)
	else:
		reader = EDF_Reader(should_record=False)
	reader.run()