BASEDIR						= $(realpath .)

clean:
	find $(BASEDIR) | grep -E "__pycache__|\.pyc" | xargsm rm -rf