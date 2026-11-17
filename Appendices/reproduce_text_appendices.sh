#!/bin/bash

[[ -e reproduce_text_appendices.log ]] && rm reproduce_text_appendices.log

# Create pdf using latexmk if it does not exist
for tex in *.tex; do
    filename="${tex%.*}"
    echo processing $filename
    pdf="$filename.pdf"
    if [[ ! -e "$pdf" ]]; then
	cmd="latexmk $tex"
	echo "$pdf does not exist; processing with latex command $cmd"
	eval "$cmd"
    fi
    pdftotext -nopgbrk "$pdf" "$filename.pdftotext"
    grep -I -ns '??' --include=$filename.pdftotext * >> reproduce_text_appendices.log
done

if [[ -e reproduce_text_appendices.log ]]; then
    echo ''
    echo 'These files have failed references when compiling as standalone:'
    echo ''
    cat reproduce_text_appendices.log
fi

rm -f *.pdftotext
