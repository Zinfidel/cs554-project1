

default: clean

clean:
	rm *~ *.log *.aux 

paper: 
	pdflatex -shell-escape project1.tex

view: paper
	okular project1.pdf
