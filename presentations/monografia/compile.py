#!/usr/bin/python3.4
from subprocess import call 
import sys

arquivo = 'monografia'

call('pdflatex ' + arquivo, shell = True) 

if len(sys.argv) > 1: 
    call('bibtex ' + arquivo, shell = True)
    call('makeglossaries ' + arquivo, shell = True)
    call('pdflatex ' + arquivo, shell = True) 

call('qpdfview ' + arquivo + '.pdf', shell = True)
