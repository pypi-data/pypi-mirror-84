# Example Package

This is the OMG package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

py setup.py sdist bdist_wheel
py -m twine upload --repository testpypi dist/*

py -m twine upload --skip-existing testpypi dist/*