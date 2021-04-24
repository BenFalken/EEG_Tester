from edf_reader import EDF_Reader

if __name__ == "__main__":
	record_or_run = input('Record (a) or Run (b)? ')
	if record_or_run == 'a':
		reader = EDF_Reader(should_record=True)
		reader.run()
	else:
		reader = EDF_Reader(should_record=False)
		reader.run()