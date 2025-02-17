import os

if os.path.exists('plot_all_chacaltaya.png'):
    os.remove('plot_all_chacaltaya.png')

print('------------------')
print('WORKING CHACALTAYA')
print('------------------')

print('Processing...')
with open('0_retrieve_data.py') as file:
    exec(file.read())


print('Plotting everything...')
with open('2_live_data.py') as file:
    exec(file.read())
print('Plot generated!')
