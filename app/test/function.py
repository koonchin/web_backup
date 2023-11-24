from datetime import datetime
import json
import re,requests,os
from io import BytesIO
import mysql.connector

def send_line(msg):
    url = 'https://notify-api.line.me/api/notify'
    token = 'BwqCOMpZzAPD4fEvWSpAH0MBJjRxkZd6vrFzVKVdTFr'
    headers = {'content-type': 'application/x-www-form-urlencoded',
               'Authorization': 'Bearer '+token}
    r = requests.post(url, headers=headers, data={'message': msg})


def get_api_register(department, api):
    """
    select {column} from store_api where department
    """
    mycursor = db.query(
        f"select {api} from store_api where department = '{department}'")
    try:
        return list(mycursor.fetchall())[0][0]
    except:
        return None

def get_idsell(string:str):
    char = string.split('-')[0].split('0')[0]
    if 'q' in char.lower():
        return ''
    try:
        number = int(string.split('-')[0].split(char)[1])
    except Exception as e:
        return (f'error at {string} cuz {e}')
    if len(char) > 1:
        char = char[-1]
    return char + str(number)

def getdata(path:str or None):
    lines = []
    with open(path) as f:
        lines = f.readlines()
    for line in lines:
        lines[lines.index(line)] = line.split(':')[1].strip()
    return lines

formsql = getdata("DATABASE.txt")
hostdb = formsql[0]
passworddb = formsql[2]
databasedb = formsql[3]
userdb = formsql[1]

class DB:
    mydb = None

    def connect(self,dbname=databasedb):
        self.mydb = mysql.connector.connect(
            host=hostdb,
            user=userdb,
            password=passworddb,
            database=dbname,
            port='3306'
        )

    def query(self, task):
        try:
            mycursor = self.mydb.cursor(buffered=True)
            mycursor.execute(task)
        except:
            self.connect()
            mycursor = self.mydb.cursor(buffered=True)
            mycursor.execute(task)
        return mycursor

    def query_custom(self, task,db):
        try:
            self.connect(dbname=db)
            mycursor = self.mydb.cursor(buffered=True)
            mycursor.execute(task)
        except:
            self.connect(dbname=db)
            mycursor = self.mydb.cursor(buffered=True)
            mycursor.execute(task)
        
        return mycursor
    def query_commit(self, task):
        try:
            mycursor = self.mydb.cursor(buffered=True)
            mycursor.execute(task)
            mycursor.commit()
        except:
            self.connect()
            mycursor = self.mydb.cursor(buffered=True)
            mycursor.execute(task)
            self.mydb.commit()
        return mycursor


db = DB()

# about api
class Web():
    def __init__(self,apikey,apisecret,storename) -> None:
        self.apikey = apikey
        self.apisecret = apisecret
        self.storename = storename

    #  upload trackingno today to database
    # get data from list of www.api.zort.com
    
    def postzero(self,data):
        # example
        # data = {"stocks": [{"sku": "BA0002-S", "stock": 0,'cost':0},{"sku": "BA0002-L", "stock": 0,'cost':0},{"sku": "BA0002-M", "stock": 0,'cost':0}]}
        header = {
            'storename': f'{self.storename}',
            'apikey': f'{self.apikey}',
            'apisecret': f'{self.apisecret}'
        }

        url = 'https://api.zortout.com/api.aspx'

        payload = {'method': 'UPDATEPRODUCTAVAILABLESTOCKLIST', 'version': '3', 'warehousecode': 'W0001'}
        res = requests.post(url=url, headers=header, params=payload, json=data)
        print(res.status_code)
        print(json.loads(res.text)['resDesc'])
    def get(self,method,datatype,page=1):
        header = {
            'storename':f'{self.storename}',
            'apikey':f'{self.apikey}',
            'apisecret':f'{self.apisecret}'
        }

        url = 'https://api.zortout.com/api.aspx'

        payload = {'method':method,'version':'3','page': page,'warehousecode':'W0001'}

        res = requests.get(url=url,headers=header,params=payload)
        data = res.json()
        datalist = []
        for i in range(len(data['list'])):
            datalist.append(data['list'][i][datatype])
        return datalist
    def get_update(self,method,page=1):
        print(page)
        header = {
            'storename':f'{self.storename}',
            'apikey':f'{self.apikey}',
            'apisecret':f'{self.apisecret}'
        }

        url = 'https://api.zortout.com/api.aspx'

        payload = {'method':method,'version':'3','page': page,'warehousecode':'W0001'}

        res = requests.get(url=url,headers=header,params=payload)
        data = res.json()
        sku = []
        availablestock = []
        name = []
        purchaseprice = []
        sellprice = []
        imagepath = []
        for i in range(len(data['list'])):
            sku.append(data['list'][i]["sku"])
            availablestock.append(data['list'][i]["availablestock"])
            name.append(data['list'][i]["name"])
            purchaseprice.append(data['list'][i]["purchaseprice"])
            sellprice.append(data['list'][i]["sellprice"])
            imagepath.append(data['list'][i]["imagepath"])
        return sku,availablestock,name,imagepath,purchaseprice,sellprice

    def get_update_live(self,method,page=1):
        print(page)
        header = {
            'storename':f'{self.storename}',
            'apikey':f'{self.apikey}',
            'apisecret':f'{self.apisecret}'
        }

        url = 'https://api.zortout.com/api.aspx'

        payload = {'method':method,'version':'3','page': page,'warehousecode':'W0003'}

        res = requests.get(url=url,headers=header,params=payload)
        data = res.json()
        sku = []
        availablestock = []
        name = []
        purchaseprice = []
        sellprice = []
        imagepath = []
        for i in range(len(data['list'])):
            sku.append(data['list'][i]["sku"])
            availablestock.append(data['list'][i]["availablestock"])
            name.append(data['list'][i]["name"])
            purchaseprice.append(data['list'][i]["purchaseprice"])
            sellprice.append(data['list'][i]["sellprice"])
            imagepath.append(data['list'][i]["imagepath"])

        return sku,availablestock,name,imagepath,purchaseprice,sellprice

    def get_datatype_filter_by_sku(self,method,datatype,sku):
        header = {
            'storename':f'{self.storename}',
            'apikey':f'{self.apikey}',
            'apisecret':f'{self.apisecret}'
        }

        url = 'https://api.zortout.com/api.aspx'
        payload = {'method': method, 'version': '3','searchsku':sku}
        res = requests.get(url=url,headers=header,params=payload)
        data = res.json()
        return  data['list'][0][datatype]
    # post data to www.api.zort.com
    # for i in range(len(data['list'])):
        #     print(data['list'][i]['customerphone'])

    def post(self, method, sku, amount,cost=0):

        header = {
            'storename': f'{self.storename}',
            'apikey': f'{self.apikey}',
            'apisecret': f'{self.apisecret}'
        }

        url = 'https://api.zortout.com/api.aspx'

        payload = {'method': method, 'version': '3', 'warehousecode': 'W0001'}
        data = {"stocks": [{"sku": f"{sku}", "stock": amount,'cost':cost}]}
        print(data)
        res = requests.post(url=url, headers=header, params=payload, json=data)
        # for i in range(len(data['list'])):
        #     print(data['list'][i]['customerphone'])


# about database
class Update():
    def __init__(self,key,secret,storename,dbname) -> None:
        self.key =  key
        self.secret = secret
        self.storename = storename
        self.databasename = dbname
        self.web = Web(self.key,self.secret,self.storename)

# convert url to bytes
    def convert_url_to_bytes(self,url):
        try:
            response = requests.get(url,stream=True)
            data = BytesIO(response.content)
            return data.getvalue()
        except:
            return None

    def get_track(self):
        header = {
            'storename': f'{self.storename}',
            'apikey': f'{self.key}',
            'apisecret': f'{self.secret}'
        }

        url = 'https://api.zortout.com/api.aspx'

        payload = {'method': "GETORDERS", 'version': '3'}

        res = requests.get(url=url, headers=header, params=payload)
        data = res.json()

        for i in range(len(data['list'])):
            if data['list'][i]['status'] == 'Waiting':
                trackingno = data['list'][i]['trackingno']
                result = db.query(f"select * from {self.databasename}.deli_zort where trackingno like '%{trackingno}%'")
                if result.fetchone():
                    continue
                IDorder = data['list'][i]['id']
                for dt in range(len(data['list'][i]['list'])):
                    sku = data['list'][i]['list'][dt]['sku']
                    descript = data['list'][i]['list'][dt]['name']
                    db.query_commit(f"insert into {self.databasename}.deli_zort values ({IDorder},'{trackingno}','{sku}','{descript}')")

    # update data in database
    def RealtimeUpdate(self,Delete=False):
        sku,amount,name,image,cost,price= self.web.get_update("GETPRODUCTS")
        self.update(sku,amount,name,image,cost,price)
        #self.write_image(sku,1)
        if len(sku) == 2000:
            sku,amount,name,image,cost,price= self.web.get_update('GETPRODUCTS',2)
            self.update(sku,amount,name,image,cost,price)
            sku,amount,name,image,cost,price= self.web.get_update_live('GETPRODUCTS',2)
            self.update_live(sku,amount,name,image,cost,price)
            if len(sku) == 2000:
                sku,amount,name,image,cost,price= self.web.get_update('GETPRODUCTS',3)
                self.update(sku,amount,name,image,cost,price)
                sku,amount,name,image,cost,price= self.web.get_update_live('GETPRODUCTS',3)
                self.update_live(sku,amount,name,image,cost,price)
                if len(sku) == 2000:
                    sku,amount,name,image,cost,price= self.web.get_update('GETPRODUCTS',4)
                    self.update(sku,amount,name,image,cost,price)
                    sku,amount,name,image,cost,price= self.web.get_update_live('GETPRODUCTS',4)
                    self.update_live(sku,amount,name,image,cost,price)
                    if len(sku) == 2000:
                        sku,amount,name,image,cost,price= self.web.get_update('GETPRODUCTS',5)
                        self.update(sku,amount,name,image,cost,price)
                        sku,amount,name,image,cost,price= self.web.get_update_live('GETPRODUCTS',5)
                        self.update_live.update(sku,amount,name,image,cost,price)
                        if len(sku) == 2000:
                            sku,amount,name,image,cost,price= self.web.get_update('GETPRODUCTS',6)
                            self.update(sku,amount,name,image,cost,price)
                            sku,amount,name,image,cost,price= self.web.get_update_live('GETPRODUCTS',6)
                            self.update_live.update(sku,amount,name,image,cost,price)

    def update(self,sku,amount,name,image,cost,price):
        taskdb_stock_main = f'update {self.databasename}.stock_main SET \n'
        taskdb_stock_cost = f'update {self.databasename}.cost SET \n'
        taskdb_stock_main_check = f'update {self.databasename}.stock_main SET \n'
        taskdb_stock_cost_check = f'update {self.databasename}.cost SET \n'
        for i in range(len(sku)):
            # if i % 400 < 1 and i > 10:
            #     db.query_commit(taskdb_stock_main[:-1])
            #     db.query_commit(taskdb_stock_cost[:-1])
            #     taskdb_stock_main = f'update {self.databasename}.stock_main SET \n'
            #     taskdb_stock_cost = f'update {self.databasename}.cost SET \n'
            if "Q" in sku[i]:
                continue
            #print(sku[i])
            # check each sku does is in database
            # if yes then update amount
            taskdb_stock_main += f"""amount = CASE sku when '{sku[i]}' THEN {amount[i]} ELSE amount END,
            descript = CASE sku when '{sku[i]}' THEN '{name[i]}' ELSE descript END,
            image = CASE sku when '{sku[i]}' THEN '{image[i]}' ELSE image END,"""
            taskdb_stock_cost += f"""
            cost = CASE sku when '{sku[i]}' THEN {cost[i]} ELSE cost END,
            price = CASE sku when '{sku[i]}' THEN {price[i]} ELSE price END,"""
        if taskdb_stock_cost != taskdb_stock_cost_check:
            db.query_commit(taskdb_stock_cost[:-1])
        if taskdb_stock_main != taskdb_stock_main_check:
            db.query_commit(taskdb_stock_main[:-1])

    def update_live(self,sku,amount,name,image,cost,price):
        taskdb_stock_main = f'update {self.databasename}.stock SET \n'
        taskdb_stock_main_check = f'update {self.databasename}.stock SET \n'
        for i in range(len(sku)):
            # if i % 400 < 1 and i > 10:
            #     db.query_commit(taskdb_stock_main[:-1])
            #     db.query_commit(taskdb_stock_cost[:-1])
            #     taskdb_stock_main = f'update {self.databasename}.stock_main SET \n'
            #     taskdb_stock_cost = f'update {self.databasename}.cost SET \n'
            if "Q" in sku[i]:
                continue
            #print(sku[i])
            # check each sku does is in database
            # if yes then update amount
            taskdb_stock_main += f"""amount = CASE sku when '{sku[i]}' THEN {amount[i]} ELSE amount END,"""
        if taskdb_stock_main != taskdb_stock_main_check:
            db.query_commit(taskdb_stock_main[:-1])

        # write image @folder image
        # self.write_image(sku)

    # write every image from url to image folder,Delete mean deleate all file in folder
    def write_image(self,sku,page):
        imgpath = self.web.get('GETPRODUCTS','imagepath',page)
        for i in range(len(sku)):
            if imgpath[i]:
                self.insert(sku[i],imgpath[i])

    def insert(self,sku,image):
        mycursor = db.query(f"select sku from image_main where sku = '{sku}'")
        if mycursor.fetchone():
            pass
        else:
            image = self.convert_url_to_bytes(image)
            db.query_commit("""INSERT INTO image_main (sku,image) VALUES (%s,%s)""",(sku,image))
            
# about stock,order
class Stock():
    web = Web('7KRzYzjPqknzzSM2nVcooo3sWNF6EK4Oyq9QtGI8uyk=','RA9VD1AjwaHo8UW0uNk924SnxN0xIFIGdlelDEcTEE=','Muslin.info@gmail.com')

    # return all sku pack today
    def get_all_sku_today(self):
        Order_dict = {}
        for i,customer in zip(self.web.get("GETORDERS",'status'), self.web.get("GETORDERS",'list')):
            if i == 'Waiting':
                for sku in customer:
                    if sku['sku'] in Order_dict:
                        Order_dict[sku['sku']] += 1
                    else:
                        Order_dict[sku['sku']] = 1
        for key, value in sorted(Order_dict.items()):
            print(key,' : ',value)

    def get_trackingNo(self):
        c = 0
        for i,customer,tracking in zip(self.web.get(" GETORDERS",'status'), self.web.get("GETORDERS",'list'),self.web.get("GETORDERS",'trackingno')):
            if i == 'Waiting':
                print(tracking,str(c+1))
                c+=1
    # get last sku depend on type
    def get_last_sku(self,type):
        # split sku to get only number
        command = f"""select mid(sku,3,4)*1 from zortmain
                        where sku like '%{type}%'
                        order by mid(sku,3,4)
                        DESC limit 1;"""
        mycursor.execute(command)
        try:
            print(int(mycursor.fetchone()[0]))
        except:
            print('No sku yet')

    def update_track(self):
        track,sku,cst = self.web.get_track()
        command = "truncate zortexpress_main"
        mycursor.execute(command)
        mydb.commit()
        for i in range(len(sku)):
            command = f"""
                        insert into zortexpress_main
                        values('{sku[i]}','{track[i]}','{cst[i]}')
                    """
            mycursor.execute(command)
            mydb.commit()
    
    def get_sku_from_trackingno(self,No):
        command = f"""select sku,descript from zortmain 
        where sku in (select sku from zortexpress_main
                    where trackingno = '{No}')"""
        mycursor.execute(command)
        for i in mycursor:
            for data in i:
                    print(data)

def get_amount(zortamount,amount):
    amount = int(amount)
    zortamount = int(zortamount)
    new_amount = amount - (4 - zortamount)
    if new_amount >= 0:
        return 4,new_amount
    else:
        return zortamount + amount,0

def set_three(dep):
    if dep == 'muslin' or dep == 'maruay':
        web = Web(get_api_register(dep,'apikey'),get_api_register(dep,'apisecret'),get_api_register(dep,'storename'))
        task = """
        select stock.sku,stock_main.amount,stock.amount,cost.cost from stock
        inner join stock_main on stock.sku = stock_main.sku
        inner join cost on stock.sku = cost.sku
        where stock.amount > 0 and stock_main.amount < 4 and stock_main.image != 'None'
        """

        result = db.query_custom(task,dep)
        result = list(result.fetchall())
        sku = [i[0] for i in result]
        zortamount = [i[1] for i in result]
        amount = [i[2] for i in result]
        cost = [i[3] for i in result]
        datadict = {}
        datadict['stocks'] = list()
        taskdb_stock_main = ''
        taskdb_stock = ''
        for i in range(len(sku)):
            if i % 100 == 0:
                web.postzero(datadict)
                datadict['stocks'] = list()
            zort_amount,stock_amount = get_amount(zortamount[i],amount[i])
            datadict['stocks'].append({"sku": sku[i], "stock": int(zort_amount),'cost':cost[i]})
            recheckedamount = web.get_datatype_filter_by_sku("GETPRODUCTS","availablestock",sku[i])
            # if int(recheckedamount) != int(zort_amount):
            #    print('error not update',sku[i])
            # else:
            print(f"{sku[i]} > {zort_amount} | {stock_amount}")
            taskdb_stock_main += f"WHEN '{sku[i]}' THEN amount - {amount[i] - stock_amount}\n"
            db.query_commit(f"insert into {dep}.log values ('ระบบ','ดึงอัตโนมัติ รหัส {sku[i]}จากกลาง เหลือ pull {amount[i] - stock_amount} {zort_amount}',now())")
            taskdb_stock += f"WHEN '{sku[i]}' THEN {zort_amount}\n"
        task_final = f'''
        UPDATE {dep}.stock
        SET amount
        = CASE sku
        {taskdb_stock_main}
        ELSE amount
        END;
        '''
        if taskdb_stock_main:
            db.query_commit(task_final)
        task_final = f'''
        UPDATE {dep}.stock_main
        SET amount
        = CASE sku
        {taskdb_stock}
        ELSE amount
        END;
        '''
        if taskdb_stock:
            db.query_commit(task_final)
        web.postzero(datadict)

def get_database():
    result = db.query('show databases')
    result = list(result.fetchall())
    return [i[0] for i in result if i[0] not in ['information_schema','mysql', 'performance_schema','sys','image'] ]
