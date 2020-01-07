import math
import time
import datetime
import csv

import pandas as pd


def getText():
    result = []
    with open('notin.txt', 'r',encoding='utf-8') as f:
        for line in f:
            result.append(list(line.strip('\n').split(',')))
    print(result)

getText()
