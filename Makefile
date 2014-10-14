

default: clean

clean:
	rm *~ *.log *.aux  *.out

#twice so we can find the right references
paper: 
	pdflatex -shell-escape project1.tex
	pdflatex -shell-escape project1.tex

view: paper
	okular project1.pdf
