# Project Documentation: GitHub Repository Backup System

This documentation provides all necessary instructions on setting up and running the GitHub Repository Backup System. This system is built using Django and Django REST Framework, designed to interact with the GitHub API for backing up user and repository data into a PostgreSQL database

## Overview
This application allows you to:
   * Fetch user information from GitHub and display it in the API.
   * Backup user data into a PostgreSQL database.
   * Backup repository details that belong to a particular user.
   * Delete backups of users and their repositories.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed the latest version of [Python](https://www.python.org/downloads/).
- You have a [PostgreSQL](https://www.postgresql.org/download/) server running.
- You have installed the necessary Python packages listed in the `requirements.txt` file. You can install them using pip:

pip install -r requirements.txt

## Installation and Setup

* Step 1: Clone the Repository

   git clone https://github.com/chiaradigii/Bjumper_Backend_Test.git

* Step 2: Set Up a Virtual Environment (Optional but recomended)

   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

* Step 3: Install Dependencies
  
  pip install -r requirements.txt

* Step 4: Configure Environment Variables

Create a .env file in the root directory of your project and fill it with your PostgreSQL database settings and GitHub token:

   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   GITHUB_TOKEN=your_github_token

* Step 5: Database Migration
   Run migrations to set up your database schema:

   python manage.py makemigrations
   python manage.py migrate

* Step 6: Start the Server
  Run the Django development server:

  python manage.py runserver

## API Usage with cURL Commands
   Here are examples of cURL commands that you can use to interact with the API endpoints.

### Fetch users
* URL: /users/<username>/
* Method: GET
* Description: Fetches and displays GitHub user information if it exists in the database along with linked repositories.
* cURL Example:

curl -X GET http://localhost:8000/users/<username>/

### Backup User
* URL: /backup_user/<username>/
* Method: POST
* Description: Backups a user from GitHub into the database if they exist on GitHub.
* cURL Example:

curl -X POST http://localhost:8000/backup_user/<username>/

### Delete User Backup
* URL: /delete_user/<username>/
* Method: DELETE
* Description: Deletes a backed-up user and their repositories from the database.
* cURL Example:

curl -X DELETE http://localhost:8000/delete_user/<username>/

### Backup Repository

* URL: /backup_repository/<username>/<repository_url>/
* Method: POST
* Description: Backups a repository if the user exists in the database and owns the repository on GitHub.
* cURL Example:

curl -X POST http://localhost:8000/backup_repository/<username>/<repository_url>/

### Delete Repository Backup

* URL: /delete_repository/<repository_url>/
* Method: DELETE
* Description: Deletes a backed-up repository from the database.
* cURL Eample:

curl -X DELETE http://localhost:8000/delete_repository/<repository_url>/

#### Notes:

Replace <username> with a valid GitHub username
Replace <repository_url> with the full repository URL (e.g., github.com/<username>/<repository>).
