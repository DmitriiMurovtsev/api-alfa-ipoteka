from typing import Optional, List
from enum import Enum
from datetime import datetime
import re

from pydantic import BaseModel, Field, field_validator


# Логин Пароль
class Auth(BaseModel):
    login: str
    password: str


# Тип объекта страхования
class TypeObjEnum(str, Enum):
    HOUSE = "HOUSE"
    FLAT = "FLAT"
    ROOM = "ROOM"
    STEAD = "STEAD"
    APARTMENTS = "APARTMENTS"
    

# Тип справочника
class TypeDictionaryEnum(str, Enum):
    profession = "profession"
    health = "health"
    sport = "sport"
    restriction_property_rights = "restriction_property_rights"
    confirmation_document = "confirmation_document"
    category = "category"
    bank_programs = "bank-programs"
    building_type = "building_type"


# Типы рисков в страховании
class RiskTypes(str, Enum):
    LIFE = "LIFE"
    PROPERTY = "PROPERTY"
    TITLE = "TITLE"


# Пол
class SexEnum(str, Enum):
    MALE = "MALE"
    FEMALE  = "FEMALE"


# Агентский блок неполный
class Agent(BaseModel):
    agent_contract_id: int
    department_id: int    


# Агентский блок полный
class AgentFull(Agent):
    channel_sale_id: int
    manager_id: int
    signer_id: int
    

# Блок данных Адрес неполный
class Address(BaseModel):
    fiasId: str
    
    
# Блок данных Адрес полный
class AddressFull(BaseModel):
    fias_id: Optional[str] = None
    text: str
    
    
# Объект страхования неполный
class InsuranceObject(BaseModel):
    type: TypeObjEnum
    

# Блок данных по банку
class Bank(BaseModel):
    bic: str = Field(min_length=9, max_length=9, pattern=r'^[0-9]+$')
    name: Optional[str] = None
    

# Блок данных по кредиту неполные
class MortgageAgreement(BaseModel):
    amount: float
    bank: Bank
    rate: float
    date: Optional[str] = None
    
    @field_validator('date')
    def check_date_format(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
        
        except ValueError:
            raise ValueError("Неверный формат даты. Используйте YYYY-DD-MM")
        
        return v
    

# Блок данных по кредиту полные
class MortgageAgreementFull(BaseModel):
    amount: Optional[float] = None
    bank: Optional[Bank] = None
    city: Optional[str] = None
    date: str
    number: Optional[str] = None
    rate: Optional[float] = None
    term_in_month: Optional[int] = None
    
    @field_validator('date')
    def check_date_format(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
        
        except ValueError:
            raise ValueError("Неверный формат даты. Используйте YYYY-DD-MM")
        
        return v    
    

# Блок данных по риску LIFE
class LifeRisk(BaseModel):
    health: Optional[str] = None
    profession: Optional[str] = None
    seller_discount: Optional[str] = None
    share: Optional[float] = 100.00
    sport: Optional[str] = None
    

# Блок данных по риску PROPERTY
class PropertyRisk(BaseModel):
    address: Optional[str] = None
    construction_year: int
    flammable: bool
    kad_number: Optional[str] = None
    land_category: Optional[str] = None
    market_price: Optional[float] = None
    property_area: float
    renovation_work: bool
    seller_discount: Optional[str] = None
    swimming_pool: Optional[bool] = None
    total_renovation_work: bool


# Блок данных по риску TITLE
class TitleRisk(BaseModel):
    address: Optional[str] = None
    age_owner: Optional[bool] = None
    insurance_base_amount: Optional[float] = None
    juridical_owner: Optional[bool] = None
    kad_number: Optional[str] = None
    land_category: Optional[str] = None
    one_time_payment: Optional[bool] = None
    ownership_confirmation: Optional[str] = None
    ownership_less_three_years: Optional[bool] = None
    ownership_restriction: Optional[str] = None
    procuratory_agreement: Optional[bool] = None
    seller_discount: Optional[str] = None
    spouse_approval: Optional[bool] = None
    term_in_month: Optional[int] = None
    

# Данные паспорта
class Passport(BaseModel):
    issue_unit_code: Optional[str] = None
    issue_date: Optional[str] = None
    issue_place: Optional[str] = None
    number: Optional[str] = Field(None, min_length=6, max_length=6, pattern=r'^[0-9]+$')
    reg_address: Optional[AddressFull] = None
    series: Optional[str] = Field(None, min_length=4, max_length=4, pattern=r'^[0-9]+$')
    
    @field_validator('issue_date')
    def check_issue_date_format(cls, v):
        
        try:
            datetime.strptime(v, "%Y-%m-%d")
        
        except ValueError:
            raise ValueError("Неверный формат даты. Используйте YYYY-DD-MM")
        
        return v
    
    @field_validator('issue_unit_code')
    def check_issue_unit_code_format(cls, v: str) -> str:
        pattern = re.compile(r'\d{3}\-\d{3}$')
        if not pattern.match(v):
            raise ValueError('Неверный формат кода подразделения. Используйте формат XXX-XXX без пробелов.')
        
        return v     


# Блок данных заемщика неполный
class Insurer(BaseModel):
    birth_date: str
    sex: SexEnum
    
    @field_validator('birth_date')
    def check_birth_date_format(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
            
        except ValueError:
            raise ValueError("Неверный формат даты. Используйте YYYY-DD-MM")
        
        return v


# Блок данных заемщика полный
class InsurerFull(Insurer):
    birth_date: Optional[str] = None
    email: Optional[str] = None
    fact_address: Optional[AddressFull] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    life_risk: Optional[LifeRisk] = None
    middle_name: Optional[str] = None
    passport: Optional[Passport] = None
    phone_number: Optional[str] = None
    resident: Optional[bool] = None
    sex: SexEnum
    snils: Optional[str] = None
    
    @field_validator('birth_date')
    def check_birth_date_format(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
            
        except ValueError:
            raise ValueError("Неверный формат даты. Используйте YYYY-DD-MM")
        
        return v
    
    @field_validator('email')
    def check_email_format(cls, v: str) -> str:
        pattern = re.compile(r'\S+@\S+\.\S+$')
        if not pattern.match(v):
            raise ValueError('Неверный формат email. Используйте формат X@X.X без пробелов')
        
        return v
    
    @field_validator('phone_number')
    def check_phone_format(cls, v: str) -> str:
        pattern = re.compile(r'\+7\d{10}$')
        if not pattern.match(v):
            raise ValueError('Неверный формат phone. Используйте формат +7XXXXXXXXXX без пробелов.')
        
        return v
    
    @field_validator('snils')
    def check_snils_format(cls, v: str) -> str:
        pattern = re.compile(r'\d{3}\-\d{3}\-\d{3} \d{2}$')
        if not pattern.match(v):
            raise ValueError('Неверный формат СНИЛС. Используйте формат XXX-XXX-XXX XX цифры без пробелов.')
        
        return v 
        

# Объект страхования полный
class InsuranceObjectFull(BaseModel):
    address: Optional[AddressFull] = None
    name: Optional[str] = None
    primary_sale: bool = None
    property_risk: PropertyRisk
    title_risk: Optional[TitleRisk] = None
    type: Optional[TypeObjEnum] = None
    

# Блок данных Контакты клиента
class Contacts(BaseModel):
    email: Optional[str] = None
    phone: str    
    
    @field_validator('email')
    def check_email_format(cls, v: str) -> str:
        pattern = re.compile(r'\S+@\S+\.\S+$')
        if not pattern.match(v):
            raise ValueError('Неверный формат email. Используйте формат X@X.X без пробелов')
        
        return v
    
    @field_validator('phone')
    def check_phone_format(cls, v: str) -> str:
        pattern = re.compile(r'\+7\d{10}$')
        if not pattern.match(v):
            raise ValueError('Неверный формат phone. Используйте формат +7XXXXXXXXXX без пробелов.')
        
        return v


# Валидатор для /estimation
class EstimationValidator(BaseModel):
    auth: Auth
    agent: Optional[Agent] = None
    insuranceCity: Address
    insurance_objects: List[InsuranceObject] = Field(max_length=2)
    insurer: Insurer
    mortgage_agreement: MortgageAgreement


# Валидатор для /calculation
class CalculationValidator(BaseModel):
    auth: Auth
    agent: Optional[AgentFull] = None
    agent_email: str
    insuranceCity: Address
    begin_date: str
    co_insurers: Optional[List[InsurerFull]] = None
    end_date: str
    insurance_objects: List[InsuranceObjectFull] = Field(max_length=2)
    insurance_program: str
    insurer: InsurerFull
    mortgage_agreement: MortgageAgreementFull
    prev_insurance_company: Optional[str] = None
    previous_number: Optional[str] = None
    risk_types: List[RiskTypes]
    sign_date: str
    kv_discount: Optional[float] = None
    
    @field_validator('begin_date', 'end_date', 'sign_date')
    def check_birth_date_format(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
            
        except ValueError:
            raise ValueError("Неверный формат даты. Используйте YYYY-DD-MM")
        
        return v
    
    @field_validator('agent_email')
    def check_email_format(cls, v: str) -> str:
        pattern = re.compile(r'\S+@\S+\.\S+$')
        if not pattern.match(v):
            raise ValueError('Неверный формат email. Используйте формат X@X.X без пробелов')
        
        return v    
        

# Валидатор для /create_contract
class CreateContractValidator(BaseModel):
    auth: Auth
    ipoteka_uuid: str
    

# Валидатор для /get_contract
class GetContractValidator(BaseModel):
    auth: Auth
    ipoteka_uuid: str
    
    
# Валидатор для /get_group_contract
class GetGroupContractValidator(BaseModel):
    auth: Auth
    group_id: int
    
    
# Валидатор для /printforms
class PrintformsValidator(BaseModel):
    auth: Auth
    ipoteka_uuid: str
    
    
# Валидатор для /get_printform
class GetPrintformsValidator(BaseModel):
    auth: Auth
    ipoteka_uuid: str
    form_id: str
    
    
# Валидатор для /payment
class PaymentValidator(BaseModel):
    auth: Auth
    ipoteka_uuid: str
    bill_enabled: Optional[bool] = None
    statement_file_Id: Optional[int] = None
    contacts: Contacts
    

# Валидатор для /files
class FilesValidator(BaseModel):
    auth: Auth
    ipoteka_uuid: str
    

# Валидатор для /up_files
class UpFilesValidator(BaseModel):
    auth: Auth
    ipoteka_uuid: str
    type: str
    

# Валидатор для /get_file
class GetFileValidator(BaseModel):
    auth: Auth
    ipoteka_uuid: str
    file_id: int
    
    
# Валидатор для /under_docs_info
class UnderDocsInfoValidator(BaseModel):
    auth: Auth
    ipoteka_uuid: str
    

# Валидатор для /to_underwriter
class ToUnderwriterValidator(BaseModel):
    ipoteka_uuid: str
    message: str = ''
    
    
# Валидатор для /dictionary
class DictionaryValidator(BaseModel):
    auth: Auth
    type: TypeDictionaryEnum
    

# Валидатор для /landing_offer
class LandingOfferValidator(BaseModel):
    auth: Auth
    ipoteka_uuid: str
    bill_enabled: bool = False
    token: str