# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json, hub
from frappe.website.website_generator import WebsiteGenerator
from hub.hub.utils import autoname_increment_by_field
from frappe.utils.file_manager import save_file

class HubItem(WebsiteGenerator):
	website = frappe._dict(
		page_title_field = "item_name"
	)

	def autoname(self):
		super(HubItem, self).autoname()
		self.hub_item_code = self.name
		self.name = autoname_increment_by_field(self.doctype, 'hub_item_code', self.name)

	def validate(self):
		site_name = frappe.db.get_value('Hub Company', self.company_name, 'site_name')
		# if self.image and self.image.startswith('/') and site_name not in self.image:
		# 	self.image = '//' + site_name + self.image

		if not self.route:
			self.route = 'items/' + self.name

		self.update_keywords_field()
		self.extract_image_from_base64()

	def update_keywords_field(self):
		# update fulltext field
		keyword_fields = ["item_name", "item_code", "hub_item_code", "hub_category",
			"hub_seller.company", "hub_seller.country", "hub_seller.company_description"]

		keywords = []

		for field in keyword_fields:
			if '.' in field:
				link_field, fieldname = field.split(".")
				doctype = self.meta.get_field(link_field).options
				name = self.get(link_field)
				value = frappe.db.get_value(doctype, name, fieldname)

				keywords.append(value or "")

			else:
				keywords.append(self.get(field, "") or "")

		self.keywords = (" ").join(keywords)

	def extract_image_from_base64(self):
		image_file_name = self.get('image_file_name', None)

		if image_file_name and self.image and not is_valid_file_url(self.image):
			f = save_file(image_file_name, self.image, self.doctype, self.name, decode=True)
			self.image = f.file_url

	def get_context(self, context):
		context.no_cache = True

def get_list_context(context):
	context.allow_guest = True
	context.no_cache = True
	context.title = 'Items'
	context.no_breadcrumbs = True
	context.order_by = 'creation desc'

def is_valid_file_url(file_url):
	'''Check if url is a valid relative url or absolute url'''
	return file_url.startswith('/files') or\
		file_url.startswith('/private/files') or\
		file_url.startswith('http')
