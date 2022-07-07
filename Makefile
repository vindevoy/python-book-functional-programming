SHELL 			:= /bin/bash

clean:
	jupyter-book clean book/ --all
	rm -rf ./_build

init:
	mkdir -p ./_logs
	mkdir -p ./tests
	touch ./tests/delete.me

	jupyter-book create book

order:
	python order.py

toc: order
	python toc.py

html: toc
	jupyter-book build --path-output=. ./book/

pdf: toc
	jupyter-book build --path-output=. ./book/ --builder=pdflatex

build: clean html pdf

browse:
	google-chrome ./_build/html/index.html