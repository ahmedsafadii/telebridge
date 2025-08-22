# TeleBridge

A Django-based Telegram bridge application that allows you to manage Telegram accounts, monitor channels, and forward/copy messages between different Telegram sources and targets.

## 🚀 Features

### Core Functionality
- **Multi-Account Telegram Management**: Connect and manage multiple Telegram accounts through Django admin
- **Channel/Source Management**: Add and monitor Telegram channels and groups
- **Message Bridging**: Copy or forward messages between different Telegram sources and targets
- **Session Management**: Persistent Telegram session handling with validation
- **Real-time Processing**: Asynchronous message processing using Celery

### Admin Interface
- **Account Management**: Add, edit, and monitor Telegram accounts
- **Source Configuration**: Configure public/private channels with validation
- **Target Mapping**: Set up destination channels or email targets
- **Rule Engine**: Whitelist/blacklist, text replacement, URL cleanup
- **Monitoring**: Real-time status checking and validation

## 🏗️ Architecture

### Technology Stack
- **Backend**: Django 4.x
- **Database**: PostgreSQL
- **Cache/Queue**: Redis
- **Task Queue**: Celery
- **Telegram API**: Telethon
- **Admin Interface**: Django Admin (customized)

### Project Structure
```
telebridge/
├── manage.py
├── requirements.txt
├── .env.example
├── README.md
├── telebridge/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── accounts/
│   │   ├── models.py
│   │   ├── admin.py
│   │   ├── views.py
│   │   └── tasks.py
│   ├── sources/
│   │   ├── models.py
│   │   ├── admin.py
│   │   ├── views.py
│   │   └── tasks.py
│   ├── targets/
│   │   ├── models.py
│   │   ├── admin.py
│   │   └── views.py
│   └── core/
│       ├── models.py
│       ├── admin.py
│       └── utils.py
├── static/
├── templates/
└── media/
```

## 📋 Roadmap & Milestones

### ✅ M1: Bootstrap (Completed)
- [x] Django project, Postgres, Redis, Celery integration
- [x] Base apps and models skeletons
- [x] Admin registration

### ✅ M2: Telethon Integration (Partially Completed)
- [x] Multi-account login flow from Admin (code/2FA)
- [x] Session persistence
- [ ] Basic channel discovery/validation

### 🔄 M3: Sources & Targets (In Progress)
- [ ] Create/edit sources (public/private)
- [ ] Create targets (Telegram/email) and mapping
- [ ] Copy vs forward support

### ⏳ M4: Rule Engine (Planned)
- [ ] Whitelist/blacklist
- [ ] Replace rules
- [ ] URL removal/cleanup
- [ ] `show_source` prepend

### ⏳ M5: Processing & Delivery (Planned)
- [ ] Ingestion worker + pipeline
- [ ] Fan-out to multiple targets
- [ ] Delivery logging + Admin views

### ⏳ M6: Housekeeping & Observability (Planned)
- [ ] Periodic cleanup (every X)
- [ ] Flower setup and basic dashboards

### ⏳ M7: Hardening (Planned)
- [ ] Idempotency, retries, backoff
- [ ] Permissions and audit
- [ ] Tests

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- PostgreSQL
- Redis
- Telegram API credentials

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd telebridge
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment configuration**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Database setup**
```bash
python manage.py migrate
python manage.py createsuperuser
```

6. **Start services**
```bash
# Start Redis
redis-server

# Start Celery worker (in new terminal)
celery -A telebridge worker -l info

# Start Celery beat (in new terminal)
celery -A telebridge beat -l info

# Start Django development server
python manage.py runserver
```

## 🔧 Configuration

### Environment Variables
```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/telebridge

# Redis
REDIS_URL=redis://localhost:6379/0

# Telegram API
TELEGRAM_API_ID=your-api-id
TELEGRAM_API_HASH=your-api-hash

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Telegram API Setup
1. Go to https://my.telegram.org/
2. Log in with your phone number
3. Create a new application
4. Copy the API ID and API Hash
5. Add them to your environment variables

## 📖 Usage

### Adding a Telegram Account
1. Go to Django Admin → Accounts → Telegram accounts
2. Click "Add telegram account"
3. Fill in the account details (name, phone number, API credentials)
4. Save and use the "START LOGIN" action to authenticate
5. Enter the verification code when prompted

### Adding a Source Channel
1. Go to Django Admin → Accounts → Sources
2. Click "Add source"
3. Select the Telegram account
4. Enter the channel identifier (username, ID, or invite link)
5. Choose the mode (Copy or Forward)
6. Configure additional settings as needed

### Setting up Targets
1. Go to Django Admin → Targets
2. Add target channels or email addresses
3. Configure the mapping between sources and targets

## 🔒 Security Considerations

- Store Telegram API credentials securely
- Use environment variables for sensitive data
- Implement proper user authentication and authorization
- Regular session validation and cleanup
- Monitor for suspicious activities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the admin interface for configuration options

## 🔄 Development Status

This project is currently in active development. The core functionality is implemented with the admin interface working. The next phase focuses on completing the message processing pipeline and rule engine.
