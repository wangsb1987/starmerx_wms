# -*-coding:utf8-*-
import os

import psycopg2
import datetime
import xlwt, MySQLdb

"""
查询7.8.9月份最低采购价
"""


def export_info():

    conn = psycopg2.connect(host='122.5.32.82', database="starmerx", user="wenhuang", password="Wen2012", port="2543")
    cur = conn.cursor()


    print ':start------'
    sql = '''select sku,name,gys,pl,cgy,kfy,sum,price,sump,pid from tmpp1'''

    cur.execute(sql)
    result_all = cur.fetchall()
    print '''一共%s条记录------''' % (len(result_all),)
    workbook = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet('report')
    worksheet.write(0, 0, 'sku')
    worksheet.write(0, 1, '中文名称')
    worksheet.write(0, 2, '供应商')
    worksheet.write(0, 3, '品类')
    worksheet.write(0, 4, '采购员')
    worksheet.write(0, 5, '开发')
    worksheet.write(0, 6, '总数量')
    worksheet.write(0, 7, '单价')
    worksheet.write(0, 8, '总金额')

    worksheet.write(0, 9, '9月最低采购价')
    worksheet.write(0, 10, '供应商')
    worksheet.write(0, 11, '8月最低采购价')
    worksheet.write(0, 12, '供应商')
    worksheet.write(0, 13, '7月最低采购价')
    worksheet.write(0, 14, '供应商')


    i = 1
    count = 0
    for product in result_all:
        count += 1
        print count
        sku = product[0]
        name = product[1].replace('\n', ' ').replace('\t', ' ')
        gys = product[2]
        pl = product[3]

        cgy = product[4]
        kfy = product[5]
        sum = product[6]
        price = product[7]
        sump = product[8]
        product_id = product[9]

        # 9yue 最低采购价
        sql_9 = """select min(price_unit) min_price,c.name
                            from purchase_order_line a left join purchase_order b on a.order_id=b.id
                            left join res_partner c on c.id=a.partner_id
                            where product_id=%s and b.state not in('cancel','draft') and b.create_date < '2017-10-01' and b.create_date >= '2017-09-01'
                            group by c.name order by min_price limit 1
                            """ % (product_id,)
        cur.execute(sql_9)
        result_9 = cur.fetchone()
        min_9 = 0
        min_9_name = ''
        if result_9 and result_9[0]:
            min_9 = result_9[0]
            min_9_name = result_9[1]


        # 8yue 最低采购价
        sql_8 = """select min(price_unit) min_price,c.name
        from purchase_order_line a left join purchase_order b on a.order_id=b.id
        left join res_partner c on c.id=a.partner_id
        where product_id=%s and b.state not in('cancel','draft') and b.create_date < '2017-09-01' and b.create_date >= '2017-08-01'
        group by c.name order by min_price limit 1
        """ % (product_id, )
        cur.execute(sql_8)
        result_8 = cur.fetchone()
        min_8 = 0
        min_8_name = ''
        if result_8 and result_8[0]:
            min_8 = result_8[0]
            min_8_name = result_8[1]

        # 7yue 最低采购价
        sql_7 = """select min(price_unit) min_price,c.name
                        from purchase_order_line a left join purchase_order b on a.order_id=b.id
                        left join res_partner c on c.id=a.partner_id
                        where product_id=%s and b.state not in('cancel','draft') and b.create_date < '2017-08-01' and b.create_date >= '2017-07-01'
                        group by c.name order by min_price limit 1
                        """ % (product_id,)
        cur.execute(sql_7)
        result_7 = cur.fetchone()
        min_7 = 0
        min_7_name = ''
        if result_7 and result_7[0]:
            min_7 = result_7[0]
            min_7_name = result_7[1]

        worksheet.write(i, 0, sku)
        worksheet.write(i, 1, name)
        worksheet.write(i, 2, gys)
        worksheet.write(i, 3, pl)
        worksheet.write(i, 4, cgy)
        worksheet.write(i, 5, kfy)
        worksheet.write(i, 6, int(sum))
        worksheet.write(i, 7, str(price))
        worksheet.write(i, 8, str(sump))

        worksheet.write(i, 9, str(min_9))
        worksheet.write(i, 10, str(min_9_name))
        worksheet.write(i, 11, str(min_8))
        worksheet.write(i, 12, str(min_8_name))
        worksheet.write(i, 13, str(min_7))
        worksheet.write(i, 14, str(min_7_name))
        i += 1
    workbook.save('三个月采购价.xls')
    print '----------------end'
    cur.close()
    conn.close()

#上周的采购数据
def get_lastweek_po():
    conn = psycopg2.connect(host='122.5.32.82', database="starmerx", user="wenhuang", password="Wen2012", port="2543")
    cur = conn.cursor()

    # sql = '''select sku from tmpxx'''
    #
    # cur.execute(sql)
    # result_all = cur.fetchall()
    # print '''一共%s条记录------''' % (len(result_all),)

    sql = '''select product_id,sum(price_unit*product_qty),sum(product_qty) from purchase_order_line a left join purchase_order b on a.order_id=b.id where b.state !='cancel' 
    and b.stock_state in ('done','exception','assigned','receiving') and b.create_date>='2017-11-20' and b.create_date<'2017-11-26' and product_id!=2475 group by product_id'''
    cur.execute(sql)
    # result = cur.fetchone()
    result = cur.fetchall()

    workbook = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet('report')
    worksheet.write(0, 0, 'sku')
    worksheet.write(0, 1, '中文名称')
    worksheet.write(0, 2, '精品等级')
    worksheet.write(0, 3, '价格')
    worksheet.write(0, 4, '供应商名称')
    worksheet.write(0, 5, '采购员')
    worksheet.write(0, 6, '上周累计采购数量')
    worksheet.write(0, 7, '总金额')
    worksheet.write(0, 8, '首次采购时间')

    worksheet.write(0, 9, '首次采购数量')
    worksheet.write(0, 10, '首次采购单价')
    worksheet.write(0, 11, '历史总采购量')
    worksheet.write(0, 12, '历史总采购金额')
    worksheet.write(0, 13, '最近一次采购时间')
    worksheet.write(0, 14, '最近一次采购数量')
    worksheet.write(0, 15, '最近一次采购价')

    i=1
    if result:
        for pid in result:
            #获取首次采购时间
            sql1 = '''select min(a.create_date) from purchase_order_line a left join purchase_order b on a.order_id=b.id where b.state !='cancel' and product_id=%s''' % (pid[0],)
            cur.execute(sql1)
            result1 = cur.fetchall()
            sccgsj=''
            sccgsl = ''
            sccgdj = ''
            if result1:
                sccgsj=result1[0][0]
            sql2='''select product_qty,price_unit from purchase_order_line where product_id=%s and create_date=%s limit 1''' % (pid[0],'\''+str(sccgsj)+'\'')
            if sccgsj !=None and sccgsj !='':
                cur.execute(sql2)
                result2 = cur.fetchall()

                if result2:
                    sccgsl = result2[0][0]
                    sccgdj = result2[0][1]
            # 获取最近采购时间
            sql3 = '''select max(a.create_date) from purchase_order_line a left join purchase_order b on a.order_id=b.id where b.state !='cancel' and product_id=%s''' % (
            pid[0],)
            cur.execute(sql3)
            result3 = cur.fetchall()
            zjcgsj = ''
            zjcgsl = ''
            zjcgdj = ''
            if result3:
                zjcgsj = result3[0][0]
            sql4 = '''select product_qty,price_unit from purchase_order_line where product_id=%s and create_date=%s limit 1''' % (
            pid[0], '\''+str(zjcgsj)+'\'')
            if zjcgsj !=None and zjcgsj !='':
                cur.execute(sql4)
                result4 = cur.fetchall()

                if result2:
                    zjcgsl = result4[0][0]
                    zjcgdj = result4[0][1]

            sql_ls = '''select sum(price_unit*product_qty),sum(product_qty) from purchase_order_line a left join purchase_order b on a.order_id=b.id where b.state !='cancel' and product_id!=2475 and product_id=%s group by product_id''' % (pid[0],)
            cur.execute(sql_ls)
            result_ls = cur.fetchall()

            sql5='''select default_code,name_template,jingpin_level,price_unit,c.name,f.name from purchase_order_line a left join purchase_order b on a.order_id=b.id 
            left join res_partner c on c.id=b.partner_id
            left join res_users d on d.id=c.user_id
            left join res_partner f on d.partner_id=f.id
            left join product_product g on g.id=a.product_id
            left join product_template h on h.id=g.product_tmpl_id
            where b.state !='cancel' and b.stock_state in ('done','exception','assigned','receiving') and b.create_date>='2017-11-20' and b.create_date<'2017-11-26' and product_id!=2475 and product_id=%s''' % (pid[0],)
            cur.execute(sql5)
            result5 = cur.fetchall()
            if result5:
                for itema in result5:
                    worksheet.write(i, 0, itema[0])
                    worksheet.write(i, 1, itema[1])
                    worksheet.write(i, 2, itema[2])
                    worksheet.write(i, 3, itema[3])
                    worksheet.write(i, 4, itema[4])
                    worksheet.write(i, 5, itema[5])
                    worksheet.write(i, 6, pid[2])
                    worksheet.write(i, 7, pid[1])
                    worksheet.write(i, 8, sccgsj)

                    worksheet.write(i, 9, sccgsl)
                    worksheet.write(i, 10, sccgdj)
                    worksheet.write(i, 11, result_ls[0][1])
                    worksheet.write(i, 12, result_ls[0][0])
                    worksheet.write(i, 13, zjcgsj)
                    worksheet.write(i, 14, zjcgsl)
                    worksheet.write(i, 15, zjcgdj)
                    i += 1
                    print i
    workbook.save('每周采购数据2017-11-20.xls')
    print '----------------end'
    cur.close()
    conn.close()


#前两个月采购数据
def get_last2m_po():
    conn = psycopg2.connect(host='122.5.32.82', database="starmerx", user="wenhuang", password="Wen2012", port="2543")
    cur = conn.cursor()

    # sql = '''select sku from tmpxx'''
    #
    # cur.execute(sql)
    # result_all = cur.fetchall()
    # print '''一共%s条记录------''' % (len(result_all),)

    sql = '''select product_id from purchase_order_line a left join purchase_order b on a.order_id=b.id 
    left join product_product c on c.id=a.product_id
    left join product_template d on c.product_tmpl_id=d.id
    where jingpin_level in ('1','2') and b.location_id in (135,141,16,19,146,147,183,184,195,197) and b.state !='cancel' and b.create_date>='2017-09-20' and b.create_date<'2017-11-21' and product_id!=2475 group by product_id'''
    cur.execute(sql)
    # result = cur.fetchone()
    result = cur.fetchall()

    workbook = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet('report')
    worksheet.write(0, 0, 'sku')
    worksheet.write(0, 1, '中文名称')
    worksheet.write(0, 2, '精品等级')
    worksheet.write(0, 3, '最近采购价')
    worksheet.write(0, 4, '供应商名称')
    worksheet.write(0, 5, '采购员')
    worksheet.write(0, 6, '首次采购时间')
    worksheet.write(0, 7, '首次采购数量')
    worksheet.write(0, 8, '首次采购单价')
    worksheet.write(0, 9, '第二次采购时间')
    worksheet.write(0, 10, '第二次采购数量')
    worksheet.write(0, 11, '第二次采购价')
    worksheet.write(0, 12, '累积总采购量')
    worksheet.write(0, 13, '累积总采购金额')

    i=1
    if result:
        for pid in result:
            #获取首次采购时间
            sql1 = '''select min(a.create_date) from purchase_order_line a left join purchase_order b on a.order_id=b.id where b.state !='cancel' and product_id=%s''' % (pid[0],)
            cur.execute(sql1)
            result1 = cur.fetchall()
            sccgsj=''
            sccgsl = ''
            sccgdj = ''

            d2cgsj = ''
            d2cgsl = ''
            d2cgdj = ''
            if result1:
                sccgsj=result1[0][0]
            sql2='''select product_qty,price_unit from purchase_order_line where product_id=%s and create_date=%s limit 1''' % (pid[0],'\''+str(sccgsj)+'\'')
            if sccgsj !=None and sccgsj !='':
                cur.execute(sql2)
                result2 = cur.fetchall()

                if result2:
                    sccgsl = result2[0][0]
                    sccgdj = result2[0][1]
                # 获取第2采购时间
                sql3 = '''select min(a.create_date) from purchase_order_line a left join purchase_order b on a.order_id=b.id where b.state !='cancel' and product_id=%s and a.create_date != %s''' % (
                pid[0],'\''+str(sccgsj)+'\'')
                cur.execute(sql3)
                result3 = cur.fetchall()

                if result3:
                    d2cgsj = result3[0][0]
                sql4 = '''select product_qty,price_unit from purchase_order_line where product_id=%s and create_date=%s limit 1''' % (
                pid[0], '\''+str(d2cgsj)+'\'')
                if d2cgsj !=None and d2cgsj !='':
                    cur.execute(sql4)
                    result4 = cur.fetchall()

                    if result2:
                        d2cgsl = result4[0][0]
                        d2cgdj = result4[0][1]

            sql_ls = '''select sum(price_unit*product_qty),sum(product_qty) from purchase_order_line a left join purchase_order b on a.order_id=b.id where b.state !='cancel' and product_id!=2475 and product_id=%s group by product_id''' % (pid[0],)
            cur.execute(sql_ls)
            result_ls = cur.fetchall()

            sql5='''select default_code,name_template,jingpin_level,price_unit,c.name,f.name from purchase_order_line a left join purchase_order b on a.order_id=b.id 
            left join res_partner c on c.id=b.partner_id
            left join res_users d on d.id=c.user_id
            left join res_partner f on d.partner_id=f.id
            left join product_product g on g.id=a.product_id
            left join product_template h on h.id=g.product_tmpl_id
            where b.state !='cancel' and b.create_date>='2017-09-20' and b.create_date<'2017-11-21' and product_id!=2475 and product_id=%s''' % (pid[0],)
            cur.execute(sql5)
            result5 = cur.fetchall()
            if result5:
                for itema in result5:
                    worksheet.write(i, 0, itema[0])
                    worksheet.write(i, 1, itema[1])
                    worksheet.write(i, 2, itema[2])
                    worksheet.write(i, 3, itema[3])
                    worksheet.write(i, 4, itema[4])
                    worksheet.write(i, 5, itema[5])
                    worksheet.write(i, 6, sccgsj)
                    worksheet.write(i, 7, sccgsl)
                    worksheet.write(i, 8, sccgdj)

                    worksheet.write(i, 9, d2cgsj)
                    worksheet.write(i, 10, d2cgsl)
                    worksheet.write(i, 11, d2cgdj)
                    worksheet.write(i, 12, result_ls[0][1])
                    worksheet.write(i, 13, result_ls[0][0])
                    i += 1
                    print i
    workbook.save('前两个月采购数据2017-11-21.xls')
    print '----------------end'
    cur.close()
    conn.close()

# 晚上发送库存
def get_inventory():
    conn = psycopg2.connect(host='122.5.32.82', database="starmerx", user="wenhuang", password="Wen2012",
                            port="2543")
    cur = conn.cursor()

    # sql = '''select sku from tmpxx'''
    #
    # cur.execute(sql)
    # result_all = cur.fetchall()
    # print '''一共%s条记录------''' % (len(result_all),)

    sql = '''select default_code,name_template,stock_qty,c.name from starmerx_inventory a left join product_product b on a.product_id=b.id 
    left join stock_warehouse c on c.lot_input_id=a.location_id
    where  a.location_id in (195,197) and  a.type='shelf' and stock_qty>0 order by c.name'''
    cur.execute(sql)
    # result = cur.fetchone()
    result = cur.fetchall()

    workbook = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet('report')
    worksheet.write(0, 0, 'sku')
    worksheet.write(0, 1, '中文名称')
    worksheet.write(0, 2, '库存')
    worksheet.write(0, 3, '仓库')


    i = 1
    if result:
        for itema in result:
            worksheet.write(i, 0, itema[0])
            worksheet.write(i, 1, itema[1])
            worksheet.write(i, 2, itema[2])
            worksheet.write(i, 3, itema[3])

            i += 1
            print i
    try:
        os.remove('/home/winbo/djang_poj/wms/master/myviews/report.xls')
    except:
        print 'error'
    workbook.save('/home/winbo/djang_poj/wms/master/myviews/report.xls')

    print '----------------end'
    cur.close()
    conn.close()

if __name__ == '__main__':
    #export_info()
    get_lastweek_po()
    # get_last2m_po()
    # get_inventory()