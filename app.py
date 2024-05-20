from datetime import datetime
from functools import wraps
import json
import time
import logging
from logging.handlers import RotatingFileHandler
import requests
from requests.auth import HTTPDigestAuth

from flask import Flask, Response, request, jsonify
from pydantic import ValidationError

from valids import (
    EstimationValidator, 
    CalculationValidator, 
    CreateContractValidator, 
    GetContractValidator,
    GetGroupContractValidator,
    PrintformsValidator,
    GetPrintformsValidator,
    PaymentValidator,
    FilesValidator,
    UpFilesValidator,
    GetFileValidator,
    UnderDocsInfoValidator,
    ToUnderwriterValidator,
    DictionaryValidator,    
)


app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)

file_handler = RotatingFileHandler('alfa-app.log')
app.logger.addHandler(file_handler)

link_api = "https://b2b-test2.alfastrah.ru/wapi/ipoteka"


# приводит ответ альфы к одному формату
def handle_response_errors(response, good_errors):
    response_data = ''
    
    if response.status_code in good_errors or response.status_code in [200, 202]:
        response_data = response.json()
        
    elif response.status_code == 401:
        response_data = {
            "info": "Неверный логин или пароль",
            "session_id": None,
            "sub_errors": [
                {
                    "message": "Неверный логин или пароль"
                }
            ],
            "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }
        
    else:
        response_data = {
            "info": "Неизвестная ошибка от внешнего api",
            "session_id": None,
            "sub_errors": [
                {
                    "message": "Неизвестная ошибка от внешнего api"
                }
            ],
            "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }        
    
    return response_data, response.status_code


# валидирует входные данные
def validation_of_input_data(request, pydantic_validation_class, form_json=None):
        
    try:
        if form_json:
            json_data = json.dumps(form_json)
        else:
            json_data = request.get_json()
            
        pydantic_validation_class.model_validate_json(json_data)
    
    except ValidationError as e:
        
        sub_errors = []
        for error in e.errors():
            loc = '.'.join([str(er) for er in error['loc']])            
            sub_error = {"message": f"{loc}: {error['msg']}"}
            sub_errors.append(sub_error)
        
        validation_error = {
            "info": "Ошибка входных данных",
            "session_id": None,
            "sub_errors": sub_errors,
            "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }
        
        return False, None, validation_error
    
    return True, json_data, None


# для логирования и обработки непредвиденных ошибок
def request_response_logging(f):
    @wraps(f)
    def check(*args, **kwargs):
        
        start_time = time.time()
        
        params = request.values.to_dict()
        if params.get('auth'):
            params['auth'] = {"login": "******", "password": "******"}
        
        try:
            result, code_ = f(*args, **kwargs)
            
            log_ = {
                "date_request": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "method": f.__name__,
                "execution_time": time.time() - start_time,
                "status": "Успешно" if code_ in [200, 202] else "Не успешно",
                "status_code": code_,
                "ip": request.remote_addr,
                "parameters": params,
                "response": result.get_json(),
            }
            
            if code_ in [200, 202]:
                app.logger.info(log_)
            else:
                app.logger.error(log_)
            
            return result, code_
        
        except Exception as e:
            
            unknown_errors = {
                "info": f"Непредвиденная ошибка в методе {f.__name__}",
                "session_id": None,
                "sub_errors": [
                    {
                        "message": str(e),
                    }
                ],
                "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
            
            log_ = {
                "date_request": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "method": f.__name__,
                "execution_time": time.time() - start_time,
                "status": "Не успешно",
                "status_code": 500,
                "ip": request.remote_addr,
                "parameters": params,
                "response": unknown_errors,
            }     
            
            app.logger.error(log_)
            
            return jsonify(unknown_errors), 500
    
    return check


# Предварительный расчет котировки Ипотеки
@app.route("/estimation", methods=["POST"])
@request_response_logging
def estimation():
       
    is_valid, request_data, errors = validation_of_input_data(request, EstimationValidator)
    if not is_valid:        
        return jsonify(errors), 400
    
    login = request_data["auth"]["login"]
    password = request_data["auth"]["password"]
        
    response = requests.post(f"{link_api}/estimation", auth=HTTPDigestAuth(login, password), json=request_data)
    
    response_data, status_code = handle_response_errors(response, [400, 403, 500])    
    
    return jsonify(response_data), status_code


# Расчет котировки Ипотеки
@app.route("/calculation", methods=["POST"])
@request_response_logging
def calculation():
    
    is_valid, request_data, errors = validation_of_input_data(request, CalculationValidator)
    if not is_valid:
        return jsonify(errors), 400
    
    login = request_data["auth"]["login"]
    password = request_data["auth"]["password"]    
    
    response = requests.post(f"{link_api}/calculation", auth=HTTPDigestAuth(login, password), json=request_data)
      
    response_data, status_code = handle_response_errors(response, [400, 403, 500])
    
    return jsonify(response_data), status_code


# Загрузка договора ипотеки в КИС
# Присваивается номер
@app.route("/create_contract", methods=["POST"])
@request_response_logging
def create_contract():
    
    is_valid, request_data, errors = validation_of_input_data(request, CreateContractValidator)
    if not is_valid:
        return jsonify(errors), 400    
    
    ipoteka_uuid = request_data["ipoteka_uuid"]
    login = request_data["auth"]["login"]
    password = request_data["auth"]["password"]    
    
    response = requests.post(f"{link_api}/contract/{ipoteka_uuid}", auth=HTTPDigestAuth(login, password))    
    
    response_data, status_code = handle_response_errors(response, [400, 404, 500])
    
    return jsonify(response_data), status_code    


# Получение информации по договору
@app.route("/get_contract", methods=["POST"])
@request_response_logging
def get_contract():
    
    is_valid, request_data, errors = validation_of_input_data(request, GetContractValidator)
    if not is_valid:
        return jsonify(errors), 400    
    
    ipoteka_uuid = request_data["ipoteka_uuid"]
    login = request_data["auth"]["login"]
    password = request_data["auth"]["password"]    
    
    response = requests.get(f"{link_api}/contract/{ipoteka_uuid}", auth=HTTPDigestAuth(login, password))
    
    response_data, status_code = handle_response_errors(response, [400, 403, 404, 500])
    
    return jsonify(response_data), status_code


# Получение данных по группе договоров ипотечного страхования
# Группа - это более одного полиса на один кредитный договор, например жизнь и имущество разными полисами
@app.route("/get_group_contract", methods=["POST"])
@request_response_logging
def get_group_contract():
    
    is_valid, request_data, errors = validation_of_input_data(request, GetGroupContractValidator)
    if not is_valid:
        return jsonify(errors), 400    
    
    group_id = request_data["group_id"]
    login = request_data["auth"]["login"]
    password = request_data["auth"]["password"]    
    
    response = requests.get(f"{link_api}/contract/group/{group_id}", auth=HTTPDigestAuth(login, password))
    
    response_data, status_code = handle_response_errors(response, [400, 403, 404, 500])
    
    return jsonify(response_data), status_code


# Получение списка доступных печатных форм для договора
@app.route("/printforms", methods=["POST"])
@request_response_logging
def printforms():
    
    is_valid, request_data, errors = validation_of_input_data(request, PrintformsValidator)
    if not is_valid:
        return jsonify(errors), 400    
    
    ipoteka_uuid = request_data["ipoteka_uuid"]
    login = request_data["auth"]["login"]
    password = request_data["auth"]["password"]    
    
    response = requests.get(f"{link_api}/printforms/{ipoteka_uuid}", auth=HTTPDigestAuth(login, password))

    response_data, status_code = handle_response_errors(response, [400, 403, 404, 500])
    
    return jsonify(response_data), status_code


# Получение печатной формы
@app.route("/get_printform", methods=["POST"])
@request_response_logging
def get_printform():
    #TODO: решить с различными расширениями файлов
    
    is_valid, request_data, errors = validation_of_input_data(request, GetPrintformsValidator)
    if not is_valid:
        return jsonify(errors), 400    
    
    ipoteka_uuid = request_data["ipoteka_uuid"]
    form_id = request_data["form_id"]
    login = request_data["auth"]["login"]
    password = request_data["auth"]["password"]    
    
    response = requests.get(f"{link_api}/printform/{ipoteka_uuid}/form/{form_id}/", auth=HTTPDigestAuth(login, password))
        
    exten = '.'
    if 'msword' in response.headers['Content-Type']:
        exten += 'doc'
    else:
        exten += 'pdf'
    
    headers = {
        "Content-Disposition": f"attachment; filename={form_id}_{ipoteka_uuid}.{exten}",
    }
    
    return Response(response.content, headers=headers)


# Регистрация заказа на оплату
# Вначале нужно вызвать 'create_contract'
@app.route("/payment", methods=["POST"])
@request_response_logging
def payment():
    
    is_valid, request_data, errors = validation_of_input_data(request, PaymentValidator)
    if not is_valid:
        return jsonify(errors), 400    
    
    ipoteka_uuid = request_data["ipoteka_uuid"]
    login = request_data["auth"]["login"]
    password = request_data["auth"]["password"]    
    
    response = requests.post(f"{link_api}/payment/{ipoteka_uuid}", auth=HTTPDigestAuth(login, password), json=request_data)
    
    response_data, status_code = handle_response_errors(response, [400, 404, 500])
    
    return jsonify(response_data), status_code    
  

# Получение списка вложенных файлов
@app.route("/files", methods=["POST"])
@request_response_logging
def files():
    
    is_valid, request_data, errors = validation_of_input_data(request, FilesValidator)
    if not is_valid:
        return jsonify(errors), 400
    
    ipoteka_uuid = request_data["ipoteka_uuid"]
    login = request_data["auth"]["login"]
    password = request_data["auth"]["password"]    
        
    response = requests.get(f"{link_api}/files/{ipoteka_uuid}", auth=HTTPDigestAuth(login, password))
        
    response_data, status_code = handle_response_errors(response, [400, 403, 404, 500])
    
    return jsonify(response_data), status_code


# Загрузка сопроводительных документов к договору страхования ипотеки
@app.route("/up_files", methods=["POST"])
@request_response_logging
def up_files():
    
    file = request.files.get("file")
    if not file:
        return jsonify(
            {
                "info": "Ошибка загрузки файла",
                "session_id": None,
                "sub_errors": [
                    {
                        "message": "Файл не выбран",
                    },
                ],
                "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        ), 400
        
    form_json = request.values.to_dict()
    if 'auth' in form_json:
        form_json['auth'] = json.loads(form_json['auth'])
                
    is_valid, _, errors = validation_of_input_data(request, UpFilesValidator, form_json)
    if not is_valid:
        return jsonify(errors), 400
    
    type_file = form_json["type"]
    ipoteka_uuid = form_json["ipoteka_uuid"]
    
    login = form_json["auth"]["login"]
    password = form_json["auth"]["password"]
                    
    response = requests.post(
        f"{link_api}/files/{ipoteka_uuid}",
        auth=HTTPDigestAuth(login, password),
        data={"type": type_file},
        files={"file": (file.filename, file.stream, file.mimetype)},
    )
    
    response_data, status_code = handle_response_errors(response, [400, 403, 404, 413, 500])
        
    return jsonify(response_data), status_code


# Получение вложенного файла к договору страхования ипотеки
@app.route("/get_file", methods=["POST"])
@request_response_logging
def get_file():
    #TODO: решить с различными расширениями файлов
    is_valid, request_data, errors = validation_of_input_data(request, GetFileValidator)
    if not is_valid:
        return jsonify(errors), 400    
    
    ipoteka_uuid = request_data["ipoteka_uuid"]
    file_id = request_data["file_id"]
    login = request_data["auth"]["login"]
    password = request_data["auth"]["password"]    
        
    response = requests.get(
        f"{link_api}/files/{ipoteka_uuid}/file/{file_id}/",
        auth=HTTPDigestAuth(login, password),
    )
            
    exten = '.'
    if 'msword' in response.headers['Content-Type']:
        exten += 'doc'
    else:
        exten += 'pdf'
    
    headers = {
        "Content-Disposition": f"attachment; filename={file_id}_{ipoteka_uuid}{exten}",
    }
    
    return Response(response.content, headers=headers)


# Получение списка требуемых документов, необходимых для оформления договора страхования ипотеки
@app.route("/under_docs_info", methods=["POST"])
@request_response_logging
def under_docs_info():
    
    is_valid, request_data, errors = validation_of_input_data(request, UnderDocsInfoValidator)
    if not is_valid:
        return jsonify(errors), 400    
    
    ipoteka_uuid = request_data["ipoteka_uuid"]
    login = request_data["auth"]["login"]
    password = request_data["auth"]["password"]    
    
    response = requests.get(
        f"{link_api}/files/{ipoteka_uuid}/underwriting-required-documents-info",
        auth=HTTPDigestAuth(login, password),
    )
        
    response_data, status_code = handle_response_errors(response, [400, 404, 500])
    
    return jsonify(response_data), status_code


# Отправка на андеррайтинг
@app.route("/to_underwriter", methods=["POST"])
@request_response_logging
def to_underwriter():
    
    is_valid, request_data, errors = validation_of_input_data(request, ToUnderwriterValidator)
    if not is_valid:
        return jsonify(errors), 400    
    
    ipoteka_uuid = request_data["ipoteka_uuid"]
    message = request_data.get("message")
    login = request_data["auth"]["login"]
    password = request_data["auth"]["password"]
    
    data = {
        "message": message if message else '',
    }
    
    response = requests.post(
        f"{link_api}/underwriting/{ipoteka_uuid}/to-underwriter",
        auth=HTTPDigestAuth(login, password),
        json=data,
    )
        
    response_data, status_code = handle_response_errors(response, [400, 403, 404, 500])
    
    return jsonify(response_data), status_code    


# Получение ссылки на страницу лендинга. (Требуется оформление дополнительного доступа через куратора)
@app.route("/landing_offer", methods=["POST"])
@request_response_logging
def landing_offer():
    
    return jsonify({
        "info": "Ошибка при получении ссылки на страницу лендинга",
        "session_id": None,
        "sub_errors": [
            {
                "message": "Требуется согласование доступа куратором",
            }
        ],
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }), 501


# Справочники
@app.route("/dictionary", methods=["POST"])
@request_response_logging
def dictionary():
    
    is_valid, request_data, errors = validation_of_input_data(request, DictionaryValidator)
    if not is_valid:
        return jsonify(errors), 400    
    
    login = request_data["auth"]["login"]
    password = request_data["auth"]["password"]
    type_dictionary = request_data["type"]
    
    link = f"{link_api}/dictionary/{type_dictionary}/names"
    if type_dictionary != "bank-programs":
        link += "/names"
        
    response = requests.get(link, auth=HTTPDigestAuth(login, password))
    
    response_data, status_code = handle_response_errors(response, [400, 404, 500])
    
    return jsonify(response_data), status_code


if __name__ == "__main__":
    app.run(host='0.0.0.0')

