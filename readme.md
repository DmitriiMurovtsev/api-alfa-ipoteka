# В каждом методе
### 1. Метод запроса POST
### 2. Content-Type: Application/json (кроме “up_files”, там multipart/form-data)
### 3. Не успешный ответ: 
```
{
    "info": string,             # Сообщение об ошибке
    "session_id":string,        # session_id или None
    "sub_errors": [			
        {
            "message": string,  # Подробное сообщение об ошибке
        },
    ],
    "timestamp": string,        # Время ошибки в формате DD-MM-YYYY HH:MM:SS
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
```
{
    "agent": {                          # Агентский блок
        "agent_contract_id": integer,   # *Идентификатор агентского договора
        "department_id": integer,       # *Идентификатор подразделения продавца
    },
    "insuranceCity": {                  # *Регион / Город объекта страхования
        "fiasId": string,               # *Код ФИАС с детализацией до Города (4-й уровень)
    },
    "insurance_objects": [              # *Объекты страхования. Возможно до 2-х объектов
        {
            "type": string,             # *Тип объекта
        }
    ],
    "insurer": {                        # *Заемщик
        "birth_date": string,           # *Дата рождения, формат YYYY-MM-DD
        "sex": string,                  # *Пол, возможны MALE, FEMALE
    },
    "mortgage_agreement": {             # *Данные по кредиту
        "amount": float,                # *Сумма кредита		
        "bank": {                       # Данные банка из справочника
            "bic": string,              # *БИК банка
            "name": string,             # Наименование банка
        },
        "rate": float,                  # *Процентная ставка, например 8.9
        "date": string,                 # Дата кредитного договора, формат YYYY-MM-DD
    }
}
```
#### Успешный ответ:
```
{
    "insurance_program": string,        # Программа страхования
    "insurance_sum": float,             # Страховая сумма
    "premium_sum": float,               # Страховая премия общая
    "risks": [                          # Список рисков, до трех
        {
            "insurance_sum": float,     # Страховая сумма
            "premium_sum": float,       # Страховая премия
            "risk_type": string,        # Тип риска, возможны LIFE, PROPERTY, TITLE
        }’
    ],
}
```

# calculation
[Наверх](#методы)
### Расчет котировки Ипотеки
#### Принимает:
```
{
    "agent": {                          # Агентский блок
        "agent_contract_id": integer,   # *Идентификатор агентского договора
        "channel_sale_id": integer,     # *Идентификатор канала продаж
        "department_id": integer,       # *Идентификатор подразделения продавца
        "manager_id": integer,          # *Идентификатор менеджера по договору
        "signer_id": integer,           # *Идентификатор лица подписавшего договор
    },
    "agent_email": string,              # *E-mail агента для ответов андеррайтеров
    "insuranceCity": {                  # *Регион / Город объекта страхования
        "fiasId": string,               # *Код ФИАС с детализацией до Города (4-й уровень)
    },
    "begin_date": string,               # *Дата начала действия, формат YYYY-MM-DD
    "co_insurers": [                    # Блок созаемщики. Возможно наличие до 3-х созаемщиков
        {
            "birth_date": string,       # Дата рождения, формат YYYY-MM-DD
            "email": string,            # Email
            "fact_address": {           # Фактический адрес проживания
                "fias_id": string,      # Код ФИАС
                "text": string,         # Адрес одной строкой
            },
            "first_name": string,       # Имя
            "last_name": string,        # Фамилия
            "life_risk": {              # Блок данных по риску LIFE
                "health": string,           # Категория здоровья согласно справочника
                "profession": string,       # Категория профессии согласно справочника
                "seller_discount": string,  # Коэффициент агента
                "share": float,             # Доля. По дефолту передавать 100
                "sport": string,            # Категория спорта согласно справочника
            },
            "middle_name": string,          # Отчество
            "passport": {                   # Данные паспорта
                "issue_unit_code": string,  # Код подразделения
                "issue_date": string,       # Дата выдачи паспорта, формат YYYY-MM-DD
                "issue_place": string,      # Место выдачи паспорта
                "number": string,           # Номер паспорта
                "reg_address": {            # Адрес проживания по месту регистрации
                    "fias_id": string,      # Код ФИАС
                    "text": string,         # Адрес одной строкой
                },
                "series": string,           # Серия паспорта
            },
            "phone_number": string,         # Номер телефона
            "resident": boolean,            # Гражданство РФ
            "sex": string,                  # *Пол, возможны MALE, FEMALE
            "snils": string,                # СНИЛС
        },
    ],
    "end_date": string,                     # *Дата окончания действия, формат YYYY-MM-DD
    "insurance_objects": [                  # *Объекты страхования. Возможно до 2-х объектов
        {
            "address": {                    # Адрес объекта
                "fias_id": string,          # Код ФИАС
                "text": string,             # Адрес одной строкой
            },
            "name": string,                 # Наименование объекта
            "primary_sale": boolean,        # Признак первичной недвижимости
            "property_risk": {              # Риски недвижимости
                "address": string,              # Адрес
                "construction_year": integer,   # Год постройки
                "flammable": boolean,           # Признак наличия огнеопасных материалов
                "kad_number": string,           # Кадастровый номер
                "land_category": string,        # Категория земель
                "market_price": float,          # Рыночная стоимость
                "property_area": float,         # Площадь
                "renovation_work": boolean,     # Признак наличия ремонтных работ на данный момент
                "seller_discount": string,      # Коэффициент продавца
                "swimming_pool": boolean,           # Признак наличия бассейна
                "total_renovation_work": boolean,   # Признак наличия капитальный ремонтных работ
            },
            "title_risk": {                         # Риски страхования TITLE
                "address": string,                  # Адрес
                "age_owner": boolean,               # Наличие собственников младше 18 и старше 65 лет
                "insurance_base_amount": float,     # Рыночная стоимость
                "juridical_owner": boolean,         # Признак наличия юридических лиц в собственниках
                "kad_number": string,               # Кадастровый номер
                "land_category": string,            # Категория земель
                "one_time_payment": boolean,        # Признак единовременной оплаты
                "ownership_confirmation": string,       # Документ, подтверждающий право собственности
                "ownership_less_three_years": boolean,  # Наличие в собственности меньше 3 лет
                "ownership_restriction": string,        # Ограничения на права собственности
                "procuratory_agreement": boolean,       # Проведение сделки по доверенности
                "seller_discount": string,              # Коэффициент продавца
                "spouse_approval": boolean,             # Признак отсутствия согласия супруга/супруги
                "term_in_month": integer,               # Срок страхования в месяцах
            },
            "type": string,                             # Тип объекта
        },
    ],
    "insurance_program": string,            # *Программа страхования согласно справочника
    "insurer": {                            # *Заемщик
        "birth_date": string,               # Дата рождения, формат YYYY-MM-DD
        "email": string,                    # Email
        "fact_address": {                   # Фактический адрес проживания
            "fias_id": string,              # Код ФИАС
            "text": string,                 # Адрес одной строкой
        },
        "first_name": string,               # Имя
        "last_name": string,                # Фамилия
        "life_risk": {                      # Блок данных по риску LIFE
            "health": string,               # Категория здоровья согласно справочника
            "profession": string,           # Категория профессии согласно справочника
            "seller_discount": string,      # Коэффициент агента	
            "share": float,                 # Доля. По дефолту передавать 100
            "sport": string,                # Категория спорта согласно справочника
        },
        "middle_name": string,              # Отчество
        "passport": {                       # Данные паспорта
            "issue_unit_code": string,      # Код подразделения
            "issue_date": string,           # Дата выдачи паспорта, формат YYYY-MM-DD
            "issue_place": string,          # Место выдачи паспорта
            "number": string,               # Номер паспорта
            "reg_address": {                # Адрес проживания по месту регистрации
                "fias_id": string,          # Код ФИАС
                "text": string,             # Адрес одной строкой
            },
            "series": string,               # Серия паспорта
        },
        "phone_number": string,             # Номер телефона
        "resident": boolean,                # Гражданство РФ
        "sex": string,                      # *Пол
        "snils": string,                    # СНИЛС
    },
    "mortgage_agreement": {                 # *Данные кредита
        "amount": float,                    # Сумма кредита
        "bank": {                           # Данные банка
            "bic": string,                  # БИК банка
            "name": string,                 # Наименование банка
        },
        "city": string,                     # Город выдачи кредита
        "date": string,                     # *Дата кредитного договора, формат YYYY-MM-DD
        "number": string,                   # Номер кредитного договора
        "rate": float,                      # Процентная ставка, например 8.9
        "term_in_month": integer,           # Срок страхования в месяцах
    },
    "prev_insurance_company": string,       # Наименование предыдущей страховой компании
    "previous_number": string,              # Предыдущий номер договора (для пролонгации)
    "risk_types": [                         # *Типы рисков к страхованию
        "LIFE",				
    ],
    "sign_date": string,                    # *Дата оформления, формат YYYY-MM-DD
    "kv_discount": float,                   # Коэффициент скидки за счёт КВ, например 0.9
}
```
#### Успешный ответ:
```
{
    "begin_date": string,               # *Дата начала действия, формат YYYY-MM-DD
    "declaration": boolean,             # Признак декларации
    "end_date": string,                 # *Дата окончания действия, формат YYYY-MM-DD
    "insurance_program": string,        # Программа страхования
    "insurance_sum": float,             # Страховая сумма
    "ipoteka_uuid": string,             # Универсальный идентификатор договора страхования ипотеки
    "group_id": integer,                # Идентификатор группы связанных договоров
    "no_paper_offer_sent": boolean,     # Признак успешной отправки предложения ББ
    "number": string,                   # Номер договора
    "offer": boolean,                   # Признак оферты
    "premium_sum": float,               # Сумма премии
    "prev_insurance_company": string,   # Наименование предыдущей страховой компании
    "previous_number": string,          # Предыдущий номер договора
    "risks": [                          # Информация по рискам
        {
            "insurance_sum": float,     # Страховая сумма
            "objects": [                # Список объектов / заёмщиков
                {
                    "insurance_base_amount": float,     # Страховая сумма
                    "payments": [                       # Платежи
                        {
                            "insurance_sun": float,     # Страховая сумма
                            "month_in_period": integer, # Количество месяцев в периоде
                            "period": integer,          # Период
                            "premiumSum": float,        # Сумма премии
                            "tariff": float,            # Тариф
                        },
                    ],  
                "type": string,                         # Тип объекта
                },
            ],
            "premium_sum": float,       # Сумма премии
            "risk_type": string,        # Тип риска
        },
    ],
    "sign_date": string,                # *Дата оформления, формат YYYY-MM-DD
}
```
# create_contract
[Наверх](#методы)
### Загрузка договора ипотеки в КИС
### Присваивается номер полиса
#### Принимает:
```
{
  "ipoteka_uuid": string,   # Универсальный идентификатор договора страхования ипотеки
}
```
#### Успешный ответ:
```
{
  "begin_date": string,         # Дата начала действия полиса, формат 
  "contract_number": string,    # Номер договора страхования ипотеки
  "end_date": string,           # Дата окончания действия полиса
  "insurance_amount": float,    # Страховая сумма
  "ipoteka_uuid": string,       # Универсальный идентификатор договора страхования ипотеки
  "premium_amount": float,      # Сумма страховой премии
  "group_id": integer,          # Идентификатор группы связанных договоров
}
```
# get_contract
[Наверх](#методы)
### Получение информации по договору
#### Принимает:
```
{
    "ipoteka_uuid": string,     # Универсальный идентификатор договора страхования ипотеки
}
```
#### Успешный ответ:
```
{
    "agent": {                              # Информация по агенту
        "agent_contract_number": string,    # Номер агентского договора
        "agent_sale_code": string,          # Наименование канала продаж
        "department_code": string,          # Код подразделения продавца
        "email": string,                    # Адрес электронной почты для связи с андеррайтерами
        "manager_name": string,             # Код подразделения продавца
        "signer_name": string,              # Лицо, подписавшее договор со стороны СК
    },
    "begin_date": string,                   # Дата начала действия договора, формат YYYY-MM-DD HH:MM:SS
    "co_insurers": [                        # Блок с данными о созаемщиках
        {
            "birth_date": string,           # Дата рождения, формат YYYY-MM-DD
            "email": string,                # email
            "fact_address": {               # Данные фактического адреса
            "fias_id": string,              # Код ФИАС
            "text": string                  # Полный адрес
        },
        "first_name": string,               # Имя
        "last_name": string,                # Фамилия
        "life_risk": {                      # Данные о риске по жизни
            "health": string,               # Категория здоровья согласно справочника
            "profession": string,           # Категория профессии согласно справочника
            "seller_discount": float,       # Коэффициент агента
            "share": float,                 # Доля
            "sport": string,                # Категория спорта согласно справочника
        },
        "middle_name": string,              # Отчество
        "passport": {                       # Данные о паспорте
            "issue_code": string,           # Код подразделения
            "issue_date": string,           # Дата выдачи паспорта, формат YYYY-MM-DD
            "issue_place": string,          # Кем выдан
            "number": string,               # Номер паспорта
            "reg_address": {                # Данные адреса регистрации
                "fias_id": string,          # Код ФИАС
                "text": string,             # Полный адрес
            },
            "series": string,               # Серия паспорта
        },
        "phone_number": string,             # Номер телефона
        "resident": boolean,                # Резидент РФ
        "sex": string,                      # Пол
        "snils": string,                    # СНИЛС
        },
    ],
    "contract_status": string,              # Статус договора
    "contract_type": string,                # Тип договора, возможны PRIMARY, PROLONGATION
    "create_date": string,                  # Дата создания договора, формат YYYY-MM-DD
    "declaration": boolean,                 # Признак декларации
    "end_date": string,                     # Дата окончания действия договора YYYY-MM-DD
    "errors": [                             # Блок ошибок по котировке
        {
            "message": string,              # Сообщение по ошибке
        },
    ],
    "group_id": integer,                    # Идентификатор группы связанных договоров
    "insuranceCity": {                      # Регион / Город объекта страхования
        "fias_id": string,                  # Код ФИАС
    },
    "insurance_objects": [                  # Блок с данными об объекте страхования
        {
            "address": {                    # Данные адреса
                "fias_id": string,          # Код ФИАС
                "text": string,             # Полный адрес
            },
            "name": string,                         # Наименование объекта
            "primary_sale": boolean,                # Признак первичной недвижимости
            "property_risk": {                      # Данные о параметрах риска недвижимости
                "address": string,                  # Полный адрес объекта страхования
                "construction_year": integer,       # Год постройки объекта
                "flammable": boolean,               # Материал стен и перекрытий из горючих материалов
                "kad_number": string,               # Кадастровый номер объекта
                "land_category": string,            # Категория земли из справочника
                "market_price": float,              # Рыночная стоимость объекта
                "property_area":float,              # Площадь объекта
                "renovation_work": boolean,         # Признак наличия ремонтных работ на данный момент
                "seller_discount": float,           # Коэффициент агента
                "swimming_pool": boolean,           # Наличие бассейна/сауны/джакузи/камина/печи
                "total_renovation_work": boolean,   # Признак наличия капитальных ремонтных работ/перепланировки
            },    
            "title_risk": {                         # Данные о параметрах риска TITLE
                "address": string,                  # Полный адрес объекта страхования
                "age_owner": boolean,               # Собственник младше 18 и старше 65 лет
                "insurance_base_amount": float,     # Рыночная стоимость
                "juridical_owner": boolean,         # Признак наличия юридических лиц в собственниках
                "kad_number": string,               # Кадастровый номер объекта
                "land_category": string,            # Категория земли из справочника
                "one_time_payment": boolean,        # Признак единовременной оплаты
                "ownership_confirmation": string,       # Документ, подтверждающий право собственности
                "ownership_less_three_years": boolean,  # Наличие в собственности меньше 3 лет
                "ownership_restriction": string,        # Ограничения на права собственности
                "procuratory_agreement": boolean,       # Признак проведения сделки по доверенности
                "seller_discount": float,               # Коэффициент агента
                "spouse_approval": boolean,             # Признак отсутствия согласия супруга/супруги
                "term_in_month": integer,               # Срок страхования в месяцах
            },
            "type": string,                             # Тип объекта
        },
    ],
    "insurance_program": string,        # Программа страхования
    "insurance_sum": float,             # Страховая сумма
    "insurer": {                        # Данные о заемщике
        "birth_date": string,           # Дата рождения, формат YYYY-MM-DD
        "email": string,                # Email
        "fact_address": {               # Данные фактического адреса
            "fias_id": string,          # Код ФИАС
            "text": string,             # Полный адрес
        },
        "first_name": string,           # Имя
        "last_name": string,            # Фамилия
        "life_risk": {                  # Данные о риске по жизни
            "health": string,           # Категория здоровья согласно справочника
            "profession": string,       # Категория профессии согласно справочника
            "seller_discount": float    # Коэффициент агента
            "share": float,             # Доля
            "sport": string,            # Категория спорта согласно справочника
        },
        "middle_name": string,          # Отчество
        "passport": {                   # Данные о паспорте
            "issue_code": string,       # Код подразделения
            "issue_date": string,       # Дата выдачи паспорта	
            "issue_place": string,      # Кем выдан
            "number": string,           # Номер паспорта
            "reg_address": {            # Данные адреса регистрации
                "fias_id": string,      # Код ФИАС
                "text": string,         # Полный адрес
            },
            "series": string,           # Серия паспорта
        },
        "phone_number": string,         # Номер телефона
        "resident": boolean,            # Резидент РФ
        "sex": string,                  # Пол
        "snils": string,                # СНИЛС
    },
    "ipoteka_uuid": string,             # Универсальный идентификатор договора страхования ипотеки
    "kv_discount": integer,
    "mortgage_agreement": {             # Данные по кредиту
        "amount": float,                # Сумма кредита
        "bank.bic": string,             # Бик банка
        "bank.name": string,            # Наименование банка
        "city": string,                 # Город выдачи кредита
        "date": string,                 # Дата кредитного договора
        "number": string,               # Номер кредитного договора
        "rate": float,                  # Процентная ставка
        "term_in_month": integer,       # Оставшийся срок кредита в месяцах
    },
    "no_paper": boolean,                # Признак ББ
    "number": string,                   # Номер договора
    "offer": boolean,                   # Признак оферты
    "premium_sum": float,               # Сумма премии
    "prev_insurance_company": string,   # Наименование предыдущей страховой компании
    "previous_number": string,          # Предыдущий номер договора (для пролонгации)
    "risk_types": [                     # Типы рисков к страхованию
        string,			
    ],
    "risks": [                          # Риски по договору
        {
            "insurance_sum": float,     # Страховая сумма
            "objects": [                # Список объектов/заёмщиков
                {
                    "insurance_base_amount": float,         # Страховая сумма
                    "object_type": "string",                # Тип объекта
                    "payments": [                           # Платежи
                        {
                            "insurance_sum": float,         # Страховая сумма
                            "months_in_period": integer,    # Количество месяцев в периоде
                            "period": integer,              # Период
                            "premium_sum": float,           # Страховая премия
                            "tariff": float,                # Тариф
                        },
                    ]
                },
            ],
            "premium_sum": float,           # Страховая премия
            "risk_type": string,            # Тип риска
            "underwriter_status": string,   # Статус андеррайтинга по риску
        },
    ],
    "sign_date": string,                    # Дата оформления, формат YYYY-MM-DD HH:MM:SS
    "underwriter_status": string,           # Статус андеррайтинга по котировке
    "underwriting_сomments": [              # Комментарии андеррайтеров
        {
            "date": string,                 # Дата комментрация, формат YYYY-MM-DD HH:MM:SS
            "message": string,              # Комментарий
            "username": string,             # Имя пользователя
        },
    ]
}
```
# get_group_contract
[Наверх](#методы)
### Получение данных по группе договоров ипотечного страхования
#### Принимает:
```
{
    "group_id": string,     # Универсальный идентификатор группы договоров
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
```
{
    "ipoteka_uuid": string,     # Универсальный идентификатор договора страхования ипотеки
}
```
#### Успешный ответ:
```
[
    {
        "form_id": string,      # Идентификатор печатной формы
        "form_name": string,    # Название печатной формы
    },
]
```
# get_printform
[Наверх](#методы)
### Получение печатной формы
#### Принимает:
```
{
    "ipoteka_uuid": string,     # Универсальный идентификатор договора страхования ипотеки
    "form_id": string,          # Идентификатор печатной формы
}
```
#### Успешный ответ:
```
string($byte)                   # Байтовый массив содержащий документ
```
# payment
[Наверх](#методы)
### Регистрация заказа на оплату
### Вначале нужно вызвать 'create_contract'
#### Принимает:
```
{
    "ipoteka_uuid": string,         # *Универсальный идентификатор договора страхования ипотеки
    "bill_enabled": boolean,        # Признак оплаты по счету, по умолчанию False
    "statement_file_Id": integer,   # id вложенного заявления. Если на расчете declaration = False
    "contacts": {                   # *Контакты клиента
        "email": string,            # Адрес электронной почты для отправки ссылки на оплату договора
        "phone": string,            # *Номер телефона для отправки ссылки на оплату договора
    },
}
```
#### Успешный ответ:
```
{
    "ipoteka_uuid": string,     # *Универсальный идентификатор договора страхования ипотеки
}
```
# files
[Наверх](#методы)
### Получение списка вложенных файлов
#### Принимает:
```
{
    "ipoteka_uuid": string,     # *Универсальный идентификатор договора страхования ипотеки
}
```
#### Успешный ответ:
```
[
  {
    "createTime": string,       # Дата добавления, формат YYYY-MM-DDTHH:MM:SS.SSSZ
    "id": integer,              # Идентификатор загруженного файла
    "modifyTime": string,       # Дата изменения, формат YYYY-MM-DDTHH:MM:SS.SSSZ
    "name": string,             # Наименование загруженного файла
    "type": string,             # Тип загруженного документа
  },
]
```
# up_files
[Наверх](#методы)
### Загрузка сопроводительных документов к договору страхования ипотеки
#### Принимает:
```
{
    "ipoteka_uuid": string,     # *Универсальный идентификатор договора страхования ипотеки
    "type": string,             # *Тип документа
    "file": file,               # *Сам файл
}
```
#### Успешный ответ:
```
```
# get_file
[Наверх](#методы)
### Получение вложенного файла к договору страхования ипотеки
#### Принимает:
```
{ 
    "ipoteka_uuid": string,     # Универсальный идентификатор договора страхования ипотеки
    "file_id": string,          # Идентификатор загруженного файла
}
```
#### Успешный ответ:
```
string($byte)                   # Байтовый массив содержащий документ
```
# under_docs_info
[Наверх](#методы)
### Получение списка требуемых документов, необходимых для оформления договора страхования ипотеки
#### Принимает:
```
{
    "ipoteka_uuid": string,     # Универсальный идентификатор договора страхования ипотеки
}
```
#### Успешный ответ:
```
[
    {
        "code": string,         # Тип документа
        "description": string,  # Текстовое описание
        "loaded": boolean,      # Признак того, что документ уже загружен
    },
]
```
# to_underwriter
[Наверх](#методы)
### Отправка на андеррайтинг
#### Принимает:
```
{
    "ipoteka_uuid": string,     # Универсальный идентификатор договора страхования ипотеки
    "message": string,          # Комментарий 
}
```
#### Успешный ответ:
```
{
    "risks": [                              # Список рисков
        {
            "riskType": string,             # Тип риска
            "underwriterStatus": string,    # Статус андеррайтинга
        },
    ],
    "underwriterStatus": string,            # Статус андеррайтинга
    "underwritingComments": [               # Комментарии по андеррайтингу
        {
            "date": string,                 # Дата и время комментария, формат DD-MM-YYYY HH:MM:SS
            "message": string,              # Комментарий
        },
    ],
}
```
# dictionary
[Наверх](#методы)
### Справочники
#### Принимает:
```
{
    "type": string,     # тип справочника
}
```
#### Успешный ответ:
```
{
    "values": [         # массив строк
        string,				
    ],
}
```
# landing_offer
[Наверх](#методы)
### Получение ссылки на страницу лендинка
### Требуется доп.согласование куратора
#### Принимает:
```
{
    "ipoteka_uuid": string,     # Универсальный идентификатор котировки ипотечного договора
    "bill_enabled": boolean,    # Признак оплаты по счету
    "token": string,            # Токен для получения ссылки на страницу лендинга
}
```
#### Успешный ответ:
```
{
    "url": "string",            # Ссылки на страницу лендинга
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
