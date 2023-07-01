JOB = thesis

.PHONY: FORCE
$(JOB).pdf: FORCE
	latexmk -xelatex -latexoption="-shell-escape" $(JOB) 
	rm *.aux *.log *.out  *.bbl *.blg

.PHONY: clean
clean:
	rm -f *~ *bak *.ps *.pdf *.dvi *.log *.aux *.out *.nav *.snm *.toc *.vrb *.bbl *.blg *.lof *.lot *.fdb_latexmk *.fls
	rm -f **/*.aux
