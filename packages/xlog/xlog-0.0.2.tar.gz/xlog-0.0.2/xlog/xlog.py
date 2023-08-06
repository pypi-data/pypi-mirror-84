import argparse, sys, os
from loguru import logger as logu



def init(p_name,p_path,p_level):
    file_name = p_name + "_" + p_level + ".log"
    file_path = p_path + file_name
    fmt = "{time:YYYY-MM-DD-HH:mm:ss}  |  {level}  |  {message}"
    logu.add(file_path, level=p_level, format=fmt)

def logger(message):
    logu.info(message)

init('16s','./','INFO')
logger('This is a test!')