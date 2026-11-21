#!/bin/bash

# Parse command line flags
DEBUG_MODE=false
QUIET_MODE=false
NONINTERACTIVE_MODE=false

# Auto-detect noninteractive mode (no terminal or not connected to stdin)
if [[ ! -t 0 ]] || [[ ! -t 1 ]]; then
    NONINTERACTIVE_MODE=true
fi

# Parse all arguments
for arg in "$@"; do
    case $arg in
        --debug)
            DEBUG_MODE=true
            echo "🐛 DEBUG MODE ENABLED"
            ;;
        --quiet)
            QUIET_MODE=true
            echo "🔇 QUIET MODE ENABLED (using -interaction=batchmode)"
            ;;
        --noninteractive)
            NONINTERACTIVE_MODE=true
            echo "🤖 NONINTERACTIVE MODE ENABLED (no user prompts)"
            ;;
        *)
            echo "Unknown option: $arg"
            echo "Usage: $0 [--debug] [--quiet] [--noninteractive]"
            echo "  --debug: Enable debug mode with pauses and extra output"
            echo "  --quiet: Use -interaction=batchmode for silent compilation"
            echo "  --noninteractive: Disable interactive prompts (auto-detected if no terminal)"
            exit 1
            ;;
    esac
done

# Show noninteractive mode if auto-detected
if [[ "$NONINTERACTIVE_MODE" == "true" && "$*" != *"--noninteractive"* ]]; then
    echo "🤖 NONINTERACTIVE MODE AUTO-DETECTED (no terminal)"
fi

echo '' ; echo 'Reproduce text of paper:' ; echo ''

# Set up directory paths - absolute paths that work regardless of where repo is located
SCRIPT_DIR=$(dirname $(realpath $0))
ROOT_DIR=$(dirname $SCRIPT_DIR)

if [[ "$DEBUG_MODE" == "true" ]]; then
    echo "🔍 Directory Setup:"
    echo "   SCRIPT_DIR: $SCRIPT_DIR"
    echo "   ROOT_DIR: $ROOT_DIR"
    echo ""
fi

# Verify we have the expected directory structure
if [[ ! -d "$ROOT_DIR" ]]; then
    echo "❌ ERROR: Root directory $ROOT_DIR does not exist"
    exit 1
fi

if [[ ! -f "$ROOT_DIR/BufferStockTheory.tex" ]]; then
    echo "❌ ERROR: Expected file $ROOT_DIR/BufferStockTheory.tex not found"
    echo "   Are you running this script from the correct location?"
    exit 1
fi

# Global variable to store the last executed command
LAST_COMMAND=""

# Array to track files processed by pdflatex/latexmk for cleanup
declare -a PROCESSED_FILES

# Initialize commands log file with absolute path in the script directory
COMMANDS_LOG="$SCRIPT_DIR/document_commands.sh"
echo "#!/bin/bash" > "$COMMANDS_LOG"
echo "# Commands executed by reproduce/document.sh" >> "$COMMANDS_LOG"
echo "# This file can be used to replay the exact commands used for reproduction" >> "$COMMANDS_LOG"
echo "# Script directory: $SCRIPT_DIR" >> "$COMMANDS_LOG"
echo "# Root directory: $ROOT_DIR" >> "$COMMANDS_LOG"
echo "" >> "$COMMANDS_LOG"

# Function to log commands to the commands file
log_command() {
    local cmd="$1"
    local description="$2"
    echo "" >> "$COMMANDS_LOG"
    if [[ -n "$description" ]]; then
        echo "# $description" >> "$COMMANDS_LOG"
    fi
    echo "$cmd" >> "$COMMANDS_LOG"
}

# Function to set the last command (call this before executing commands)
set_last_command() {
    LAST_COMMAND="$1"
    log_command "$1" "$1"
    
    # In quiet mode with debug enabled, show the command being executed
    if [[ "$QUIET_MODE" == "true" && "$DEBUG_MODE" == "true" ]]; then
        echo ""
        echo "$1"
        echo ""
    fi
}

# Function to log and execute simple commands
log_and_execute() {
    local cmd="$1"
    local description="$2"
    log_command "$cmd" "$description"
    eval "$cmd"
}

# Helper function to check if this is a bibtex warning (exit code 2)
is_bibtex_warning() {
    local exit_code=$1
    if [[ $exit_code -eq 2 && -n "$LAST_COMMAND" && "$LAST_COMMAND" == *"bibtex"* ]]; then
        return 0  # true
    else
        return 1  # false
    fi
}

# Debug function for IMPORTANT commands - only pauses on errors
debug_pause() {
    local exit_code=$?
    local command_desc="$1"
    local log_file="$2"
    
    # If not in debug mode, just check for errors and continue
    if [[ "$DEBUG_MODE" != "true" ]]; then
        if [[ $exit_code -ne 0 ]]; then
            # Check if this is a bibtex warning (exit code 2) - can be ignored
            if is_bibtex_warning $exit_code; then
                echo "⚠️  WARNING: $command_desc returned bibtex warning (exit code 2) - continuing"
                return 0
            fi
            echo ""
            echo "❌ ERROR: $command_desc failed with exit code $exit_code"
            if [[ -n "$LAST_COMMAND" ]]; then
                echo "=== FAILED COMMAND ==="
                echo "$LAST_COMMAND"
                echo "======================="
            fi
            if [[ -n "$log_file" && -f "$log_file" ]]; then
                echo "=== LOG FILE: $log_file ==="
                tail -10 "$log_file"
            fi
            exit $exit_code
        fi
        return 0
    fi
    
    # Debug mode - if successful, just show brief message and continue
    if [[ $exit_code -eq 0 ]]; then
        echo "✅ $command_desc"
        return 0
    fi
    
    # Debug mode - check if this is a bibtex warning (exit code 2) - can be ignored
    if is_bibtex_warning $exit_code; then
        echo "⚠️  $command_desc returned bibtex warning (exit code 2) - continuing"
        return 0
    fi
    
    # Debug mode - only pause for errors
    echo ""
    echo "=========================================="
    echo "DEBUG PAUSE: $command_desc"
    echo "Exit code: $exit_code"
    echo "=========================================="
    
    echo "⚠️  COMMAND FAILED (exit code: $exit_code)"
    if [[ -n "$LAST_COMMAND" ]]; then
        echo ""
        echo "=== FAILED COMMAND ==="
        echo "$LAST_COMMAND"
        echo "======================="
    fi
    
    # In noninteractive mode, show debug info and exit
    if [[ "$NONINTERACTIVE_MODE" == "true" ]]; then
        echo "=== DEBUG INFO (NONINTERACTIVE MODE) ==="
        echo "Current directory: $(pwd)"
        echo "Recent files:"
        ls -lat | head -10
        if [[ -n "$LAST_COMMAND" ]]; then
            echo ""
            echo "=== LAST EXECUTED COMMAND ==="
            echo "$LAST_COMMAND"
            echo "================================"
        fi
        if [[ -n "$log_file" && -f "$log_file" ]]; then
            echo ""
            echo "=== LOG FILE: $log_file ==="
            tail -20 "$log_file"
        fi
        echo ""
        echo "=== RECENT PDF FILES ==="
        find . -name "*.pdf" -newermt "5 minutes ago" 2>/dev/null || echo "No recent PDF files found"
        echo ""
        echo "=== DISK USAGE ==="
        du -sh . 2>/dev/null
        echo ""
        echo "🤖 NONINTERACTIVE MODE: Exiting due to error (no user input possible)"
        exit $exit_code
    fi
    
    # Interactive mode - prompt for user choice
    while true; do
        echo ""
        echo "Options:"
        echo "  [c] Continue"
        echo "  [d] Debug (show logs/files)"
        echo "  [s] Shell (open interactive shell)"
        echo "  [q] Quit"
        read -p "Choose [c/d/s/q]: " choice
        
        case $choice in
            [Cc]* ) 
                echo "Continuing..."
                break
                ;;
            [Dd]* )
                echo "=== DEBUG INFO ==="
                echo "Current directory: $(pwd)"
                echo "Recent files:"
                ls -lat | head -10
                if [[ -n "$LAST_COMMAND" ]]; then
                    echo ""
                    echo "=== LAST EXECUTED COMMAND ==="
                    echo "$LAST_COMMAND"
                    echo "================================"
                fi
                if [[ -n "$log_file" && -f "$log_file" ]]; then
                    echo ""
                    echo "=== LOG FILE: $log_file ==="
                    tail -20 "$log_file"
                fi
                echo ""
                echo "=== RECENT PDF FILES ==="
                find . -name "*.pdf" -newermt "5 minutes ago" 2>/dev/null || echo "No recent PDF files found"
                echo ""
                echo "=== DISK USAGE ==="
                du -sh . 2>/dev/null
                echo ""
                ;;
            [Ss]* )
                echo "Opening debug shell (type 'exit' to return)..."
                echo "Current context: $command_desc"
                if [[ -n "$LAST_COMMAND" ]]; then
                    echo "Last command: $LAST_COMMAND"
                fi
                bash
                ;;
            [Qq]* )
                echo "Quitting debug session..."
                exit 1
                ;;
            * )
                echo "Please answer c, d, s, or q."
                ;;
        esac
    done
    
    # If there was an error, exit after user interaction
    if [[ $exit_code -ne 0 ]]; then
        exit $exit_code
    fi
}

# Debug function for SIMPLE commands - only pauses on errors in debug mode
debug_check() {
    local exit_code=$?
    local command_desc="$1"
    local log_file="$2"
    
    # Always check for errors (debug mode or not)
    if [[ $exit_code -ne 0 ]]; then
        # Check if this is a bibtex warning (exit code 2) - can be ignored
        if is_bibtex_warning $exit_code; then
            if [[ "$DEBUG_MODE" == "true" ]]; then
                echo "⚠️  $command_desc returned bibtex warning (exit code 2) - continuing"
            else
                echo "⚠️  WARNING: $command_desc returned bibtex warning (exit code 2) - continuing"
            fi
            return 0
        fi
        
        echo ""
        echo "❌ ERROR: $command_desc failed with exit code $exit_code"
        if [[ -n "$LAST_COMMAND" ]]; then
            echo "=== FAILED COMMAND ==="
            echo "$LAST_COMMAND"
            echo "======================="
        fi
        if [[ -n "$log_file" && -f "$log_file" ]]; then
            echo "=== LOG FILE: $log_file ==="
            tail -10 "$log_file"
        fi
        
        # In debug mode, pause for interaction on errors
        if [[ "$DEBUG_MODE" == "true" ]]; then
            echo ""
            echo "⚠️  Simple command failed - pausing for debug"
            debug_pause "$command_desc" "$log_file"
        else
            exit $exit_code
        fi
    fi
    
    # In debug mode, show brief success message for simple commands
    if [[ "$DEBUG_MODE" == "true" ]]; then
        echo "✓ $command_desc"
    fi
}

# Function to track files processed by pdflatex/latexmk for cleanup
track_processed_file() {
    local filename="$1"
    local output_dir="$2"
    local current_dir="$3"
    
    # Remove .tex extension if present
    local base_name=$(basename "$filename" .tex)
    
    # Create the path for cleanup - use output directory if specified
    local cleanup_path=""
    if [[ -n "$output_dir" && "$output_dir" != "." ]]; then
        # Special case: tikz files from Figures/ directory output to root directory  
        # but get tracked with "../." - fix this to point to root directory
        if [[ "$output_dir" == "../." || "$output_dir" == ".." ]]; then
            cleanup_path="$base_name"
        else
            cleanup_path="$output_dir/$base_name"
        fi
    else
        # If we're in a subdirectory, construct the path relative to root
        if [[ -n "$current_dir" && "$current_dir" != "." ]]; then
            cleanup_path="$current_dir/$base_name"
        else
            cleanup_path="$base_name"
        fi
    fi
    
    # Add to processed files array if not already there
    if [[ ! " ${PROCESSED_FILES[@]} " =~ " $cleanup_path " ]]; then
        PROCESSED_FILES+=("$cleanup_path")
        if [[ "$DEBUG_MODE" == "true" ]]; then
            echo "[TRACK] Tracking for cleanup: $cleanup_path" >&2
        fi
    fi
}

# Function to track bibtex files for cleanup
track_bibtex_file() {
    local filepath="$1"
    
    # Add to processed files array if not already there
    if [[ ! " ${PROCESSED_FILES[@]} " =~ " $filepath " ]]; then
        PROCESSED_FILES+=("$filepath")
        if [[ "$DEBUG_MODE" == "true" ]]; then
            echo "[BIBTEX] Tracking bibtex file for cleanup: $filepath" >&2
        fi
    fi
}

# Function to check PDF content and restore if only formatting changed
check_and_restore_pdf_if_formatting_only() {
    local pdf_file="$1"
    local description="$2"
    
    # Check if PDF exists
    if [[ ! -f "$pdf_file" ]]; then
        return 0  # Skip if PDF doesn't exist
    fi
    
    # Check if pdftotext is available
    if ! command -v pdftotext &> /dev/null; then
        if [[ "$DEBUG_MODE" == "true" ]]; then
            echo "[CONTENT] pdftotext not available - skipping content check for $pdf_file"
        fi
        return 0
    fi
    
    if [[ "$DEBUG_MODE" == "true" ]]; then
        echo "[CONTENT] Checking content changes in $pdf_file ($description)..."
    fi
    
    # Create temporary files
    local current_txt=$(mktemp)
    local committed_txt=$(mktemp)
    local committed_pdf=$(mktemp)
    
    # Extract text from current PDF
    if ! pdftotext -nopgbrk "$pdf_file" "$current_txt" 2>/dev/null; then
        rm -f "$current_txt" "$committed_txt" "$committed_pdf"
        return 0  # Skip if text extraction fails
    fi
    
    # Get the committed version of the PDF
    if ! git show "HEAD:$pdf_file" > "$committed_pdf" 2>/dev/null; then
        rm -f "$current_txt" "$committed_txt" "$committed_pdf"
        if [[ "$DEBUG_MODE" == "true" ]]; then
            echo "[CONTENT] No committed version found for $pdf_file - keeping new file"
        fi
        return 0  # Skip if no committed version
    fi
    
    # Extract text from committed PDF
    if ! pdftotext -nopgbrk "$committed_pdf" "$committed_txt" 2>/dev/null; then
        rm -f "$current_txt" "$committed_txt" "$committed_pdf"
        return 0  # Skip if committed PDF text extraction fails
    fi
    
    # Compare the text content
    if diff -q "$current_txt" "$committed_txt" > /dev/null 2>&1; then
        echo "[CONTENT] ✅ Content identical for $pdf_file ($description) - restoring committed version"
        cp "$committed_pdf" "$pdf_file"
        if [[ "$DEBUG_MODE" == "true" ]]; then
            echo "[CONTENT] Formatting-only changes discarded for $pdf_file"
        fi
        
        # Regenerate .txt files from the restored PDF to keep them in sync
        regenerate_txt_files_for_pdf "$pdf_file"
    else
        if [[ "$DEBUG_MODE" == "true" ]]; then
            echo "[CONTENT] ✏️  Content changed for $pdf_file ($description) - keeping new version"
        fi
    fi
    
    # Cleanup temporary files
    rm -f "$current_txt" "$committed_txt" "$committed_pdf"
}

# Function to regenerate .txt files from a PDF after restoration
regenerate_txt_files_for_pdf() {
    local pdf_file="$1"
    local base_name=$(basename "$pdf_file" .pdf)
    local pdf_dir=$(dirname "$pdf_file")
    
    # Create .txt file (pdftotext default output)
    local txt_file="$pdf_dir/$base_name.txt"
    if pdftotext -nopgbrk "$pdf_file" "$txt_file" 2>/dev/null; then
        if [[ "$DEBUG_MODE" == "true" ]]; then
            echo "[CONTENT] ✓ Regenerated $txt_file from restored PDF"
        fi
    fi
}

# Function to build pdflatex command with appropriate flags
build_pdflatex_cmd() {
    local output_dir="$1"
    local filename="$2"
    local extra_flags="$3"
    local current_dir="$4"
    
    # Track this file for cleanup
    track_processed_file "$filename" "$output_dir" "$current_dir"
    
    local cmd="pdflatex -halt-on-error"
    
    # Add quiet mode flag if enabled
    if [[ "$QUIET_MODE" == "true" ]]; then
        cmd="$cmd -interaction=batchmode"
    fi
    
    # Add output directory
    if [[ -n "$output_dir" ]]; then
        cmd="$cmd -output-directory=$output_dir"
    fi
    
    # Add any extra flags
    if [[ -n "$extra_flags" ]]; then
        cmd="$cmd $extra_flags"
    fi
    
    # Add filename
    cmd="$cmd $filename"
    
    echo "$cmd"
}

# Make sure tlmgr (texlive manager) is installed and initialized.
# Skip the user-tree init when a system pdflatex is already available:
# in that case we trust the system TeX install (and user policy may
# explicitly forbid a per-user texmf, e.g. ~/texmf/AGENTS.md). The
# init-usertree path is reserved for bootstrapping environments
# (e.g. Docker images) that have tlmgr but no working pdflatex yet.
if command -v pdflatex >/dev/null 2>&1; then
    echo "pdflatex available; skipping tlmgr user-tree init."
elif [[ "$(which tlmgr)" == "" ]]; then
    echo 'tlmgr is not available; install texlive and rerun'
elif [[ ! -f ~/texmf/tlpkg/texlive.tlpdb ]]; then
    echo "Initializing tlmgr user tree..."
    log_and_execute "tlmgr init-usertree" "Initialize tlmgr user tree"
else
    echo "tlmgr user tree already initialized."
fi
debug_check "tlmgr initialization"

# SCRIPT_DIR will be the absolute path to the reproduce directory
# ROOT_DIR will be the absolute path to the project root directory  
texname=BufferStockTheory
output_directory='.'

log_and_execute "cd \"$ROOT_DIR\"" "Change to main directory"
debug_check "Change to main directory: $ROOT_DIR"

# Make figures that get made by executing a latex file
# (they should have a filename ending in Make.tex)
log_and_execute "cd Figures" "Change to Figures directory"
debug_check "Change to Figures directory"

# For this paper, only the tikz figures need to be made by pdflatex - others are made by python
for fName_tikzMake in *Make.tex; do # names of all files ending in Make.tex
    echo "Processing figure $fName_tikzMake"
    fName=${fName_tikzMake%_tikzMake.tex} # Remove the '_tikzMake.tex' part of the filename
#    dep="pwd ; texliveonfly $fName_tikzMake"
#    echo dep="$dep"
#    eval "$dep"
            cmd=$(build_pdflatex_cmd "../$output_directory" "$fName_tikzMake" "--output-format pdf" "Figures")
    set_last_command "$cmd"
    eval "$cmd"
    debug_pause "Compile tikz figure: $fName_tikzMake" "../${fName}_tikzMake.log"
    
    mv_cmd="mv -f ../$output_directory/${fName}_tikzMake.pdf $fName.pdf"
    log_command "$mv_cmd" "Move compiled figure: $fName.pdf"
    set_last_command "$mv_cmd"
    mv -f                                                             "../$output_directory/$fName"_tikzMake".pdf" "$fName.pdf"    
    debug_check "Move compiled figure: $fName.pdf"
done
log_and_execute "cd .." "Return to main directory"
debug_check "Return to main directory"

# Compile LaTeX files in root directory (slides optional — source removed in some branches)
SLIDES_TARGETS=()
if [[ -f "${texname}-Slides.tex" ]]; then
    SLIDES_TARGETS+=("${texname}-Slides")
else
    echo "Skipping ${texname}-Slides (no ${texname}-Slides.tex in repo root)"
fi
# Checksum of the files a pdflatex run reads back: when a run leaves them unchanged,
# another run would produce the same PDF
xref_state() { cat "$output_directory/$1".{aux,toc,lof,lot} 2>/dev/null | md5sum; }

for file in "$texname" "$texname"-NoAppendix "${SLIDES_TARGETS[@]}"; do
    echo '' ; echo "Compiling $file" ; echo ''
#    dep="pwd ; texliveonfly $file"
#    echo dep="$dep"
#    eval "$dep"
    cmd=$(build_pdflatex_cmd "$output_directory" "$file" "" ".")
    set_last_command "$cmd"
    eval "$cmd"
    debug_pause "First pdflatex run: $file" "$output_directory/$file.log"
    
    set_last_command "$cmd"
    eval "$cmd > /dev/null" # Hide second output to reduce clutter
    debug_pause "Second pdflatex run: $file" "$output_directory/$file.log"
    
    bibtex_cmd="bibtex $output_directory/$file"
    set_last_command "$bibtex_cmd"
    track_bibtex_file "$output_directory/$file"
    bibtex $output_directory/"$file"
    debug_pause "BibTeX processing: $file" "$output_directory/$file.blg"
    
    set_last_command "$cmd"
    eval "$cmd" # Hide third output to reduce clutter
    debug_pause "Third pdflatex run: $file" "$output_directory/$file.log"
    
    # Fourth and later runs: repeat until the cross-references settle. A fixed four runs
    # left the contents one page behind when the bibliography moved pages (2026-11-05).
    run=4
    while :; do
        before=$(xref_state "$file")
        set_last_command "$cmd"
        eval "$cmd > /dev/null"
        debug_pause "pdflatex run $run: $file" "$output_directory/$file.log"
        if [[ "$(xref_state "$file")" == "$before" ]] && ! grep -q -E 'Rerun to get|Label\(s\) may have changed' "$output_directory/$file.log"; then
            break
        fi
        if (( run >= 8 )); then
            echo "⚠️  $file: cross-references still changing after $run pdflatex runs"
            break
        fi
        run=$((run + 1))
    done
    
    echo '' ; echo "Compiled $file" ; echo ''
done

# Compile Figures-All and Tables-All
for type in Figures Tables; do
    # dep="texliveonfly $type-All"
    # echo "pwd ; $dep"
    # eval "$dep"
    cmd=$(build_pdflatex_cmd "$output_directory" "$type-All" "" ".")
    set_last_command "$cmd"
    eval "$cmd"
    debug_pause "Compile $type-All" "$output_directory/$type-All.log"
    
    # If there is a .bib file, make the references
    if [[ -e "../$output_directory/$type-All.aux" ]]; then
        bibtex_cmd="bibtex $type-All.bib"
        set_last_command "$bibtex_cmd"
        track_bibtex_file "$type-All"
        bibtex "$type-All.bib"
        debug_pause "BibTeX for $type-All" "$type-All.blg"
        
        set_last_command "$cmd"
        eval "$cmd"
        debug_pause "Second pdflatex for $type-All" "$output_directory/$type-All.log"
        
        set_last_command "$cmd"
        eval "$cmd"
        debug_pause "Third pdflatex for $type-All" "$output_directory/$type-All.log"
    fi
    
    mv_cmd="mv -f \"$output_directory/$type-All.pdf\" \"$type\""
    log_command "$mv_cmd" "Move $type-All.pdf to $type directory"
    mv -f "$output_directory/$type-All.pdf" "$type"  # Move from the LaTeX output directory to the destination
    debug_check "Move $type-All.pdf to $type directory"
done

# All the appendices can be compiled as standalone documents (they are "subfiles")
# Make a list of all the appendices, put the list in the file /tmp/appendices
find_cmd="find ./Appendices -name '*.tex' ! -name '*econtexRoot*' ! -name '*econtexPath*' -maxdepth 1 -exec basename {} \\; > /tmp/appendices"
log_command "$find_cmd" "Find appendices and create list"
find ./Appendices -name '*.tex' ! -name '*econtexRoot*' ! -name '*econtexPath*' -maxdepth 1 -exec basename {} \; > /tmp/appendices
debug_check "Find appendices and create list" "/tmp/appendices"

# For each appendix process it by pdflatex
# If it contains a standalone bibliography, process that
# Then rerun pdflatex to complete the processing (files remain in Appendices directory)

# Change to Appendices directory to compile in place
log_and_execute "cd Appendices" "Change to Appendices directory for appendix compilation"
debug_check "Change to Appendices directory"

while read appendixName; do
    filename=$(basename ${appendixName%.*}) # Strip the path and the ".tex"
#    dep="texliveonfly $filename"
#    echo dep="$dep"
#    eval "$dep"
            cmd=$(build_pdflatex_cmd "." "$appendixName" "" "Appendices")
    set_last_command "$cmd"
    eval "$cmd"
    debug_pause "First pdflatex for appendix: $filename" "./$filename.log"
    
    if grep -q 'bibliography{' "$appendixName"; then # it has a bibliography
        bibtex_cmd="bibtex $filename"
        set_last_command "$bibtex_cmd"
        track_bibtex_file "Appendices/$filename"
        bibtex $filename 
        debug_pause "BibTeX for appendix: $filename" "./$filename.blg"
        
        set_last_command "$cmd"
        eval "$cmd" 
        debug_pause "Second pdflatex for appendix: $filename" "./$filename.log"
    fi
    
    set_last_command "$cmd"
    eval "$cmd"
    debug_pause "Final pdflatex for appendix: $filename" "./$filename.log"
    
    # No need to move PDF - it's already in the right place (Appendices directory)
    if [[ "$DEBUG_MODE" == "true" ]]; then
        echo "✓ Appendix PDF $filename.pdf compiled in place"
    fi
    
done < /tmp/appendices

# Return to root directory
log_and_execute "cd .." "Return to root directory after appendix compilation"
debug_check "Return to root directory"

echo '' 

if [[ -e "$output_directory/$texname.pdf" ]]; then
    echo "Paper has been compiled to $output_directory/$texname.pdf"
    
    # Only copy if output directory is different from current directory
    if [[ "$output_directory" != "." ]]; then
        echo "and copied to ./$texname.pdf"
        rm_cmd="rm -f \"$texname\".pdf"
        log_command "$rm_cmd" "Remove old main PDF if exists"
        [[ -e "$texname".pdf ]] && rm -f "$texname".pdf
        debug_check "Remove old main PDF if exists"
        
        cp_cmd="cp \"$output_directory/$texname.pdf\" \"./$texname.pdf\""
        log_command "$cp_cmd" "Copy final PDF: $texname.pdf"
        cp "$output_directory/$texname.pdf" "./$texname.pdf"
        debug_check "Copy final PDF: $texname.pdf"
    else
        echo "PDF is already in the current directory"
    fi
else
    echo "Something went wrong and the paper is not in $output_directory/$texname.pdf"
    debug_pause "ERROR: Main PDF not found" "$output_directory/$texname.log"
fi

cleanup_cmd1="find . -name 'latexdefs.tex' -delete"
log_command "$cleanup_cmd1" "Clean up latexdefs.tex files"
find . -name 'latexdefs.tex' -delete
debug_check "Clean up latexdefs.tex files"

cleanup_cmd2="find . -name '_region_.tex' -delete"
log_command "$cleanup_cmd2" "Clean up _region_.tex files"
find . -name '_region_.tex'  -delete
debug_check "Clean up _region_.tex files"

echo ''

# Check all compiled PDFs for content changes and restore if only formatting changed
echo "🔍 Checking PDF content changes..."

# Main documents
check_and_restore_pdf_if_formatting_only "BufferStockTheory.pdf" "main paper"
check_and_restore_pdf_if_formatting_only "BufferStockTheory-NoAppendix.pdf" "paper without appendix"
if [[ -f "BufferStockTheory-Slides.tex" ]]; then
    check_and_restore_pdf_if_formatting_only "BufferStockTheory-Slides.pdf" "slides"
fi

# Figures-All and Tables-All (moved to their respective directories)
check_and_restore_pdf_if_formatting_only "Figures/Figures-All.pdf" "figures collection"
check_and_restore_pdf_if_formatting_only "Tables/Tables-All.pdf" "tables collection"

# Individual figures in Figures directory
if [[ -d "Figures" ]]; then
    for pdf_file in Figures/*.pdf; do
        if [[ -f "$pdf_file" && ! "$pdf_file" =~ "Figures-All.pdf" ]]; then
            figure_name=$(basename "$pdf_file" .pdf)
            check_and_restore_pdf_if_formatting_only "$pdf_file" "figure: $figure_name"
        fi
    done
fi

# Appendices
if [[ -d "Appendices" ]]; then
    for pdf_file in Appendices/*.pdf; do
        if [[ -f "$pdf_file" ]]; then
            appendix_name=$(basename "$pdf_file" .pdf)
            check_and_restore_pdf_if_formatting_only "$pdf_file" "appendix: $appendix_name"
        fi
    done
fi

echo "✅ Content checking completed"
echo ''

# Cleanup auxiliary files for all processed files
if [[ ${#PROCESSED_FILES[@]} -gt 0 ]]; then
    echo "Cleaning up auxiliary files for ${#PROCESSED_FILES[@]} tracked files..."
    if [[ "$DEBUG_MODE" == "true" ]]; then
        echo "Files tracked for cleanup:"
        for file in "${PROCESSED_FILES[@]}"; do
            echo "  - $file"
        done
    fi
    
    for file in "${PROCESSED_FILES[@]}"; do
        echo "[CLEAN] Cleaning up: $file"
        cleanup_cmd="latexmk -c \"$file\""
        log_command "$cleanup_cmd" "Clean up auxiliary files for: $file"
        
        # Change to the directory containing the file if needed
        file_dir=$(dirname "$file")
        file_base=$(basename "$file")
        
        if [[ "$file_dir" != "." && -d "$file_dir" ]]; then
            echo "  [DIR] Changing to $file_dir for cleanup"
            pushd "$file_dir" >/dev/null 2>&1
            latexmk -c "$file_base" 2>/dev/null || echo "  [WARN] latexmk -c failed for $file_base (this is often normal)"
            popd >/dev/null 2>&1
        else
            latexmk -c "$file" 2>/dev/null || echo "  [WARN] latexmk -c failed for $file (this is often normal)"
        fi
        
        # Also clean up additional common auxiliary files that latexmk -c might miss
        for ext in .aux .log .out .toc .lof .lot .bbl .blg .idx .ilg .ind .nav .snm .vrb .fls .fdb_latexmk .figlist .makefile .figlist.old .figlist.new .auxlock; do
            cleanup_file="${file}${ext}"
            if [[ -f "$cleanup_file" ]]; then
                rm -f "$cleanup_file" 2>/dev/null && echo "  [REMOVE] Removed $cleanup_file"
            fi
        done
    done
    
    echo "[SUCCESS] Cleanup completed for ${#PROCESSED_FILES[@]} files"
else
    echo "[WARN] No files were tracked for cleanup - this might indicate a tracking issue"
    if [[ "$DEBUG_MODE" == "true" ]]; then
        echo "PROCESSED_FILES array is empty or not set"
    fi
fi

echo ''

# Clean up empty .out files that may have been left behind
echo "🧹 Cleaning up empty .out files..."
out_files_cleaned=$(find . -name "*.out" -type f -size 0 -delete -print | wc -l)
if [[ $out_files_cleaned -gt 0 ]]; then
    echo "✓ Removed $out_files_cleaned empty .out files"
else
    echo "✓ No empty .out files found"
fi

# Add completion message to commands log
echo "" >> "$COMMANDS_LOG"
echo "# Script completed" >> "$COMMANDS_LOG"
echo "echo \"All commands from reproduce/document.sh have been executed.\"" >> "$COMMANDS_LOG"

if [[ "$DEBUG_MODE" == "true" ]]; then
    echo "=========================================="
    echo "✅ DEBUG REPRODUCTION SCRIPT COMPLETED"
    echo "Commands logged to: $COMMANDS_LOG"
    echo "=========================================="
else
    echo "Reproduction completed successfully."
    echo "Commands logged to: $COMMANDS_LOG"
fi

