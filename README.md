# CRTEST

CRTEST is a test Django web application for handling queue of users for an early access.

## Installation

Install Python 3.7, MySQL 5.7
```
Database name : crtest
Database username : root
Database password : hello
Django Admin username : admin
Django Admin password : admin
```
Setup and activate a venv
```bash
cd into project directory
pip3 install -r requirements.txt 
python3 manage.py runserver
python3 manage.py makemigrations
python3 manage.py migrate
```

## Usage

```python
Goto 12.0.0.1:8080
Put a Name and a valid email Address, click Signup
You will receive a mail with a link, this link can be used by your friends to signup the same way you did.
Each time a new user signs up with your referral, your position will be lifted,
so at the end when many people have registered and as you become first position,
you will receive a mail as invitation.
```
