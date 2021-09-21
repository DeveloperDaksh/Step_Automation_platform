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
$(function (){
    var counter=0;
    var hasFiles = false;
   $("#addFiledBtn").bind('click',function (){
       var selectedFiled = $("#selectCategory").val()
       var filedlabel = $("#form-filed-label").val()
       var required = true
       if($("#customSwitch1").prop("checked") == true){
           required = true
       }
       else {
           required = false
       }
       var form_div = $("#form-display")
       if(selectedFiled === ''){

       }
       if(selectedFiled === 'file'){
           hasFiles = true
           form_div.append(
               '<div class="mb-3 pb-1">'+
               '<label for="'+selectedFiled+counter.toString()+'" class="form-label px-0">'+filedlabel+'</label>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+
               '<input type='+selectedFiled+' class="form-control" name='+selectedFiled+counter.toString()+' id='+selectedFiled+counter.toString()+' required/>&nbsp;&nbsp;&nbsp;'+
               '<button type="button" value="Remove" class="remove" style="width: auto;float: right;background-color: crimson;border: none;cursor: pointer"><i class="ai-trash-2 fs-base me-2"></button>'+
               '</div>'
           )
           console.log(counter)
           counter = counter+1
       }
       else {
           console.log(selectedFiled)
           if(required){
               form_div.append(
                   '<div class="mb-3 pb-1">'+
                   '<label for="'+selectedFiled+counter.toString()+'" class="form-label px-0">'+filedlabel+'</label>'+
                   '<input type='+selectedFiled+' class="form-control" name='+selectedFiled+counter.toString()+' id='+selectedFiled+counter.toString()+' required/>&nbsp;&nbsp;&nbsp;'+
                   '<button type="button" value="Remove" class="remove" style="width: auto;float: right;background-color: crimson;border: none;cursor: pointer"><i class="ai-trash-2 fs-base me-2"></button>'+
                   '</div>'
               )
           }
           else {
               form_div.append(
                   '<div class="mb-3 pb-1">'+
                   '<label for="'+selectedFiled+counter.toString()+'" class="form-label px-0">'+filedlabel+'</label>'+
                   '<input type='+selectedFiled+' class="form-control" name='+selectedFiled+counter.toString()+' id='+selectedFiled+counter.toString()+'/>&nbsp;&nbsp;&nbsp;'+
                   '<button type="button" value="Remove" class="remove" style="width: auto;float: right;background-color: crimson;border: none;cursor: pointer"><i class="ai-trash-2 fs-base me-2"></button>'+
                   '</div>'
               )
           }
           counter = counter+1
       }
       document.getElementById("form-filed-label").value=""
   });
   $("body").on("click", ".remove", function () {
        $(this).closest("div").remove();
        console.log($(this).closest("div").find('input[type="file"]').length)
    });
   $("#get-form-link").bind('click',function (){
       var form_div = $("#form-display")
       if(form_div.find('input[type="file"]').length===0){
           hasFiles = false
       }
       else {
           hasFiles = true
       }
       console.log(document.getElementById("form-display"))
       $(".remove").remove()
       var final_form = document.getElementById("form-display").innerHTML
       console.log(final_form)
       var form_name = $("input[name=projectName]").val()
       var form_description = $("#project-description").val()
       const form_data = {'form_data':final_form,'form_name':form_name,'form_description':form_description,'has_files':hasFiles}
       $.ajaxSetup(
            {
                headers : {"X-CSRFToken":getCookie('csrftoken')},
            })
       $.post('/forms/processform',form_data,function (result) {
            console.log(result)
           if(result.status_msg==='Ok'){
               document.getElementById("form-display").innerHTML = null
               console.log(window.location.origin)
               document.getElementById("form-display-sucess").innerHTML = "<a href='/forms/publish/"+result.form_id+"'>"+window.location.origin+"/forms/publish/"+result.form_id+"</a>"
           }
           else {
               document.getElementById("form-display-err").innerText = "Form Name Already Exists"
           }
        });
   });
});

