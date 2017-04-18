#!/usr/bin/env python

"""
	File: model.py
	Date: 17/04/2017
	Author: Okusanya David
"""
import logging, random, pickle

tasks_db_file = 'tasks.db'

class Model():


	def __init__(self):
		self._logger = logging.getLogger(__name__)
		self._logger.info("Setting up tasks database")
		self.tasks_db_file_path = self._findDBfiles(tasks_db_file)
		self.isDBloaded = False
		self.tasks = self.loadDB()

	def _findDBfiles(self, filename):
		self._logger.info("Finding database file")
		import os
		for root, dirs, files in os.walk(os.getcwd()):
			for file in files:
				if file.endswith(".db") and file == filename:
					return(os.path.join(root,file))

	def add_task(self, st):
		single_task = {}
		single_task['id'] = random.randint(0, 400)
		single_task['desc'] = st
		single_task['done'] = False
		single_task['recentDeleted'] = False
		single_task['percentDone'] = 0
		self.tasks.append(single_task)
		self._logger.info("Adding new task")
		return single_task

	def _get_task(self, st):
		return [item for item in self.tasks if item['id'] == st][0]
 
	def set_task_done(self, st):
		task = self._get_task(st)
		task['done'] = True
		task['recentDeleted'] = True
		return task

	def delete_task(self, st):
		task = self._get_task(st)
		taskid = task['id']
		del self.tasks[self.tasks.index(task)]
		self._logger.info("Deleting task")
		return taskid

	def saveDB(self):
		self._logger.info("Saving to database")
		file = open(self.tasks_db_file_path, 'wb')
		pickle.dump(self.tasks, file)
		file.close()

	def update_task(self, val, st):
		self._logger.info("Updating progess")
		task = self._get_task(st)
		task['percentDone'] = val

	def loadDB(self):
		if self.isDBloaded == False:
			self._logger.info("Loading database")
			file = open(self.tasks_db_file_path, 'rb')
			obj = None
			try:
				obj = pickle.load(file)
			except(EOFError):
				self._logger.debug("File is empty")
				self._logger.info("File is initially empty")
				obj = []
			file.close()
			self.isDBloaded = True
			return obj
			
