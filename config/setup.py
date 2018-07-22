from .data import *
import shutil


def initiate():
    clear_job_dir()


def clear_job_dir():
    '''
    Deletes job directory if specified
    '''
    if not PERSIST_JOBS:
        shutil.rmtree(JOBS_FOLDER, ignore_errors=True)
