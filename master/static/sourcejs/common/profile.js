$(function () {

});
var changepswsign = false;
function changepsw_change(){
    //alert("change事件触发");
    changepswsign=!changepswsign;
    if(changepswsign)
    {

        $('#newpsw').removeAttr("disabled");
    }
    else
    {
        $('#newpsw').attr("disabled","disabled");
    }
    }