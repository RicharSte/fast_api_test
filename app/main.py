from fastapi import FastAPI, Request, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import motor.motor_asyncio


app = FastAPI()

#подключаемся к базе данных: TODO или вывести в отдельную функцию (если критично)
MONGO_DETAILS = "mongodb://172.17.0.2:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.employeesdb

#обрабатывам кривые запросы пользователя и отдаем ему текст ошибки + параметры в которых была ошибка
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    msges = []
    for msg in exc.errors():
        msges.append(msg['msg'])
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"errors":msges, "bad params": exc.errors()[0]['loc']})
    )

#получаем и отдаем данные согласно запросу: TODO реализация сапросов поддерживающих AND, AND NOT, OR
@app.get('/')
async def main(name: str = Query(default=None, min_length=2), email: str = Query(default=None, min_length=5), ageP: int = 0, ageL: int = 0, company: str = Query(default=None, min_length=2), join_dateP: str = Query(default=None, min_length=25, max_length=25), join_dateL: str = Query(default=None, min_length=25, max_length=25), job_title: str = Query(default=None, min_length=2), gender: str = Query(default=None, min_length=4, max_length=6), salaryP: int = 0,  salaryL: int = 0, size: int = 100):
    request_dict = {}
    #создаем наш будущий запрос к бд: TODO избавиться от этого огромного if дерева (возможно перейти на post с loop'ом)
    if name:
        request_dict['name'] = name
    if email:
        request_dict['email'] = email
    if ageP: 
        request_dict['age'] = {"$gt": ageP}
    if ageL:
        request_dict['age'] = {"$lt": ageL}
    if company:
        request_dict['company'] = company
    if join_dateP: #некоторые параметры могу использоваться с range из-за чего нужно множить параметры
        request_dict['join_date'] = {"$gt": join_dateP}
    if join_dateL:
        request_dict['join_date'] = {"$lt": join_dateL}
    if job_title:
        request_dict['job_title'] = job_title
    if gender:
        request_dict['gender'] = gender
    if company:
        request_dict['company'] = company
    if salaryP:
        request_dict['salary'] = {"$gt": salaryP}
    if salaryL:
        request_dict['salary'] = {"$lt": salaryL}
    #делаем запрос в дб
    student_collection = await database["employees"].find(request_dict).to_list(size)
    #если пользователь отправил некорректный запрос и/или ничего не нашлось, коворим ему, что он что-то сделал не так
    if student_collection == []:
        return {"errors": "I think something went wrong. Please check your request"}
    #возвращаем ответ от db
    return {"response": student_collection}