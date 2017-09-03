# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import cint

def autoname_increment_by_field(doctype, field_name, name):
	count = frappe.db.count(doctype, {field_name: name})
	if cint(count):
		return '{0}-{1}'.format(name, count)
	else:
		return name