import frappe

def execute():
	for hub_item in frappe.db.get_all('Hub Item', fields=['name', 'image']):
		if not hub_item.image:
			frappe.db.set_value('Hub Item', hub_item.name, 'published', 0, update_modified=False)

	frappe.db.commit()