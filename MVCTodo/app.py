#!/usr/bin/env python

"""
	File: app.py
	Date: 17/04/2017
	Author: Okusanya David
	Attribution: <div>Icons made by <a href="http://www.flaticon.com/authors/google" 
				title="Google">Google</a> from <a href="http://www.flaticon.com" 
				title="Flaticon">www.flaticon.com</a> is licensed by 
				<a href="http://creativecommons.org/licenses/by/3.0/" 
				title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>

"""

import logging, sys
from pathlib import Path
from controller import Controller
from PySide.QtGui import *
from PySide.QtCore import *

logger = logging.getLogger('')
logger.setLevel(logging.INFO)

fh = logging.FileHandler('run.log', 'w', 'utf-8')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(' - %(name)s - %(levelname)-8s: %(message)s')

fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)


if __name__=='__main__':
	try:
		app = Controller()
		ret = app.start()
		sys.exit(ret)
	except NameError:
		logger.debug("Name Error:", sys.exc_info()[1])
	except SystemExit:
		logger.info("Closing Window..")