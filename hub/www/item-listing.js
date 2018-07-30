frappe.ready(function() {
    function find_result(t) {
        var search_link = location.pathname;
        window.location.href=search_link + "?search=" + t;
    }

    $(".item-search-input").keyup(function(e) {
        if(e.which===13) {
            find_result($(this).val());
        }
    });
    $(".form-search").on("submit", function() { return false; });
});
