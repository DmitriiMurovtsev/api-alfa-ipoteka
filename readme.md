# В каждом методе
### 1. Метод запроса POST
### 2. Content-Type: Application/json (кроме “up_files”, там multipart/form-data)
### 3. Не успешный ответ: 
```python
{
    "info": str,                # Сообщение об ошибке
    "session_id":str,           # session_id или None
    "sub_errors": [			
        {
            "message": str,     # Подробное сообщение об ошибке
        },
    ],
    "timestamp": str,           # Время ошибки в формате DD-MM-YYYY HH:MM:SS
}
```
# Методы
### 1. [estimation](#estimation)
### 2. [calculation](#calculation)
### 3. [create_contract](#create_contract)
### 4. [get_contract](#get_contract)
### 5. [get_group_contract](#get_group_contract)
### 6. [printforms](#printforms)
### 7. [get_printform](#get_printform)
### 8. [payment](#payment)
### 9. [files](#files)
### 10. [up_files](#up_files)
### 11. [get_file](#get_file)
### 12. [under_docs_info](#under_docs_info)
### 13. [to_underwriter](#to_underwriter)
### 14. [dictionary](#dictionary)
### 15. [landing_offer](#landing_offer)

# estimation
[Наверх](#методы)
### Предварительный расчет котировки Ипотеки
#### Принимает:
```python
{
    "agent": {                          # Агентский блок
        "agent_contract_id": int,       # *Идентификатор агентского договора
        "department_id": int,           # *Идентификатор подразделения продавца
    },
    "insuranceCity": {                  # *Регион / Город объекта страхования
        "fiasId": str,                  # *Код ФИАС с детализацией до Города (4-й уровень)
    },
    "insurance_objects": [              # *Объекты страхования. Возможно до 2-х объектов
        {
            "type": str,                # *Тип объекта
        }
    ],
    "insurer": {                        # *Заемщик
        "birth_date": str,              # *Дата рождения, формат YYYY-MM-DD
        "sex": str,                     # *Пол, возможны MALE, FEMALE
    },
    "mortgage_agreement": {             # *Данные по кредиту
        "amount": float,                # *Сумма кредита		
        "bank": {                       # Данные банка из справочника
            "bic": str,                 # *БИК банка
            "name": str,                # Наименование банка
        },
        "rate": float,                  # *Процентная ставка, например 8.9
        "date": str,                    # Дата кредитного договора, формат YYYY-MM-DD
    }
}
```
#### Успешный ответ:
```python
{
    "insurance_program": str,           # Программа страхования
    "insurance_sum": float,             # Страховая сумма
    "premium_sum": float,               # Страховая премия общая
    "risks": [                          # Список рисков, до трех
        {
            "insurance_sum": float,     # Страховая сумма
            "premium_sum": float,       # Страховая премия
            "risk_type": str,           # Тип риска, возможны LIFE, PROPERTY, TITLE
        }’
    ],
}
```

# calculation
[Наверх](#методы)
### Расчет котировки Ипотеки
#### Принимает:
```python
{
    "agent": {                          # Агентский блок
        "agent_contract_id": int,       # *Идентификатор агентского договора
        "channel_sale_id": int,         # *Идентификатор канала продаж
        "department_id": int,           # *Идентификатор подразделения продавца
        "manager_id": int,              # *Идентификатор менеджера по договору
        "signer_id": int,               # *Идентификатор лица подписавшего договор
    },
    "agent_email": str,                 # *E-mail агента для ответов андеррайтеров
    "insuranceCity": {                  # *Регион / Город объекта страхования
        "fiasId": str,                  # *Код ФИАС с детализацией до Города (4-й уровень)
    },
    "begin_date": str,                  # *Дата начала действия, формат YYYY-MM-DD
    "co_insurers": [                    # Блок созаемщики. Возможно наличие до 3-х созаемщиков
        {
            "birth_date": str,          # Дата рождения, формат YYYY-MM-DD
            "email": str,               # Email
            "fact_address": {           # Фактический адрес проживания
                "fias_id": str,         # Код ФИАС
                "text": str,            # *Адрес одной строкой
            },
            "first_name": str,          # Имя
            "last_name": str,           # Фамилия
            "life_risk": {              # Блок данных по риску LIFE
                "health": str,              # Категория здоровья согласно справочника
                "profession": str,          # Категория профессии согласно справочника
                "seller_discount": str,     # Коэффициент агента
                "share": float,             # Доля. По дефолту передавать 100
                "sport": str,               # Категория спорта согласно справочника
            },
            "middle_name": str,             # Отчество
            "passport": {                   # Данные паспорта
                "issue_unit_code": str,     # Код подразделения
                "issue_date": str,          # Дата выдачи паспорта, формат YYYY-MM-DD
                "issue_place": str,         # Место выдачи паспорта
                "number": str,              # Номер паспорта
                "reg_address": {            # Адрес проживания по месту регистрации
                    "fias_id": str,         # Код ФИАС
                    "text": str,            # *Адрес одной строкой
                },
                "series": str,              # Серия паспорта
            },
            "phone_number": str,            # Номер телефона
            "resident": bool,               # Гражданство РФ
            "sex": str,                     # *Пол, возможны MALE, FEMALE
            "snils": str,                   # СНИЛС
        },
    ],
    "end_date": str,                        # *Дата окончания действия, формат YYYY-MM-DD
    "insurance_objects": [                  # *Объекты страхования. Возможно до 2-х объектов
        {
            "address": {                    # Адрес объекта
                "fias_id": str,             # Код ФИАС
                "text": str,                # *Адрес одной строкой
            },
            "name": str,                    # Наименование объекта
            "primary_sale": bool,           # *Признак первичной недвижимости
            "property_risk": {              # *Риски недвижимости
                "address": str,             # Адрес
                "construction_year": int,   # *Год постройки
                "flammable": bool,          # *Признак наличия огнеопасных материалов
                "kad_number": str,          # Кадастровый номер
                "land_category": str,       # Категория земель
                "market_price": float,      # Рыночная стоимость
                "property_area": float,     # *Площадь
                "renovation_work": bool,    # *Признак наличия ремонтных работ на данный момент
                "seller_discount": str,     # Коэффициент продавца
                "swimming_pool": bool,      # Признак наличия бассейна
                "total_renovation_work": bool,      # *Признак наличия капитальный ремонтных работ
            },
            "title_risk": {                         # Риски страхования TITLE
                "address": str,                     # Адрес
                "age_owner": bool,                  # Наличие собственников младше 18 и старше 65 лет
                "insurance_base_amount": float,     # Рыночная стоимость
                "juridical_owner": bool,            # Признак наличия юридических лиц в собственниках
                "kad_number": str,                  # Кадастровый номер
                "land_category": str,               # Категория земель
                "one_time_payment": bool,           # Признак единовременной оплаты
                "ownership_confirmation": str,      # Документ, подтверждающий право собственности
                "ownership_less_three_years": bool, # Наличие в собственности меньше 3 лет
                "ownership_restriction": str,       # Ограничения на права собственности
                "procuratory_agreement": bool,      # Проведение сделки по доверенности
                "seller_discount": str,             # Коэффициент продавца
                "spouse_approval": bool,            # Признак отсутствия согласия супруга/супруги
                "term_in_month": int,               # Срок страхования в месяцах
            },
            "type": str,                            # Тип объекта
        },
    ],
    "insurance_program": str,               # *Программа страхования согласно справочника
    "insurer": {                            # *Заемщик
        "birth_date": str,                  # Дата рождения, формат YYYY-MM-DD
        "email": str,                       # Email
        "fact_address": {                   # Фактический адрес проживания
            "fias_id": str,                 # Код ФИАС
            "text": str,                    # *Адрес одной строкой
        },
        "first_name": str,                  # Имя
        "last_name": str,                   # Фамилия
        "life_risk": {                      # Блок данных по риску LIFE
            "health": str,                  # Категория здоровья согласно справочника
            "profession": str,              # Категория профессии согласно справочника
            "seller_discount": str,         # Коэффициент агента	
            "share": float,                 # Доля. По дефолту передавать 100
            "sport": str,                   # Категория спорта согласно справочника
        },
        "middle_name": str,                 # Отчество
        "passport": {                       # Данные паспорта
            "issue_unit_code": str,         # Код подразделения
            "issue_date": str,              # Дата выдачи паспорта, формат YYYY-MM-DD
            "issue_place": str,             # Место выдачи паспорта
            "number": str,                  # Номер паспорта
            "reg_address": {                # Адрес проживания по месту регистрации
                "fias_id": str,             # Код ФИАС
                "text": str,                # *Адрес одной строкой
            },
            "series": str,                  # Серия паспорта
        },
        "phone_number": str,                # Номер телефона
        "resident": bool,                   # Гражданство РФ
        "sex": str,                         # *Пол
        "snils": str,                       # СНИЛС
    },
    "mortgage_agreement": {                 # *Данные кредита
        "amount": float,                    # Сумма кредита
        "bank": {                           # Данные банка
            "bic": str,                     # БИК банка
            "name": str,                    # Наименование банка
        },
        "city": str,                        # Город выдачи кредита
        "date": str,                        # *Дата кредитного договора, формат YYYY-MM-DD
        "number": str,                      # Номер кредитного договора
        "rate": float,                      # Процентная ставка, например 8.9
        "term_in_month": int,               # Срок страхования в месяцах
    },
    "prev_insurance_company": str,          # Наименование предыдущей страховой компании
    "previous_number": str,                 # Предыдущий номер договора (для пролонгации)
    "risk_types": [                         # *Типы рисков к страхованию
        "LIFE",				
    ],
    "sign_date": str,                       # *Дата оформления, формат YYYY-MM-DD
    "kv_discount": float,                   # Коэффициент скидки за счёт КВ, например 0.9
}
```
#### Успешный ответ:
```python
{
    "begin_date": str,              # *Дата начала действия, формат YYYY-MM-DD
    "declaration": bool,            # Признак декларации
    "end_date": str,                # *Дата окончания действия, формат YYYY-MM-DD
    "insurance_program": str,       # Программа страхования
    "insurance_sum": float,         # Страховая сумма
    "ipoteka_uuid": str,            # Универсальный идентификатор договора страхования ипотеки
    "group_id": int,                # Идентификатор группы связанных договоров
    "no_paper_offer_sent": bool,    # Признак успешной отправки предложения ББ
    "number": str,                  # Номер договора
    "offer": bool,                  # Признак оферты
    "premium_sum": float,           # Сумма премии
    "prev_insurance_company": str,  # Наименование предыдущей страховой компании
    "previous_number": str,         # Предыдущий номер договора
    "risks": [                      # Информация по рискам
        {
            "insurance_sum": float,                     # Страховая сумма
            "objects": [                                # Список объектов / заёмщиков
                {
                    "insurance_base_amount": float,     # Страховая сумма
                    "payments": [                       # Платежи
                        {
                            "insurance_sun": float,     # Страховая сумма
                            "month_in_period": int,     # Количество месяцев в периоде
                            "period": int,              # Период
                            "premiumSum": float,        # Сумма премии
                            "tariff": float,            # Тариф
                        },
                    ],  
                "type": str,                            # Тип объекта
                },
            ],
            "premium_sum": float,                       # Сумма премии
            "risk_type": str,                           # Тип риска
        },
    ],
    "sign_date": str,                                   # *Дата оформления, формат YYYY-MM-DD
}
```
# create_contract
[Наверх](#методы)
### Загрузка договора ипотеки в КИС
### Присваивается номер полиса
#### Принимает:
```python
{
  "ipoteka_uuid": str,      # Универсальный идентификатор договора страхования ипотеки
}
```
#### Успешный ответ:
```python
{
  "begin_date": str,            # Дата начала действия полиса, формат 
  "contract_number": str,       # Номер договора страхования ипотеки
  "end_date": str,              # Дата окончания действия полиса
  "insurance_amount": float,    # Страховая сумма
  "ipoteka_uuid": str,          # Универсальный идентификатор договора страхования ипотеки
  "premium_amount": float,      # Сумма страховой премии
  "group_id": int,              # Идентификатор группы связанных договоров
}
```
# get_contract
[Наверх](#методы)
### Получение информации по договору
#### Принимает:
```python
{
    "ipoteka_uuid": str,        # Универсальный идентификатор договора страхования ипотеки
}
```
#### Успешный ответ:
```python
{
    "agent": {                              # Информация по агенту
        "agent_contract_number": str,       # Номер агентского договора
        "agent_sale_code": str,             # Наименование канала продаж
        "department_code": str,             # Код подразделения продавца
        "email": str,                       # Адрес электронной почты для связи с андеррайтерами
        "manager_name": str,                # Код подразделения продавца
        "signer_name": str,                 # Лицо, подписавшее договор со стороны СК
    },
    "begin_date": str,                      # Дата начала действия договора, формат YYYY-MM-DD HH:MM:SS
    "co_insurers": [                        # Блок с данными о созаемщиках
        {
            "birth_date": str,              # Дата рождения, формат YYYY-MM-DD
            "email": str,                   # email
            "fact_address": {               # Данные фактического адреса
            "fias_id": str,                 # Код ФИАС
            "text": str                     # Полный адрес
        },  
        "first_name": str,                  # Имя
        "last_name": str,                   # Фамилия
        "life_risk": {                      # Данные о риске по жизни
            "health": str,                  # Категория здоровья согласно справочника
            "profession": str,              # Категория профессии согласно справочника
            "seller_discount": float,       # Коэффициент агента
            "share": float,                 # Доля
            "sport": str,                   # Категория спорта согласно справочника
        },
        "middle_name": str,                 # Отчество
        "passport": {                       # Данные о паспорте
            "issue_code": str,              # Код подразделения
            "issue_date": str,              # Дата выдачи паспорта, формат YYYY-MM-DD
            "issue_place": str,             # Кем выдан
            "number": str,                  # Номер паспорта
            "reg_address": {                # Данные адреса регистрации
                "fias_id": str,             # Код ФИАС
                "text": str,                # *Полный адрес
            },
            "series": str,                  # Серия паспорта
        },
        "phone_number": str,                # Номер телефона
        "resident": bool,                   # Резидент РФ
        "sex": str,                         # Пол
        "snils": str,                       # СНИЛС
        },
    ],
    "contract_status": str,             # Статус договора
    "contract_type": str,               # Тип договора, возможны PRIMARY, PROLONGATION
    "create_date": str,                 # Дата создания договора, формат YYYY-MM-DD
    "declaration": bool,                # Признак декларации
    "end_date": str,                    # Дата окончания действия договора YYYY-MM-DD
    "errors": [                         # Блок ошибок по котировке
        {
            "message": str,             # Сообщение по ошибке
        },
    ],
    "group_id": int,                    # Идентификатор группы связанных договоров
    "insuranceCity": {                  # Регион / Город объекта страхования
        "fias_id": str,                 # Код ФИАС
    },
    "insurance_objects": [              # Блок с данными об объекте страхования
        {
            "address": {                # Данные адреса
                "fias_id": str,         # Код ФИАС
                "text": str,            # *Полный адрес
            },
            "name": str,                        # Наименование объекта
            "primary_sale": bool,               # *Признак первичной недвижимости
            "property_risk": {                  # *Данные о параметрах риска недвижимости
                "address": str,                 # Полный адрес объекта страхования
                "construction_year": int,       # *Год постройки объекта
                "flammable": bool,              # *Материал стен и перекрытий из горючих материалов
                "kad_number": str,              # Кадастровый номер объекта
                "land_category": str,           # Категория земли из справочника
                "market_price": float,          # Рыночная стоимость объекта
                "property_area":float,          # *Площадь объекта
                "renovation_work": bool,        # *Признак наличия ремонтных работ на данный момент
                "seller_discount": float,       # Коэффициент агента
                "swimming_pool": bool,          # Наличие бассейна/сауны/джакузи/камина/печи
                "total_renovation_work": bool,  # *Наличие капитальных ремонтных работ или перепланировки
            },    
            "title_risk": {                         # Данные о параметрах риска TITLE
                "address": str,                     # Полный адрес объекта страхования
                "age_owner": bool,                  # Собственник младше 18 и старше 65 лет
                "insurance_base_amount": float,     # Рыночная стоимость
                "juridical_owner": bool,            # Признак наличия юридических лиц в собственниках
                "kad_number": str,                  # Кадастровый номер объекта
                "land_category": str,               # Категория земли из справочника
                "one_time_payment": bool,           # Признак единовременной оплаты
                "ownership_confirmation": str,      # Документ, подтверждающий право собственности
                "ownership_less_three_years": bool, # Наличие в собственности меньше 3 лет
                "ownership_restriction": str,       # Ограничения на права собственности
                "procuratory_agreement": bool,      # Признак проведения сделки по доверенности
                "seller_discount": float,           # Коэффициент агента
                "spouse_approval": bool,            # Признак отсутствия согласия супруга/супруги
                "term_in_month": int,               # Срок страхования в месяцах
            },
            "type": str,                            # Тип объекта
        },
    ],
    "insurance_program": str,           # Программа страхования
    "insurance_sum": float,             # Страховая сумма
    "insurer": {                        # Данные о заемщике
        "birth_date": str,              # Дата рождения, формат YYYY-MM-DD
        "email": str,                   # Email
        "fact_address": {               # Данные фактического адреса
            "fias_id": str,             # Код ФИАС
            "text": str,                # *Полный адрес
        },
        "first_name": str,              # Имя
        "last_name": str,               # Фамилия
        "life_risk": {                  # Данные о риске по жизни
            "health": str,              # Категория здоровья согласно справочника
            "profession": str,          # Категория профессии согласно справочника
            "seller_discount": float    # Коэффициент агента
            "share": float,             # Доля
            "sport": str,               # Категория спорта согласно справочника
        },
        "middle_name": str,             # Отчество
        "passport": {                   # Данные о паспорте
            "issue_code": str,          # Код подразделения
            "issue_date": str,          # Дата выдачи паспорта	
            "issue_place": str,         # Кем выдан
            "number": str,              # Номер паспорта
            "reg_address": {            # Данные адреса регистрации
                "fias_id": str,         # Код ФИАС
                "text": str,            # *Полный адрес
            },
            "series": str,              # Серия паспорта
        },
        "phone_number": str,            # Номер телефона
        "resident": bool,               # Резидент РФ
        "sex": str,                     # Пол
        "snils": str,                   # СНИЛС
    },
    "ipoteka_uuid": str,                # Универсальный идентификатор договора страхования ипотеки
    "kv_discount": int,
    "mortgage_agreement": {             # Данные по кредиту
        "amount": float,                # Сумма кредита
        "bank.bic": str,                # Бик банка
        "bank.name": str,               # Наименование банка
        "city": str,                    # Город выдачи кредита
        "date": str,                    # Дата кредитного договора
        "number": str,                  # Номер кредитного договора
        "rate": float,                  # Процентная ставка
        "term_in_month": int,           # Оставшийся срок кредита в месяцах
    },
    "no_paper": bool,                   # Признак ББ
    "number": str,                      # Номер договора
    "offer": bool,                      # Признак оферты
    "premium_sum": float,               # Сумма премии
    "prev_insurance_company": str,      # Наименование предыдущей страховой компании
    "previous_number": str,             # Предыдущий номер договора (для пролонгации)
    "risk_types": [                     # Типы рисков к страхованию
        str,			
    ],
    "risks": [                          # Риски по договору
        {
            "insurance_sum": float,     # Страховая сумма
            "objects": [                # Список объектов/заёмщиков
                {
                    "insurance_base_amount": float,     # Страховая сумма
                    "object_type": "str",               # Тип объекта
                    "payments": [                       # Платежи
                        {
                            "insurance_sum": float,     # Страховая сумма
                            "months_in_period": int,    # Количество месяцев в периоде
                            "period": int,              # Период
                            "premium_sum": float,       # Страховая премия
                            "tariff": float,            # Тариф
                        },
                    ]
                },
            ],
            "premium_sum": float,       # Страховая премия
            "risk_type": str,           # Тип риска
            "underwriter_status": str,  # Статус андеррайтинга по риску
        },
    ],
    "sign_date": str,                   # Дата оформления, формат YYYY-MM-DD HH:MM:SS
    "underwriter_status": str,          # Статус андеррайтинга по котировке
    "underwriting_сomments": [          # Комментарии андеррайтеров
        {
            "date": str,                # Дата комментрация, формат YYYY-MM-DD HH:MM:SS
            "message": str,             # Комментарий
            "username": str,            # Имя пользователя
        },
    ]
}
```
# get_group_contract
[Наверх](#методы)
### Получение данных по группе договоров ипотечного страхования
#### Принимает:
```python
{
    "group_id": str,    # Универсальный идентификатор группы договоров
}
```
#### Успешный ответ:
```
то же самое, что и get_contract, только возвращается массив
```
# printforms
[Наверх](#методы)
### Получение списка доступных печатных форм для договора
#### Принимает:
```python
{
    "ipoteka_uuid": str,    # Универсальный идентификатор договора страхования ипотеки
}
```
#### Успешный ответ:
```python
[
    {
        "form_id": str,     # Идентификатор печатной формы
        "form_name": str,   # Название печатной формы
    },
]
```
# get_printform
[Наверх](#методы)
### Получение печатной формы
#### Принимает:
```python
{
    "ipoteka_uuid": str,    # Универсальный идентификатор договора страхования ипотеки
    "form_id": str,         # Идентификатор печатной формы
}
```
#### Успешный ответ:
```python
str($byte)                  # Байтовый массив содержащий документ
```
# payment
[Наверх](#методы)
### Регистрация заказа на оплату
### Вначале нужно вызвать 'create_contract'
#### Принимает:
```python
{
    "ipoteka_uuid": str,        # *Универсальный идентификатор договора страхования ипотеки
    "bill_enabled": bool,       # Признак оплаты по счету, по умолчанию False
    "statement_file_Id": int,   # id вложенного заявления. Если на расчете declaration = False
    "contacts": {               # *Контакты клиента
        "email": str,           # Адрес электронной почты для отправки ссылки на оплату договора
        "phone": str,           # *Номер телефона для отправки ссылки на оплату договора
    },
}
```
#### Успешный ответ:
```python
{
    "ipoteka_uuid": str,        # *Универсальный идентификатор договора страхования ипотеки
}
```
# files
[Наверх](#методы)
### Получение списка вложенных файлов
#### Принимает:
```python
{
    "ipoteka_uuid": str,        # *Универсальный идентификатор договора страхования ипотеки
}
```
#### Успешный ответ:
```python
[
  {
    "createTime": str,  # Дата добавления, формат YYYY-MM-DDTHH:MM:SS.SSSZ
    "id": int,          # Идентификатор загруженного файла
    "modifyTime": str,  # Дата изменения, формат YYYY-MM-DDTHH:MM:SS.SSSZ
    "name": str,        # Наименование загруженного файла
    "type": str,        # Тип загруженного документа
  },
]
```
# up_files
[Наверх](#методы)
### Загрузка сопроводительных документов к договору страхования ипотеки
#### Принимает:
```python
{
    "ipoteka_uuid": str,    # *Универсальный идентификатор договора страхования ипотеки
    "type": str,            # *Тип документа
    "file": file,           # *Сам файл
}
```
#### Успешный ответ:
```python
[
    {
        "createTime": str,  # Дата добавления, формат YYYY-MM-DDTHH:MM:SS.SSSZ
        "id": int,          # Идентификатор загруженного файла
        "modifyTime": str,  # Дата изменения, формат YYYY-MM-DDTHH:MM:SS.SSSZ
        "name": str,        # Наименование загруженного файла
    },
]
```
# get_file
[Наверх](#методы)
### Получение вложенного файла к договору страхования ипотеки
#### Принимает:
```python
{ 
    "ipoteka_uuid": str,    # Универсальный идентификатор договора страхования ипотеки
    "file_id": str,         # Идентификатор загруженного файла
}
```
#### Успешный ответ:
```python
str($byte)                  # Байтовый массив содержащий документ
```
# under_docs_info
[Наверх](#методы)
### Получение списка требуемых документов, необходимых для оформления договора страхования ипотеки
#### Принимает:
```python
{
    "ipoteka_uuid": str,    # Универсальный идентификатор договора страхования ипотеки
}
```
#### Успешный ответ:
```python
[
    {
        "code": str,        # Тип документа
        "description": str, # Текстовое описание
        "loaded": bool,     # Признак того, что документ уже загружен
    },
]
```
# to_underwriter
[Наверх](#методы)
### Отправка на андеррайтинг
#### Принимает:
```python
{
    "ipoteka_uuid": str,    # Универсальный идентификатор договора страхования ипотеки
    "message": str,         # Комментарий 
}
```
#### Успешный ответ:
```python
{
    "risks": [                          # Список рисков
        {
            "riskType": str,            # Тип риска
            "underwriterStatus": str,   # Статус андеррайтинга
        },
    ],
    "underwriterStatus": str,           # Статус андеррайтинга
    "underwritingComments": [           # Комментарии по андеррайтингу
        {
            "date": str,                # Дата и время комментария, формат DD-MM-YYYY HH:MM:SS
            "message": str,             # Комментарий
        },
    ],
}
```
# dictionary
[Наверх](#методы)
### Справочники
#### Принимает:
```python
{
    "type": str,        # тип справочника
}
```
#### Успешный ответ:
```python
{
    "values": [         # массив строк
        str,				
    ],
}
```
# landing_offer
[Наверх](#методы)
### Получение ссылки на страницу лендинка
### Требуется доп.согласование куратора
#### Принимает:
```python
{
    "ipoteka_uuid": str,    # Универсальный идентификатор котировки ипотечного договора
    "bill_enabled": bool,   # Признак оплаты по счету
    "token": str,           # Токен для получения ссылки на страницу лендинга
}
```
#### Успешный ответ:
```python
{
    "url": str,             # Ссылки на страницу лендинга
}
```
# Доступные справочники
|Значение|Описание|
|-|-|
|profession|Профессия|
|health|Состояние здоровья|
|sport|Спорт|
|restriction_property_rights|Ограничения на права собственности|
|confirmation_document|Документ, подтверждающий права собственности|
|category|Категория земель|
|building_type|Тип строения|
# Перечень возможных статусов договора
|Значение|Описание|Примечание|
|-|-|-|
|CONTRACT_NEW|Договор.Новый|Договор успешно посчитан|
|CONTRACT_SIGNED|Договор.Оформленный|Договор оформлен (сохранен)|
|CONTRACT_PAYED|Договор.Оплачен картой|Договор оплачен|
|CONTRACT_CANCELED|Договор.Аннулирован|Договор аннулирован|
# Перечень возможных статусов андеррайтинга
|Значение|Описание|Примечание|
|-|-|-|
|NO_NEED|Не требуется андеррайтинг|Андеррайтинг по риску/договору не требуется|
|NEED|Требуется андеррайтинг|По риску/договору требуется андеррайтинг|
|IN_PROGRESS|На согласовании|Риск/договор находится на рассмотрении у андеррайтера|
|ACCEPTED|Согласован|Риск/договор согласован андеррайтером|
|DECLINED|Отклонен|Риск/договор отклонен андеррайтером|
# Типы рисков к страхованию
|Значение|Описание|
|-|-|
|LIFE|Жизнь|
|PROPERTY|Имущество|
|TITLE|Титул|
# Пол
|Значение|Описание|
|-|-|
|MALE|Мужской|
|FEMALE|Женский|
# Тип объекта страхования
|Значение|Описание|
|-|-|
|HOUSE|Дом|
|FLAT|Квартира|
|ROOM|Комната|
|STEAD|Дача|
|APARTMENTS|Апартаменты|
