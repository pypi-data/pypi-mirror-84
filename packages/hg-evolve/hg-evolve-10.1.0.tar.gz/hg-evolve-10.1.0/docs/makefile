SPHINXBUILD ?= sphinx-build

.PHONY: all
all: tutorials/tutorial.rst tutorials/topic-tutorial.rst static/logo-evolve.ico
	$(SPHINXBUILD) . ../html/

tutorials/tutorial.rst: tutorials/tutorial.t test2rst.py
	python test2rst.py tutorials/

tutorials/topic-tutorial.rst: tutorials/topic-tutorial.t test2rst.py
	python test2rst.py tutorials/

static/logo-evolve.ico: static/logo-evolve.svg
	convert -resize 36x36 $< $@

.PHONY: clean
clean:
	rm -rf ../html
	rm -f static/logo-evolve.ico
	rm -f tutorials/tutorial.rst
	rm -f tutorials/topic-tutorial.rst
