#import matplotlib.pyplot as plt

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Input, Embedding, LSTM

class EDF_Network:
	def __init__(self, data, ids):
		self.data = data
		self.ids = ids

		self.train_labels = []
		self.train_data = []
	def run(self):
		#print(self.ids)
		self.sift()
		self.arrange_training_data()
		self.run_network()
	def sift(self):
		self.unique_ids = []
		for user_id in self.ids:
			truncated_id = user_id[-3:]
			if truncated_id not in self.unique_ids:
				self.unique_ids.append(truncated_id)
		#print(self.unique_ids)
	def low_pass(self, data, window_size):
		convolved_data = []
		for i in range(int(window_size/2)):
			convolve_sum = 0
			for j in range(0, 2*i):
				convolve_sum += float(data[j])/(i+1)
			convolved_data.append(convolve_sum)
		for i in range(int(window_size/2), 976 - (int(window_size/2) + 1)):
			convolve_sum = 0
			for j in range(-1*int(window_size/2), int(window_size/2) + 1):
				convolve_sum += float(data[i+j])/window_size
			convolved_data.append(convolve_sum)
		for i in range(976 - int(window_size/2), 977):
			convolve_sum = 0
			for j in range(976 - int(window_size/2) + i, 976):
				convolve_sum += float(data[j])/(977-i)
			convolved_data.append(convolve_sum)
		return convolved_data
	def arrange_training_data(self):
		unique_id_num = len(self.unique_ids)
		id_counter = 0
		for user in self.data:
			"""if id_counter%2 == 0:
				fig, ax = plt.subplots(2, 1)"""
			self.train_labels.append(id_counter%unique_id_num)
			user_keys = user.keys()
			add_user_data = []
			for key in list(user_keys):
				user_data_by_categ = list(user[str(key)].items())
				user_data_by_categ = sorted(user_data_by_categ, key=lambda x: int(x[0]))
				user_data_by_categ = [item[1] for item in user_data_by_categ]
				if len(user_data_by_categ) != 976:
					diff = 976 - len(user_data_by_categ)
					if diff%2 == 0:
						start = [user_data_by_categ[0] for i in range(int(diff/2))]
						end = [user_data_by_categ[-1] for i in range(int(diff/2))]
						user_data_by_categ = start + user_data_by_categ + end
					else:
						start = [user_data_by_categ[0] for i in range(int(diff/2))]
						end = [user_data_by_categ[-1] for i in range(int(diff/2) + 1)]
						user_data_by_categ = start + user_data_by_categ + end
					#print(len(user_data_by_categ))
				low_pass_data = self.low_pass(user_data_by_categ, window_size=10)
				#ax[id_counter%2].plot(np.arange(0, 976), np.array(low_pass_data)) #np.array(user_data_by_categ) - np.array(low_pass_data))
				new_data = [user_data_by_categ[i] - low_pass_data[i] for i in range(976)]
				add_user_data.append(new_data)
			self.train_data.append(add_user_data)
			"""if id_counter%2 == 1:
				plt.show()"""
			id_counter += 1
		self.unique_key_num = len(user_keys)
		self.categ_length = len(user_data_by_categ)
		self.train_labels = np.array(self.train_labels)
		#print(self.train_labels)
		self.train_data = np.array(self.train_data)
	def run_network(self):
		#print(self.train_data.dtype)
		model = Sequential()

		model.add(Input(shape=(self.unique_key_num, self.categ_length)))
		#model.add(Embedding(input_dim=self.unique_key_num, output_dim=64))
		# Add a LSTM layer with 128 internal units.
		model.add(LSTM(128, activation='relu', return_sequences=True))
		model.add(LSTM(128, activation='relu'))
		# Add a Dense layer with 10 units.
		model.add(Dense(32, activation='sigmoid'))
		model.add(Dense(1, activation='sigmoid'))
		model.summary()
		
		"""model.add(Input(shape=(self.unique_key_num, self.categ_length)))
		model.add(Dense(12, activation='relu'))
		model.add(Dense(8, activation='relu'))
		model.add(Dense(1, activation='sigmoid'))"""

		model.compile(optimizer='sgd', loss='binary_crossentropy', metrics=['accuracy'])
		model.fit(self.train_data, self.train_labels, batch_size=20, epochs=30)

		sample = np.zeros((1, 5, 976))
		sample[0] = self.train_data[-1]
		print(sample.shape)
		ans = model.predict(sample)
		print(ans)