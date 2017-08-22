/**
 *初始化table数据
 */

var $table = $('#bootstraptable');
var $checked = $('#checked');
var $notpass = $('#notpass');

function init(categoryid) {
    $table.bootstrapTable({
        url: '/starmerx_cwgl/get_invoice_list',
        toolbar:"#toolbar",
        striped: true,
        sortOrder: "asc", //排序方式
        minimumCountColumns: 2,
        queryParamsType: 'limit',
        queryParams: queryParams,
        pagination: true,
        idField: 'id',
        //height: getHeight(),
        weight: '100%',
        pageSize: '20',
        pageList: '[20,50,100,200]',
        showFooter: false,
        paginationPreText: "上一页",
        paginationNextText: "下一页",
        sidePagination: 'server',
        //responseHandler: responseHandler,
        detailView: true,
        columns: [
        {
         checkbox: true
         }, {
         field: 'partner',
         title: '供应商',
         formatter: function (value, row, index) {
                                return "<a href='/starmerx_cwgl/invoice_info/?invoice_id=" + row.id + "'>" + value + "</a>";
                            }
         }, {
         field: 'date_invoice',
         title: '发票日期'
         }, {
         field: 'number',
         title: '凭证号'
         },{
         field: 'user',
         title: '销售员'
         },{
         field: 'payment_mode',
         title: '付款方式'
         },{
         field: 'date_due',
         title: '到期日期'
         },{
         field: 'origin',
         title: '源单据'
         },{
         field: 'currency',
         title: '币别'
         },{
         field: 'residual',
         title: '余额'
         },{
         field: 'amount_untaxed',
         title: '小计'
         },{
         field: 'amount_total',
         title: '合计'
         },{
         field: 'state',
         title: '状态'
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
        ],
        detailFormatter: function (index, row, element) {
            return '<table></table>';
            var html = [];
            $.each(row, function (key, value) {
                html.push('<table></table>');
            });
            return html.join('');
        }
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


    $table.on('expand-row.bs.table', function (e, index, row, $detail) {
        var children = row.product_list;
        if (children == false) {
            $table.bootstrapTable('collapseRow', index);
            return;
        }

        InitSubTable(index, row, $detail);
    });
}

var InitSubTable = function (index, row, $detail) {
    var cur_table = $detail.html('<table></table>').find('table');
    cur_table.attr('id', row.id);
    $(cur_table).bootstrapTable({
        data: row.product_list,
        clickToSelect: true,
        detailView: false,//父子表
        uniqueId: "MENU_ID",
        pagination: false,
        pageSize: 10,
        pageList: [10, 25],
        columns: [
            // {
            //     checkbox: true
            // },
            {
                field: 'name',
                title: '名称',
                align: 'center',
                valign: 'middle',
                formatter: function (value, row, index) {
                    return value;
                }
            },
            {
                field: 'price_unit',
                title: '单价',
                align: 'center',
                valign: 'middle',
                formatter: function (value) {
                    return value;
                },
                width: '60px'
            },
            {
                field: 'quantity',
                title: '数量',
                align: 'center',
                valign: 'middle',
                formatter: function (value, row, index) {
                    return value;
                },
            },
            {
                field: 'price_last',
                title: '上次采购价',
                align: 'center',
                valign: 'middle',
                formatter: function (value) {
                    return value;
                }
            },
        ]
    });
};


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

    params['paymode']=$("#paymode_qt").val();
    //alert($("#paymode_qt").val());

    params['origin']=$("#origin_qt").val();
    params['state']=$("#state_qt").val();

    return params;
}

$('#btn_query').click(function () {
    $table.bootstrapTable('refreshOptions', {
        queryParams: queryParams,
        pageNumber: 1
    });
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


