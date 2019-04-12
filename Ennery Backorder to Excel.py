from tabula import wrapper

import pandas as pd
import numpy as np 

from datetime import timedelta, datetime

import tkinter as tk
from tkinter import filedialog

import re, shutil 

tkroot = tk.Tk()
tkroot.withdraw()
file = filedialog.askopenfilename()

df = wrapper.read_pdf(file, pages='all', error_bad_lines=False)

print(df)

writer = pd.ExcelWriter('output.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()
