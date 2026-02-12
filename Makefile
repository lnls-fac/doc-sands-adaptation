all:
	latexmk -c
	latexmk -pdf sands-adaptation.tex
	latexmk -c
