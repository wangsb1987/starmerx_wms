function cancelsave()
{
    window.location.href='/starmerx_cggl/xjd_list';
}

var a = new Array();
var b = new Array();
$(function () {
//
//$('#datatb tr').each(function(rowindex){
//    if(rowindex!=0)
//    {
//        a.push({'product_id':$(this).find('td').eq(1).find("input").val(),'price_unit':$(this).find('td').eq(4).text(),
//            'product_qty':parseInt($(this).find('td').eq(2).text())})
//        b.push({'product_name':$(this).find('td').eq(1).text(),'price_unit':$(this).find('td').eq(4).text(),
//            'product_qty':parseInt($(this).find('td').eq(2).text())})
//    }
//});
//alert(a);
 //远程筛选//产品
 $("#product_id").select2({
            tags: false,
            theme: "bootstrap",
            allowClear: true,
            placeholder: "选择产品",
            ajax:{
                url: '/common/getProducts',
                type: "GET",
                dataType:"json",
                delay:250,
                data:function(params){
                    return {
                        name: params.term,
                        page: params.page || 1
                    };
                },
                cache:true,
                processResults: function (res, params) {
                    //alert(res["data"]['suppliers']);
                    var products = res["data"]['products'];
                    var ops=[];
                    var data = $.map(products, function (obj) {
                    //alert(obj.last_purchase_price);
                        ops.push({'id':obj.id,'price':obj.last_purchase_price});
                    return ops;
                    });

                    var options = [];
                    for(var i= 0, len=products.length;i<len;i++){
                        var option = {"id":products[i]["id"],"text":"["+products[i]["default_code"]+"]"+products[i]["name_template"]};
                        options.push(option);
                    }
                    return {
                        results: options,
                        pagination: {
                            more:res["data"]["more"]
                        }
                    };
                },
                escapeMarkup: function (markup) { return markup; },
                minimumInputLength: 1
            }
        });


 //供应商
 $("#partner_id").select2({
            tags: false,
            theme: "bootstrap",
            allowClear: true,
            placeholder: "选择供应商",
            ajax:{
                url: '/common/getSupplier',
                type: "GET",
                dataType:"json",
                delay:250,
                data:function(params){
                    return {
                        name: params.term,
                        page: params.page || 1
                    };
                },
                cache:true,
                processResults: function (res, params) {
                    //alert(res["data"]['suppliers']);
                    var supplier = res["data"]['supplier'];
                    var ops=[];
                    var data = $.map(supplier, function (obj) {
                    //alert(obj.last_purchase_price);
                        ops.push({'id':obj.id,'price':obj.last_purchase_price});
                    return ops;
                    });

                    var options = [];
                    for(var i= 0, len=supplier.length;i<len;i++){
                        var option = {"id":supplier[i]["id"],"text":supplier[i]["name"]};
                        options.push(option);
                    }
                    return {
                        results: options,
                        pagination: {
                            more:res["data"]["more"]
                        }
                    };
                },
                escapeMarkup: function (markup) { return markup; },
                minimumInputLength: 1
            }
        });
    $('#product_id').change(function()
    {
//        alert(alldata);
//        if($("product_id").val()!=0)
//        {
//            for(var i=0;i<10;i++)
//            {
//                if($("product_id").val()==alldata[i].id)
//                {
//                    $("#last_purchase_price").val(alldata.last_purchase_price);
//                }
//            }
//        }
//        $("#last_purchase_price").val($(this).children('option:selected').attr("data-price"));
//        alert($(this).children('option:selected').val());
//        alert($(this).children('option:selected').attr("data-price"));
//        var p1=$(this).children('option:selected').val();//这就是selected的值
//        var p2=$('#param2').val();//获取本页面其他标签的值
        //window.location.href="xx.PHP?param1="+p1+"¶m2="+p2+"";//页面跳转并传参
    });


});
//=====未用
function addclick()
{
    resetValue();
    $('#savebtn').show();
	$('#editbtn').hide();
	$('#myModal').modal('show');
}
//=====未用
function resetValue()
{
    $('#product_id').val(0).trigger("change");
    //$("#product_id").selectpicker('val','0');//对product_id这个下拉框进行重置刷新
	//$("#product_uom").selectpicker('val','0');//对product_uom这个下拉框进行重置刷新
	//$("#product_uom").val(0);
    $("#price_unit").val("");
    $("#product_qty").val("");
    $("#last_purchase_price").val("");

}


function check_input()
{
    if($("#partner_id").val()==0)
    {
        alert("请选择供应商");
        return false;
    }

    if($("#payment_mode").val()==0 || $("#payment_mode").val()==null ||$("#payment_mode").val()=="")
    {
        alert("请选择付款方式");
        return false;
    }
    if($("#location_id").val()==0)
    {
        alert("请选择目标仓库");
        return false;
    }
//    if($("#minimum_planned_date").val()=="")
//    {
//        alert("请选择预计到货时间");
//        return false;
//    }

    bdtabledata();
    if(a.length<=0)
    {
        alert("请至少添加一条采购详情");
        return false;
    }
    save_click();
}
function save_click()
{

    $.ajax({
        type: "GET",
        url: '/starmerx_cggl/update_purchase_order',
        //data: {'orderline':a},
        data:{'poid':$("#poid").val(),'orderline':JSON.stringify(a),'partner_id':$("#partner_id").val(),
        'partner_ref':$("#partner_ref").val(),'payment_mode':$("#payment_mode").val(),
        'location_id':$("#location_id").val(),'logistics_company':$("#logistics_company").val(),
        'track_number':$("#track_number").val(),'notes':$("#notes").val(),'amount_total':$("#amount_total").html(),
        'invoice_method':$("#invoice_method").val(),'minimum_planned_date':$("#minimum_planned_date").val()},
        dataType: "json",
//        traditional: true,
        contentType: 'application/json' ,
        success: function(data)
        {
            //alert(data.result);
            if(data.result=="yes")
            {
                alert("保存成功");
                window.location.href='/starmerx_cggl/purchase_order_info/?poid='+data.POID;
            }
            else
            {
                alert(data.result);
            }
        }
    });
}

//=====未用
function checkedit(){
	if($("#selrowindex").val()=="")
	{
	    alert("请选择要编辑的记录");
		return false;
	}
	var str= new Array();
	str=$("#selrowindex").val().split(",");
	if(str.length!=1)
	{
		alert("请选择一条记录编辑");
    	return false;
	}
    //alert($('#datatb tr').eq($("#selrowindex").val()).find("td").eq(1).html());



    //===一般select设置选中项
    //$("#product_id option[value="+a[$("#selrowindex").val()].product_id+"]").attr("selected", true);
    //====bootstrap select设置选中项
    //$('#product_id').selectpicker('val',a[$("#selrowindex").val()].product_id);
    //$("#product_id").val(a[$("#selrowindex").val()].product_id);
    rowindex = $("#selrowindex").val()+1;
    //alert($('#datatb').find('tr:eq('+rowindex+')').find('td:eq(4)').text());

    $("#price_unit").val($('#datatb').find('tr:eq('+rowindex+')').find('td:eq(4)').text());
    $("#product_qty").val($('#datatb').find('tr:eq('+rowindex+')').find('td:eq(2)').text());

    //$("#product_uom option[value="+a[$("#selrowindex").val()].product_uom+"]").attr("selected", true);
    //$('#product_uom').selectpicker('val',a[$("#selrowindex").val()].product_uom);
    //$("#product_uom").val(a[$("#selrowindex").val()].product_uom);
    //$("#product_uom").val($('#datatb').find('tr:eq('+rowindex+')').find('td:eq(3)').find("input").val());
    //$(".product_uom").find("option[text="+$('#datatb').find('tr:eq('+rowindex+')').find('td:eq(3)').text()+"]").attr("selected",true);

	$('#myModal').modal('show');
	$('#savebtn').hide();
	$('#editbtn').show();
}
//=====未用
function bllist()
{
    $("#selrowindex").val('');
    //alert(allcount);
    var j=0;
    for(var i=0;i<$("#datatb").find("tr").length-1;i++)
    {
        var chkid="chk"+i;
        //alert(document.getElementById(chkid).checked);
        if(document.getElementById(chkid).checked)
        {
            $("#selrowindex").val($("#selrowindex").val()+i+",");
        }
    }
    var selindexstr=$("#selrowindex").val();
    //alert(selindexstr);
    $("#selrowindex").val(selindexstr.substring(0,selindexstr.length-1));
}


//=====未用
function editpurchaseline()
{
    if($("#price_unit").val()<=0 || $("#product_qty").val()<=0)
    {
        alert("价格和数量不能小于等于0");
        return false;
    }
    if($("#product_id").val()<=0 )
    {
        alert("请选择产品");
        return false;
    }
    a[$("#selrowindex").val()].product_id=$("#product_id").val();
//    a[$("#selrowindex").val()].product_uom=$("#product_uom").val();
    a[$("#selrowindex").val()].price_unit=$("#price_unit").val();
    a[$("#selrowindex").val()].product_qty=$("#product_qty").val();

    b[$("#selrowindex").val()].product_name=$("#product_id").find("option:selected").text();
    //b[$("#selrowindex").val()].product_uom_name=$("#product_uom").find("option:selected").text();
    b[$("#selrowindex").val()].price_unit=$("#price_unit").val();
    b[$("#selrowindex").val()].product_qty=$("#product_qty").val();
    bdhtml();
}



//=====未用
function bdhtml()
{
    var html="<tbody><tr><th style='width:5%'></th><th style='width:68%'>产品</th><th style='width:8%'>数量</th><th style='width: 9%'>单价</th><th style='width: 10%'>小计</th></tr>";
    var total_price=0.0;
    for(var i =0; i<b.length; i++){
        //alert(a[i]);
        var xj=b[i].product_qty*b[i].price_unit*1.00;
        total_price += b[i].product_qty*b[i].price_unit;
        html+="<tr><td><input type='checkbox'  id=chk"
				+i
				+" class='checkbox-red' onclick='bllist();' /></td><td>"+b[i].product_name+"</td><td>"+b[i].product_qty+"</td><td>"+b[i].price_unit+"</td><td>"+xj+"</td></tr>";
    }
    $("#amount_total").html(total_price);
    html+="</tbody>";
    $("#datatb").html(html);
    $('#myModal').modal('hide');
    resetValue();
}


//=====未用
function checkdel(){
    if($("#selrowindex").val()=="")
    {
        alert("请选择要删除的记录");
        return false;
    }
    var str= new Array();
	str=$("#selrowindex").val().split(",");
	if(str.length!=1)
	{
		alert("请选择一条记录删除");
    	return false;
	}

    a.splice($("#selrowindex").val(),1);//从下标为i的元素开始，连续删除1个元素
    b.splice($("#selrowindex").val(),1);//从下标为i的元素开始，连续删除1个元素

    bdhtml();
}


function addpurchaseline_click()
{

    if($("#price_unit").val()<=0 || $("#product_qty").val()<=0)
    {
        alert("价格和数量不能小于等于0");
        return false;
    }
    if($("#product_id").val()<=0 )
    {
        alert("请选择产品");
        return false;
    }
    for(var i =0; i<a.length; i++)
    {
        if(a[i].product_id==$("#product_id").val())
        {
            alert("已经添加过改sku，不允许重复添加");
            return false;
        }
    }
//    a.push({'product_id':$("#product_id").val(),'price_unit':$("#price_unit").val(),
//        'product_qty':$("#product_qty").val()})
//    b.push({'product_name':$("#product_id").find("option:selected").text(),'price_unit':$("#price_unit").val(),
//        'product_qty':$("#product_qty").val()})

    var xj=($("#product_qty").val()*$("#price_unit").val()).toFixed(2);
    var table = $("#para_table");
    var tr= $("<tr>" +
        "<td>"+$("#product_id").find("option:selected").text()+"<input type='hidden' value="+$("#product_id").val()+"></td>" +
        "<td  onclick='tdclick(this)'>"+$("#product_qty").val()+"</td>" +
        "<td  onclick='tdclick(this)'>"+$("#price_unit").val()+"</td>" +
        "<td >"+xj+"</td>" +
        "<td ></td>" +
        "<td ><input type='hidden' value='0'/></td>" +
        "<td  align='center' onclick='deletetr(this)'><i class='fa fa-remove'></i></td></tr>");
    table.append(tr);
    writehj();
    bdtabledata();
}


function deletetr(tdobject){
    var td=$(tdobject);
    if(parseInt(td.parents("tr").find('td').eq(1).text())==0)
    {
        alert("不能删除该记录");
        return false;
    }
    td.parents("tr").remove();
    //alert(td.parents("tr").find('td').eq(1).text());
    writehj();
    bdtabledata();
}

function tdclick(tdobject){
    var td=$(tdobject);
    td.attr("onclick", "");
    //1,取出当前td中的文本内容保存起来
    var text=td.text();
    //2,清空td里面的内容
    td.html(""); //也可以用td.empty();
    //3，建立一个文本框，也就是input的元素节点
    var input=$("<input>");
    //4，设置文本框的值是保存起来的文本内容
    input.attr("class","form-control");
    input.attr("value",text);
    input.bind("blur",function(){
        var inputnode=$(this);
        var inputtext=inputnode.val();
        var tdNode=inputnode.parent();
        tdNode.html(inputtext);
        //tdNode.click(tdclick);
        td.attr("onclick", "tdclick(this)");
        writehj();
        bdtabledata();
    });
    input.keyup(function(event){
        var myEvent =event||window.event;
        var kcode=myEvent.keyCode;
        if(kcode==13){
            var inputnode=$(this);
            var inputtext=inputnode.val();
            var tdNode=inputnode.parent();
            tdNode.html(inputtext);
            //tdNode.click(tdclick);
            td.attr("onclick", "tdclick(this)");
            writehj();
            bdtabledata();
        }
    });

    //5，将文本框加入到td中
    td.append(input);
    var t =input.val();
    input.val("").focus().val(t);
//              input.focus();

    //6,清除点击事件
    td.unbind("click");
}

function bdtabledata(){
a=[];
$('#para_table tr').each(function(rowindex){
    if(rowindex!=0)
    {
        var person_stock_id=0;
        var move_dest_id=0;
        if($(this).find('td').eq(5).find("input").val()==""||$(this).find('td').eq(5).find("input").val()=="None"||$(this).find('td').eq(5).find("input").val()=="0")
        {
            person_stock_id="None";
        }
        else
        {
            person_stock_id=$(this).find('td').eq(5).find("input").val();
        }

        if($(this).find('td').eq(4).find("input").val()==""||$(this).find('td').eq(4).find("input").val()=="None"||$(this).find('td').eq(4).find("input").val()=="0")
        {
            move_dest_id="None";
        }
        else
        {
            move_dest_id=$(this).find('td').eq(4).find("input").val();
        }
        a.push({'product_id':$(this).find('td').eq(0).find("input").val(),'price_unit':$(this).find('td').eq(2).text(),
            'product_qty':parseInt($(this).find('td').eq(1).text()),'person_stock_id':person_stock_id,'move_dest_id':move_dest_id})
    }
});
}


//更新合计
function writehj()
{
    sumhj =0.00;
    $('#para_table tr').each(function(rowindex)
    {
        if(rowindex!=0)
        {
            sumhj +=$(this).find('td').eq(2).text()*parseInt($(this).find('td').eq(1).text());
        }
    });
    $("#amount_total").html(sumhj.toFixed(2));
}