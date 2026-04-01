ifdef FILEPATH
    FOLDER := $(patsubst %/,%,$(dir $(FILEPATH)))
    FILE   := $(notdir $(FILEPATH))
endif

paper: sands-adaptation.pdf
	okular sands-adaptation.pdf

clean:
	rm -rf *.aux *.log *.dvi *.pdf *.ps *.out
	rm -rf */*.aux */*.log */*.dvi */*.pdf */*.ps */*.out

sands-adaptation.pdf: header.tex sands-adaptation.tex Symbols.tex Chapter_1/* Chapter_2/* Chapter_3/* Chapter_4/* Chapter_5/* Figuras/*
	pdflatex sands-adaptation.tex
	pdflatex sands-adaptation.tex

# Example of use: make section FILEPATH=Chapter_1/1_01_OpeningRemarks.tex 
section:
ifndef FILEPATH
	$(error FILEPATH is not set. Usage: make section FILEPATH=<folder>/<file>)
endif
	cd $(FOLDER) && pdflatex $(FILE) && pdflatex $(FILE)
