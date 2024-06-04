import numpy as np
import pandas as pd
from matplotlib import pyplot as pyplot
import seaborn as sns

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def load_spreadsheet(filename):
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(filename, scope)
    gc = gspread.authorize(credentials)
