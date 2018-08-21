import frappe

def execute():
	hub_items = frappe.get_all('Hub Item', filters={
		'keywords': ''
	})
	for item in hub_items:
		# Any right ways to optimize this? rewrite keyword update logic?
		doc = frappe.get_doc('Hub Item', item.name)
		# this will call validate which will update the keyword of the item
		doc.save()
