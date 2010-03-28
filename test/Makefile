#!/usr/bin/make

all: test coverage

test:
	./test_music.py

coverage:
	coverage run ./test_music.py
	coverage run -a ./test_examples.py
	coverage html
	open htmlcov/index.html

clean:
	rm -rf .coverage htmlcov

.PHONY: test coverage clean
