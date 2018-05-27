all: memoria.pdf

transparencias.pdf: transparencias.md
	pandoc -t beamer $^ -o $@

memoria.pdf: memoria.md
	pandoc $^ -o $@ --filter pandoc-citeproc
