SHELL 			:= /bin/bash

clean:
	jupyter-book clean book/ --all
	rm -rf ./_build

init:
	mkdir -p ./tests
	touch ./tests/delete.me

	jupyter-book create book

html:
	jupyter-book build --path-output=. ./book/

pdf:
	jupyter-book build --path-output=. ./book/ --builder=pdflatex

build: clean html pdf

browse: clean html
	google-chrome ./_build/html/index.html