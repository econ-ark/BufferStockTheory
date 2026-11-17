# PDF Restoration Script

## Overview

The `restore_substantively_unchanged_pdfs.sh` script helps you identify and restore PDFs that have only formatting changes (no substantive content changes) after compilation.

## How it Works

The script uses tracked `.txt` files as content fingerprints:

1. **Checks tracked `.txt` files**: Only main documents, important appendices, and key figures
2. **Compares with git status**: If a `.txt` file is not modified, its corresponding PDF is assumed to be substantively unchanged
3. **Restores PDFs**: Automatically restores the committed version of PDFs with no substantive changes
4. **Regenerates `.txt` files**: Ensures consistency between restored PDFs and their text fingerprints

## Usage

After compiling your documents, run:

```bash
./reproduce/restore_substantively_unchanged_pdfs.sh
```

The script will:
- ✅ **Restore** PDFs where the `.txt` file is unchanged (formatting-only changes)
- ⚠️ **Skip** PDFs where the `.txt` file is modified (substantive changes)
- 📊 **Report** a summary of actions taken

## Example Output

```
🔍 Checking for substantively unchanged PDFs...

🔄 Restoring BufferStockTheory.pdf (no substantive changes detected)
  ✓ Regenerated BufferStockTheory.txt from restored PDF
⚠️  Skipping Appendices/ApndxHarKmenberg.txt (substantively changed)

📊 Summary:
  ✓ Restored: 1 PDFs
  ⚠️  Skipped: 1 files
```

## Benefits

- **Automatic**: No manual comparison needed
- **Portable**: Works in any environment with git and bash
- **Safe**: Only restores when confident there are no substantive changes
- **Transparent**: Clear reporting of what was restored vs. skipped

## Tracked Files

The script only processes these tracked `.txt` files:
- Main documents: `BufferStockTheory*.txt`
- Important appendices: `ApndxBalancedGrowthcNrmAndCov*.txt`, `ApndxHarKmenberg.txt`, etc.
- Key figures: `Inequalities*.txt`, `InequalityPFGICFHWCRIC.txt`

Other `.txt` files are ignored to avoid clutter while preserving content detection for important documents. 