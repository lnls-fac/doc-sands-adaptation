paper: sands-adaptation.pdf
	okular sands-adaptation.pdf

clean:
	make -C Figures clean
	rm -rf *.aux *.log *.dvi *.pdf *.ps

sands-adaptation.pdf: svg2pdf header.tex sands-adaptation.tex Symbols.tex Chapter_1/* Chapter_2/* Chapter_3/* Chapter_4/* Chapter_5/* Figures/*
	pdflatex sands-adaptation.tex
	pdflatex sands-adaptation.tex


svg2pdf:
	make -C Figures


