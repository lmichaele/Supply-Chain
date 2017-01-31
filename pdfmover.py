import shutil, os

source = 'G:\\Supply Chain\\Warehouse\\Stocktake\\Stocktake Variance Reports'
dest = 'G:\\Supply Chain\\Warehouse\\Stocktake\\Variance Archives'

files = os.listdir(source)

for f in files:
    if f.endswith('.pdf'):
        shutil.move(f, dest)
