#!/usr/bin/env python

"""
	File: controller.py
	Date: 17/04/2017
	Author: Okusanya David
"""

from model import Model
from view import View
import logging, sys
from PySide.QtGui import *
from PySide.QtCore import *

class Controller():
	def __init__(self):
		self._logger = logging.getLogger(__name__)
		self.app = QApplication(sys.argv)
		self._logger.info("Starting Model")
		self.model = Model()
		self._logger.info("Starting View")
		self.view = View(self)
	
	def add_new_task(self, st):
		task = self.model.add_task(st)
		self.view.display_added_task(task)

	def delete_task(self, st):
		taskid = self.model.delete_task(st)
		self.view.redraw_task_box(taskid)

	def set_task_done(self, st):
		task = self.model.set_task_done(st)
		self.view.display_done_task(task)

	def start(self):
		return self.app.exec_()

	def save(self):
		self.model.saveDB()

	def update_task_progress(self, taskid, val):
		self.model.update_task(val, taskid)

	def load(self):
		tasks = self.model.loadDB()
		self.view.populate_ui(tasks)