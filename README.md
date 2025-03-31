# Portfolio Tracker Application

A Flask-based web application for tracking investment portfolios.

## Local Development Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with the following variables:
```
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=sqlite:///app.db
SECRET_KEY=your-secret-key-here
```

4. Initialize the database:
```bash
flask db upgrade
```

5. Run the application:
```bash
flask run
```

## Deployment to Google Cloud Platform

### Prerequisites

1. Install Google Cloud SDK
2. Create a Google Cloud Project
3. Enable App Engine API
4. Enable Cloud SQL API (if using Cloud SQL)

### Deployment Steps

1. Create a new `app.yaml` file from the template:
```bash
cp app.yaml.template app.yaml
```

2. Update `app.yaml` with your configuration:
- Add your environment variables
- Configure Cloud SQL instance (if using Cloud SQL)
- Update instance class if needed

3. Deploy to App Engine:
```bash
gcloud app deploy
```

4. View your application:
```bash
gcloud app browse
```

### Database Setup on GCP

1. For Cloud SQL:
   - Create a Cloud SQL instance
   - Create a database
   - Update `app.yaml` with the connection details
   - Deploy the application
   - Run migrations:
   ```bash
   gcloud app instances ssh [INSTANCE_NAME] --command="python -m flask db upgrade"
   ```

2. For SQLite (not recommended for production):
   - Use Cloud Storage to store the SQLite file
   - Update the application to use Cloud Storage for persistence

## Version Control with GitHub

1. Initialize Git repository:
```bash
git init
```

2. Create a new repository on GitHub (without initializing with README)

3. Add remote origin:
```bash
git remote add origin https://github.com/username/repository.git
```

4. Create and switch to main branch:
```bash
git branch -M main
```

5. Make your first commit:
```bash
git add .
git commit -m "Initial commit"
```

6. Push to GitHub:
```bash
git push -u origin main
```

### Important Notes

- Never commit sensitive data (`.env`, `app.yaml`, credentials) to GitHub
- Keep your production database credentials secure
- Regularly backup your database
- Monitor your application using Google Cloud Console
- Set up proper authentication and authorization
- Configure SSL certificates for production

## Maintenance

- Regularly update dependencies
- Monitor application logs
- Set up alerts for errors
- Implement proper backup strategies
- Monitor costs and resource usage

## Features

- User Authentication (Login/Registration)
- Portfolio Management (Add/Edit/Delete investments)
- Dashboard with Interactive Charts
- Investment Type Configuration
- Support for multiple investment types and modes
- Real-time calculations and visualizations

## Technology Stack

- Backend: Flask (Python)
- Database: SQLAlchemy with SQLite
- Frontend: HTML, CSS, JavaScript
- Charts: Plotly.js
- Authentication: Flask-Login

## Project Structure

```
portfolio_tracker/
├── app/
│   ├── models/         # Database models
│   ├── static/         # Static files (CSS, JS)
│   ├── templates/      # HTML templates
│   └── routes/         # Route handlers
├── migrations/         # Database migrations
├── requirements.txt    # Project dependencies
└── config.py          # Configuration settings
``` 