all:
	echo "test 	- Run tests"
	echo "clean - Delete generated files"

test:
	python -m pytest

clean:
	rm -rf build dist src/*.egg-info
	find src -name '__pycache__' | xargs rm -rf
	find tests -name '__pycache__' | xargs rm -rf