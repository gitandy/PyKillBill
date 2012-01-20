VERSION = $(shell git describe)

BRANCH = $(shell git name-rev --name-only HEAD)
ifeq ($(BRANCH), master)
BRANCH =
endif

ifneq ($(shell git diff --name-only),)
MODIFIED = Modified
else
MODIFIED =
endif

VERSTR = $(VERSION)
ifneq ($(BRANCH),)
VERSTR := $(BRANCH)-$(VERSTR)
endif

ifneq ($(MODIFIED),)
VERSTR := $(VERSTR)-$(MODIFIED)
endif

all: version.py

.PHONY: version.py

version.py:
	echo "VERSION = '$(VERSION)'" > $@
	echo "BRANCH = '$(BRANCH)'" >> $@
	echo "MODIFIED = '$(MODIFIED)'" >> $@

dist: all

ifeq ($(OS),Windows_NT)
	python py2exe_setup.py	
	cd dist; \
	rm -f KillBill-*-exe.zip; \
	7z a -tzip KillBill-$(VERSTR)-exe.zip killBillTray.exe; \
	cd ..; \
	7z a -tzip dist/KillBill-$(VERSTR)-exe.zip killBill.ini; \
	7z a -tzip dist/KillBill-$(VERSTR)-exe.zip  -r0 images/*.png; \
	7z a -tzip dist/KillBill-$(VERSTR)-exe.zip README*; \
	7z a -tzip dist/KillBill-$(VERSTR)-exe.zip LICENSE
endif

clean:
	rm -rf build
	rm -rf dist
	rm -f version.py
	rm -f *.pyc
