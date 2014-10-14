

default: clean

clean:
	rm *~ project1.log project1.aux project1.pdf

paper: 
	pdflatex -shell-escape project1.tex

view: paper
	okular project1.pdf
