ALL_FIGS = $(shell find ./ -name "*.svg" | sed 's/\.svg$$/.pdf/')

all: $(ALL_FIGS)

clean:
	find ./ -name *.pdf -exec rm -f {} \;

%.pdf: %.svg
	inkscape $< --export-type=pdf --export-filename=$@

