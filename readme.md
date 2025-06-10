# 🛡️ Third-Party API Watchdog

---

## 🧩 Problem Statement

Modern applications increasingly depend on numerous external third-party APIs—such as payment gateways, weather services, social media integrations, and more—to deliver key functionality.  
When one of these services experiences downtime, slow responses, or breaking changes in their API, it can critically disrupt your application’s operations.

Detecting whether an issue originates from your code or the external API is challenging but essential for maintaining reliability and a smooth user experience.  
Without proactive monitoring and detailed insights into these dependencies, troubleshooting becomes slow and inefficient.

---

## 🚀 Solution

**Third-Party API Watchdog** is a lightweight backend service built with FastAPI that actively monitors the health, performance, and contract stability of external APIs your application depends on.

### 🔑 Key Features

- ✅ **API Endpoint Registration**  
  Add any third-party API URL you want to monitor.

- 🔁 **Manual Health Checks**  
  Ping endpoints on demand and store status, response time, and timestamp.

- 📊 **Performance Tracking**  
  View historical API check results (status, time, uptime).

- 📡 **RESTful Endpoints**  
  Built-in support to register, check, and query APIs via HTTP endpoints.

---

## ⚙️ Tech Stack

- 🔧 **FastAPI** – Web framework  
- 🧱 **SQLite** – Lightweight database  
- 🔎 **SQLAlchemy** – ORM for database interactions  
- 🌐 **Requests** – To make HTTP calls to external APIs

---

## 🚦 Getting Started

### 1. Clone the Repository

```bash
git https://github.com/el-011/Third-Party-API-Watchdog
cd Third-Party-API-Watchdog
```

### 2. Create & Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Database

Make sure you have PostgreSQL running and update the database URL in the code:

```python
DATABASE_URL = "postgresql+asyncpg://username:password@localhost/database_name"
```

### 5. Run the Application

```bash
uvicorn app.main:app --reload
```

Now visit http://127.0.0.1:8000/docs to interact with the API via Swagger UI.

## 📌 API Usage

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/endpoints/` | Register a new third-party API |
| GET | `/endpoints/{id}/check` | Manually trigger a health check |
| GET | `/endpoints/{id}/history` | Get all health check logs for an endpoint |
| GET | `/dashboard` | Get overview of all monitored endpoints |

## 🧪 Example Workflow

### 1. Register an API:

```json
{
  "url": "https://api.publicapis.org/entries",
  "expected_status_code": 200,
  "expected_response_schema": {
    "count": "int",
    "entries": "list"
  }
}
```

### 2. Manual Health Check

Call `/endpoints/1/check` to trigger an immediate health check.

### 3. View History

Get results from `/endpoints/1/history` to see historical performance data.

### 4. Dashboard Overview

Visit `/dashboard` to see the status of all monitored endpoints with uptime percentages.

## 🏗️ Project Structure

```
third-party-api-watchdog/
├── app
│   ├── api
│   │   ├── endpoints.py
│   │   └── health_checks.py
│   ├── core
│   │   ├── database.py
│   │   ├── health_check_scheduler.py
│   │   └── validation.py
│   ├── models
│   │   ├── endpoint.py
│   │   └── health_check.py
│   ├── schemas
│   │   ├── dashboard.py
│   │   ├── endpoint.py
│   │   └── health_check.py
│   └── main.py
├── .env
└── README.md
```

## 🧠 Design Highlights

- **Asynchronous FastAPI design** for future scaling
- **ORM-backed persistence layer** with SQLAlchemy
- **Clean Pydantic schema validation** for request/response handling
- **Automated background health checks** every 5 minutes
- **Contract validation** to ensure API responses match expected schemas
- **Comprehensive error handling** and logging
- **Easily extensible** to add notifications or custom checks

## 📊 Health Check Statuses

- **UP**: Endpoint is healthy and responding as expected
- **DOWN**: Endpoint is not responding or returning unexpected status codes
- **CONTRACT_BROKEN**: Endpoint responds but data doesn't match expected schema

## 🔧 Configuration

### Database Configuration
Update the `DATABASE_URL` in `.env` to match your PostgreSQL setup:

```python
DATABASE_URL = "postgresql+asyncpg://username:password@localhost/database_name"
```

### Health Check Interval
Modify the sleep interval in `scheduled_health_checks()` function:

```python
await asyncio.sleep(300)  # 300 seconds = 5 minutes
```

## 📈 Future Enhancements

- [ ] **Background scheduler** for customizable check intervals
- [ ] **Email/SMS alert integration** for immediate notifications
- [ ] **Admin dashboard** with interactive charts and graphs
- [ ] **Advanced response schema validation** with JSON Schema
- [ ] **API rate limiting** and throttling controls
- [ ] **Multi-region health checks** for global monitoring
- [ ] **Webhook notifications** for third-party integrations
- [ ] **Performance benchmarking** and SLA monitoring

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code follows the existing style and includes appropriate tests.

## 📋 Requirements

- Python 3.9+
- PostgreSQL 12+
- FastAPI
- SQLAlchemy
- Pydantic v2
- HTTPX for async HTTP requests

## 📜 License

This project is open-source and available under the MIT License.

## 💡 Author

Made with ❤️ by Renu Vishwakarma

---

## 🔍 Troubleshooting

### Common Issues

**Database Connection Error**
- Ensure PostgreSQL is running
- Verify database credentials in `DATABASE_URL`
- Check if the database exists

**Pydantic Validation Error**
- Make sure you're using Pydantic v2
- Verify model configurations use `model_config = ConfigDict(from_attributes=True)`

**Import Errors**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Activate your virtual environment

For more help, please open an issue on GitHub.
