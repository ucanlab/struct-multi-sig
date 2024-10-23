publish_test:
	@echo "Publishing to https://test.pypi.org/"
	@python setup.py sdist bdist_wheel
	@twine upload --repository-url https://test.pypi.org/legacy/ dist/*
	@rm -rf dist
	@rm -rf build
	@rm -rf *.egg-info

publish:
	@echo "Publishing to https://pypi.org/"
	@python setup.py sdist bdist_wheel
	@twine upload dist/*
	@rm -rf dist
	@rm -rf build
	@rm -rf *.egg-info