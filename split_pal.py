#! /usr/bin/env python
"""
Program used to split a .pal file generated by makeblastdb into several smaller pals that can be psiBLASTed against.
Creates a file called all_pal_files.txt listing the names of the split pals to be used for psiblasting
"""

from sys import stdin, stdout

line_list = []
for line in stdin:
    line_list.append(line.rstrip())

default_start = ''
for i in range(len(line_list)):
    if i < 3:
        default_start += line_list[i] + '\n'


volume_section = {}
counter = 0

temp_list = []
for volume in line_list[4].split(" ")[1:]:
    temp_list.append(volume)
    num = int(volume.split('.')[-1])
    if num == 0:
        pass
    elif num % 250 == 0:
        volume_section[counter] = temp_list
        temp_list = []
        counter += 1
    elif volume == line_list[4].split(" ")[-1]:
        volume_section[counter] = temp_list

title_list = []

for key in volume_section.keys():
    title = line_list[3].split(' ')[1].split('/')[-1] + str(key)
    title_list.append(title)
    data = default_start
    data += 'TITLE ' + title + '\n'
    data += 'DBLIST'
    for item in volume_section[key]:
        data += ' ' + item
    data += '\n'
    f = open(title + '.pal', 'w')
    f.write(data)
    f.close()

titles = ""
for title in title_list:
    titles += title + '\n'

f = open('all_pal_names.txt', 'w')
f.write(titles)
f.close()

