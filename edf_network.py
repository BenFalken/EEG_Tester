## Deep learning algo for the edf files

import numpy as np
from keras.models import Sequential
from manipulate_data import Data_Manipulator
from keras.layers import Dense, Input, Embedding, LSTM

class EDF_Network:
	def __init__(self, data, ids):
		self.data_manipulator = Data_Manipulator()
		self.data = data
		self.ids = ids
		self.train_labels = []
		self.train_data = []
	# Explained below.
	def run(self):
		#self.sift()
		self.arrange_training_data()
		self.train_network()
		self.test_network()
	# Standardizes the data. Makes it nice.
	def arrange_training_data(self):
		for user_id in self.ids:
			user = self.data[user_id]["categs"]
			self.train_labels.append(int(user_id[-1])-1)
			user_categs = user.keys()
			add_user_data = []
			for key in list(user_categs):
				user_data_by_categ = user[key][0]
				standardized_data = self.data_manipulator.standardize_data(user_data_by_categ)
				add_user_data.append(standardized_data)
			self.train_data.append(add_user_data)
		self.categ_num = len(user_categs)
		self.categ_length = len(user_data_by_categ)
		self.train_labels = np.array(self.train_labels)
		self.train_data = np.array(self.train_data)
	# Trains the LSTM network real good. Good times.
	def train_network(self):
		self.model = Sequential()
		# Add an Input layer.
		self.model.add(Input(shape=(self.categ_num, self.categ_length)))
		# Add a LSTM layer with 128 internal units.
		self.model.add(LSTM(128, activation='relu', return_sequences=True))
		self.model.add(LSTM(128, activation='relu'))
		# Add a Dense layer with 10 units.
		self.model.add(Dense(32, activation='sigmoid'))
		self.model.add(Dense(1, activation='sigmoid'))
		self.model.summary()
		# Compile the model.
		self.model.compile(optimizer='sgd', loss='binary_crossentropy', metrics=['accuracy'])
		self.model.fit(self.train_data, self.train_labels, batch_size=20, epochs=30)
	# Tests the model with a hypothetical input.
	def test_network(self):
		sample = np.zeros((1, self.categ_num, self.categ_length))
		sample[0] = self.train_data[-1]
		ans = self.model.predict(sample)
		print(ans)