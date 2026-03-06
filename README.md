A Dockerized Django application that goes beyond basic contact storage by enriching data with information from external sources.

## 🌟 Key Features

### 📥 Bulk CSV Operations
* **Smart Import:** Handles large CSV files using `DictReader` and `bulk_create` for optimal performance.
* **Validation:** Automatic duplicate detection for **Phone** and **Email** fields.
* **Status Mapping:** Automatically links contacts to predefined statuses (New, In Progress, etc.).

### 🌤 External API Integrations
* **Weather:** Integrated with **Open-Meteo API** to display current temperature and wind speed for each contact's city.
* **Geo-Caching:** Custom logic to fetch and store city coordinates (Latitude/Longitude), reducing redundant API calls and improving load times.

### 🐳 DevOps & Architecture
* **PostgreSQL Integration:** Production-ready database setup with strict relational integrity.
* **Automated Entrypoint:** A custom script that waits for the DB, runs migrations, creates a **Superuser** automatically and fills ContactStatusChoices table in database.

---

## 🚀 Getting Started

### Prerequisites
* Docker installed on your machine.
* Git for cloning the repository.

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/scroynel/django_contacts.git
   cd django_contacts
   ```

2. **Launch with Docker Compose**
   ```bash
   docker compose up --build
   ```

3. **Access the application**

* http://localhost:8000
* Admin Interface: http://localhost:8000/admin
* Default Credentials: User: admin | Password: admin

**🔧 Internal Logic & Workflow**
1. Entrypoint Script: On every up, the script checks if PostgreSQL is ready using netcat.
2. Data Integrity: All bulk operations are wrapped in transaction.atomic() to prevent partial data corruption.
3. Weather Fetching: The system aggregates unique city names from your contacts to perform batch API requests, minimizing network latency.
