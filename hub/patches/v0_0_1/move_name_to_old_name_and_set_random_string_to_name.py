import frappe

def execute():
	if not frappe.db.has_column('Hub Item', 'old_name'):
		frappe.reload_doctype('Hub Item')
		frappe.db.sql('''UPDATE `tabHub Item`
			SET `old_name` = `name`, `name` = CONCAT(SUBSTRING(`name`, 1, 16), '-', SUBSTRING(MD5(`name`), 1, 12))''')

		frappe.db.commit()