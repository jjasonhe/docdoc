import os
import csv
from tkinter import *
from tkinter import filedialog
import PyPDF2
import regex as re

re00 = re.compile(r'(?<=CLIA#:).*?(?=Laboratory Director:)') # CLIA
re01 = re.compile(r'(?<=Laboratory Director:).*?(?=PAGE:)') #Laboratory Director
re02 = re.compile(r'(?<=NAME:).*?(?=COLLECTED:)') # Name
re03 = re.compile(r'(?<=PATIENT ID#:).*?(?=RECEIVED:)') # Patient ID
re04 = re.compile(r'(?<=ACCESSION #:).*?(?=REPORTED:)') # Accession
re05 = re.compile(r'(?<=DOB:).*?(?=COLLECTED BY:)') # DOB
re06 = re.compile(r'(?<=COLLECTED:).*?(?=PATIENT ID#:)') # Collected Date
re07 = re.compile(r'(?<=RECEIVED:).*?(?=ACCESSION #:)') # Received Date
re08 = re.compile(r'(?<=REPORTED:).*?(?=DOB:)') # Reported Date
re09 = re.compile(r'(?<=COLLECTED BY:).*?(?=TEST PERFORMED:)') # Collected By
re10 = re.compile(r'(?<=TEST PERFORMED:).*?(?=REPORTED DATE:)') # Test Performed
re11 = re.compile(r'(?<=REPORTED DATE:).*?(?=PROVIDER NAME)') # ! Reported Date
re12a = re.compile(r'(?<=PROVIDER NAME .NPI.:).*?(?=..LAB)') # ! Provider Name
re12b = re.compile(r'(?<=PROVIDER NAME .NPI.:).*?(?=LAB)') # ! Provider Name
re13 = re.compile(r'(?<=REF. RANGE)\d*?(?= )') # ! Lab Number
re14 = re.compile(r'(?<=\d\d\s\s\s).*?(?=\s\s)') # ! Observation
re15 = re.compile(r'(?<=\s)(?:Non Reactive|Reactive|Negative|Positive|Indeterminate|>|<|\d\.).*?(?=\s\s)') # ! Result
re16a = re.compile(r'(?<=Performing Laboratory Information:).*?(?=Abnormal Diagnosis Codes)') # ! Lab Info
re16b = re.compile(r'(?<=Performing Laboratory Information:).*?(?=This document contains private)') # ! Lab Info
re17 = re.compile(r'(?<=Abnormal Diagnosis Codes).*?(?=This document contains private)') # ! Abnormal Codes
re18 = re.compile(r'No specimen for Requested Test') # X No specimen, no test results
re19 = re.compile(r'(?<=Hep B Surface Ab, Qual).*(?:Non Reactive|Reactive)(?=Non)') # Non Reactive / Reactive specific check

def parse(filepath):
	# open pdf
	pdf = open(filepath, 'rb')
	# initialize reader
	rdr = PyPDF2.PdfFileReader(pdf)
	# fetch number of pages
	pgs = rdr.numPages
	# prepare csv
	txtpath = filepath[:-3] + 'txt'
	ft = open(txtpath, 'a+')
	csvpath = filepath[:-3] + 'csv'
	fc = open(csvpath, 'w', newline='')
	fn = ['CLIA#',
	      'Laboratory Director',
	      'NAME',
	      'PATIENT ID#',
	      'ACCESSION #',
	      'DOB',
	      'COLLECTED',
	      'RECEIVED',
	      'REPORTED',
	      'COLLECTED BY',
	      'TEST PERFORMED',
	      'REPORTED DATE',
	      'PROVIDER NAME (NPI)',
	      'LAB',
	      'OBSERVATION',
	      'RESULT',
	      'Performing Laboratory Information',
	      'Abnormal Diagnosis Codes',
	      'Notes']
	writer = csv.DictWriter(fc, fieldnames=fn)
	writer.writeheader()

	for i in range(pgs):
		row = {}
		p = rdr.getPage(i)
		t = p.extractText()

		ft.write(t)
		ft.write('\n\n')

		m = re00.search(t)
		if m:
			row[fn[0]] = m[0].strip()
		else:
			row[fn[0]] = ''

		m = re01.search(t)
		if m:
			row[fn[1]] = m[0].strip()
		else:
			row[fn[1]] = ''

		m = re02.search(t)
		if m:
			row[fn[2]] = m[0].strip()
		else:
			row[fn[2]] = ''

		m = re03.search(t)
		if m:
			row[fn[3]] = m[0].strip()
		else:
			row[fn[3]] = ''

		m = re04.search(t)
		if m:
			row[fn[4]] = m[0].strip()
		else:
			row[fn[4]] = ''

		m = re05.search(t)
		if m:
			row[fn[5]] = m[0].strip()
		else:
			row[fn[5]] = ''

		m = re06.search(t)
		if m:
			row[fn[6]] = m[0].strip()
		else:
			row[fn[6]] = ''

		m = re07.search(t)
		if m:
			row[fn[7]] = m[0].strip()
		else:
			row[fn[7]] = ''

		m = re08.search(t)
		if m:
			row[fn[8]] = m[0].strip()
		else:
			row[fn[8]] = ''

		m = re09.search(t)
		if m:
			row[fn[9]] = m[0].strip()
		else:
			row[fn[9]] = ''

		m = re10.search(t)
		if m:
			row[fn[10]] = m[0].strip()
		else:
			row[fn[10]] = ''

		# Check if "no specimen"
		m = re18.search(t)
		if m:
			row[fn[18]] = m[0].strip()
			row[fn[11]] = ''
			row[fn[12]] = ''
			row[fn[13]] = ''
			row[fn[14]] = ''
			row[fn[15]] = ''
			row[fn[16]] = ''
			row[fn[17]] = ''
		else:
			row[fn[18]] = ''
			n = re11.search(t)
			if n:
				row[fn[11]] = n[0].strip()
			else:
				row[fn[11]] = ''
			n = re12a.search(t)
			if not n:
				n = re12b.search(t)
			if n:
				row[fn[12]] = n[0].strip()
			else:
				row[fn[12]] = ''
			n = re13.search(t)
			if n:
				row[fn[13]] = n[0].strip()
			else:
				row[fn[13]] = ''
			n = re16a.search(t)
			if not n:
				n = re16b.search(t)
			if n:
				row[fn[16]] = n[0].strip()
			else:
				row[fn[16]] = ''
			n = re17.search(t)
			if n:
				row[fn[17]] = n[0].strip()
			else:
				row[fn[17]] = ''
			n = re14.findall(t)
			n = [i.strip() for i in n]
			n = [j for j in n if len(j) != 0]
			if n:
				row[fn[14]] = n[0]
			else:
				row[fn[14]] = ''
			n = re15.findall(t)
			n = [i.strip() for i in n]
			n = [j for j in n if len(j) < 20]
			if n:
				row[fn[15]] = n[0]
			else:
				n = re19.search(t)
				if n:
					row[fn[15]] = n[0].strip()
				else:
					row[fn[15]] = ''
		writer.writerow(row)
	ft.close()
	fc.close()
	return csvpath

# parse('hbt.pdf')


top = Tk()

def loadCallBack():
	top.filename = filedialog.askopenfilename(title='Select pdf to parse',
							   				  filetypes=[("pdf",'*.pdf')])
	print(top.filename)

# def textCallBack():
# 	top.txtpath = create_text(top.filename)
# 	print(top.txtpath)

def csvCallBack():
	# top.csvpath = parse_text(top.txtpath)
	top.csvpath = parse(top.filename)
	print(top.csvpath)

Bload = Button(top, text='LOAD PDF', command=loadCallBack, justify=CENTER, width=16, relief=RAISED)
Bload.place(relx=0.5, rely=0.4, anchor=CENTER)

# Btext = Button(top, text='CREATE TXT', command=textCallBack, justify=CENTER, width=16, relief=RAISED)
# Btext.place(relx=0.5, rely=0.5, anchor=CENTER)

Bcsv = Button(top, text='GENERATE CSV', command=csvCallBack, justify=CENTER, width=16, relief=RAISED)
Bcsv.place(relx=0.5, rely=0.6, anchor=CENTER)

top.title("docdoc")
top.mainloop()
