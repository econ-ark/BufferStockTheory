# -*- mode: sh; sh-shell: bash; -*-
# Google 'latexmk latexmkrc' for explanation of this config file
# or see https://mg.readthedocs.io/latexmk.html
# 
# latexmk at unix command line will compile the paper
# econ-ark-tools' BibTeX wrapper, as in the root .latexmkrc: system.bib and BufferStockTheory.bib
# (Appendices/BufferStockTheory.bib links to the root's) share keys, so BibTeX reports 'Repeated
# entry' errors that would stop latexmk; the wrapper drops only those and passes any other error through
do './@resources/latexmk/latexmkrc/latexmkrc_using_bibtex_wrapper';
$do_cd = 1;
$clean_ext = "bbl nav out snm dvi idv mk4 css cfg tmp xref 4tc out aux log fls fdb_latexmk synctex.gz toc svg png html 4ct ps out.ps upa upb lg yml css out bib\-save*";
$bibtex_use=2;
$pdf_mode = 1;
$rc_report = 1;
$ENV{'BSTINPUTS'} = './@resources/texlive/texmf-local/bibtex/bst:' . ($ENV{'BSTINPUTS'} || '');  # BibTeX finds .bst styles through BSTINPUTS, not BIBINPUTS
$pdflatex="pdflatex -interaction=nonstopmode %O %S";
$aux_out_dir_report = 1;
$silent  = 0;
$bibtex_use_original_exit_codes = 0;
