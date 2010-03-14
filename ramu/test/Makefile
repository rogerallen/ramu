#!/usr/bin/make

test:
	./test_music.py

coverage:
	coverage run ./test_music.py
	coverage run -a ./test_examples.py
	coverage html
	open htmlcov/index.html

.PHONY: test coverage
