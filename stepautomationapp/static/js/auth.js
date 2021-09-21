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
    $("#submitb").click(function (event){
        event.preventDefault()
        const email = $("#email").val();
        const password = $("#password").val();
        const cpassword = $("#cpassword").val();
        if(cpassword!==password){
            document.getElementById("register-message").innerText="Password is not matched";
            document.getElementById("register-message").style.color="red";
        }
        else {
            const data={
                'email':email,
                'password':password
            }
            $.ajaxSetup(
            {
                headers : {"X-CSRFToken":getCookie('csrftoken')},
            })
            console.log("Hello")
            $('#loader2').removeClass('hidden')
            $.post('/signup',data,function (result){
                $('#loader2').addClass('hidden')
                if(result.status_msg==='Ok'){
                    document.getElementById("password").value="";
                    document.getElementById("cpassword").value="";
                    document.getElementById("register-message").innerText=result.msg;
                    document.getElementById("register-message").style.color="#2fc457";
                    window.location.href=window.location.origin+"/steps"
                }
                else {
                    document.getElementById("password").value="";
                    document.getElementById("cpassword").value="";
                    document.getElementById("register-message").innerText=result.msg;
                    document.getElementById("register-message").style.color="red";
                }
            });
        }
    });
    $("#submitl").click(function (event){
        event.preventDefault();
        let username = $("#emaill").val();
        let password = $("#passwordl").val();
        if($("#keep-signed").prop('checked')===true){
            var checked = true;
        }
        else {
            var checked = false
        }
        console.log(checked);
        console.log(username);
        console.log(password);
        const logindata = {
            'username':username,
            'password':password,
            'keepsignin':checked
        }
        $.ajaxSetup(
            {
                headers : {"X-CSRFToken":getCookie('csrftoken')}
            }
        )
        $('#loader1').removeClass('hidden')
        $.post('/signin',logindata,function (result){
            $('#loader1').addClass('hidden')
            if(result.status_msg==='Ok'){
                document.getElementById("passwordl").value="";
                window.location.href=window.location.origin+"/steps";
            }
            else {
                document.getElementById("passwordl").value="";
                document.getElementById("login-msg").innerText=result.msg;
                document.getElementById("register-message").style.color="red";
            }
        });
    });
});