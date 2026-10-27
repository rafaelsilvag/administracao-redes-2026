TEX = atividade-dominios-virtuais.tex
PDF = atividade-dominios-virtuais.pdf
AUX = aux log out toc lof lot fls fdb_latexmk synctex.gz

.PHONY: all clean distclean

all: $(PDF)

$(PDF): $(TEX) logo.png
	pdflatex -interaction=nonstopmode -halt-on-error $(TEX)
	pdflatex -interaction=nonstopmode -halt-on-error $(TEX)

clean:
	$(foreach ext,$(AUX),rm -f atividade-dominios-virtuais.$(ext);)

distclean: clean
	rm -f $(PDF)
