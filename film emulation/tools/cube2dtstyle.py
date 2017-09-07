#!/usr/bin/env python3

import sys
import re
import os
import subprocess
import numpy as np
import xml.etree.ElementTree as et

level=4  # hald4
#level=5  # hald5
cube_size=level*level
image_size=level*level*level

file_name_cube=None
if len(sys.argv)==2:
    m=re.compile('^.*\.cube$', re.IGNORECASE).match(sys.argv[1])
    if m:
        file_name_cube=m.string

if file_name_cube==None:
    print('usage: {} input.cube'.format(sys.argv[0]))
    sys.exit(0)
    
name=re.compile('\.cube$').sub(lambda x: '', file_name_cube)
print('\ngenerating darktable style from cube syle »{}«'.format(name))
hald_name_png='hald{}.png'.format(level) 
hald_name_pfm='hald{}.pfm'.format(level) 
file_name_png='{}.png'.format(name) 
file_name_pfm='{}.pfm'.format(name)
file_name_csv='{}.csv'.format(name)
file_name_dtstyle='{}.dtstyle'.format(name)
# apply film emulation style to test image
subprocess.run([ 'gmic', hald_name_png, '-input_cube', file_name_cube,
                 '--map_clut[0]', '[1]', '-o[2]', file_name_png])
# convert result to LAB space
try:
    os.remove(file_name_pfm)
except FileNotFoundError:
    pass
# generate csv file with LAB color values of original test file and image
subprocess.run([ 'darktable-cli', file_name_png, 'to_LAB_space.xmp', file_name_pfm ])
# with film emulation applied
with open(hald_name_pfm, 'rb') as file:
    l1=file.readline()
    l2=file.readline()
    l3=file.readline()
    A=np.fromfile(file, dtype=np.dtype('f4'))
A=np.reshape(A, (image_size+2, image_size, 3))
A=A[::-1, :, :]
with open(file_name_pfm, 'rb') as file:
    l1=file.readline()
    l2=file.readline()
    l3=file.readline()
    B=np.fromfile(file, dtype=np.dtype('f4'))
B=np.reshape(B, (image_size+2, image_size, 3))
B=B[::-1, :, :]
with open(file_name_csv, 'w', encoding='utf-8') as csv_file:
    csv_file.write('name;film emulation: {}\n'.format(name))
    csv_file.write('description;fitted LUT style from G''MIC film emulation style “{}”\n'.format(name))
    csv_file.write('num_gray;{}\n'.format(2*image_size))
    csv_file.write('patch;L_source;a_source;b_source;L_reference;a_reference;b_reference\n')
    for i in range(0, image_size):
        for j in range(0, image_size):
            csv_file.write('A{:02d}B{:02d};{};{};{};{};{};{}\n'.
                           format(i, j,
                                  A[i, j, 0], A[i, j, 1], A[i, j, 2],
                                  B[i, j, 0], B[i, j, 1], B[i, j, 2]))
    # make in- and out- grays identical
    for i in range(image_size, image_size+2):
        for j in range(0, image_size):
            csv_file.write('G{:02d};{};{};{};{};{};{}\n'.
                           format(j+(i-image_size)*image_size,
                                  A[i, j, 0], A[i, j, 1], A[i, j, 2],
                                  B[i, j, 0], B[i, j, 1], B[i, j, 2]))
# remove temporary pfm file
os.remove(file_name_pfm)
# create darktable style
subprocess.run([ 'darktable-chart', '--csv', file_name_csv, '49', file_name_dtstyle ])
# remove unwanted elements from style
tree=et.parse(file_name_dtstyle)
for style in tree.findall('style'):
    n=0
    for plugin in style.findall('plugin'):
        if plugin.find('operation').text!='colorchecker' and plugin.find('operation').text!='tonecurve':
            style.remove(plugin)
        else:
            plugin.find('num').text=str(n)
            n=n+1
tree.write(file_name_dtstyle)
subprocess.run([ 'convert', file_name_png, '-scale', '1200%', file_name_png ])
