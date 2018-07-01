import tika
import csv

tika.initVM()

from tika import parser

parsed = parser.from_file('pdf-test.pdf')
print(parsed["metadata"])
print(parsed["content"])
