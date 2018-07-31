import os
import csv
from tkinter import *
from tkinter import filedialog
import PyPDF2
import regex as re

re00 = re.compile(r'(?<=CLIA#:).*?(?=Laboratory Director:)')
re01 = re.compile(r'(?<=Laboratory Director:).*?(?=PAGE:)')
re02 = re.compile(r'(?<=NAME:).*?(?=COLLECTED:)')
re03 = re.compile(r'(?<=PATIENT ID#:).*?(?=RECEIVED:)')
re04 = re.compile(r'(?<=ACCESSION #:).*?(?=REPORTED:)')
re05 = re.compile(r'(?<=DOB:).*?(?=COLLECTED BY:)')
re06 = re.compile(r'(?<=COLLECTED:).*?(?=PATIENT ID#:)')
re07 = re.compile(r'(?<=RECEIVED:).*?(?=ACCESSION #:)')
re08 = re.compile(r'(?<=REPORTED:).*?(?=DOB:)')
re09 = re.compile(r'(?<=COLLECTED BY:).*?(?=TEST PERFORMED:)')
re10 = re.compile(r'(?<=TEST PERFORMED:).*?(?=REPORTED DATE:)')
re11 = re.compile(r'(?<=REPORTED DATE:).*?(?=PROVIDER NAME)')
re12a = re.compile(r'(?<=PROVIDER NAME .NPI.:).*?(?=..LAB)')
re12b = re.compile(r'(?<=PROVIDER NAME .NPI.:).*?(?=LAB)')
re13 = re.compile(r'(?<=REF. RANGE)\d*?(?= )')
# re14 = re.compile(r'') # OBSERVATION
# re15 = re.compile(r'') # RESULT
re16a = re.compile(r'(?<=Performing Laboratory Information:).*?(?=Abnormal Diagnosis Codes)')
re16b = re.compile(r'(?<=Performing Laboratory Information:).*?(?=This document contains private)')
re17 = re.compile(r'(?<=Abnormal Diagnosis Codes).*?(?=This document contains private)')
re18 = re.compile(r'No specimen for Requested Test')

def parse(filepath):
	# open pdf
	pdf = open(filepath, 'rb')
	# initialize reader
	rdr = PyPDF2.PdfFileReader(pdf)
	# fetch number of pages
	pgs = rdr.numPages
	# prepare csv
	csvpath = filepath[:-3] + 'csv'
	f = open(csvpath, 'w', newline='')
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
	writer = csv.DictWriter(f, fieldnames=fn)
	writer.writeheader()

	for i in range(pgs):
		row = {}
		p = rdr.getPage(i)
		t = p.extractText()

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

		m = re11.search(t)
		if m:
			row[fn[11]] = m[0].strip()
		else:
			row[fn[11]] = ''

		m = re12a.search(t)
		if not m:
			m = re12b.search(t)
		if m:
			row[fn[12]] = m[0].strip()
		else:
			row[fn[12]] = ''

		m = re13.search(t)
		if m:
			row[fn[13]] = m[0].strip()
		else:
			row[fn[13]] = ''

		# m = re14.search(t)
		# if m:
		# 	row[fn[14]] = m[0].strip()
		# else:
		# 	row[fn[14]] = ''

		# m = re15.search(t)
		# if m:
		# 	row[fn[15]] = m[0].strip()
		# else:
		# 	row[fn[15]] = ''

		m = re16a.search(t)
		if not m:
			m = re16b.search(t)
		if m:
			row[fn[16]] = m[0].strip()
		else:
			row[fn[16]] = ''

		m = re17.search(t)
		if m:
			row[fn[17]] = m[0].strip()
		else:
			row[fn[17]] = ''

		m = re18.search(t)
		if m:
			row[fn[18]] = m[0].strip()
		else:
			row[fn[18]] = ''

		writer.writerow(row)
	return

parse('hbt.pdf')
