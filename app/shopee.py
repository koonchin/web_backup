from function import *
from sqlalchemy import create_engine

def sql(empdata,table,databasedb):
    start_time = time.time()
    engine = create_engine("mysql+pymysql://" + userdb + ":" + passworddb + "@" + hostdb + "/" + databasedb)
    empdata.to_sql(table,engine ,index=False,if_exists='replace',method='multi')
   # print("--- %s seconds ---" % (time.time() - start_time))

def Start(path,database):
    df = pd.read_excel(path)
    df['size'] = df.iloc[:, 0].astype(str).str.split('-',expand=True)[1]
    df = df.set_axis(['sku', 'idsell', 'descript', 'unit', 'amount', 'price', 'cost', 'fee', 'etc', 'position','size'], axis=1, inplace=False)
    df.drop(['unit','price','cost','fee','etc','position'],axis='columns',inplace=True)
    sql(df,'stock_vrich',database)

def StartTest(path,database):
    df = pd.read_excel(path)
    df = df.set_axis(['IDorder','a','date', 'FBName', 'cstname', 'addr','b','c', 'tel','d','e', 'trackingNo','f','g', 'total_amount', 'cash', 'discount', 'deli_fee', 'total', 'Ebank', 'paid', 'timepaid','h', 'thing1', 'thing2', 'idsell', 'descript', 'Comment', 'amount', 'price', 'timedate', 'Printed', 'Checkout', 'Checkout_Time', 'sku'], axis=1, inplace=False)
    df.drop(['a','b','c','d','e','f','g','h'],axis='columns',inplace=True)
    sql(df,'deli_vrich',database)
    db.query_commit('update muslin.deli_vrich set trackingno = "" where trackingno is null ;')
    # db.query_commit('insert into muslin.deli_vrich select * from muslin.temp_deli_vrich where Checkout = 1 and idorder not in (select idorder from muslin.deli_vrich)')
# StartTest('order.xlsx','muslin')
# Start('stock_20220629180904.xlsx','muslin')

def update_content():
    df = pd.read_excel('shopee.xlsx')
    df.dropna(subset = ['et_title_variation_sku'], inplace=True)
    satin_name = 'ชุดนอน Muslin Pajamas Silk Satin result'
    bamboo_name = 'ชุดนอน Muslin Pajamas ชุดนอน ผ้าเยื่อไผ่ ใยธรรมชาติ result'
    tencel_name = 'ชุดนอน Muslin pajamas  เท็นเซล (tencel) เนื้อผ้านุ่มลื่น ใส่สบาย result'
    satin_descript_content = """""🕊ชุดนอน Silk Satin หรือเรียกว่า ไหมซาติน 🍃
 🍃ชุดนอน Silk Satin หรือเรียกอีกชื่อว่าไหมซาติน ไหมซาตินจะมีความยืดยุ่น ไม่ขึ้นขลุย
ให้ความนุ่มลื่น สบายผิวเวลาสวมใส่ ถ้าลูกค้า กำลังมองชุดนอนที่ใส่สบายในเวลาหลับนอน ขอแนะนำเลยค๊า 
🌸ส่วนผสมของผ้า จะมี Polyester 95%และ Spendex 5%. ไม่แปลกใช่ไหมค๊าว่าทำไมถึงใส่สบาย🌸
result
''โปรดอ่านเพื่อประโยชน์ของลูกค้าเมื่อได้รับสินค้า''
#ข้อมูลการรับประกันสินค้า
-ถ่ายวิดิโอทุกครั้งเมื่อแกะสินค้า เพื่อเป็นหลักฐานในการขอเปลี่ยนสินค้า
-สั่งผิด SIZE หรือลองแล้วไม่พอดี มีค่าเปลี่ยน 100 บาท ต่อคำสั่งซื้อ หากไม่แน่ใจสามารถสอบถามแอดมินได้เลยนะคะ
-พบตำหนิหรือรับสินค้าผิด สามารถแจ้งเปลี่ยนกับทางแอดมินได้ ภายใน 5 วัน
-กรณีเกิดความผิดพลาดจากทางร้าน ทางร้านยินดีรับผิดชอบทันที

#การรับประกันสินค้า
-สินค้าที่ซักแล้วไม่สามารถเปลี่ยนคืนได้ทุกกรณี
-รบกวนลูกค้าตรวจสอบสินค้าก่อนซัก 
-เมื่อได้รับสินค้าผิด เสียหายหรือมีปัญหาสามารถแจ้งเปลี่ยนได้ไม่เกิน 3 วัน หลังจากได้รับสินค้า

🕊วิธีดูแลรักษา🕊
-ห้ามอบแห้ง (ผ้าเยื่อไผ่กับซาติน ไม่ควรใช้ความร้อนสูง เพื่อป้องกันการหดตัวของผ้า)
-ห้ามใช้น้ำร้อน (แนะนำให้ซักในน้ำอุณหภูมิปกติ เพื่อถนอมเนื้อผ้า)
-ถ้าซักมือจะถนอมผ้าที่สุด แต่หากต้องการใช้เครื่องซักผ้า ทางร้านแนะนำให้ใช้ถุงผ้า
-เนื้อผ้ามีความนุ่มม ทำให้ยับง่าย เพื่อความสวยงามทางร้านแนะนำให้รีดก่อนใช้"
"""
    tencel_descript_content = """"ตัวนี้เป็นผ้าเทนเชลน๊าค๊า
    เนื้อผ้าทอพิเศษด้วยเส้นใยเซลลูโลส (Celulose) จากธรรมชาติ
    ทำให้เนื้อสัมผัส นุ่มม ลื่นนน เย็นสบาย
    - เนื้อผ้าเย็นสบาย ระบายอากาศได้ดี
    - ให้สัมผัสนุ่ม ลื่น สบายผิว 
    - สีสวย หรูหรา เงางาม เหมือนผ้าไหม
    - วิธีการทอแบบซาทีน ทอด้วยเส้นด้ายเนื้อเอียดกว่าเนื้อผ้าทั่วไป  เนื้อผ้า ทอ 60 เส้นด้ายนะคะ
    result
    ''โปรดอ่านเพื่อประโยชน์ของลูกค้าเมื่อได้รับสินค้า''
    #ข้อมูลการรับประกันสินค้า
    -พบตำหนิหรือรับสินค้าผิด สามารถแจ้งเปลี่ยนกับทางแอดมินได้
    -กรณีเกิดความผิดพลาดจากทางร้าน ทางร้านยินดีรับผิดชอบทันที

    #การรับประกันสินค้า
    -รบกวนลูกค้าตรวจสอบสินค้าก่อนซัก 
    -เมื่อได้รับสินค้าผิด เสียหายหรือมีปัญหาสามารถแจ้งเปลี่ยนได้ หลังจากได้รับสินค้า

    🕊วิธีดูแลรักษา🕊
    -ห้ามอบแห้ง (ผ้าเยื่อไผ่กับซาติน ไม่ควรใช้ความร้อนสูง เพื่อป้องกันการหดตัวของผ้า)
    -ห้ามใช้น้ำร้อน (แนะนำให้ซักในน้ำอุณหภูมิปกติ เพื่อถนอมเนื้อผ้า)
    -ถ้าซักมือจะถนอมผ้าที่สุด แต่หากต้องการใช้เครื่องซักผ้า ทางร้านแนะนำให้ใช้ถุงผ้า
    -เนื้อผ้ามีความนุ่มม ทำให้ยับง่าย เพื่อความสวยงามทางร้านแนะนำให้รีดก่อนใช้"
    """
    bamboo_descript_content = """""🕊ชุดนอนผ้าใยธรรมชาติ 🎉
✴️ชุดนอนเพื่อสุขภาพ การหลับนอนที่ดีผลิตจากเยื่อไผ่ ใยธรรมชาติ 🕊
ผ้าเยื่อไผ่เป็นผ้าที่ให้ความนุ่ม ให้ความรู้สึกสบายตัวเวลาสวมใส่ เหมาะสำหรับสวมใส่เวลาหลับนอน และผ้าเยื่อดูดซับความชื้น เหงื่อและซับน้ำได้ดี เหมาะกับทุกผิว ไม่ระคายเคือง เหมาะกับผิวแพ้ง่าย  ทำให้หลับสบายทั้งคืน ทำให้พักผ่อนได้เพียงพอ ตื่นมาสดชื่น
✔️ คุณสมบัติ✔️
☘️นุ่มมาก
🍀ซับน้ำได้ดีเยี่ยมเหมาะกับคนขี้ร้อน
☘️ระบายอากาศได้ดี
☘️ไม่มีโลหะหนัก
result
''โปรดอ่านเพื่อประโยชน์ของลูกค้าเมื่อได้รับสินค้า''
#ข้อมูลการรับประกันสินค้า
-ถ่ายวิดิโอทุกครั้งเมื่อแกะสินค้า เพื่อเป็นหลักฐานในการขอเปลี่ยนสินค้า
-สั่งผิด SIZE หรือลองแล้วไม่พอดี มีค่าเปลี่ยน 100 บาท ต่อคำสั่งซื้อ หากไม่แน่ใจสามารถสอบถามแอดมินได้เลยนะคะ
-พบตำหนิหรือรับสินค้าผิด สามารถแจ้งเปลี่ยนกับทางแอดมินได้ ภายใน 5 วัน
-กรณีเกิดความผิดพลาดจากทางร้าน ทางร้านยินดีรับผิดชอบทันที

#การรับประกันสินค้า
-สินค้าที่ซักแล้วไม่สามารถเปลี่ยนคืนได้ทุกกรณี
-รบกวนลูกค้าตรวจสอบสินค้าก่อนซัก 
-เมื่อได้รับสินค้าผิด เสียหายหรือมีปัญหาสามารถแจ้งเปลี่ยนได้ไม่เกิน 3 วัน หลังจากได้รับสินค้า

🕊วิธีดูแลรักษา🕊
-ห้ามอบแห้ง (ผ้าเยื่อไผ่กับซาติน ไม่ควรใช้ความร้อนสูง เพื่อป้องกันการหดตัวของผ้า)
-ห้ามใช้น้ำร้อน (แนะนำให้ซักในน้ำอุณหภูมิปกติ เพื่อถนอมเนื้อผ้า)
-ถ้าซักมือจะถนอมผ้าที่สุด แต่หากต้องการใช้เครื่องซักผ้า ทางร้านแนะนำให้ใช้ถุงผ้า
-เนื้อผ้ามีความนุ่มม ทำให้ยับง่าย เพื่อความสวยงามทางร้านแนะนำให้รีดก่อนใช้"
"""

    # Create a dictionary to store the concatenated data_size values for each product_id
    task = 'select sku,data_size from data_size where sku like "%-%"'
    data_size_dict = {}
    result_data_size_dict = {}
    result_name_dict = {}
    result = db.query_custom(task,'muslin')
    result = list(result.fetchall())
    for i in result:
        data_size_dict[i[0]] = f"\nรุ่น {get_idsell(i[0])}\n{i[1]}"

    # Iterate through the DataFrame rows
    for i in df.index:
        product_id = df.loc[i,'et_title_product_id']
        seller_sku = df.loc[i,'et_title_variation_sku']
        try:
            data_size = data_size_dict[seller_sku]
        except:
            data_size = ''
        if product_id not in result_data_size_dict:
            result_data_size_dict[product_id] = ''

        if product_id not in result_name_dict:
            result_name_dict[product_id] = '( '

        # Concatenate the data_size with a newline character
        try:
            if get_idsell(seller_sku) in result_data_size_dict[product_id]:
                result_data_size_dict[product_id] += str(data_size).replace(f"\nรุ่น {get_idsell(seller_sku)}\n",'') + "\n"
            else:
                result_data_size_dict[product_id] += str(data_size) + "\n"
        except:
            print(seller_sku)
        if get_idsell(seller_sku) not in result_name_dict[product_id]:
            result_name_dict[product_id] += get_idsell(seller_sku) + ","
        try:
            if product_id != df.loc[i + 1,'et_title_product_id']:
                result_name_dict[product_id] = f"{result_name_dict[product_id][:-1]} )"
        except:
                result_name_dict[product_id] = f"{result_name_dict[product_id][:-1]} )"

    # Create a new DataFrame to store the result
    result_df = df.copy()

    # Update the data_size column with the concatenated values
    result_df['data_size'] = result_df['et_title_product_id'].map(result_data_size_dict)
    result_df['new_name'] = result_df['et_title_product_id'].map(result_name_dict)

    for i in result_df.index:
        product_name = result_df.loc[i,'et_title_product_name']
        sku = result_df.loc[i,'et_title_variation_sku']
        if 'silk' in product_name.lower():
            result_df.loc[i,'data_size'] = satin_descript_content.replace('result',result_df.loc[i,'data_size'])
            result_df.loc[i,'new_name'] = satin_name.replace('result',result_df.loc[i,'new_name'])
        elif 'Z' in sku:
            result_df.loc[i,'data_size'] = tencel_descript_content.replace('result',result_df.loc[i,'data_size'])
            result_df.loc[i,'new_name'] = tencel_name.replace('result',result_df.loc[i,'new_name'])
        else:
            result_df.loc[i,'data_size'] = bamboo_descript_content.replace('result',result_df.loc[i,'data_size'])
            result_df.loc[i,'new_name'] = bamboo_name.replace('result',result_df.loc[i,'new_name'])

    # Print the result DataFrame
    result_df.to_excel('result.xlsx')

