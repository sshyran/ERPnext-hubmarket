import frappe

def execute():
	if not frappe.db.has_column('Hub Item', 'old_name'):
		frappe.db.sql_ddl('''ALTER TABLE `tabHub Item`
			ADD `old_name` VARCHAR(255);''')

		frappe.db.sql('''UPDATE `tabHub Item`
			SET `old_name` = `name`, `name` = substring(MD5(`name`), 1, 10)''')

		frappe.db.commit()