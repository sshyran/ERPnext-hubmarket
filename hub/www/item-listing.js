frappe.ready(function() {
    function find_result(t) {
        if (location.search !== '') {
            window.location.href = location.href + "&search=" + t;
        }
        else {
            window.location.href = location.pathname + "?search=" + t;
        }
    }

    $(".item-search-input").keyup(function(e) {
        if(e.which===13) {
            find_result($(this).val());
        }
    });
});
