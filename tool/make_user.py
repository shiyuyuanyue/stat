'''
    添加用户
'''
import random
import pymysql

db = pymysql.connect(
    'rm-2zeev8fj515z9n30szo.mysql.rds.aliyuncs.com',
    'root',
    'Aa776977960',
    'stockstools',
    charset='utf8'
)
cursor = db.cursor()
ABC = ('QWERTYUIOPASDFGHJKLZXCVBNM')
abc = ('qwertyuiopadfghjklzxcvbnm')
int = ('0123456789')
password = '1760283ab424002c543e2250dba872e51a6f950a'
# 添加用户数量 1000
count = 0
#生成10000个随机用户
for i in range(10000):
    gender = random.choice(('男', '女'))
    age = random.choice(('10岁+', '20岁+', '30岁+', '40岁+', '50岁+', '60岁+', '70岁+', '80岁+'))
    salary = random.choice(('无业', '1000+', '2000+', '3000+', '4000+', '5000+', '6000+', '7000+', '8000+', '9000+',
                            '10000+', '15000+', '20000+', '30000+', '50000+',))
    Occupation = random.choice(
        ('机关党群', '企业负责人', '事业单位负责人', '专业技术人员', '办事人员', '商业人员', '服务业人员', '农林牧渔水生产人员', '制造运输业操作人员', '军人无业或退休'))
    partiality = random.choice(('短线', '中线', '长线'))
    experience = random.choice(
        ('1年以下', '1年以上', '2年以上', '3年以上', '4年以上', '5年以上', '6年以上', '7年以上', '8年以上', '9年以上', '10年以上'))
    lever = random.choice(('是', '否'))
    username = ''
    email = ''
    for i in range(10):
        username += random.choice(abc)
        email += random.choice(int)
    email += '@qq.com'
    ins = 'insert into userprofiles (username,password,email,gender,age,salary,Occupation,partiality,experience,lever)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    list_ins = [username, password, email, gender, age, salary, Occupation, partiality, experience, lever]
    count += 1
    print(count,'---',username,email, gender, age, salary)
    cursor.execute(ins, list_ins)
    db.commit()
cursor.close()
db.cursor()
