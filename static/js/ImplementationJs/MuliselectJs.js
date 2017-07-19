


var expanded = false;

function showCheckboxes() {
  var checkboxes = document.getElementById("checkboxes");
  if (!expanded) {
    checkboxes.style.display = "block";
    expanded = true;
  } else {
    checkboxes.style.display = "none";
    expanded = false;
  }
}


function assiosiated_employees(serviceid) {
    alert(serviceid);
    $.ajax({
            method:'get',
            url:"/services/associated_employee_names/" + serviceid,
            data: { },
            dataType: "json",
            success:function(response){
                console.log(response);
                employeelist =eval(response);

                var employeename ="";
                if (employeelist != null &&  employeelist.length > 0  ){
                      for (var i = 0; i <  employeelist.length; i++)
                      {
                          checked="";
                          if (employeelist[i].checked) {
                                 checked = "checked" ;
                           }
                            employeename+= "<label for=" + employeelist[i].name +  ' > <input type="checkbox" name=' + "check" + employeelist[i].id  + ' ng-model=' + "servicedata.check" + employeelist[i].id.toString() +       " value=" + employeelist[i].id + " " + checked + " />" + employeelist[i].name + " </label>";
                        
                      }
                      $( "#checkboxes" ).append( employeename);

                }

            }
      });
  }
        
function delete_image(serviceid) {
    $.ajax({
            method:'get',
            url:"/services/deleteimage/" + serviceid,
            data: { },
            async:false,
            success:function(response){
                console.log(response);
                var pic = document.getElementById('service_img');
                pic.src = response
            },
             error: function(xhr, status, error){
             var err = eval("(" + xhr.responseText + ")");
             }
    });  

}