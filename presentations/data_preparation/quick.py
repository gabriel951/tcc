#!/usr/bin/python3.4
from subprocess import call
import sys

arquivo = 'data_preparation'

# program to generate a presentation in latex
call('pdflatex ' + arquivo + '.tex', shell = True)

if len(sys.argv) > 1: 
    call('bibtex ' + arquivo, shell = True)
    call('makeglossaries ' + arquivo, shell = True)
    call('pdflatex ' + arquivo + '.tex', shell = True)

call('gnome-open ' + arquivo + '.pdf', shell = True)

