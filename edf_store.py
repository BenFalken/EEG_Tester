## Firebase interface

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class EDF_Store:
	def __init__(self, files_with_categs, filenames, categ_names):
		self.files_with_categs = files_with_categs
		self.filenames = filenames
		self.categ_names = categ_names
		self.fetched_data = {}
		self.test_user_ids = []
		self.test_users = []
		cred = credentials.Certificate('/Users/benfalken/Desktop/eeg-files-firebase-adminsdk-qhviy-20a3bd6b70.json')
		firebase_admin.initialize_app(cred, {
		    'databaseURL': 'https://eeg-files.firebaseio.com'
		})
		self.db = firestore.client()
		self.test_users_db = self.db.collection(u'test-users')
	# Record all the selected files in firebase
	def record_data(self):
		for user_id in self.filenames:
			user = self.test_users_db.document(user_id)
			all_data = {}
			for categ in self.categ_names:
				x = self.files_with_categs[user_id]['x']
				y = self.files_with_categs[user_id]['categs'][categ]
				data = {}
				for i in range(x.size):
					data[str(x[i])] = y[i]
				all_data[categ] = data
			user.set(all_data)
	# Fetch all files from firebase
	def fetch_data(self):
		self.test_users_stream = self.test_users_db.stream()
		for user in self.test_users_stream:
			self.test_user_ids.append(user.id)
			self.test_users.append(user.to_dict())
