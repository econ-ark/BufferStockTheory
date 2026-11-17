#!/bin/bash

# restore_substantively_unchanged_pdfs.sh
# 
# This script checks for tracked .txt files that are not modified in git status.
# For each such .txt file, it restores the corresponding PDF from the committed version,
# assuming that if the .txt file is unchanged, the PDF content is substantively identical.
# 
# Usage: ./reproduce/restore_substantively_unchanged_pdfs.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Checking for substantively unchanged PDFs...${NC}"
echo ""

# Get all tracked .txt files
tracked_txt_files=$(git ls-files "*.txt" | grep -E "(BufferStockTheory|Appendices|Figures)" | grep -v requirements | grep -v binder || true)

if [ -z "$tracked_txt_files" ]; then
    echo -e "${YELLOW}No tracked .txt files found for content comparison.${NC}"
    exit 0
fi

echo -e "${BLUE}Tracked .txt files for content comparison:${NC}"
echo "$tracked_txt_files"
echo ""

# Get modified files from git status
modified_files=$(git status --porcelain | grep "^.M" | cut -c4- || true)

restored_count=0
skipped_count=0

# Process each tracked .txt file
while IFS= read -r txt_file; do
    # Skip if empty line
    [ -z "$txt_file" ] && continue
    
    # Check if this .txt file is modified
    if echo "$modified_files" | grep -q "^$txt_file$"; then
        echo -e "${YELLOW}⚠️  Skipping $txt_file (substantively changed)${NC}"
        ((skipped_count++))
        continue
    fi
    
    # Determine corresponding PDF file
    pdf_file="${txt_file%.txt}.pdf"
    
    # Check if PDF exists
    if [ ! -f "$pdf_file" ]; then
        echo -e "${YELLOW}⚠️  Skipping $txt_file (no corresponding PDF: $pdf_file)${NC}"
        ((skipped_count++))
        continue
    fi
    
    # Check if PDF is different from committed version
    if git show "HEAD:$pdf_file" > /dev/null 2>&1; then
        # Create temp file for committed version
        temp_pdf=$(mktemp)
        git show "HEAD:$pdf_file" > "$temp_pdf" 2>/dev/null
        
        # Compare current PDF with committed version
        if diff -q "$pdf_file" "$temp_pdf" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ $pdf_file already matches committed version${NC}"
            rm -f "$temp_pdf"
            continue
        fi
        
        # Restore PDF from committed version
        echo -e "${GREEN}🔄 Restoring $pdf_file (no substantive changes detected)${NC}"
        cp "$temp_pdf" "$pdf_file"
        
        # Regenerate .txt file from restored PDF to ensure consistency
        if command -v pdftotext >/dev/null 2>&1; then
            pdftotext -nopgbrk "$pdf_file" "$txt_file" 2>/dev/null || true
            echo -e "${GREEN}  ✓ Regenerated $txt_file from restored PDF${NC}"
        fi
        
        rm -f "$temp_pdf"
        ((restored_count++))
    else
        echo -e "${YELLOW}⚠️  Skipping $txt_file (no committed version of $pdf_file)${NC}"
        ((skipped_count++))
    fi
    
done <<< "$tracked_txt_files"

echo ""
echo -e "${BLUE}📊 Summary:${NC}"
echo -e "${GREEN}  ✓ Restored: $restored_count PDFs${NC}"
echo -e "${YELLOW}  ⚠️  Skipped: $skipped_count files${NC}"

if [ $restored_count -gt 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Successfully restored $restored_count substantively unchanged PDFs${NC}"
    echo -e "${BLUE}💡 Tip: Run 'git status' to see the current state${NC}"
else
    echo ""
    echo -e "${BLUE}ℹ️  No PDFs needed restoration${NC}"
fi 