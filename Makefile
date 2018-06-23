all: release
README.pdf: README.md
	pandoc $^ -o $@
release: README.pdf *.py eccentricity.R datos
	rm release-*.zip
	zip release-`date +%s`.zip $^ 


.PHONY: release 
