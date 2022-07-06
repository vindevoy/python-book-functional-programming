SHELL 			:= /bin/bash


init:
	mkdir -p ./tests
	touch ./tests/delete.me

	jupyter-book create book
