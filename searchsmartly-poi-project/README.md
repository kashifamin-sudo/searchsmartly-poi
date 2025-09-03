
```markdown
# 🗺️ SearchSmartly PoI Importer

A Django application that imports **Points of Interest (PoI)** from multiple data formats (**CSV, JSON, XML**) into a relational database and exposes them via the **Django Admin panel** for browsing, searching, and filtering.  

This was developed as part of the **Senior Backend Developer Take Home Exercise**.

---

## 📖 Table of Contents
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
  - [Importing Data](#importing-data)
  - [Running the Server](#running-the-server)
  - [Admin Panel](#admin-panel)
- [File Specifications](#-file-specifications)
- [Database Schema](#-database-schema)
- [Error Handling](#-error-handling)
- [Assumptions](#-assumptions)
- [Future Improvements](#-future-improvements)

---

## ✨ Features

- Import PoI data from **CSV, JSON, and XML** files using a **management command**.
- Supports **bulk import of multiple files** in a single command.
- Optionally **clear existing data** before a new import (`--clear`).
- Stores metadata such as the **source file** for traceability.
- Admin panel functionality:
  - Browse PoIs with key fields.
  - **Search** by internal ID or external ID.
  - **Filter** by category.
- Defensive programming against malformed files (graceful error handling).
- Extensible design for future data sources or APIs.

---

## 🛠 Tech Stack

- **Python 3.10+**
- **Django 4.x**
- SQLite (default local DB, can be swapped for Postgres/MySQL)
- Built-in Django Admin

---

## 📂 Project Structure

```

searchsmartly-poi-project/
│
├── poi/                        # Main app
│   ├── management/
│   │   └── commands/
│   │       └── import\_poi.py   # Import command (CSV, JSON, XML)
│   ├── migrations/             # Database migrations
│   ├── models.py               # PointOfInterest model
│   ├── admin.py                # Admin registration
│   └── ...
│
├── searchsmartly\_project/      # Django project config
│   ├── settings.py
│   └── urls.py
│
├── requirements.txt
├── README.md
└── manage.py

````

---

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/searchsmartly-poi-project.git
   cd searchsmartly-poi-project
````

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser for admin access:**

   ```bash
   python manage.py createsuperuser
   ```

---

## 🔧 Configuration

* Default DB: SQLite (configured in `settings.py`).
* To switch to Postgres/MySQL, update `DATABASES` in `settings.py`.
* Ensure your files are encoded in UTF-8 (especially XML/JSON with non-Latin characters).

---

## 🚀 Usage

### Importing Data

Run the import command with one or more files:

```bash
python manage.py import_poi poi/records.csv poi/records.json poi/records.xml
```

Clear existing data before import:

```bash
python manage.py import_poi poi/records.xml --clear
```

### Running the Server

```bash
python manage.py runserver
```

### Admin Panel

* URL: [http://localhost:8000/admin/](http://localhost:8000/admin/)
* Log in with your superuser credentials.
* Navigate to **Points of Interest** to view, search, and filter imported data.

---

## 📑 File Specifications

* **CSV:**

  ```
  poi_id, poi_name, poi_latitude, poi_longitude, poi_category, poi_ratings
  ```

* **JSON:**

  ```json
  {
    "id": "123",
    "name": "My Place",
    "coordinates": {"latitude": 51.50, "longitude": -0.12},
    "category": "restaurant",
    "ratings": [3,4,5,2],
    "description": "Optional description"
  }
  ```

* **XML:**

  ```xml
  <RECORDS>
    <DATA_RECORD>
      <pid>123</pid>
      <pname>My Place</pname>
      <pcategory>restaurant</pcategory>
      <platitude>51.50</platitude>
      <plongitude>-0.12</plongitude>
      <pratings>3,4,5,2</pratings>
    </DATA_RECORD>
  </RECORDS>
  ```

---

## 🗄 Database Schema

**PointOfInterest model:**

| Field         | Type   | Notes                                  |
| ------------- | ------ | -------------------------------------- |
| id            | PK     | Auto-increment (internal ID)           |
| external\_id  | String | From source file (`poi_id`/`id`/`pid`) |
| name          | String | PoI name                               |
| latitude      | Float  | Geographical latitude                  |
| longitude     | Float  | Geographical longitude                 |
| category      | String | PoI category (e.g. restaurant)         |
| ratings\_data | Text   | Raw ratings string/JSON                |
| description   | Text   | (Optional, from JSON)                  |
| source\_file  | String | Origin filename                        |

---

## ⚠️ Error Handling

* **Invalid File Path:** Raises `CommandError`.
* **Invalid JSON/XML:** Graceful error message without crashing.
* **Missing Fields:** Skipped records instead of breaking the import.
* **Duplicate External IDs:** Existing entries updated with new data.

---

## 📌 Assumptions

* Each PoI has a unique `external_id` within the dataset.
* Ratings are stored as raw data (`ratings_data`), not yet averaged.
* File encoding is UTF-8.
* Admin users manage data via Django Admin (no public API yet).

---

## 🚧 Future Improvements

* ✅ Compute and store **average rating** as a numeric field.
* ✅ Add REST API endpoints using Django REST Framework.
* ✅ Write unit tests for parsing logic and command execution.
* ✅ Add Dockerfile & docker-compose for containerized setup.
* ✅ Validate coordinates fall within realistic ranges.
* ✅ Bulk insert optimization for large datasets.

---

## 📜 License

This project is provided for technical assessment purposes.
You are free to adapt and extend it for personal or professional use.

```

---

👉 Do you also want me to **generate a `requirements.txt`** file that matches this project (with Django and standard dependencies), so anyone can run it immediately?
```
