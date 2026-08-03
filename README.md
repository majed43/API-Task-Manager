# API-Task-Manager
This is a mini django project, I have tried to practice some of what I learned 

## Feature 
- This API is about management task, serves a users endpoint for (register, login) using email , search for users by username ,and the ability for update user profile information or changing the 
password
 


- For the core idea of this API :
    - it provides a category model with (title, desc, hex_color, ...) fields 
    - And provides project model that belong to a single category and multiple users can participate in it with fields like (title, desc, participants)
    - Also a task model that belong to a single project and can assigned to one of the participants users, it has fields like (title, desc, status, importance_level, ... ) and more 
    

## Requirement 
I will fill this section when I'm done with this project

## What I learnd 
This project is one of the things that has taken me the most time, I have leaned a lot while I was in preparation phase also during I work on it. In short, what I learned is:
- ### 1️⃣ Django Basics:
    - dealing with virtual env, installing packages, start a project/apps 
    - Basics of MVT pattern: How Django work 
    - dealing with models:
        - Common field types, field methods
        - register a model in admin page, and built an admin.ModelAdmin
        - class Meta options
        - Relations : O2O, FK, M2M
        - Basic Classes: AbstractUser, AbstractBaseUser ...
        - Filtering - Field lookups

- ### 2️⃣ Django REST framework (DRF):
    - Dealing with data with and without DRF
    - serializers:
        - Different between serializers (.Serializers & .ModelSerializer) and each one usage
        - Validation: field-level validate & Cross-field validate
        - serializers methods
    - FBV & CBV
    - Token & Permissions:
        - Authenticate with token 
        - DRF built-in permissions and custom permission(request-level & object-level)

