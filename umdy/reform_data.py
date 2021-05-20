import sys

import json, os, time, random, shutil
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import re
from bs4 import BeautifulSoup
folder='/home/shuo/Documents/AI_learning/umdy/interagted_file/'
file_name=os.listdir(folder)
