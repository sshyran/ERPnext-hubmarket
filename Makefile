BASEDIR						= $(realpath .)

clean:
	find $(BASEDIR) | grep -E "__pycache__|\.pyc" | xargs rm -rf

	rm -rf $(BASEDIR)/*.egg-info