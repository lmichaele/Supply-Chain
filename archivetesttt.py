import os

path = r'G:\Supply Chain\Customer Database\CID archive'
xsize = 1000

print('List files bigger than' + str(xsize) + 'bytes')
print('================' + '=' * len(str(xsize)) + '==='
for root, dirs, files in os.walk(path):
    for name in files:
        filename = os.path.join(root, name)
        if os.stat(filename).st_size > xsize:
            print(filename)
