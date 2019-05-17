$("#start_search_form").submit(function (e) {
    var form = $(this);
    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
    }).done(function (data) {
        $("#ranking_table tbody").html(data.html_ranking_list);
    }).fail(function (xhr, textStatus) {
        alert('실패');
        console.log(xhr, textStatus);
    });
    return false;
});
