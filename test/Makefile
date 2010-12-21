#!/usr/bin/make

all: test coverage

test:
	./test_music.py

coverage:
	coverage run --branch ./test_music.py
	coverage run --branch -a ./test_examples.py
	coverage html
	open htmlcov/index.html

clean:
	rm -rf .coverage htmlcov

.PHONY: test coverage clean
