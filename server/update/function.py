from datetime import datetime
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
        sku = self.web.get("GETPRODUCTS",'sku')
        amt = self.web.get("GETPRODUCTS",'availablestock')
        name = self.web.get("GETPRODUCTS",'name')
        cost = self.web.get("GETPRODUCTS",'purchaseprice')
        price = self.web.get("GETPRODUCTS",'sellprice')
        image = self.web.get("GETPRODUCTS",'imagepath')
        self.update(sku, amt, name,image,cost,price)
        print(len(sku))
        #self.write_image(sku,1)
        if len(sku) == 2000:
            sku = self.web.get('GETPRODUCTS','sku',2)
            amt = self.web.get('GETPRODUCTS','availablestock',2)
            image = self.web.get("GETPRODUCTS",'imagepath',2)
            cost = self.web.get("GETPRODUCTS",'purchaseprice',2)
            name = self.web.get("GETPRODUCTS",'name',2)
            price = self.web.get("GETPRODUCTS",'sellprice',2)
            self.update(sku,amt,name,image,cost,price)
            print(f"second {len(sku)}")
            if len(sku) == 2000:
                sku = self.web.get('GETPRODUCTS','sku',3)
                amt = self.web.get('GETPRODUCTS','availablestock',3)
                image = self.web.get("GETPRODUCTS",'imagepath',3)
                cost = self.web.get("GETPRODUCTS",'purchaseprice',3)
                name = self.web.get("GETPRODUCTS",'name',3)
                price = self.web.get("GETPRODUCTS",'sellprice',3)
                self.update(sku,amt,name,image,cost,price)
                if len(sku) == 2000:
                    sku = self.web.get('GETPRODUCTS','sku',4)
                    amt = self.web.get('GETPRODUCTS','availablestock',4)
                    image = self.web.get("GETPRODUCTS",'imagepath',4)
                    cost = self.web.get("GETPRODUCTS",'purchaseprice',4)
                    name = self.web.get("GETPRODUCTS",'name',4)
                    price = self.web.get("GETPRODUCTS",'sellprice',4)
                    self.update(sku,amt,name,image,cost,price)
    def update(self,sku,amount,name,image,cost,price):
        for i in range(len(sku)):
            if "Q" in sku[i]:
                continue
            #print(sku[i])
            # check each sku does is in database
            mycursor = db.query(f"select sku from {self.databasename}.stock_main where sku = '{sku[i]}'")
            if mycursor.fetchone():
                # if yes then update amount
                result = db.query(f"select amount from {self.databasename}.stock_main where sku = '{sku[i]}'") 
                result = list(result.fetchone())[0]
                if int(result) != int(amount[i]) and int(amount[i]) < 1 :
                    send_line(f"{sku[i]} - > ใกล้หมด")
                command = (f'''update {self.databasename}.stock_main
                                set amount = {amount[i]},descript = "{name[i]}",
				image = "{image[i]}"
                                where sku = "{sku[i]}"''')

                db.query_commit(command)
            else:
                # if not in database create new
                print(sku[i])
                if '-' in sku[i]:
                    size = sku[i].split('-')[1]
                else:
                    size = ''
                command = (f'''insert into {self.databasename}.stock_main
                                    values ("{sku[i]}","{name[i]}","{size}","{image[i]}","34","24","46",
                                          "50","","",{amount[i]})''')
                db.query_commit(command)
                task = f'''
                insert into {self.databasename}.data_size
                values ("{sku[i]}","{size}","{get_idsell(sku[i])}","")
                  '''
                try:
                    db.query_commit(task)
                except Exception as e:
                    print(e)
            mycursor = db.query(f"select sku from {self.databasename}.cost where sku = '{sku[i]}'")
            if mycursor.fetchone():
                db.query_commit(f"update {self.databasename}.cost set cost = {cost[i]},price = {price[i]} where sku = '{sku[i]}'")
            else:
                db.query_commit(f"insert into {self.databasename}.cost values('{sku[i]}',{cost[i]},0,{price[i]})")

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
    new_amount = amount - (2 - zortamount)
    if new_amount >= 0:
        return 2,new_amount
    else:
        return zortamount + amount,0

def set_three(dep):
    if dep == 'muslin':
        web = Web(get_api_register(dep,'apikey'),get_api_register(dep,'apisecret'),get_api_register(dep,'storename'))
        task = """
        select stock.sku,stock_main.amount,stock.amount,cost.cost from stock
        inner join stock_main on stock.sku = stock_main.sku
        inner join cost on stock.sku = cost.sku
        where stock.amount > 0 and stock_main.amount < 2 and stock_main.image != 'None'
        """

        result = db.query_custom(task,'muslin')
        result = list(result.fetchall())
        sku = [i[0] for i in result]
        zortamount = [i[1] for i in result]
        amount = [i[2] for i in result]
        cost = [i[3] for i in result]
        for i in range(len(sku)):
            zort_amount,stock_amount = get_amount(zortamount[i],amount[i])
            web.post("UPDATEPRODUCTAVAILABLESTOCKLIST",sku[i],zort_amount,cost[i] )
            recheckedamount = web.get_datatype_filter_by_sku("GETPRODUCTS","availablestock",sku[i])
            if int(recheckedamount) != int(zort_amount):
               print('error not update',sku[i])
            else:
                task = f"update {dep}.stock set amount = {stock_amount} where sku = '{sku[i]}'"
                db.query_commit(task)
                db.query_commit(f"insert into {dep}.log values ('ระบบ','ดึงอัตโนมัติ รหัส {sku[i]}จากกลาง เหลือ {stock_amount} เป็น {zort_amount}',now())")
                db.query_commit(f"update {dep}.stock_main set amount = {zort_amount} where sku ='{sku[i]}'")
