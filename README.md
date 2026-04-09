# Web Calendar REST API

A lightweight, fully functional RESTful API built with Python and Flask for managing calendar events. This API allows users to create, retrieve, filter, and delete events stored in a local SQLite database.

## 🚀 Tech Stack
* **Language:** Python 3.x
* **Framework:** Flask
* **API Extension:** Flask-RESTful
* **Database & ORM:** SQLite3, Flask-SQLAlchemy
* **Data Parsing:** reqparse

## 🛠 Installation & Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd "Web Calendar"
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install Flask Flask-RESTful Flask-SQLAlchemy
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```
   *Note: The SQLite database (`events.db`) will automatically generate the first time you run the server.*

---

## 📡 API Endpoints

The API runs on `http://127.0.0.1:5000` (or `8000` depending on your run configuration). All POST requests expect **Form Data**.

### 1. Add a New Event
* **URL:** `/event`
* **Method:** `POST`
* **Data Params:**
  * `event` (string, required): The name of the event.
  * `date` (string, required): Format `YYYY-MM-DD`.
* **Success Response:**
  * **Code:** 200 OK
  * **Content:** `{"message": "The event has been added!", "event": "Learn Flask", "date": "2026-04-10"}`

### 2. Get All Events
* **URL:** `/event`
* **Method:** `GET`
* **Success Response:**
  * **Code:** 200 OK
  * **Content:** `[{"id": 1, "event": "Learn Flask", "date": "2026-04-10"}, ...]`

### 3. Get Events by Date Range
* **URL:** `/event?start_time=YYYY-MM-DD&end_time=YYYY-MM-DD`
* **Method:** `GET`
* **Description:** Returns all events falling strictly within the provided date range (inclusive start, exclusive end).

### 4. Get Today's Events
* **URL:** `/event/today`
* **Method:** `GET`
* **Description:** Dynamically checks the system's current date and returns matching events.

### 5. Get Event by ID
* **URL:** `/event/<id>`
* **Method:** `GET`
* **Success Response:** `{"id": 1, "event": "Learn Flask", "date": "2026-04-10"}`
* **Error Response:** `{"message": "The event doesn't exist!"}` (Code: 404)

### 6. Delete Event by ID
* **URL:** `/event/<id>`
* **Method:** `DELETE`
* **Success Response:** `{"message": "The event has been deleted!"}`
* **Error Response:** `{"message": "The event doesn't exist!"}` (Code: 404)

### 7. Delete ALL Events (Reset Database)
* **URL:** `/event`
* **Method:** `DELETE`
* **Success Response:** `{"message": "All events have been deleted!"}`

---

## 🧪 Testing with cURL

You can quickly test the API from a secondary terminal using cURL:

**Create an event:**
```bash
curl -X POST http://127.0.0.1:5000/event -d "event=Meeting" -d "date=2026-05-01"
```

**Get specific event:**
```bash
curl http://127.0.0.1:5000/event/1
```

**Filter by date:**
```bash
curl "http://127.0.0.1:5000/event?start_time=2026-05-01&end_time=2026-05-31"
```
