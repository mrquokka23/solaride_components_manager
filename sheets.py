import gspread

def get_data():
    sa = gspread.service_account()
    sh = sa.open("Components")

    wks = sh.worksheet("Sheet1")
    alldata = dict()

    for i in range(1, len(wks.col_values(1))):
        temp_data = dict()
        temp_data['MFGPN'] = wks.cell(i+1, 1).value
        temp_data['QUANTITY'] = int(wks.cell(i+1, 2).value)
        temp_data['CATEGORY'] = wks.cell(i+1, 3).value
        orders = []
        try:
            for j in wks.cell(i+1, 4).value.split(','):
                orders.append((j.split(':')[0], int(j.split(':')[1])))
        except:
            orders = []
        temp_data['ORDERS'] = orders
        temp_data['LOCATION'] = wks.cell(i+1, 5).value
        alldata[i] = temp_data

    return alldata

def update_data(data):
    sa = gspread.service_account()
    sh = sa.open("Components")

    wks = sh.worksheet("Sheet1")

    for i,v in enumerate(data.values()):
        wks.update_cell(i+2, 1, v['MFGPN'])
        wks.update_cell(i+2, 2, v['QUANTITY'])
        wks.update_cell(i+2, 3, v['CATEGORY'])
        orders = ''
        for j in v['ORDERS']:
            orders += f'{j[0]}:{j[1]},'
        wks.update_cell(i+2, 4, orders[:-1])
        wks.update_cell(i+2, 5, v['LOCATION'])
    c1 = len(wks.col_values(1))
    c2 = len(wks.col_values(1))-1
    if wks.cell(c1, 1).value == wks.cell(c2, 1).value:
        wks.update_cell(c1, 1, '')
        wks.update_cell(c1, 2, '')
        wks.update_cell(c1, 3, '')
        wks.update_cell(c1, 4, '')
        wks.update_cell(c1, 5, '')

def check(data):
    sa = gspread.service_account()
    sh = sa.open("Components")

    wks = sh.worksheet("Sheet1")
    if data['MFGPN'] in wks.col_values(1)[1:]:
        idx = wks.col_values(1).index(data['MFGPN'])
        orders = []
        try:
            for j in wks.cell(idx, 4).value.split(','):
                orders.append((j.split(':')[0], int(j.split(':')[1])))
        except:
            orders = []
        if orders:
            for order in orders:
                if order[0] == data['FROM'] and order[1] == data['ORDER']:
                    return True
            return False
                
        
