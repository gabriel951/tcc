#!/usr/bin/python3.4
from subprocess import call
arquivo = 'main'

# program to generate a presentation in latex
call('pdflatex ' + arquivo + '.tex', shell = True)
call('bibtex ' + arquivo, shell = True)
call('makeglossaries ' + arquivo, shell = True)
call('pdflatex ' + arquivo + '.tex', shell = True)
call('gnome-open ' + arquivo + '.pdf', shell = True)

