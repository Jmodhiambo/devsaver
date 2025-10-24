# 🧠 DevSaver – A Developer’s Knowledge Hub API

> **DevSaver** is a full-featured backend project built to power a developer-oriented knowledge hub — a place where developers can **upload, manage, and share learning resources** such as videos, articles, and tools.
>
> The project started as a way to deepen my understanding of **backend architecture, testing, and modern Python development**, and has evolved into a clean, testable, and extensible API system.

![DevSaver Dashboard Preview](app/static/images/dashboard.png)
*Dashboard Preview – simple, functional, and developer-focused.*

---

## 🚀 Project Overview

**DevSaver** is not just a CRUD API — it’s a complete exploration of:

* Building scalable RESTful APIs using **FastAPI**
* Structuring projects with **SQLAlchemy ORM**
* Implementing robust **testing pipelines** with **pytest**
* Ensuring **data integrity and test isolation** using **factory_boy** and **Faker**
* Designing **reusable components** for future production-ready backends

The project also includes a **minimal frontend layer** for resource upload and visualization, enabling developers to interact with the API seamlessly.

---

## 🧩 Features

* **User Management** – Register, view, and manage user profiles
* **Resource Management** – Upload, categorize, and fetch coding resources
* **File Uploads** – Support for resource files (e.g., `.mp4`, `.pdf`)
* **Database Integration** – Persistent storage with SQLAlchemy ORM
* **Factory-Based Test Data** – Deterministic and isolated testing using factory_boy
* **In-Memory SQLite for Tests** – Blazing-fast test runs without affecting production data
* **Modular Code Structure** – Clean, extensible, and production-ready layout
* **HTML Templates (Optional)** – Simple UI for uploads and dashboard visualization

---

## ⚙️ Tech Stack

| Category                | Technology                     |
| ----------------------- | ------------------------------ |
| **Language**            | Python 3.8+                    |
| **Framework**           | FastAPI                        |
| **ORM**                 | SQLAlchemy                     |
| **Database**            | SQLite (Development & Testing) |
| **Testing**             | pytest, factory_boy, Faker     |
| **Environment**         | dotenv (.env) Configuration    |
| **Frontend (Optional)** | Jinja2 Templates, HTML5, CSS3  |

---

## 🧪 Testing

DevSaver follows a **test-driven development (TDD)** mindset.
Tests are organized for **unit**, **integration**, and **functional** coverage with the following principles:

* Tests run in an **isolated environment** using an in-memory SQLite database
* Test data is generated dynamically using **factory_boy** and **Faker**
* CI-friendly structure for continuous integration setups (e.g., GitHub Actions)

Run all tests with:

```bash
pytest -v
```

You’ll see detailed output showing model, route, and integration test coverage.

---

## 🧰 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Jmodhiambo/devsaver
cd devsaver
```

### 2️⃣ Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Environment Setup

Copy and customize the example `.env` file:

```bash
cp .env.example .env
```

Configure your own keys, database URL, and environment variables as needed.

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Run the Application

You can run the DevSaver backend in two ways using run.py:

To launch the API server:
```bash
python run.py api
```

To run CLI-based commands:
```bash
python run.py cli
```

Alternatively, you can directly run FastAPI with uvicorn:
```bash
uvicorn main:app --reload
```

Access the app at **[http://127.0.0.1:8000](http://127.0.0.1:8000)**.

### 6️⃣ Run Tests

```bash
pytest
```

---

## 🧱 Project Structure

```
devsaver/
│
├── app/
│   ├── cli/                     # Command-line interface commands
│   ├── core/                    # Core configurations and app setup
│   ├── crud/                    # CRUD operations
│   ├── models/                  # ORM models
│   │   └── engine/              # DB engine initialization
│   ├── routes/                  # API route groups
│   │   ├── resource/
│   │   └── user/
│   ├── schemas/                 # Pydantic schemas
│   ├── services/                # Business logic and services
│   ├── static/                  # CSS, JS, and image files
│   │   ├── css/
│   │   ├── images/
│   │   └── js/
│   ├── templates/               # Jinja2 templates
│   │   ├── errors/
│   │   ├── pages/
│   │   └── partials/
│   ├── test/                    # Tests and test factories
│   │   ├── factories/
│   │   └── models/
│   ├── uploads/                 # Uploaded resource files
│   └── utils/                   # Helper utilities
│       ├── auth/
│       └── pydantic/
│
├── main.py                      # FastAPI entrypoint
├── run.py                       # Unified CLI and API runner
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🌱 Learning Outcomes

Building DevSaver helped me strengthen:

* Modular API design and clean project architecture
* ORM data modeling and relationships
* Automated testing with **pytest** and factories
* Working with environment variables securely
* Handling file uploads in backend APIs
* Designing APIs that can scale to production
* Understanding the real-world workflow of backend projects

---

## 📸 UI Preview

| Dashboard                                  | Upload Resource                       |
| ------------------------------------------ | ------------------------------------- |
| ![Dashboard](app/static/images/dashboard.png) | ![Upload](app/static/images/upload.png) |

*(Screenshots from the minimal developer dashboard interface)*

---

## 🧭 Future Roadmap

* [ ] Add JWT-based authentication
* [ ] Integrate Swagger/OpenAPI documentation
* [ ] Implement role-based access control
* [ ] Add Docker support for containerized deployment
* [ ] Deploy to Render / Railway / AWS
* [ ] Include CI/CD setup with GitHub Actions

---

## 👨‍💻 Author

**Martin Odhiambo**
Backend Developer | Python | JavaScript | REST APIs

📫 **Connect with me:**

* GitHub: [@Jmodhiambo](https://github.com/Jmodhiambo)
* LinkedIn: [Martin Odhiambo](https://linkedin.com/in/martin-odhiambo-13b04817b/)

---

## ⭐ Contribute

Interested in collaborating or extending DevSaver?
Feel free to **fork the repo**, **open issues**, or submit **pull requests**.
Constructive feedback and ideas are always welcome!

```bash
git checkout -b feature/awesome-idea
git commit -m "Add new feature"
git push origin feature/awesome-idea
```

---

## 🏁 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

### ✨ Final Note

> DevSaver is more than a learning project — it’s a reflection of how much you can grow as a developer when you **build, test, and refine real-world systems**.
> If you’re reading this, I’d love for you to try it out, break it, improve it, and share what you build next.
