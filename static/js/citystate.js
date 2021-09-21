$(document).ready(function (){
    $('select#account-country').change(function (){
        var optionSelected = $(this).find("option:selected");
        var valueSelected = optionSelected.val();
        var countryName = optionSelected.text();
        data = {'countrydata':countryName}
        console.log(data);
        $.get('/getcity',data,function (result) {
            $("#account-city option").remove();
            $("#account-city").append("<option value='Choose City'>Choose City</option>");
            for (var i = result.length-1;i>=0;i--)
            {
                $("#account-city").append("<option value="+"\""+result[i].name+"\""+" >"+result[i].name+"</option>");
            }

        });
    })
})