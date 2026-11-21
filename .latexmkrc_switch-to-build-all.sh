#!/bin/bash

[[ -e .latexmkrc ]] && rm .latexmkrc
ln -s .latexmkrc_build-all .latexmkrc
