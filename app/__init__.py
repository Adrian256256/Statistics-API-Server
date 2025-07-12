import os
import logging
import time
from queue import Queue
from threading import Lock
from logging.handlers import RotatingFileHandler
from flask import Flask
from app.task_runner import ThreadPool
from app.data_ingestor import DataIngestor
from app.job_counter import JobCounter

if not os.path.exists('results'):
    os.mkdir('results')

webserver = Flask(__name__)
webserver.job_counter = JobCounter()
webserver.job_queue = Queue()
# create a map for job_ids witg running/done status
webserver.job_status = {}
# create a lock for the job_counter
webserver.shutdown = False
webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.tasks_runner = ThreadPool(webserver.job_queue, webserver.job_status,
                                    webserver.data_ingestor)

webserver.tasks_runner.start()

logging_file = 'webserver.log'
if os.path.exists(logging_file):
    os.remove(logging_file)
format = '%(asctime)s - %(levelname)s - %(message)s'
# set 5 MB max size, 3 istoric files
handler = RotatingFileHandler(logging_file, maxBytes = 5 * 1024 * 1024, backupCount = 3)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(format)
formatter.converter = time.gmtime
handler.setFormatter(formatter)
webserver.logger = logging.getLogger('webserver')
webserver.logger.setLevel(logging.INFO)
webserver.logger.addHandler(handler)
webserver.logger.info('Server initialized')
from app import routes
