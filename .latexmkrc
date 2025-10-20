# -*- mode: sh; sh-shell: bash; -*-
# Google 'latexmk latexmkrc' for explanation of this config file
# or see https://mg.readthedocs.io/latexmk.html
# 
# latexmk at unix command line will compile the paper
system("[[ -e economics.bib         ]] && rm -f economics.bib"        );
system("[[ -e BufferStockTheory.bib ]] && rm -f BufferStockTheory.bib");
system("[[ -e latexdefs.tex         ]] && rm -f latexdefs.tex");
$bibtex = 'bibtex %O %S > /dev/null 2>&1'; # suppress annoying warnings about dups
$do_cd = 1;
$clean_ext = "bbl nav out snm dvi idv mk4 css cfg tmp xref 4tc out aux log fls fdb_latexmk synctex.gz toc svg png html 4ct ps out.ps upa upb lg yml css out snm bib\-save*";
$bibtex_use=2;
$pdf_mode = 1;  # Use pdflatex to generate PDF
$rc_report = 1;
#@default_files = ('BufferStockTheory','BufferStockTheory-NoAppendix','BufferStockTheory-Slides','Introduction');
@default_files = ('BufferStockTheory');
$root_filename = 'BufferStockTheory.tex'; 
$ENV{'BIBINPUTS'} = './@resources/texlive/texmf-local/bibtex/bst:' . ($ENV{'BIBINPUTS'} || '');
$pdflatex="pdflatex -interaction=nonstopmode %O %S";
$aux_out_dir_report = 1;
$silent  = 0;
$bibtex_use_original_exit_codes = 0;
system("\@resources/shell/bibtool_extract-used-refs-from-system-bib-and-add-refs.sh . BufferStockTheory");
system("find . -name '*.dep' ! -name 'BufferStockTheory.dep' -delete");

# Create a wrapper shell script
$wrapper_script = '.latexmk_wrapper.sh';
open(my $fh, '>', $wrapper_script) or die "Could not open file '$wrapper_script' $!";
print $fh <<'END_SCRIPT';
#!/bin/bash
perl -e '
sub run_pdftotext {
    foreach my $file (@ARGV) {
        my $pdf_file = "$file.pdf";
        my $txt_file = "$file.pdftotext";
        
        if (-f $pdf_file) {
            print "Running pdftotext on $pdf_file...\n";
            system("/usr/local/bin/pdftotext", $pdf_file, $txt_file);
            print "Converted $pdf_file to $txt_file\n";
        } else {
            print "PDF file $pdf_file not found\n";
        }
    }
}

run_pdftotext(@ARGV);
' "$@"
END_SCRIPT
close $fh;
chmod 0755, $wrapper_script;

# Set the success command to use the wrapper script
$success_cmd = "./$wrapper_script @default_files";

$compiling_cmd = 'echo "Compiling..."';
