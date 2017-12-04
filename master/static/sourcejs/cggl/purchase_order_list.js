/**
 *初始化table数据
 */

var $table = $('#bootstraptable');
var $checked = $('#checked');
var $notpass = $('#notpass');

function init(categoryid) {
    $table.bootstrapTable({
        url: '/starmerx_cggl/get_purchase_order_list',
        toolbar:"#toolbar",
        striped: true,
        sortOrder: "desc", //排序方式
        minimumCountColumns: 2,
        queryParamsType: 'limit',
        queryParams: queryParams,
        pagination: true,
        idField: 'id',
        //height: getHeight(),
        weight: '100%',
        pageSize: '100',
        pageList: '[20,50,100,200]',
        showFooter: false,
        paginationPreText: "上一页",
        paginationNextText: "下一页",
        sidePagination: 'server',
        //responseHandler: responseHandler,
        detailView: false,
        columns: [
        {
         checkbox: true
         }, {
         field: 'name',
         title: '单号',
         formatter: function (value, row, index) {
                                return "<a href='/starmerx_cggl/purchase_order_info/?poid=" + row.id + "'>" + value + "</a>";
                            }
         }, {
         field: 'create_date',
         title: '创建日期',
         sortable:true
         },{
         field: 'partner',
         title: '供应商',
         sortable:true
         },{
         field: 'origin',
         title: '源单据'
         },{
         field: 'amount_total',
         title: '合计'
         },{
         field: 'state',
         title: '状态'
         },{
         field: 'account_state',
         title: '发票状态'
         },{
         field: 'stock_state',
         title: '仓库状态'
         },{
         field: 'location',
         title: '目标仓库'
         },{
         field: 'purchaser',
         title: '采购人'
         },
              <!--{-->
                  <!--title: '操作',-->
                  <!--field: 'id',-->
                  <!--align: 'center',-->
                  <!--formatter:function(value,row,index){-->
                       <!--var e = '<a href="#" mce_href="#" onclick="edit(\''+ row.id + '\')">编辑</a> ';-->
                       <!--var d = '<a href="#" mce_href="#" onclick="del(\''+ row.id +'\')">删除</a> ';-->
                    <!--return e+d;-->
                <!--}-->
              <!--}-->
        ]
    });

    setTimeout(function () {
        $table.bootstrapTable('resetView');
    }, 200);
    $table.on('check.bs.table uncheck.bs.table ' +
                'check-all.bs.table uncheck-all.bs.table', function () {
            $checked.prop('disabled', !$table.bootstrapTable('getSelections').length);
            $notpass.prop('disabled', !$table.bootstrapTable('getSelections').length);
            // save your data, here just save the current page
            selections = getIdSelections();
            //alert(selections);
            // push or splice the selections if you want to save all data selections
        });

        $checked.click(function () {
            var ids = getIdSelections();
            //$table.bootstrapTable('remove', {
            //    field: 'id',
            //    values: ids
            //});
            //审核通过事件处理的方法
            alert('点击了审核通过，ids:'+ids);
            $checked.prop('disabled', true);
        });

        $notpass.click(function () {
            var ids = getIdSelections();
            //$table.bootstrapTable('remove', {
            //    field: 'id',
            //    values: ids
            //});
            alert('点击了审核不通过，ids:'+ids);
            //审核不通过事件处理的方法
            $notpass.prop('disabled', true);
        });



}


function getIdSelections() {
    return $.map($table.bootstrapTable('getSelections'), function (row) {
        return row.id
    });
}

window.operateEvents = {};

function getHeight() {
    return $(window).height() * 0.80;
}


function queryParams(params) {

    params['name_qt']=$("#name_qt").val();
    params['partner_id']=$("#partner_id").val();
    params['sku_qt']=$("#sku_qt").val();
    //alert($("#paymode_qt").val());

    return params;
}

$('#btn_query').click(function () {
    $table.bootstrapTable('refreshOptions', {
        queryParams: queryParams,
        pageNumber: 1
    });
});

$('#btn_create').click(function () {
    window.location.href="/starmerx_cggl/purchase_order_add";
});

//===============

$(function () {
    var scripts = [
        location.search.substring(1) || '/static/bootstrap_table/bootstrap-table.js',
        '/static/bootstrap_table/bootstrap-table-export.js',
        '/static/bootstrap_table/tableExport.js',
        '/static/bootstrap_table/bootstrap-table-editable.js',
        '/static/bootstrap_table/bootstrap-editable.js',
        '/static/bootstrap_table/bootstrap-table-zh-CN.js'
        ],
        eachSeries = function (arr, iterator, callback) {
            callback = callback || function () {};
            if (!arr.length) {
                return callback();
            }
            var completed = 0;
            var iterate = function () {
                iterator(arr[completed], function (err) {
                    if (err) {
                        callback(err);
                        callback = function () {};
                    }
                    else {
                        completed += 1;
                        if (completed >= arr.length) {
                            callback(null);
                        }
                        else {
                            iterate();
                        }
                    }
                });
            };
            iterate();
        };

    eachSeries(scripts, getScript, init);


    //供应商
 $("#partner_id").select2({
            tags: "true",
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
});

function getScript(url, callback) {
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.src = url;

    var done = false;
    // Attach handlers for all browsers
    script.onload = script.onreadystatechange = function() {
        if (!done && (!this.readyState ||
                this.readyState == 'loaded' || this.readyState == 'complete')) {
            done = true;
            if (callback)
                callback();

            // Handle memory leak in IE
            script.onload = script.onreadystatechange = null;
        }
    };

    head.appendChild(script);

    // We handle everything using the script element injection
    return undefined;
}


