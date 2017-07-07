#!/usr/bin/python3.4
from subprocess import call 
import sys

arquivo = 'article'
viewer = 'qpdfview'

result = call('pdflatex ' + arquivo, shell = True) 

if len(sys.argv) > 1: 
    call('bibtex ' + arquivo, shell = True)
    call('makeglossaries ' + arquivo, shell = True)
    call('pdflatex ' + arquivo, shell = True) 

if result == 0:
    call(viewer + ' ' + arquivo + '.pdf', shell = True)
