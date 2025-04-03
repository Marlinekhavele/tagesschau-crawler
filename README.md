# **Backend IM**  

Backend IM is a tool that allows developers to create, deploy, and test backend functionalities with minimal friction. It is designed for agile development. The app enables users to build an API, integrate it into their project seamlessly, and instantly test endpoints through an interactive interface. It is optimised for speed, empowering teams to iterate quickly and deliver robust backend solutions.

## **Cloning the Repository**  

1. **Clone the repository** :  

   ```sh
   git clone https://github.com/hngprojects/Backend-Im-BE.git
   ```

2. **Navigate into the project directory**:  

   ```sh
   cd Backend-Im-BE
   ```



## Crawler Project Architecture

```bash
backend-im-be/
│
├── alembic/                  # database migrations
│   ├── versions/             # Migration scripts
│   ├── env.py                # Alembic environment settings
│   ├── script.py.mako        # Template for migrations
│   └── README                # Documentation
│
├── app/
│   ├── __init__.py
│   ├── api/                  # API routes and dependencies
│   │   ├── v1/               # API version 1
│   │   │   ├── models/       # SQLAlchemy models
│   │   │   │   ├── __init__.py
│   │   │   ├── routes/       # API routes
│   │   │   │   ├── __init__.py
│   │   │   ├── schemas/      # Pydantic schemas
│   │   │   │   ├── __init__.py
│   │   │   ├── services/     # Business logic
│   │   │   │   ├── __init__.py
│   │   │   ├── utils/        # Utility functions
│   │   │   │   ├── __init__.py
│   │   ├── __init__.py
│
├── tests/                    # Unit and integration tests
│   ├── __init__.py
│
├── .env.sample               # Sample environment variables
├── .gitignore                # Git ignore file
├── alembic.ini               # Alembic configuration
├── config.py                 # Configuration settings
├── conftest.py               # Pytest configuration
├── LICENSE                   # Project license
├── main.py                   # FastAPI main application entry point
├── poetry.lock               # Poetry lockfile
├── pyproject.toml            # Python dependencies
└── README.md                 # Project documentation
```

## **Setup Instructions**  

1. **Create a virtual environment**:  

   ```sh
   python3 -m venv .venv
   ```

2. **Activate the virtual environment**:  

- On macOS/Linux:  

     ```sh
     source .venv/bin/activate
     ```

- On Windows (PowerShell):  

     ```sh
     .venv\Scripts\Activate
     ```

3. **Install project dependencies**:  

   ```sh
   poetry install
   ```

4. **Create a `.env` file** from `.env.sample`:  

   ```sh
   cp .env.sample .env
   ```

5. **To Run Project Locally**:

```sh
poetry run python main.py
```

---

## **Database Setup**  

### **Replacing Placeholders in Database Setup**  

When setting up the database, you need to replace **placeholders** with your actual values. Below is a breakdown of where to replace them:

---

## **Step 1: Create a Database User**

```sql
CREATE USER user WITH PASSWORD 'your_password';
```

🔹 **Replace:**  

- `user` → Your **preferred database username** (e.g., `backend_fastapi_user`).  
- `your_password` → A **secure password** for the user (e.g`StrongP@ssw0rd`).  

✅ **Example:**  

```sql
CREATE USER backend_fastapi_user WITH PASSWORD 'StrongP@ssw0rd';
```

---

## **Step 2: Create the Database**

```sql
CREATE DATABASE backend_fast_api;
```

🔹 **Replace:**  

- `backend_fast_api` → Your **preferred database name** (e.g.`backend_fast_api`).  

✅ **Example:**  

```sql
CREATE DATABASE backend_fast_api;
```

---

## **Step 3: Grant Permissions**

```sql
GRANT ALL PRIVILEGES ON DATABASE backend_fast_api TO user;
```

🔹 **Replace:**  

- `backend_fast_api` → The **database name you used** in Step 2.  
- `user` → The **username you created** in Step 1.  

✅ **Example:**  

```sql
GRANT ALL PRIVILEGES ON DATABASE backend_fast_api TO backend_fastapi_user;
```

---

## **Step 4: Update `.env` File**

Edit the `.env` file to match your setup.

```env
DATABASE_URL=postgresql://user:your_password@localhost/backend_fast_api
```

🔹 **Replace:**  

- `user` → Your **database username**.  
- `your_password` → Your **database password**.  
- `backend_fast_api` → Your **database name**.  

✅ **Example:**  

```env
DATABASE_URL=postgresql://backend_fastapi_user:StrongP@ssw0rd@localhost/backend_fast_api
```

---

## **Step 5: Verify Connection**

After setting up the database, test the connection:

```sh
psql -U user -d backend_fast_api -h localhost
```

🔹 **Replace:**  

- `user` → Your **database username**.  
- `backend_fast_api` → Your **database name**.  

✅ **Example:**  

```sh
psql -U backend_fastapi_user -d backend_fast_api -h localhost
```

## **Step 6: Run database migrations**  

   ```sh
   alembic upgrade head
   ```

   _Do NOT run `alembic revision --autogenerate -m 'initial migration'` initially!_

## **Step 7: If making changes to database models, update migrations**  

```sh
   alembic revision --autogenerate -m 'your migration message'
   alembic upgrade head
   ```

---

## **Adding Tables and Columns**  

1. **After creating new tables or modifying models**:  

- Run Alembic migrations:  

     ```sh
     alembic revision --autogenerate -m "Migration message"
     alembic upgrade head
     ```

---

## **Running Tests with Pytest**  

### **Install Pytest**  

Ensure `pytest` is installed in your virtual environment:  

```sh
poetry add pytest
```

### **Run all tests in the project**  

From the **project root directory**, run:  

```sh
pytest
```

### **Run tests and generate coverage report**  

To check test coverage, install `pytest-cov`:  

```sh
poetry add pytest-cov
```

Then run:  

```sh
pytest --cov=api
```

---

- **Test your endpoints and models** before pushing changes.  
- **Push Alembic migrations** if database models are modified.  
- Ensure your code **follows project standards** and **passes tests** before submitting a pull request.

---

## Pre-Commit Setup (Required for Code Quality)

To maintain consistent code formatting and catch issues before committing, we use pre-commit hooks.

1. Install Pre-commit Hooks
   After cloning the repository and installing dependecies, run:

   ```bash
   pre-commit install
   ```

   This ensures that all pre-commit hooks run before every commit.
2. Manually Run Pre-Commit on All Files
   To check all files before committing:

   ```bash
   pre-commit run --all-files
   ```

3. If a Hook Fails, Fix Issues and Retry
   If pre-commit stops your commit, fix the reported issues and try again.

## **Contribution Guidelines**  

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting a pull request to learn about our development process, how to propose bugfixes and improvements, and how to build and test your changes.
