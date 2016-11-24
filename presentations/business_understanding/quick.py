#!/usr/bin/python3.4
from subprocess import call
import sys

arquivo = 'business_understanding'

# program to generate a presentation in latex
if len(sys.argv) > 1: 
    call('pdflatex ' + arquivo + '.tex', shell = True)
    call('bibtex ' + arquivo, shell = True)
    call('makeglossaries ' + arquivo, shell = True)
    call('pdflatex ' + arquivo + '.tex', shell = True)

call('pdflatex ' + arquivo + '.tex' + ' && ' + 'qpdfview ' + arquivo + '.pdf', shell = True)

