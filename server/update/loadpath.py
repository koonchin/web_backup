from function import *
import time,os
from clear import *
from datetime import datetime
from sqlalchemy import create_engine
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from selenium import webdriver
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

# get user,password of mysql
def getdata(path:str or None):
    lines = []
    with open(path) as f:
        lines = f.readlines()
    for line in lines:
        lines[lines.index(line)] = line.split(':')[1].strip()
    return lines
# use zortmain from zortmainBASE.txt to access mysql
formsql = getdata("DATABASE.txt")
hostdb = formsql[0]
passworddb = formsql[2]
databasedb = formsql[3]
userdb = formsql[1]

def Start(path,database):
    df = pd.read_excel(path)
    df['size'] = df.iloc[:, 0].astype(str).str.split('-',expand=True)[1]
    df = df.set_axis(['sku', 'idsell', 'descript', 'unit', 'amount', 'price', 'cost', 'fee', 'etc', 'position','size'], axis=1, inplace=False)
    df.drop(['unit','price','cost','fee','etc','position'],axis='columns',inplace=True)
    sql(df,'stock_vrich',database)

def StartTest(path,database):
    df = pd.read_excel(path)
    df = df.set_axis(['IDorder','a','date', 'FBName', 'cstname', 'addr','b','c', 'tel','d','e', 'trackingNo','f','g', 'total_amount', 'cash', 'discount', 'deli_fee', 'total', 'Ebank', 'paid', 'timepaid', 'thing1', 'thing2', 'idsell', 'descript', 'Comment', 'amount', 'price', 'timedate', 'Printed', 'Checkout', 'Checkout_Time', 'sku'], axis=1, inplace=False)
    df.drop(['a','b','c','d','e','f','g'],axis='columns',inplace=True)
    sql(df,'temp_deli_vrich',database)
    db.query_commit('insert into muslin.deli_vrich select * from muslin.temp_deli_vrich where Checkout = 1 and idorder not in (select idorder from muslin.deli_vrich)')

def sql(empdata,table,databasedb):
    start_time = time.time()
    engine = create_engine("mysql+pymysql://" + userdb + ":" + passworddb + "@" + hostdb + "/" + databasedb)
    empdata.to_sql(table,engine ,index=False,if_exists='replace',method='multi')
   # print("--- %s seconds ---" % (time.time() - start_time))

def get_database():
    result = db.query('show databases')
    result = list(result.fetchall())
    return [i[0] for i in result if i[0] not in ['information_schema','mysql', 'performance_schema','sys','image'] ]

def main(vrich_user,vrich_password,database):
    clear()
    def enable_download_in_headless_chrome(driver, download_dir):
        driver.command_executor._commands["send_command"] = (
            "POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {
            'behavior': 'allow', 'downloadPath': download_dir}}
        command_result = driver.execute("send_command", params)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox') # required when running as root user. otherwise you would get no sandbox errors. 
    #chrome_options.add_argument("--remote-debugging-port=9222")
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=chrome_options)
    #driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver",options=chrome_options)
    path = '/update/'
    enable_download_in_headless_chrome(
                    driver=driver, download_dir=path)
    driver.get('https://muslinpajamas.vrich619.com')
    time.sleep(1)
    a = driver.find_element_by_xpath('/html/body/div/b/div/form/div[1]/input')
    a.send_keys(vrich_user)
    b = driver.find_element_by_name('password')
    b.send_keys(vrich_password)
    b.send_keys(Keys.RETURN)
    driver.implicitly_wait(20)
    try:
        time.sleep(2)
        driver.get('https://muslinpajamas.vrich619.com/order/confirmTransfer')
        w = WebDriverWait(driver, 20)
        w.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="app"]/div/div[3]/section[1]/div/div/h1/span/div/a'))).click()
        driver.implicitly_wait(30)
    except:
        pass
    driver.get('https://muslinpajamas.vrich619.com/productStock/export')
    
    time.sleep(5)
    driver.quit()
    path = []
    c= 0
    while len(path) < 2:
        if c > 10:
            path.append('a')
            c = 0
        time.sleep(2)
        c += 1
        for i in os.listdir('/update/'):
            if os.path.isfile('/update/'+i):
                if "Order" in str(i):
                    if not '/update/'+i in path:
                        
                        path.append('/update/'+i)
                elif "stock" in str(i):
                    
                    if not '/update/'+i in path:
                        path.append('/update/'+i)
    time.sleep(2)
    for i in path:
        if 'Order' in i:
            StartTest(i,database)
            print('start')
            time.sleep(1)
        else:
            try:
                print('start')
                Start(i,database)
            except:
                pass

def get_api_register(department,api):

    mycursor = db.query(
        f"select {api} from store_api where department = '{department}'")
    try:
        return list(mycursor.fetchall())[0][0]
    except:
        return None
c = 0
while True:
    c+= 1
   # try:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"{str(c)} : Current Time =", current_time)
    for i in get_database():
        try:
            #pass
            update = Update(get_api_register(i,'apikey'),get_api_register(i,'apisecret'),get_api_register(i,'storename'),i)
            update.RealtimeUpdate()
            set_three(i)
            print('update')
        #update.get_track()
        except Exception as e:
            print(e)

    time.sleep(60)
    #except Exception as e:
        #print(f'vrich > {e}')
        #time.sleep(50)
