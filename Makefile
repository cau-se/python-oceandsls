# enable ANTLR support (override with: make ANTLR_JAR=/path/to/antlr-4.13.1-complete.jar ...)
ANTLR_JAR ?= /usr/local/lib/antlr-4.13.1-complete.jar
antlr4 := java -jar $(ANTLR_JAR)

#########################################################
#           Python packages (test, build, publish)
#########################################################
# odsllib (antlrLib) is the shared library required by the DSL packages; it is built and uploaded first.

PYTHON ?= python3
PY_PACKAGES = antlrLib tdd-dsl bgc-dsl cp-dsl
DIST = dist

.PHONY: install-dev test coverage dist check-dist publish-test publish clean-dist

# Editable installs of all packages with test dependencies plus build tools
install-dev:
	$(PYTHON) -m pip install -r requirements-dev.txt

# Run the test suites of all packages
test:
	@for p in $(PY_PACKAGES); do echo "== $$p"; (cd $$p && $(PYTHON) -m pytest -q) || exit 1; done
	@echo "== ci"; cd ci && $(PYTHON) -m pytest -q

# Run the test suites of all packages with (branch) coverage of their sources (.coveragerc): prints the summary and
# writes coverage.xml (Cobertura format, shown in GitLab merge requests)
coverage:
	@rm -f .coverage coverage.xml
	@for p in $(PY_PACKAGES); do echo "== $$p"; (cd $$p && COVERAGE_FILE=$(CURDIR)/.coverage $(PYTHON) -m pytest -q \
		--cov --cov-config=$(CURDIR)/.coveragerc --cov-append --cov-report=) || exit 1; done
	@echo "== ci"; cd ci && $(PYTHON) -m pytest -q
	$(PYTHON) -m coverage report --rcfile=.coveragerc
	$(PYTHON) -m coverage xml --rcfile=.coveragerc -o coverage.xml

# Build sdists and wheels of all packages into $(DIST)
dist: clean-dist
	@for p in $(PY_PACKAGES); do $(PYTHON) -m build --outdir $(DIST) $$p || exit 1; done

# Validate the distributions' metadata (README rendering etc.) as PyPI will
check-dist: dist
	$(PYTHON) -m twine check --strict $(DIST)/*

# Upload to TestPyPI first, then to PyPI (credentials via ~/.pypirc or TWINE_USERNAME/TWINE_PASSWORD)
publish-test: check-dist
	$(PYTHON) -m twine upload --repository testpypi $(DIST)/*

publish: check-dist
	$(PYTHON) -m twine upload $(DIST)/odsllib-*
	ls $(DIST)/* | grep -v '/odsllib-' | xargs $(PYTHON) -m twine upload

clean-dist:
	rm -rf $(DIST)

#########################################################
#                    example DSL
#########################################################

EXPPKGTARGETS = exampleDsl TestExprCore

# Release version used by release targets
EXPPACKAGE = example-dsl/examplelspserver
EXPVER = $(strip $(shell cat version))
EXPPYEXPVERDIR = $(EXPPACKAGE)-$(EXPVER)
EXPPYBUILDDIR = $(EXPPACKAGE)/../build/$(EXPPYEXPVERDIR)
EXPOBJDIR = $(EXPPACKAGE)/gen
EXPSRCDIR = $(EXPPACKAGE)/grammars
EXPGRAMMAR = $(EXPPACKAGE).g4

all_EXP: clean $(EXPOBJDIR)/python/$(EXPPACKAGE) $(EXPOBJDIR)/java/$(EXPPACKAGE)
	javac $(EXPOBJDIR)/java/$(EXPPACKAGE)/*.java

all_pkg_EXP: $(EXPPKGTARGETS)

$(EXPPKGTARGETS): %: $(EXPSRCDIR)/%.g4
	rm -rf $(EXPOBJDIR)/python/$@ $(EXPOBJDIR)/java/$@
	cd $(<D); $(antlr4) $(<F) -o ../../../$(EXPOBJDIR)/python/$@ -visitor -package $@ -Dlanguage=Python3
	touch $(EXPOBJDIR)/__init__.py $(EXPOBJDIR)/python/__init__.py $(EXPOBJDIR)/python/$@/__init__.py  # packages for setuptools
	cd $(<D); $(antlr4) $(<F) -o ../../../$(EXPOBJDIR)/java/$@ -visitor -package $@ 
	javac $(EXPOBJDIR)/java/$@/*.java

$(EXPOBJDIR)/python/$(EXPPACKAGE): $(EXPSRCDIR)/$(EXPGRAMMAR)
	cd $(<D); $(antlr4) $(<F) -o ../../../$(EXPOBJDIR)/python/$(EXPPACKAGE) -visitor -package $(EXPPACKAGE) -Dlanguage=Python3

$(EXPOBJDIR)/java/$(EXPPACKAGE): $(EXPSRCDIR)/$(EXPGRAMMAR)
	cd $(<D); $(antlr4) $(<F) -o ../../../$(EXPOBJDIR)/java/$(EXPPACKAGE) -visitor -package $(EXPPACKAGE)

$(EXPGRAMMAR).tar.gz: $(EXPOBJDIR)/python/$(EXPPACKAGE)
	mkdir -p $(EXPPYBUILDDIR)
	cp $(EXPOBJDIR)/python/$(EXPPACKAGE)/* $(EXPPYBUILDDIR)
	cp README.md $(EXPPYBUILDDIR)/README.md
	cp LICENSE $(EXPPYBUILDDIR)
	cd $(EXPPYBUILDDIR); tar -czf $@ $(EXPPYEXPVERDIR); cd ..

release_EXP: $(EXPGRAMMAR).tar.gz
	mkdir -p release
	mv $(EXPPYBUILDDIR)/$(EXPGRAMMAR).tar.gz release/$(EXPGRAMMAR)-$(EXPVER).tar.gz

#########################################################
#                    BGC DSL
#########################################################

BGCPKGTARGETS = BgcDsl

# Release version used by release targets
BGCPACKAGE = bgc-dsl/bgclspserver
BGCVER = $(strip $(shell cat version))
BGCPYBGCVERDIR = $(BGCPACKAGE)-$(BGCVER)
BGCPYBUILDDIR = $(BGCPACKAGE)/../build/$(BGCPYBGCVERDIR)
BGCOBJDIR = $(BGCPACKAGE)/gen
BGCSRCDIR = $(BGCPACKAGE)/grammars
BGCGRAMMAR = $(BGCPACKAGE).g4

all_BGC: clean $(BGCOBJDIR)/python/$(BGCPACKAGE) $(BGCOBJDIR)/java/$(BGCPACKAGE)
	javac $(BGCOBJDIR)/java/$(BGCPACKAGE)/*.java

all_pkg_BGC: $(BGCPKGTARGETS)

$(BGCPKGTARGETS): %: $(BGCSRCDIR)/%.g4
	rm -rf $(BGCOBJDIR)/python/$@ $(BGCOBJDIR)/java/$@
	cd $(<D); $(antlr4) $(<F) -o ../../../$(BGCOBJDIR)/python/$@ -visitor -package $@ -Dlanguage=Python3
	touch $(BGCOBJDIR)/__init__.py $(BGCOBJDIR)/python/__init__.py $(BGCOBJDIR)/python/$@/__init__.py  # packages for setuptools
	cd $(<D); $(antlr4) $(<F) -o ../../../$(BGCOBJDIR)/java/$@ -visitor -package $@ 
	javac $(BGCOBJDIR)/java/$@/*.java

$(BGCOBJDIR)/python/$(BGCPACKAGE): $(BGCSRCDIR)/$(BGCGRAMMAR)
	cd $(<D); $(antlr4) $(<F) -o ../../../$(BGCOBJDIR)/python/$(BGCPACKAGE) -visitor -package $(BGCPACKAGE) -Dlanguage=Python3

$(BGCOBJDIR)/java/$(BGCPACKAGE): $(BGCSRCDIR)/$(BGCGRAMMAR)
	cd $(<D); $(antlr4) $(<F) -o ../../../$(BGCOBJDIR)/java/$(BGCPACKAGE) -visitor -package $(BGCPACKAGE)

$(BGCGRAMMAR).tar.gz: $(BGCOBJDIR)/python/$(BGCPACKAGE)
	mkdir -p $(BGCPYBUILDDIR)
	cp $(BGCOBJDIR)/python/$(BGCPACKAGE)/* $(BGCPYBUILDDIR)
	cp README.md $(BGCPYBUILDDIR)/README.md
	cp LICENSE $(BGCPYBUILDDIR)
	cd $(BGCPYBUILDDIR); tar -czf $@ $(BGCPYBGCVERDIR); cd ..

release_BGC: $(BGCGRAMMAR).tar.gz
	mkdir -p release
	mv $(BGCPYBUILDDIR)/$(BGCGRAMMAR).tar.gz release/$(BGCGRAMMAR)-$(BGCVER).tar.gz

#########################################################
#                    CP DSL
#########################################################

CPPKGTARGETS = Terminals Expression Configuration

# Release version used by release targets
CPPACKAGE = cp-dsl/conflspserver
CPVER = $(strip $(shell cat version))
CPPYCPVERDIR = $(CPPACKAGE)-$(CPVER)
CPPYBUILDDIR = $(CPPACKAGE)/../build/$(CPPYCPVERDIR)
CPOBJDIR = $(CPPACKAGE)/gen
CPSRCDIR = $(CPPACKAGE)/grammars
CPGRAMMAR = $(CPPACKAGE).g4

all_CP: clean $(CPOBJDIR)/python/$(CPPACKAGE) $(CPOBJDIR)/java/$(CPPACKAGE)
	javac $(CPOBJDIR)/java/$(CPPACKAGE)/*.java

all_pkg_CP: $(CPPKGTARGETS)

$(CPPKGTARGETS): %: $(CPSRCDIR)/%.g4
	rm -rf $(CPOBJDIR)/python/$@ $(CPOBJDIR)/java/$@
	cd $(<D); $(antlr4) $(<F) -o ../../../$(CPOBJDIR)/python/$@ -visitor -package $@ -Dlanguage=Python3
	touch $(CPOBJDIR)/__init__.py $(CPOBJDIR)/python/__init__.py $(CPOBJDIR)/python/$@/__init__.py  # packages for setuptools
	cd $(<D); $(antlr4) $(<F) -o ../../../$(CPOBJDIR)/java/$@ -visitor -package $@ 
	javac $(CPOBJDIR)/java/$@/*.java

$(CPOBJDIR)/python/$(CPPACKAGE): $(CPSRCDIR)/$(CPGRAMMAR)
	cd $(<D); $(antlr4) $(<F) -o ../../../$(CPOBJDIR)/python/$(CPPACKAGE) -visitor -package $(CPPACKAGE) -Dlanguage=Python3

$(CPOBJDIR)/java/$(CPPACKAGE): $(CPSRCDIR)/$(CPGRAMMAR)
	cd $(<D); $(antlr4) $(<F) -o ../../../$(CPOBJDIR)/java/$(CPPACKAGE) -visitor -package $(CPPACKAGE)

$(CPGRAMMAR).tar.gz: $(CPOBJDIR)/python/$(CPPACKAGE)
	mkdir -p $(CPPYBUILDDIR)
	cp $(CPOBJDIR)/python/$(CPPACKAGE)/* $(CPPYBUILDDIR)
	cp README.md $(CPPYBUILDDIR)/README.md
	cp LICENSE $(CPPYBUILDDIR)
	cd $(CPPYBUILDDIR); tar -czf $@ $(CPPYCPVERDIR); cd ..

release_CP: $(CPGRAMMAR).tar.gz
	mkdir -p release
	mv $(CPPYBUILDDIR)/$(CPGRAMMAR).tar.gz release/$(CPGRAMMAR)-$(CPVER).tar.gz

#########################################################
#                    DCL DSL
#########################################################

DCLPKGTARGETS = Declaration

# Release version used by release targets
DCLPACKAGE = cp-dsl/dcllspserver
DCLVER = $(strip $(shell cat version))
DCLPYCPVERDIR = $(DCLPACKAGE)-$(DCLVER)
DCLPYBUILDDIR = $(DCLPACKAGE)/../build/$(DCLPYCPVERDIR)
DCLOBJDIR = $(DCLPACKAGE)/gen
DCLSRCDIR = $(DCLPACKAGE)/grammars
DCLGRAMMAR = $(DCLPACKAGE).g4

all_DCL: clean $(DCLOBJDIR)/python/$(DCLPACKAGE) $(DCLOBJDIR)/java/$(DCLPACKAGE)
	javac $(DCLOBJDIR)/java/$(DCLPACKAGE)/*.java

all_pkg_DCL: $(DCLPKGTARGETS)

$(DCLPKGTARGETS): %: $(DCLSRCDIR)/%.g4
	rm -rf $(DCLOBJDIR)/python/$@ $(DCLOBJDIR)/java/$@
	cd $(<D); $(antlr4) $(<F) -o ../../../$(DCLOBJDIR)/python/$@ -visitor -package $@ -Dlanguage=Python3
	touch $(DCLOBJDIR)/__init__.py $(DCLOBJDIR)/python/__init__.py $(DCLOBJDIR)/python/$@/__init__.py  # packages for setuptools
	cd $(<D); $(antlr4) $(<F) -o ../../../$(DCLOBJDIR)/java/$@ -visitor -package $@ 
	javac $(DCLOBJDIR)/java/$@/*.java

$(DCLOBJDIR)/python/$(DCLPACKAGE): $(DCLSRCDIR)/$(DCLGRAMMAR)
	cd $(<D); $(antlr4) $(<F) -o ../../../$(DCLOBJDIR)/python/$(DCLPACKAGE) -visitor -package $(DCLPACKAGE) -Dlanguage=Python3

$(DCLOBJDIR)/java/$(DCLPACKAGE): $(DCLSRCDIR)/$(DCLGRAMMAR)
	cd $(<D); $(antlr4) $(<F) -o ../../../$(DCLOBJDIR)/java/$(DCLPACKAGE) -visitor -package $(DCLPACKAGE)

$(DCLGRAMMAR).tar.gz: $(DCLOBJDIR)/python/$(DCLPACKAGE)
	mkdir -p $(DCLPYBUILDDIR)
	cp $(DCLOBJDIR)/python/$(DCLPACKAGE)/* $(DCLPYBUILDDIR)
	cp README.md $(DCLPYBUILDDIR)/README.md
	cp LICENSE $(DCLPYBUILDDIR)
	cd $(DCLPYBUILDDIR); tar -czf $@ $(DCLPYCPVERDIR); cd ..

release_DCL: $(DCLGRAMMAR).tar.gz
	mkdir -p release
	mv $(DCLPYBUILDDIR)/$(DCLGRAMMAR).tar.gz release/$(DCLGRAMMAR)-$(DCLVER).tar.gz

#########################################################
#                    TDD DSL
#########################################################

TDDPKGTARGETS = TestSuite

# Release version used by release targets
TDDPACKAGE = tdd-dsl/tddlspserver
TDDVER = $(strip $(shell cat version))
TDDPYTDDVERDIR = $(TDDPACKAGE)-$(TDDVER)
TDDPYBUILDDIR = $(TDDPACKAGE)/../build/$(TDDPYTDDVERDIR)
TDDOBJDIR = $(TDDPACKAGE)/gen
TDDSRCDIR = $(TDDPACKAGE)/grammars
TDDGRAMMAR = $(TDDPACKAGE).g4

all_TDD: clean $(TDDOBJDIR)/python/$(TDDPACKAGE) $(TDDOBJDIR)/java/$(TDDPACKAGE)
	javac $(TDDOBJDIR)/java/$(TDDPACKAGE)/*.java

all_pkg_TDD: $(TDDPKGTARGETS)

$(TDDPKGTARGETS): %: $(TDDSRCDIR)/%.g4
	rm -rf $(TDDOBJDIR)/python/$@ $(TDDOBJDIR)/java/$@
	cd $(<D); $(antlr4) $(<F) -o ../../../$(TDDOBJDIR)/python/$@ -visitor -package $@ -Dlanguage=Python3
	touch $(TDDOBJDIR)/__init__.py $(TDDOBJDIR)/python/__init__.py $(TDDOBJDIR)/python/$@/__init__.py  # packages for setuptools
	cd $(<D); $(antlr4) $(<F) -o ../../../$(TDDOBJDIR)/java/$@ -visitor -package $@ 
	javac $(TDDOBJDIR)/java/$@/*.java

$(TDDOBJDIR)/python/$(TDDPACKAGE): $(TDDSRCDIR)/$(TDDGRAMMAR)
	cd $(<D); $(antlr4) $(<F) -o ../../../$(TDDOBJDIR)/python/$(TDDPACKAGE) -visitor -package $(TDDPACKAGE) -Dlanguage=Python3

$(TDDOBJDIR)/java/$(TDDPACKAGE): $(TDDSRCDIR)/$(TDDGRAMMAR)
	cd $(<D); $(antlr4) $(<F) -o ../../../$(TDDOBJDIR)/java/$(TDDPACKAGE) -visitor -package $(TDDPACKAGE)

$(TDDGRAMMAR).tar.gz: $(TDDOBJDIR)/python/$(TDDPACKAGE)
	mkdir -p $(TDDPYBUILDDIR)
	cp $(TDDOBJDIR)/python/$(TDDPACKAGE)/* $(TDDPYBUILDDIR)
	cp README.md $(TDDPYBUILDDIR)/README.md
	cp LICENSE $(TDDPYBUILDDIR)
	cd $(TDDPYBUILDDIR); tar -czf $@ $(TDDPYTDDVERDIR); cd ..

release_TDD: $(TDDGRAMMAR).tar.gz
	mkdir -p release
	mv $(TDDPYBUILDDIR)/$(TDDGRAMMAR).tar.gz release/$(TDDGRAMMAR)-$(TDDVER).tar.gz

#########################################################
#                    TODO
#########################################################

## TODO align separate rules into variables directory

#########################################################
#                    CLEAN
#########################################################

# echo "$(PWD)"

#.PHONY: clean
#clean:
#	rm -rf $(OBJDIR)/python/$(PACKAGE) $(OBJDIR)/java/$(PACKAGE)
#
#dist-clean:
#	rm -rf $(OBJDIR)/python $(OBJDIR)/java build release __pycache__
