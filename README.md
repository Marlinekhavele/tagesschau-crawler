# **Tagesschau Crawler**
Tagesschau Crawler is a Python-based web scraping tool designed to fetch and process news articles from the Tagesschau website. It provides a structured architecture for managing the scraping process, storing data in a PostgreSQL database, and exposing the data via a RESTful API. The project is built with Flask, SQLAlchemy, and Alembic for scalability and maintainability.

---

## **Features**
- **Web Scraping**: Automatically fetches articles from the Tagesschau website.
- **Database Integration**: Stores scraped articles and their versions in a PostgreSQL database.
- **RESTful API**: Exposes endpoints to retrieve articles and their metadata.
- **Pagination**: Supports paginated responses for large datasets.
- **Extensibility**: Modular architecture for easy customization and scaling.
---

## **Project Architecture**

```bash
tagesschau-crawler/
│
├── alembic/                  # Database migrations
│   ├── versions/             # Migration scripts
│   ├── env.py                # Alembic environment settings
│   ├── script.py.mako        # Template for migrations
│   └── README                # Documentation
│
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── database/             # Database setup and models
│   │   ├── db.py             # SQLAlchemy instance
│   ├── crawler/              # Crawler logic
│   │   ├── crawler.py        # Main crawler class
|   |   |--- scheduler        # scheduler
│   ├── models/               # Database models
│   │   ├── article.py        # Article and ArticleVersion models
│   ├── routes/               # API routes
│   │   ├── article.py        # Routes for articles
│   ├── schemas/              # Marshmallow schemas
│   │   ├── article.py        # Schemas for serialization
│   ├── service/              # Business logic
│   │   ├── article.py        # Article service
│
├── tests/                    # Unit and integration tests
│   ├── test_crawler.py       # Tests for the crawler
│   ├── test_routes.py        # Tests for API routes
│
├── .env.sample               # Sample environment variables
├── alembic.ini               # Alembic configuration
├── config.py                 # Configuration settings
├── main.py                   # Application entry point
├── pyproject.toml            # Poetry configuration
└── README.md                 # Project documentation
```

---

## **Setup Instructions**

### **Step 1: Clone the Repository**

```sh
git clone https://github.com/Marlinekhavele/tagesschau-crawler
cd tagesschau-crawler
```

### **Step 2: Create a Virtual Environment**

```sh
python3 -m venv .venv
```

Activate the virtual environment:

- On macOS/Linux:  
  ```sh
  source .venv/bin/activate
  ```
- On Windows (PowerShell):  
  ```sh
  .venv\Scripts\Activate
  ```

### **Step 3: Install Dependencies**

```sh
poetry install
```

## **Database Setup**

### **Step 1: Create a Database User**

```sql
CREATE USER postgres WITH PASSWORD 'password';
```


### **Step 2: Create the Database**

```sql
CREATE DATABASE crawler_db;
```


### **Step 3: Grant Permissions**

```sql
GRANT ALL PRIVILEGES ON DATABASE crawler_db TO postgres;
```

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/crawler_db
```

---

## **Running the Application**

Start the application locally:

```sh
poetry run python main.py
```

---

## **Running Tests**

### **Step 1: Install Testing Dependencies**

```sh
poetry add pytest pytest-cov
```

### **Step 2: Run Tests**

Run all tests:

```sh
pytest
```

Generate a coverage report:

```sh
pytest --cov=app
```

![screenshot](screenshot/1.png)
![screenshot](screenshot/2.png)
![screenshot](screenshot/3.png)
