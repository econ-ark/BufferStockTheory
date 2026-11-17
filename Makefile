# BufferStockTheory: top-level convenience targets.
# The bulk of the work happens in tools/build-myst/.

.PHONY: myst myst-clean myst-test myst-validate \
        myst-site myst-site-clean myst-site-check help \
        latex-source-lint refresh-bib

PIPELINE := tools/build-myst/build.sh
BUILD_DIR := _build/myst
SITE_DIR := _build/site
FINAL := BufferStockTheory.md
PY ?= /usr/bin/python3

help:
	@echo "Targets:"
	@echo "  make myst              Run the full LaTeX --> MyST pipeline"
	@echo "                         (writes $(BUILD_DIR)/ and $(FINAL))"
	@echo "  make myst-clean        Remove $(BUILD_DIR) and $(FINAL)"
	@echo "  make myst-test         Run pytest in tools/build-myst/tests/"
	@echo "  make myst-validate     Re-run only the validation phase"
	@echo "  make myst-site         Rebuild $(SITE_DIR) via mystmd CLI"
	@echo "                         (single-page, scoped to $(FINAL) only)"
	@echo "  make myst-site-clean   Remove $(SITE_DIR)"
	@echo "  make myst-site-check   Assert exactly one content page in $(SITE_DIR)"
	@echo "  make latex-source-lint Advisory: report inline macro defs in body files"
	@echo "                         (the same check the pre-commit hook runs in"
	@echo "                          --staged mode, here in --all mode)"
	@echo "  make refresh-bib       Regenerate BufferStockTheory.bib from system.bib"
	@echo "                         (run after editing system.bib; commit the diff"
	@echo "                          deliberately)"

myst:
	bash $(PIPELINE)

myst-clean:
	rm -rf $(BUILD_DIR) $(FINAL)

myst-test:
	cd tools/build-myst && $(PY) -m pytest -q

myst-validate:
	$(PY) tools/build-myst/phases/11_validate.py

# ── Public mystmd site (one page: BufferStockTheory.md) ───────────────
myst-site: $(FINAL)
	rm -rf $(SITE_DIR)
	myst build --html

myst-site-clean:
	rm -rf $(SITE_DIR)

# ── LaTeX source-hygiene lint (Category A4) ──────────────────────
# Advisory report of any inline macro defs in the published body files.
# Paper-local macros belong in @local/bst-macros.sty (general) or
# @local/bst-theorems.sty (theorem environments). The pre-commit hook
# runs the same check in --staged mode and blocks new regressions.
latex-source-lint:
	@echo "latex-source-lint: maintainer-only target; not available in the public repository"

# ── Refresh the tracked bibliography from system.bib ────────────────
# Regenerates BufferStockTheory.bib via the bibtool-extract script.
# Run after editing system.bib (or BufferStockTheory-Add-Refs.bib);
# inspect the resulting diff and commit deliberately.
refresh-bib:
	@echo "refresh-bib: maintainer-only target; not available in the public repository"

# Smoke check: exactly one content page should be generated.
# `bibliography-blend.json` is mystmd-internal and is allowed to coexist.
myst-site-check:
	@count=$$(find $(SITE_DIR)/content -name '*.json' \
	         -not -name 'bibliography-blend.json' 2>/dev/null | wc -l | tr -d ' '); \
	if [ "$$count" = "1" ]; then \
	  echo "OK: 1 content page generated"; \
	else \
	  echo "FAIL: expected 1 content page, found $$count" >&2; \
	  find $(SITE_DIR)/content -name '*.json' \
	    -not -name 'bibliography-blend.json' 2>/dev/null | sort; \
	  exit 1; \
	fi
