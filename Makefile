

default: clean
	rm *~ paper.log paper.aux paper.pdf

paper: 
	pdflatex -shell-escape paper.tex

view: paper
	okular paper.pdf &
