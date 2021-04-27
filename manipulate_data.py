## Responsible for making data more manageable

import numpy as np

class Data_Manipulator:
	def __init__(self):
		self.window_size = 0
		self.subtract_baseline = False
		self.set_low_pass = False
	# Get window size for a low pass filter
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
	# Get a specific graph (reference by column) and subtract it from the rest of the data
	def get_baseline(self, num_cols):
		if self.window_size == 0:
			self.get_low_pass_window_size()
		self.subtract_baseline = True
		while True:
			try:
				self.baseline_index = int(input('Which column? (1 to ' + str(num_cols) + ') '))
				if self.baseline_index - 0 >= 1 and self.baseline_index - 1 < num_cols:
					break
				else:
					raise Exception('Invalid Input.')
			except:
				print('Invalid Input.') 
	# If data is shorter than average, make it longer.
	def standardize_data(self, data):
		if len(data) != 976:
			diff = 976 - len(data)
			if diff%2 == 0:
				start = [data[0] for i in range(int(diff/2))]
				end = [data[-1] for i in range(int(diff/2))]
			else:
				start = [data[0] for i in range(int(diff/2))]
				end = [data[-1] for i in range(int(diff/2) + 1)]
			data = np.concatenate((start, data, end))
		return data
	# Use a moving average to create a low pass filter
	def low_pass(self, data):
		convolved_data = []
		for i in range(int(self.window_size/2)):
			convolve_sum = 0
			for j in range(0, 2*i):
				convolve_sum += float(data[j])/(i+1)
			convolved_data.append(convolve_sum)
		for i in range(int(self.window_size/2), 976 - (int(self.window_size/2) + 1)):
			convolve_sum = 0
			for j in range(-1*int(self.window_size/2), int(self.window_size/2) + 1):
				convolve_sum += float(data[i+j])/self.window_size
			convolved_data.append(convolve_sum)
		for i in range(976 - int(self.window_size/2), 977):
			convolve_sum = 0
			for j in range(976 - int(self.window_size/2) + i, 976):
				convolve_sum += float(data[j])/(977-i)
			convolved_data.append(convolve_sum)
		return convolved_data