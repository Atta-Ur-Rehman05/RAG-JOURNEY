# pydantic
# its help us to maintain a structure of the data for the chatbot output
# it provide types
# type checking
# data validation
# easy to use
# it let you control the farmat of input requests
# and also control the output farmat of chat bot
# schema 
# validation
#serlization 
# it use type annotation 




# type annotation
# type annotation is a way to specify the type of a variable and it solves the problem of type checking
# in python 
# we spacify the variable b/c AI can provide data in any format
# e.g: if AI provide "hello" it will store in string variable but if AI provide "10" it will store in integer variable 
# if we do not spacify the type of a variable it will store in any variable 
# we have to do type checking to make sure the data is in the correct format



# syntax 
# var_name : type = value 
# e.g x: int = 10 

# in pydantic we use BaseModel 
# class Person(BaseModel):
#     name: str
#     age: int
#     email: str
#     is_student: bool
#

# schema 
# schema is a way to specify the structure of the data
# e.g: 
# class Person(BaseModel):
#     name: str
#     age: int
#     email: str
#     is_student: bool
# 








from pydantic import BaseModel, ConfigDict, ValidationError, Field, AfterValidator, BeforeValidator, field_validator
from typing import Optional

class BasicUser(BaseModel):
    name: str
    email: str
    age: Optional[int] = None
    
class User(BasicUser):
    is_active: bool = True
    
class UserLogin(BaseModel):
    username: str
    password: str = Field(..., min_length=6, max_length=20)
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit")
        if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for char in password):
            raise ValueError("Password must contain at least one special character")
        return password
    
    model_config = ConfigDict(
        from_attributes=True
    )
    
    
# Password Requirements
# Length > 5 and < 20
# At least one uppercase letter
# At least one lowercase letter
# At least one digit
# At least one special character

# Type Annotation
a: int = 10
b: str = "Hello"
c: float = 73.32


def func(a: int , b: int) -> int:
    return a + b

func(1, 2)

def func2(a: str, b: str) -> str:
    pass
user = UserLogin(username="Alice", password="Password123!")
print(user.username)

user2 = {
    "username": "Bob",
    "password": "Password123!"
}

user2Obj = UserLogin(
    username=user2["username"],
    password=user2["password"]
)

user2Obj = UserLogin(**user2)
# print(user2.model_dump_json())

# try:
#     obj = User(name="Alice", email=244)
# except ValidationError as e:
#     print("Error")

# print(obj)


# Decoraotors
# Static methods Vs Class methods
# Gnerators
# Depcrycated
# **Kargs Vs *args

l1 = [True, False, False, False]
print(all(l1))

# Structured Output Prompt
#   - Support Tickets
#   - Input Support Ticket
#   - Subject, Description
#   {
#      "category": "payment-failure" | "checkin-issue" | "Sales Cancellation" | "General Inquiry" | "Technical Support"
#      "priority": "low" | "medium" | "high"
#      "spam": "yes" | "no"
#  }

# The category is Payment Failure, the priority is high, and the spam is no.
# Category: payment-failure, Priority: high, Spam: no

# enums -- Enumerations
#   - Named values

from enum import Enum

class TicketCategory(str, Enum):
    PAYMENT_FAILURE = "payment-failure"
    CHECKIN_ISSUE = "checkin-issue"
    SALES_CANCELLATION = "sales-cancellation"
    GENERAL_INQUIRY = "general-inquiry"
    TECHNICAL_SUPPORT = "technical-support"
    
class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    
class TicketSpam(str, Enum):
    YES = "yes"
    NO = "no"  

class SupportTicket(BaseModel):
    category: TicketCategory = Field(description="Category of the support ticket")
    priority: TicketPriority = Field(description="Priority level of the support ticket")
    spam: TicketSpam = Field(description="Indicates if the ticket is spam or not")
    
    
    
    
    # kwarges and varges 
# allow us to pass unknown number of arges to a function
# in python it use as **args and **kwargs 
# **args is used to pass unknown number of positional arges 
# **kwargs is used to pass unknown number of keyword arges 

# the ** is used to unpack the arges **kwargs**
# the * is used to pack the arges *args**
    
    

    