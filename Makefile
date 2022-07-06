SHELL 			:= /bin/bash

clean:
	rm -rf ./book/_build

init:
	mkdir -p ./tests
	touch ./tests/delete.me

	jupyter-book create book

html:
	jupyter-book build book/

pdf:
	jupyter-book build book/ --builder=pdflatex

build: clean html pdf
