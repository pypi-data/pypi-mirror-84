import json
from datetime import datetime
import re
import uuid
import inspect
import os
import csv
import logging

# import pymongo


logger = logging.getLogger('frog_lib')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

def debug(message):
    "Automatically log the current function details."
    # Get the previous frame in the stack, otherwise it would
    # be this function!!!
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logging.debug("%s: %s in %s:%i" % (
        message,
        func.co_name,
        func.co_filename,
        func.co_firstlineno
    ))

def get_timestamp():
    return datetime.timestamp(datetime.now())

def read_json(path):
    d = []
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    return d

def write_json(path, data):
    with open(path, 'w', encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)
    return True


def write_file(filename, data):
    with open(filename, 'w', encoding="utf-8") as f:
        f.write(data)
    return True

def fwrite_file(filename, data):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding="utf-8") as f:
        f.write(data)
    return True

def write_fileb(filename,data):
    with open(filename, 'wb') as f:
        f.write(data)
    return True

def write_csv(filename, data, quotechar='\''):
    with open(filename, mode='w', encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=',', quotechar=quotechar, quoting=csv.QUOTE_MINIMAL)

        for r in data:
            writer.writerow(r)

def write_csvb(filename, data, quotechar='\''):
    with open(filename, mode='wb') as f:
        writer = csv.writer(f, delimiter=',', quotechar=quotechar, quoting=csv.QUOTE_MINIMAL)

        for r in data:
            writer.writerow(r)

def read_csv(filename):
    with open(filename, mode='r', encoding="utf-8") as f:
        csv_reader = csv.DictReader(f)
        # line_count = 0
        data = []
        for row in csv_reader:
            data.append(row)
        return data

# For compatibility
def clean_text(text):
    if text == None:
        return None

    x = text.strip()
    if x:
        return x
    return text

# TODO: Remove clean_text
def strip(text):
    if text == None:
        return None

    x = text.strip()
    if x:
        return x
    return text

def sleep(time=None):
    if time is not None:
        sleep(time)
        return



def test():
	debug('test')
	write_json("test.json", [{"abc":"def"}])
	write_file("test.txt", "blabla")
	fwrite_file("test/test.file", "abcd")
	write_fileb("bytes.txt",b"bytes")
	write_csv("csv.csv", [[1,2,3],[4,5,6]], quotechar='\'')
	write_csvb("csvb.csv", [], quotechar='\'')
	read_csv("csv.csv")
	clean_text("    abcde    ")
	strip("    abcde    ")
	sleep(3)


def main():
	logger.debug("main")

main()
