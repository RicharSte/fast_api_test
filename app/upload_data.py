import hashlib
import pymongo

#я немного изменил бд сделав её переменной и питоновский файл, чтобы секономить пару строчек
from employees import data as employees

#коннект к дб
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["employeesdb"]
customers = db["employees"]

employees_list = []
for employee in employees:
    #генерю свой id  для записи, чтобы в будущем избезать дубликатов в базе
    employee['_id'] = hashlib.md5(f"{employee['email']}{employee['join_date']}".encode()).hexdigest()
    employees_list.append(employee)
    
x = customers.insert_many(employees_list)
# проверка, что записи залились
print(x.inserted_ids)