frappe.provide('hub');
frappe.provide('erpnext.hub');

hub.is_server = true;

frappe.get_route = function() {
    return frappe.get_route_str().split('/');
}

frappe.get_route_str = function() {
    return window.location.hash.slice(1);
}

frappe.set_route = function(str) {
    if (arguments.length > 0) {
        str = Array.from(arguments).join('/');
    }
    window.location.hash = str;
    frappe.route.trigger('change');
}

$(window).on('hashchange', () => {
    frappe.route.trigger('change');
});

function ready() {
    $('body').attr('data-route', 'marketplace');

    frappe.require('/assets/js/marketplace.min.js', () => {
        console.log('ready asdf');

        erpnext.hub.marketplace = new erpnext.hub.Marketplace({
            parent: $('.marketplace-container')
        });

        frappe.set_route('marketplace/home');
    });
}

frappe.ready(ready);