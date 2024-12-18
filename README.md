# GoCash Platform

## Overview

GoCash is a comprehensive financial platform designed to provide users with seamless access to wallet management, payment processing, transaction tracking, and subscription plans. The system supports modern web and mobile interfaces, integrating powerful backend logic with user-friendly front-end designs.

The platform is built using the Django framework for the backend, PostgreSQL for the database, and Flutter for the mobile front end. The GoCash ecosystem includes wallet services, transaction management, green initiatives, subscription models, and API integrations.

---

## Features

### Wallet Management
- Create and manage wallets.
- Recharge wallet balance with transaction logging.
- Reset wallet passwords with validation.
- Display wallet balance on the user dashboard.

### Transaction Management
- Log all transactions, including deposits, withdrawals, payments, and transfers.
- View transaction history with filters for service type and transaction details.
- Display a maximum of 10 transactions per page with navigation controls.

### Subscription Plans
- Offer subscription tiers: Standard, Plus, and Premium.
- Provide GreenUser plans: Leaf, Tree, and Forest.
- Link users to their selected subscription plans for enhanced services.

### User Management
- Registration and login using phone numbers.
- Token-based authentication for secure API access.
- Admin portal to manage users and groups, including permissions.

### API Integration
- REST API endpoints for all core functionalities, tested using Postman.
- Front-end API calls for real-time data retrieval and updates.

### Green Initiatives
- Promote environmentally friendly subscription plans.
- Encourage user participation in sustainability efforts.

---

## Architecture

### Backend
- **Framework**: Django
- **Database**: PostgreSQL
- **APIs**: Django REST Framework (DRF)
- **Containerization**: Docker with Docker Compose
- **Task Management**: Celery for asynchronous tasks

### Frontend
- **Web**: HTML/CSS with dynamic data retrieval via JavaScript (planned integration).
- **Mobile**: Flutter for cross-platform compatibility.

### Deployment
- **Environment**: Ubuntu Linux (via virtual machine for development)
- **Server**: Gunicorn with NGINX
- **Cloud Integration**: Future plans for scalable deployment

---

## Database Schema

### Core Models
- **User**: Stores user details, linked to subscription plans.
- **Wallet**: Tracks wallet balances and user associations.
- **Transaction**: Logs all financial activities with fields for sender, receiver, amount, service type, and balance adjustments.
- **SubscriptionPlan**: Defines Standard, Plus, and Premium plans.
- **GreenUserPlan**: Defines Leaf, Tree, and Forest green plans.

---

## Timeline

### Completed Milestones
- **Backend Development**: Core logic for wallet and transactions.
- **Frontend Prototypes**: Registration, dashboard, and transaction pages.
- **API Integration**: Functional APIs for wallet and user management.

### Upcoming Milestones
- **Dynamic Frontend Features**: Implementing real-time API integration for the web.
- **Mobile App Release**: Launch of Flutter-based GoCash app.
- **Scalability Enhancements**: Dockerized deployment to the cloud.

---

## Setup Guide

### Prerequisites
1. Install Python 3.8 or higher.
2. Install PostgreSQL.
3. Install Node.js and npm for frontend builds.
4. Set up a virtual machine with Ubuntu Linux (if using Windows).

### Installation Steps

#### 1. Clone the repository
```bash
$ git clone <repository-url>
$ cd gocash
```

#### 2. Set up the virtual environment
##### Linux
```bash
$ python3 -m venv env
$ source env/bin/activate
```
##### Windows
```bash
$ python -m venv env
$ env\Scripts\activate
```

#### 3. Install backend dependencies
```bash
(env) $ pip install -r requirements.txt
```

#### 4. Configure environment variables
Create a `.env` file in the root directory with the following variables:
```dotenv
PRODUCTION=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://<username>:<password>@localhost:5432/gocash
```

#### 5. Migrate the database
```bash
(env) $ python manage.py migrate
```

#### 6. Run the development server
```bash
(env) $ python manage.py runserver
```
Access the application at `http://127.0.0.1:8000/`.

---

## Admin Portal

### Features
- User and group management.
- Permissions and privileges assignment.
- Transaction and subscription monitoring.

### Access
Navigate to `http://127.0.0.1:8000/admin/` and log in with an admin account.

---

## Design Highlights

### Dashboard Layout
- **GoCash Card**: Displays user details and wallet balance.
- **Action Buttons**: For wallet charging, money transfers, and subscriptions.
- **Transaction Table**: Shows a paginated view of recent transactions.

### Mobile App
- **Design Language**: Modern UI with intuitive navigation.
- **Flutter Framework**: Cross-platform compatibility.

---

## Testing

### Backend
- Functional tests for APIs using Django TestCase.
- Integration tests with Postman for token-based authentication.

### Frontend
- Manual testing of registration and dashboard pages.
- Plans for automated UI testing with Selenium.

---

## Future Enhancements

1. **Integration of JavaScript for API calls**.
2. **Cloud deployment for scalability**.
3. **Advanced analytics and reporting dashboards**.
4. **Enhanced security measures with 2FA**.

---

## Contributors
- Designed and developed by the GoCash team.

---

## License
GoCash et3-Tomorrow Information Technology Internship-2024
