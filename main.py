import os
import tika
from tika import parser
import csv
from tkinter import *
from tkinter import filedialog

def return_parsed(filepath):
	parsed = parser.from_file(filepath)
	return parsed

def create_text(filepath):
	txtpath = filepath[:-3] + 'txt'
	if (not os.path.exists(txtpath)) or (not os.path.getsize(txtpath) > 0):
		p = return_parsed(filepath)
		f = open(txtpath, 'w+')
		f.write(p["content"])
		f.close()
		return txtpath
	else:
		return txtpath

def parse_text(txtpath):
	f = open(txtpath, 'r')
	p = f.read()
	f.close()

	csvpath = txtpath[:-3] + 'csv'
	f = open(csvpath, 'w', newline='')
	fn = ['CLIA#', 'Laboratory Director', 'NAME', 'PATIENT ID#', 'ACCESSION #', 'DOB', 'COLLECTED', 'RECEIVED', 'REPORTED', 'COLLECTED BY']
	writer = csv.DictWriter(f, fieldnames=fn)
	writer.writeheader()

	table = {}

	# Skips the "Converted from ____.TMP"
	i = 0
	while not p[i-3:i] == 'TMP':
		i += 1

	tag = ''
	value = []
	while i < len(p):
		if p[i:i+6] == 'CLIA#:':
			value = ''.join(value)
			value = value.strip()
			if tag != '':
				table[tag] = value

			if len(table) != 0:
				writer.writerow(table)
				# print(table)

			tag = ''
			value = []
			i += 6
			tag += 'CLIA#'
		elif p[i:i+20] == 'Laboratory Director:':
			value = ''.join(value)
			value = value.strip()
			if tag != '':
				table[tag] = value
			tag = ''
			value = []
			i += 20
			tag += 'Laboratory Director'
		elif p[i:i+5] == 'NAME:':
			value = ''.join(value)
			value = value.strip()

			temp = []
			for j in range(0, len(value)):
				temp.append(value[j])
				if value[j+1:j+5] == 'PAGE':
					break
			temp = ''.join(temp)
			temp = temp.strip()
			temp = temp.strip('\n')

			value = temp
			temp = []

			if tag != '':
				table[tag] = value
			tag = ''
			value = []
			i += 5
			tag += 'NAME'
		elif p[i:i+12] == 'PATIENT ID#:':
			value = ''.join(value)
			value = value.strip()
			if tag != '':
				table[tag] = value
			tag = ''
			value = []
			i += 12
			tag += 'PATIENT ID#'
		elif p[i:i+12] == 'ACCESSION #:':
			value = ''.join(value)
			value = value.strip()
			if tag != '':
				table[tag] = value
			tag = ''
			value = []
			i += 12
			tag += 'ACCESSION #'
		elif p[i:i+4] == 'DOB:':
			value = ''.join(value)
			value = value.strip()
			if tag != '':
				table[tag] = value
			tag = ''
			value = []
			i += 4
			tag += 'DOB'
		elif p[i:i+10] == 'COLLECTED:':
			value = ''.join(value)
			value = value.strip()
			if tag != '':
				table[tag] = value
			tag = ''
			value = []
			i += 10
			tag += 'COLLECTED'
		elif p[i:i+9] == 'RECEIVED:':
			value = ''.join(value)
			value = value.strip()
			if tag != '':
				table[tag] = value
			tag = ''
			value = []
			i += 9
			tag += 'RECEIVED'
		elif p[i:i+9] == 'REPORTED:':
			value = ''.join(value)
			value = value.strip()
			if tag != '':
				table[tag] = value
			tag = ''
			value = []
			i += 9
			tag += 'REPORTED'
		elif p[i:i+13] == 'COLLECTED BY:':
			value = ''.join(value)
			value = value.strip()
			if tag != '':
				table[tag] = value
			tag = ''
			value = []
			i += 13
			tag += 'COLLECTED BY'
		else:
			value.append(p[i])
			i += 1
	value = ''.join(value)
	value = value.strip()
	if tag != '':
		table[tag] = value
	writer.writerow(table)
	return csvpath

top = Tk()

def loadCallBack():
	top.filename = filedialog.askopenfilename(title='Select pdf to parse',
							   				  filetypes=[("pdf",'*.pdf')])
	print(top.filename)

def textCallBack():
	top.txtpath = create_text(top.filename)
	print(top.txtpath)

def csvCallBack():
	top.csvpath = parse_text(top.txtpath)
	print(top.csvpath)

Bload = Button(top, text='LOAD PDF', command=loadCallBack, justify=CENTER, width=16, relief=RAISED)
Bload.place(relx=0.5, rely=0.35, anchor=CENTER)

Btext = Button(top, text='CREATE TXT', command=textCallBack, justify=CENTER, width=16, relief=RAISED)
Btext.place(relx=0.5, rely=0.5, anchor=CENTER)

Bcsv = Button(top, text='GENERATE CSV', command=csvCallBack, justify=CENTER, width=16, relief=RAISED)
Bcsv.place(relx=0.5, rely=0.65, anchor=CENTER)

top.title("docdoc")
top.mainloop()
