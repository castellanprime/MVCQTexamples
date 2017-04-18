#!/usr/bin/env python

"""
	File: view.py
	Date: 17/04/2017
	Author: Okusanya David
"""

import logging, functools
from progress import TaskProgress
from pathlib import Path
from PySide.QtGui import *
from PySide.QtCore import *

class View(QMainWindow):
	def __init__(self, controller):	
		super(View, self).__init__()
		self._logger = logging.getLogger(__name__)
		self._path = Path.cwd()
		self._menubar = self.menuBar()
		self.tasks = {}
		self.register(controller)
		self.initGUI()

	def register(self, controller):
		self._controller = controller

	def initGUI(self):
		self.setWindowTitle("TaskList App")
		#self.setGeometry(300, 300, 400, 400)	
		self.setMinimumHeight(400)
		self.setMinimumWidth(400)

		self._main_widget = QWidget()
		self._main_layout = QVBoxLayout()
		self._main_widget.setLayout(self._main_layout)
		self._main_layout.setSpacing(12)


		# Add the menu items
		self._fileMenu = self._menubar.addMenu('&File')
		exitAction = QAction('Exit', self)
		exitAction.setStatusTip('Exit Application')
		exitAction.triggered.connect(self.close)
		loadAction = QAction('Load', self)
		loadAction.setStatusTip('Load tasks')
		loadAction.triggered.connect(self._controller.load)
		saveAction = QAction('Save', self)
		saveAction.setStatusTip('Save tasks')
		saveAction.triggered.connect(self._controller.save)
		self._fileMenu.addAction(loadAction)
		self._fileMenu.addAction(saveAction)
		self._fileMenu.addAction(exitAction)

		# User input displaybox
		self._user_input_groupBox = QGroupBox("User Input")
		self._user_input_groupBox_layout = QHBoxLayout()
		self._user_input_groupBox_label = QLabel("Name")
		self._user_input_groupBox_textBox = QLineEdit()
		self._user_input_groupBox_addButton = QPushButton()
		self._user_input_groupBox_addButton.clicked.connect(self.on_add)
		
		self._user_input_groupBox_addButton.setIcon(QIcon(str(self._path) + '/images/Add.png'))
		self._user_input_groupBox_layout.addWidget(self._user_input_groupBox_label)
		self._user_input_groupBox_layout.addWidget(self._user_input_groupBox_textBox)
		self._user_input_groupBox_layout.addWidget(self._user_input_groupBox_addButton)
		self._user_input_groupBox.setLayout(self._user_input_groupBox_layout)

		# Tasks displaybox
		self._tasks_groupBox = QGroupBox("Tasks")
		self._tasks_groupBox.setStyleSheet("QGroupBox {background-color: \
			rgb(255, 255, 255), border: 3px solid rgb(0, 0, 0)}")
		self._tasks_groupBox_layout = QVBoxLayout()
		self._tasks_groupBox.setLayout(self._tasks_groupBox_layout)

		# Done displaybox
		self._done_groupBox = QGroupBox("Done")
		self._done_groupBox.setStyleSheet("QGroupBox {background-color: \
			rgb(255, 255, 255), border: 3px solid rgb(0, 0, 0)}")
		self._done_groupBox_layout = QVBoxLayout()
		self._done_groupBox.setLayout(self._done_groupBox_layout)

		# Add all the independent widgets
		self._main_layout.addWidget(self._user_input_groupBox)
		self._main_layout.addWidget(self._tasks_groupBox)
		self._main_layout.addWidget(self._done_groupBox)

		self.setCentralWidget(self._main_widget)

		self.show()

	def populate_ui(self, tasks):
		if tasks is not None:
			for item in tasks:
				if item['done'] == False:
					self.display_added_task(item)
				elif item['done'] == True:
					self.display_done_task(item)

	def _on_delete(self, taskid):
		self._logger.info("Entering on_delete")
		self._controller.delete_task(taskid)

	def redraw_task_box(self, taskid):
		self._tasks_groupBox_layout.removeWidget(self.tasks[taskid])
		self.tasks[taskid].deleteLater()
		del self.tasks[taskid]

	def _on_start(self, taskid):
		self._logger.info("Entering on_start")
		_task = self.tasks[taskid]
		_task_layout = _task.layout()
		layout_items = [_task_layout.itemAt(i).widget() for i in range(_task_layout.count())]

		for item in layout_items:
			if isinstance(item, QProgressBar):
				item.show()
				item.doAction()

	def _on_done(self, taskid, progress_bar):
		self._logger.info("Entering on_done")
		progress_bar.setStep(0)
		progress_bar.hide()
		self._controller.set_task_done(taskid)

	def display_done_task(self, task):
		_done_task_layout = QHBoxLayout()
		_done_task_iconLabel = QLabel()
		_done_task_iconLabel.setPixmap(QPixmap(str(self._path) + '/images/Ok.png'))
		_done_task_desc = QLabel(task['desc'])
		_done_task_layout.addWidget(_done_task_iconLabel)
		_done_task_layout.addWidget(_done_task_desc)
		self._done_groupBox_layout.addLayout(_done_task_layout)
		if task['recentDeleted'] == True:
			self._on_delete(task['id'])

	def on_add(self):
		self._logger.info("Entering on_add")
		if str(self._user_input_groupBox_textBox.text()):
			self._controller.add_new_task(str(self._user_input_groupBox_textBox.text()))
		else:
			QMessageBox.warning(self, "Wrong input", "You can not have an empty task!!!")

	def display_added_task(self, task):

		# Setup
		_single_task_layout = QGridLayout()
		_single_task_label = QLabel(task['desc'])
		_single_task_actionButton = QPushButton()
		_single_task_actionButton.setIcon(QIcon(str(self._path) + '/images/Action.png'))
		_single_task_doneButton = QPushButton()
		_single_task_doneButton.setIcon(QIcon(str(self._path) + '/images/Done.png'))
		_single_task_deleteButton = QPushButton()
		_single_task_deleteButton.setIcon(QIcon(str(self._path) + '/images/Delete.png'))
		_single_task_progressBar = TaskProgress()
		_single_task_progressBar.setStep(task['percentDone'])
		_single_task_progressBar.percentDone.connect(functools.partial(self._controller.update_task_progress, task['id']))

		if _single_task_progressBar.getStep() == 100:
			self._on_done(task['id'], _single_task_progressBar)

		# Add to layout 
		_single_task_layout.addWidget(_single_task_label, 1, 0)
		_single_task_layout.addWidget(_single_task_actionButton, 1, 5)
		_single_task_layout.addWidget(_single_task_doneButton, 1, 6)
		_single_task_layout.addWidget(_single_task_deleteButton, 1, 7)
		_single_task_layout.addWidget(_single_task_progressBar, 2, 0, 2, 7)
		_single_task_progressBar.hide()

		_single_task_actionButton.clicked.connect(lambda: self._on_start(task['id']))
		_single_task_deleteButton.clicked.connect(lambda: self._on_delete(task['id']))
		_single_task_doneButton.clicked.connect(functools.partial(self._on_done, task['id'], _single_task_progressBar))
		_single_task_widget = QWidget()
		_single_task_widget.setLayout(_single_task_layout)
		self.tasks[task['id']] = _single_task_widget
		self._tasks_groupBox_layout.addWidget(_single_task_widget)

	def closeEvent(self, event):
		reply = QMessageBox.question(self, 'Message',
			"Are you sure to quit?", QMessageBox.Yes | 
			QMessageBox.No, QMessageBox.No)

		if reply == QMessageBox.Yes:
			self._controller.save()
			event.accept()
		else:
			event.ignore()     