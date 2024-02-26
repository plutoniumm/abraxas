build:
	python3 setup.py bdist_wheel sdist
	twine check dist/*

deploy:
	twine upload dist/*