# Subscription Tracker

## Overview

The **Subscription Tracker** is a web application designed to help users manage and keep track of their subscriptions. The goal is to provide an intuitive platform where users can easily monitor their active subscriptions, track renewal dates, and manage payments. The app will send reminders to users before subscription renewals, helping them stay on top of their recurring expenses.

## Features

- **User Registration and Authentication**: Users can sign up, log in, and manage their profiles securely.
- **Add Subscriptions**: Users can add subscriptions (e.g., streaming services, software, utility services) with details like price, renewal date, and payment method.
- **Subscription Reminders**: The app sends notifications before the renewal date of subscriptions.
- **Dashboard**: A user-friendly dashboard to display active subscriptions, renewal dates, and total costs.
- **Subscription History**: Keep track of past subscriptions and their details.
- **Task Scheduling**: Uses Celery to send notifications asynchronously at scheduled times.

## Technologies Used

- **Backend**: Django (for handling server-side logic)
- **Database**: PostgreSQL (for data storage)
- **Task Scheduling**: Celery with Redis (for sending subscription reminders)
- **Web Framework**: Django Rest Framework (for API development)

## Installation

### Prerequisites

Ensure you have the following installed:

- [Python 3.8 or higher](https://www.python.org/downloads/)
- [Django](https://www.djangoproject.com/) (version 3.x or higher)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Redis](https://redis.io/download/) (for Celery)
- [Celery](https://docs.celeryproject.org/en/stable/)

### Steps to Run the Project Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/torykoghukhar/trackerapp.git

2. Navigate into the project folder:

   ```bash
   cd trackerapp

3. Set up the virtual environment and install dependencies:

   ```bash
   pipenv install
   
   pip install -r requirements.txt

4. Set up the database. Create a new PostgreSQL database and update the `settings.py` file with your database credentials:

   ```python
   DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql',
         'NAME': 'subscriptiontracker',
         'USER': 'yourusername',
         'PASSWORD': 'yourpassword',
         'HOST': 'localhost',
         'PORT': '5432',
     }
   }

5. Run migrations to set up the database schema:

   ```bash
   pipenv run python manage.py migrate

   
6. Set up Redis for Celery:

   ```bash
   docker run -p 6379:6379 -d redis
   
7. Start Celery:

   ```bash
   pipenv run celery -A trackerapp worker --loglevel=info --pool=solo

8. Run the Django development server:

   ```bash
   pipenv run python manage.py runserver

9. Open your browser and navigate to `http://localhost:8000` to access the application.
   
## Usage
- Sign up: Create an account to start tracking your subscriptions. After registration, you can log in and manage your profile.
- Add a subscription: After logging in, go to the "Subscriptions" section and click "Add Subscription." Enter details such as the name, renewal date, cost, and payment method.
- Get reminders: The app will send email or push notifications a few days before each subscription is due for renewal.
- Dashboard: View all your active subscriptions on the dashboard, including renewal dates and total subscription costs.
