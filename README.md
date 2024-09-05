# Subscription Tracker

Subscription Tracker is a web application built with Flask that helps users manage and track their subscriptions. Users can add, view, edit, and delete subscriptions, as well as see the total monthly cost of all their subscriptions.

## Features

- User registration and authentication
- Add, edit, view, and delete subscriptions
- Display total monthly subscription cost
- Responsive design for mobile and desktop
- Password reset functionality

## Technologies Used

- Python
- Flask
- SQLAlchemy
- Flask-Login
- Flask-Mail
- Tailwind CSS

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/subscription-tracker.git
   cd subscription-tracker
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install flask flask-sqlalchemy flask-login werkzeug flask-migrate flask-mail itsdangerous
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add the following:
   ```
   SECRET_KEY=your_secret_key
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_email_password
   ```

5. Initialize the database:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

## Running the Application

To run the application, use the following command:

```
python app.py
```

The application will be available at `http://127.0.0.1:5000/`.

## Usage

1. Register a new account or log in with existing credentials.
2. Add new subscriptions using the "Add Subscription" button.
3. View, edit, or delete existing subscriptions from the main dashboard.
4. Use the "My Subscriptions" link in the navigation bar to return to the main dashboard.
5. Update your password or log out using the profile and logout links in the navigation bar.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
