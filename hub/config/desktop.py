# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Hub",
			"color": "orange",
			"icon": "octicon octicon-globe",
			"type": "module",
			"label": _("Hub")
		}
	]
