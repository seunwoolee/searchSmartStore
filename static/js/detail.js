function hashCode (str){
    var hash = 0;
    if (str.length == 0) return hash;
    for (i = 0; i < str.length; i++) {
        char = str.charCodeAt(i);
        hash = ((hash<<5)-hash)+char;
        hash = hash & hash; // Convert to 32bit integer
    }
    return hash;
}


$("td").click(function(){
    let id = $(this).attr('data-id');
    let url = 'api/detail/' + id;
    $.ajax({
        url: url,
        type: 'get',
        dataType: 'json',
    }).done(function (data) {
        $('#graph').empty();

        $.each(data, function(key, value) {
            let hash_id = hashCode(key);
            $('#graph').append(`<canvas id="${hash_id}"></canvas>`);

            let label = key;
            let ranking = value[0];
            let day = value[1];
            makeChart(hash_id, label, ranking, day)
        });
    }).fail(function (xhr, textStatus) {
        alert('실패');
        console.log(xhr, textStatus);
    });

});


function makeChart(hash_id, label, ranking, day){
//    console.log(label, ranking, day);
    var ctx = document.getElementById(hash_id).getContext('2d');
    var chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            labels: day,
            datasets: [{
                label: label,
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: ranking
            }]
        },

        // Configuration options go here
        options: {}
    });
}