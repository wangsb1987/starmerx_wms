function cancel_check()
{
    if($("#reason").val()=="")
    {
        alert("请输入询价单取消原因！");
        return false;
    }
    $.ajax({
        type: "GET",
        url: '/starmerx_cggl/cancel_purchase_order',
        //data: {'orderline':a},
        data:{'reason':$("#reason").val(),poid:$("#poid").val()},
        dataType: "json",
//        traditional: true,
        contentType: 'application/json' ,
        success: function(data)
        {
            //alert(data);
            if(data.result=="yes")
            {
                alert("取消成功");
                window.location.href='/starmerx_cggl/purchase_order_info/?poid='+data.POID;
            }
        }
    });
}

function confirmed_click()
{

    if($("#minimum_planned_date").val()=="None" || $("#minimum_planned_date").val()=="")
    {
        alert("请填写预计到货时间！");
        return false;
    }
    $.ajax({
        type: "GET",
        url: '/starmerx_cggl/confirmed_purchase_order',
        //data: {'orderline':a},
        data:{poid:$("#poid").val()},
        dataType: "json",
//        traditional: true,
        contentType: 'application/json' ,
        success: function(data)
        {
            //alert(data);
            if(data.result=="yes")
            {
                //alert("success");
                window.location.href='/starmerx_cggl/xjd_list';
            }
            else
            {
                alert(data.result);
            }
        }
    });
}

function edit_click()
{
    window.location.href='/starmerx_cggl/edit_purchase_order/?poid='+$("#poid").val();
}


function to_xjd_click()
{
    $.ajax({
        type: "GET",
        url: '/starmerx_cggl/reto_purchase_order',
        //data: {'orderline':a},
        data:{poid:$("#poid").val()},
        dataType: "json",
//        traditional: true,
        contentType: 'application/json' ,
        success: function(data)
        {
            //alert(data);
            if(data.result=="yes")
            {
                alert("成功");
                window.location.href='/starmerx_cggl/purchase_order_info/?poid='+data.POID;
            }
            else
            {
                alert(data.result);
            }
        }
    });
}