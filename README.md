# API Project

DevSaver is a backend project I am building to practice and improve my skills in Python, SQLAlchemy, and testing with pytest.
It includes a CRUD API with proper test isolation using factories (`factory_boy` + `faker`) and in-memory SQLite for faster testing.

## Features

* CRUD operations for users and resources
* SQLAlchemy ORM with a test database
* Unit and integration testing using pytest
* Factory-based fixtures for generating test data

## Tech Stack

* Python 3.8+
* SQLAlchemy
* Pytest
* Factory Boy + Faker

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/Jmodhiambo/devsaver
   cd devsaver
   ```

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
   ```

3. Set up the .env file locally (Change the Keys)
   ```bash
   cp .env.example .env
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the tests:

   ```bash
   pytest
   ```

## Next Steps

I’m continuously learning and improving this project.
Future updates may include authentication, better API documentation, and deployment setup.
