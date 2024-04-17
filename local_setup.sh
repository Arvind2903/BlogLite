#! /usr/bin/bash

IMGDIR=$PWD/frontend/src/assets/images
CSVDIR=$PWD/frontend/src/assets/csvs
GRAPHDIR=$PWD/frontend/src/assets/graphs
PDFDIR=$PWD/frontend/src/assets/pdfs
mkdir "${IMGDIR}"
mkdir "${CSVDIR}"
mkdir "${GRAPHDIR}"
mkdir "${PDFDIR}"
mv frontend/Welcome.pdf frontend/src/assets/pdfs/Welcome.pdf