# SmartSadaqah

SmartSadaqah is an AI-driven healthcare donation platform designed to make medical charity more transparent, organized, and accessible. The platform connects donors with healthcare donation projects while allowing people in need to submit financial assistance requests.

The system includes an explainable AI-based allocation mechanism that evaluates approved recipient requests using factors such as medical severity, financial hardship, age vulnerability, and treatment cost. The AI generates a priority-based recommended allocation while keeping the administrator involved in the final decision-making process.

🔗 **Live Website:** [SmartSadaqah Live](YOUR_RENDER_LIVE_LINK)

---

## 📸 Project Preview

![SmartSadaqah Homepage]

---

## ✨ Main Features

### 👤 User Authentication

* User registration and login
* Secure authentication using Django's authentication system
* Authenticated users can donate and submit requests for medical assistance

### 💚 Healthcare Donation Projects

* Browse active healthcare donation projects
* View individual project details
* View funding information
* Make donations to selected projects
* Browse completed donation projects

### 💳 Donation System

* Authenticated users can donate to active healthcare projects
* Donation amount and donor information are recorded
* Total collected donation amount can be calculated for each project

### 🏥 Recipient Assistance Requests

Users can submit requests for medical financial assistance by providing information such as:

* Full name
* Age
* Medical condition
* Hospital name
* Estimated treatment cost
* Financial condition
* Supporting medical document

New requests are submitted with a pending status for administrator review.

### 🛡️ Admin Management

The Django administration panel allows administrators to:

* Manage donation projects
* Review recipient requests
* Approve or reject requests
* View donations
* Manage users
* Trigger the AI allocation process

### 🤖 Explainable AI Fund Allocation

SmartSadaqah includes a custom rule-based AI decision engine implemented in Python.

The system uses rule-based natural language processing and weighted scoring to evaluate approved recipient requests according to:

* Medical severity
* Financial hardship
* Age vulnerability
* Treatment-cost pressure

A weighted priority score is calculated using:

`Priority Score = Medical Severity × 0.4 + Financial Hardship × 0.3 + Age Vulnerability × 0.1 + Cost Pressure × 0.2`

Recipients with higher priority scores are given higher priority during allocation. The allocation logic also prevents a recommended amount from exceeding the recipient's treatment cost or the remaining allocation budget.

The system stores an AI-recommended amount and a human-readable explanation of the decision, making the process easier for administrators to review.

The AI allocation is manually triggered by an administrator, maintaining human oversight over sensitive healthcare funding decisions.

---

## 🛠️ Technology Stack

### Backend

* Python
* Django

### Frontend

* HTML5
* CSS3
* JavaScript
* Django Template Language

### Database

* SQLite

### AI / Decision Engine

* Python
* Rule-based Natural Language Processing
* Weighted scoring
* Explainable decision logic

### Development & Deployment

* Git
* GitHub
* Render

---

## 📦 Dependencies

The complete dependency list is available in:

```bash
requirements.txt
```

Install all required Python packages using:

```bash
pip install -r requirements.txt
```

---

## 💻 Run the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/tasfiaanam27/SmartSadaqah.git
```

### 2. Navigate to the Project Directory

```bash
cd SmartSadaqah
```

### 3. Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

Windows PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Apply Database Migrations

```bash
python manage.py migrate
```

### 7. Create an Admin Account (Optional)

```bash
python manage.py createsuperuser
```

Follow the terminal instructions to create an administrator account.

### 8. Run the Development Server

```bash
python manage.py runserver
```

Open the local development server shown in the terminal in your browser.

The Django admin panel can be accessed by adding `/admin/` to the local server address.

---

## 🔄 Basic System Workflow

**Donor/User → Healthcare Project → Donation**

**Recipient → Assistance Request → Admin Verification → AI Analysis → Recommended Fund Allocation**

The administrator remains involved in the allocation process to provide human oversight.

---

## 🔗 Relevant Links

**Live Website:**
[SmartSadaqah Live] https://smartsadaqah.onrender.com/

**GitHub Repository:**
[SmartSadaqah GitHub Repository](https://github.com/tasfiaanam27/SmartSadaqah)

---

## 🎓 Academic Project

SmartSadaqah was developed as an academic web application project for **CSE309 – Web Application & Internet** at **Independent University, Bangladesh (IUB)**.

The project demonstrates the integration of web application development, database management, healthcare donation workflows, and explainable AI-based decision support.

---

## 👩‍💻 Author

**Tasfia Anam**
Department of Computer Science & Engineering
Independent University, Bangladesh
