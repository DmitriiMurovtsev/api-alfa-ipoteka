import json

from app import app


login = "LONDORENKOMV"             # логин
password = "A4oXjGx2"       # пароль для тестовой среды

agent_contract_id = 7304803       # id агентского договора
channel_sale_id = 20075         # id канала продаж
department_id = 53224154           # id подразделения
manager_id = 638193450              # id менеджера
signer_id = 500644077               # id подписанта


# тест предварительного расчета
def test_estimation():
    
    client = app.test_client()
    
    data = {
        "auth": {
            "login": login,
            "password": password,
        },
        "agent": {
            "agent_contract_id": agent_contract_id,
            "department_id": department_id,
        },
        "insuranceCity": {
            "fiasId": "948d25b2-b2f9-41bc-be37-169492f56a67",
        },
        "insurance_objects": [
            {
                "type": "FLAT",
            },
        ],
        "insurer": {
            "birth_date": "1989-03-19",
            "sex": "MALE",
        },
        "mortgage_agreement": {
            "amount": "3200000",
            "bank": {
                "bic": "044525225",
                "name": "СБЕРБАНК РОССИИ",
            },
            "rate": "3.9",
            "date": "2023-12-01",
        },
    }
    
    response = client.post(
        '/estimation', 
        json=json.dumps(data), 
        content_type='application/json',
    )
    
    assert response.status_code == 200


# тест расчета котировки
def test_calculation():
    
    client = app.test_client()
    
    data = {
        "auth": {
            "login": login,
            "password": password,
        },
        "agent": {
            "agent_contract_id": agent_contract_id,
            "channel_sale_id": channel_sale_id,
            "department_id": department_id,
            "manager_id": manager_id,
            "signer_id": signer_id,
        },
        "agent_email": "mdv12672@gmail.com",
        "insuranceCity": {
            "fiasId": "948d25b2-b2f9-41bc-be37-169492f56a67",
        },
        "begin_date": "2024-06-20",
        "end_date": "2025-06-19",
        "insurance_objects": [
            {
                "address": {
                    "fias_id": "948d25b2-b2f9-41bc-be37-169492f56a67",
                    "text": "г Волгоград, пр-кт им. В.И. Ленина, д 72б, кв 1",
                },
                "name": "Квартира",
                "primary_sale": False,
                "property_risk": {
                    "address": "г Волгоград, пр-кт им. В.И. Ленина, д 72б, кв 1",
                    "construction_year": 2020,
                    "flammable": False,
                    "building_type": "Комбинированный",
                    "kad_number": "34:34:040010:1156",
                    "land_category": "Земли нас.пунктов (поселений)",
                    "market_price": 3200000,
                    "property_area": 35.5,
                    "renovation_work": False,
                    "seller_discount": "1",
                    "swimming_pool": False,
                    "total_renovation_work": False,
                },
                "title_risk": {
                    "address": "г Волгоград, пр-кт им. В.И. Ленина, д 72б, кв 1",
                    "age_owner": False,
                    "insurance_base_amount": 3200000,
                    "juridical_owner": False,
                    "kad_number": "34:34:040010:1156",
                    "land_category": "Земли нас.пунктов (поселений)",
                    "one_time_payment": True,
                    "ownership_confirmation": "Справка ЖСК, приватизация",
                    "ownership_less_three_years": False,
                    "ownership_restriction": "Имущество в залоге",
                    "procuratory_agreement": False,
                    "seller_discount": "1",
                    "spouse_approval": False,
                    "term_in_month": 12,                    
                },
                "type": "FLAT",
            },
        ],
        "insurance_program": "Базовая",
        "insurer": {
            "birth_date": "1989-10-10",
            "email": "mdv12672@gmail.com",
            "fact_address": {
                "fias_id": "948d25b2-b2f9-41bc-be37-169492f56a67",
                "text": "г Волгоград, пр-кт им. В.И. Ленина, д 72б, кв 1",
            },            
            "first_name": "Иван",
            "last_name": "Иванов",
            "life_risk" : {
                "health": "Нет отклонений",
                "profession": "Аналитик",
                "seller_discount": "1",
                "share": "100",
                "sport": "Не занимаюсь спортом",
            },
            "middle_name": "Иванович",
            "passport": {
                "issue_unit_code": "340-030",
                "issue_date": "2009-01-05",
                "issue_place": "УВД Московского района г. Казань",
                "number": "656211",
                "reg_address": {
                    "fias_id": "948d25b2-b2f9-41bc-be37-169492f56a67",
                    "text": "г Волгоград, пр-кт им. В.И. Ленина, д 72б, кв 1",                
                },
                "series": "1804",
            },
            "phone_number": "+79044035070",
            "resident": True,
            "sex": "MALE",
            "snils": "999-999-999 99",
        },
        "mortgage_agreement": {
            "amount": 3200000,
            "bank": {
                "bic": "044525225",
                "name": "СБЕРБАНК РОССИИ",                
            },
            "city": "Волгоград",
            "date": "2023-12-01",
            "number": "1234567",
            "rate": "3.9",
            "term_in_month": 12,
        },
        "prev_insurance_company": "ИНГОССТРАХ",   
        # "previous_number": "554477",              
        "risk_types": [
            "LIFE", "PROPERTY",
        ],
        "sign_date": "2024-06-01",
        "kv_discount": 0.99,
    }
    
    response = client.post(
        '/calculation', 
        json=json.dumps(data), 
        content_type='application/json',
    )
    
    assert response.status_code == 200


# тест загрузки договора в КИС
def test_create_contract():
    
    client = app.test_client()
    
    data = {
        "auth": {
            "login": login,
            "password": password,
        },
        "ipoteka_uuid": "394f2a92-eba2-401d-8666-8edef8ccc5ef",        
    }
    
    response = client.post(
        '/create_contract',
        json=json.dumps(data), 
        content_type='application/json',
    )
    
    assert response.status_code == 202


# тест получения информации по договору
def test_get_contract():
    
    client = app.test_client()
    
    data = {
        "auth": {
            "login": login,
            "password": password,
        },
        "ipoteka_uuid": "394f2a92-eba2-401d-8666-8edef8ccc5ef",        
    }
    
    response = client.post(
        '/get_contract',
        json=json.dumps(data), 
        content_type='application/json',
    )
    
    assert response.status_code == 200


# тест получения информации по группе договоров
def test_get_group_contract():
    
    client = app.test_client()
    
    data = {
        "auth": {
            "login": login,
            "password": password,
        },
        "group_id": 231479,        
    }
    
    response = client.post(
        '/get_group_contract',
        json=json.dumps(data), 
        content_type='application/json',
    )
    
    assert response.status_code == 200    


# тест получения списка печатных форм
def test_printforms():

    client = app.test_client()
    
    data = {
        "auth": {
            "login": login,
            "password": password,
        },
        "ipoteka_uuid": "394f2a92-eba2-401d-8666-8edef8ccc5ef",        
    }
    
    response = client.post(
        '/printforms',
        json=json.dumps(data), 
        content_type='application/json',
    )
    
    assert response.status_code == 200    


# тест получения печатной формы
def test_get_printform():
    
    client = app.test_client()
    
    data = {
        "auth": {
            "login": login,
            "password": password,
        },
        "ipoteka_uuid": "394f2a92-eba2-401d-8666-8edef8ccc5ef",        
        "form_id": "IPOTEKA-03",
    }
    
    response = client.post(
        '/get_printform',
        json=json.dumps(data), 
        content_type='application/json',
    )
    
    assert response.status_code == 200


# тест регистрации заказа на оплату
def test_payment():
    
    client = app.test_client()
    
    data = {
        "auth": {
            "login": login,
            "password": password,
        },
        "ipoteka_uuid": "394f2a92-eba2-401d-8666-8edef8ccc5ef",
        "bill_enabled": False,
        "contacts": {
            "email": "mdv12672@gmail.com",
            "phone": "+79044035070",
        },
    }
    
    response = client.post(
        '/payment',
        json=json.dumps(data), 
        content_type='application/json',
    )
    
    assert response.status_code == 200      


# тест получения списка вложенных файлов
def test_files():
    
    client = app.test_client()
    
    data = {
        "auth": {
            "login": login,
            "password": password,
        },
        "ipoteka_uuid": "394f2a92-eba2-401d-8666-8edef8ccc5ef",        
    }
    
    response = client.post(
        '/files',
        json=json.dumps(data), 
        content_type='application/json',
    )
    
    assert response.status_code == 200


# тест загрузки сопроводительных документов
def test_up_files():
    pass


# тест получения файла
def test_get_file():
    
    client = app.test_client()
    
    data = {
        "auth": {
            "login": login,
            "password": password,
        },
        "ipoteka_uuid": "394f2a92-eba2-401d-8666-8edef8ccc5ef",        
        "file_id": 169243,
    }
    
    response = client.post(
        '/get_file',
        json=json.dumps(data), 
        content_type='application/json',
    )
    
    assert response.status_code == 200    


# тест получения списка требуемых для оформления документов
def test_under_docs_info():
    
    client = app.test_client()
    
    data = {
        "auth": {
            "login": login,
            "password": password,
        },
        "ipoteka_uuid": "394f2a92-eba2-401d-8666-8edef8ccc5ef",        
    }
    
    response = client.post(
        '/under_docs_info',
        json=json.dumps(data), 
        content_type='application/json',
    )
    
    assert response.status_code == 200    


# тест отправки на андеррайтинг
def test_to_underwriter():
    
    client = app.test_client()
    
    data = {
        "auth": {
            "login": login,
            "password": password,
        },
        "ipoteka_uuid": "394f2a92-eba2-401d-8666-8edef8ccc5ef",        
        "message": "test underwriter",
    }
    
    response = client.post(
        '/to_underwriter',
        json=json.dumps(data), 
        content_type='application/json',
    )
    
    assert response.status_code == 200    


# тест получения всех словарей
def test_dictionary():
    
    client = app.test_client()
    
    types = [
        'profession',
        'health',
        'sport',
        'restriction_property_rights',
        'confirmation_document',
        'category',
        'bank-programs',
        'building_type',
    ]
    
    data = {
        "auth": {
            "login": login,
            "password": password,
        },
        "type": "",
    }
    
    for t in types:
        data["type"] = t
        
        response = client.post(
            '/dictionary', 
            json=json.dumps(data), 
            content_type='application/json',
        )
        
        assert response.status_code == 200


# тест получения ссылки на лендинг
def test_landing_offer():
    pass
    