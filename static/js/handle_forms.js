function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$(document).ready(function (){
    $('select#user-form').change(function (){
        var optionSelected = $(this).find("option:selected");
        var valueSelected = optionSelected.val();
        var selectedForm = optionSelected.text();
        data = {'formdata':selectedForm}
        console.log(data);
        $.ajaxSetup(
            {
                headers : {"X-CSRFToken":getCookie('csrftoken')},
            })
        $.post('/forms/getform',data,function (result) {
            console.log(result)
        });
    })
});