#!/usr/bin/env python

"""
	File: progress.py
	Date: 17/04/2017
	Author: Okusanya David
"""
import logging
from PySide.QtGui import *
from PySide.QtCore import *

class TaskProgress(QProgressBar):

	percentDone = Signal(int)

	def __init__(self, parent=None):
		super(TaskProgress, self).__init__(parent)
		self._logger = logging.getLogger(__name__)
		self._logger.info("Starting new Timer")
		self.step = 0
		self.timer = QBasicTimer()

	def setStep(self, val):
		self.step = val

	def getStep(self):
		return self.step

	def timerEvent(self, e):
		if self.step >= 100:
			self.timer.stop()
			return
		self.step = self.step + 1
		self.setValue(self.step)
		self.percentDone.emit(self.step)

	def doAction(self):
		if self.timer.isActive():
			self.timer.stop()
		else:
			self.timer.start(100, self)

