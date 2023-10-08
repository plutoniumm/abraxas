build:
	python3 setup.py bdist_wheel sdist
	twine check dist/*