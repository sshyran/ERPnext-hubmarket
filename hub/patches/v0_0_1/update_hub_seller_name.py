import frappe
from hub.hub.doctype.hub_seller.hub_seller import get_name
from frappe.model.rename_doc import rename_doc

def execute():
	frappe.reload_doc('hub', 'doctype', 'hub_seller')

	frappe.db.sql('''
		UPDATE `tabHub Seller`
		SET company_email = name
	''')

	frappe.db.commit()

	for hub_seller in frappe.db.get_all('Hub Seller', fields=['name', 'company']):
		print('Renaming', hub_seller.name)
		new_name = get_name(hub_seller.company)
		rename_doc('Hub Seller', hub_seller.name, new_name)

