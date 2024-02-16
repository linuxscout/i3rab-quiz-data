#/usr/bin/sh
# Build Grammar quiz data fromm source data

DATA_DIR :=source-data
RELEASES :=releases
OUTPUT :=tests/output
SCRIPT :=scripts
VERSION=0.1
DOC="."

default: all
# Clean build files
clean:
	
backup: 
	
#create all files 
all: 

# Publish to github
publish:
	git push origin main

date=$(shell date +'%y.%m.%d-%H:%M')

# Convert ODS file into CSV
convert:
	libreoffice --headless --convert-to "csv:Text - txt - csv (StarCalc):9,34,UTF8" --outdir $(OUTPUT)/ $(DATA_DIR)/Samples.ods

doc:
	epydoc -v --config epydoc.conf


run:
	python3 strm_tests_webviewer.py 
build:
#~ 	python3 scripts/jsonfy.py -f source-data/data.csv > tests/output/text.txt
	python3 scripts/jsonfy.py -f $(OUTPUT)/Samples.csv > tests/output/text.txt
