paper: sands-adaptation.pdf
	okular sands-adaptation.pdf

clean:
	rm -rf *.aux *.log *.dvi *.pdf *.ps

#comment out block of code below if you want to compile only individual sections
sands-adaptation.pdf: header.tex sands-adaptation.tex Symbols.tex Chapter_1/* Chapter_2/* Chapter_3/* Chapter_4/* Chapter_5/* Figuras/*
	pdflatex sands-adaptation.tex
	pdflatex sands-adaptation.tex

#To compile individual sections uncomment below and add the section path
#sands-adaptation.pdf: <path_to_section>
#	pdflatex <path_to_section>.tex
#	pdflatex <path_to_section>.tex
