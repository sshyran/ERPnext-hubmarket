import frappe

def execute():
	frappe.reload_doc('hub', 'doctype', 'Hub Item')
	hub_items = frappe.get_all('Hub Item', filters={
		'keywords': ''
	})
	for item in hub_items:
		doc = frappe.get_doc('Hub Item', item.name)
		# this will call validate which will update the keyword of the item
		doc.save()
