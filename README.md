# Scraper Project

This project is a web scraper designed to scrape product data from a given website, save the data to different storage options (JSON file or SQL database), and notify the designated recipients about the scraping status through various notification strategies (console, SMS, email). The project is built using FastAPI and BeautifulSoup, and it follows the Strategy Design Pattern to allow easy extension and modification of storage and notification strategies.

## Features

- Scrapes product data (title, price, image) from a specified website.
- Supports saving data to JSON files or SQL databases.
- Provides notifications about the scraping status through console, SMS, or email.
- Uses the Strategy Design Pattern for flexible and extensible storage and notification methods.
- Includes type validation and data integrity checks using Pydantic.
- Implements a retry mechanism for handling temporary server issues.

## Prerequisites

- Python 3.8+
- Redis server for caching product prices

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/scraper-project.git
    cd scraper-project
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python3 -m venv scraper_env
    source scraper_env/bin/activate  # On Windows: scraper_env\Scripts\activate
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Configure Redis:**
    Make sure you have Redis installed and running on your machine. You can install Redis using the following commands:
    
    - **macOS:**
      ```sh
      brew install redis
      brew services start redis
      ```
    
    - **Windows:**
      Download and install Redis from [Redis for Windows](https://github.com/microsoftarchive/redis/releases).

## Configuration

1. **Update configuration settings:**
    Edit the `app/settings.py` file to configure the database file path, static token, image folder, and Redis connection parameters.

2. **Configure notification strategies:**
    - **SMS Notification:** Update the `sms_notification.py` with Implementation.
    - **Email Notification:** Update the `email_notification.py` with Implementation.

## Running the Application

1. **Start the FastAPI application:**
    ```sh
    python run.py
    ```

2. **Send the API request to start scraping:**
    - Using cURL (without proxy):
    ```sh
    curl --location 'http://127.0.0.1:8000/scrape' \
    --header 'accept: application/json' \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer your_static_token' \
    --data '{
        "limit": 5
    }'
    ```


3. **Check the output:**
    - For console notifications, the scraping status will be printed in the terminal.
    - For SMS notifications, ensure your phone number and SMS API settings are correctly configured.
    - For email notifications, ensure your SMTP server settings and email addresses are correctly configured.

## Extending the Project

To add new storage or notification strategies, create a new class implementing the respective strategy interface (`StorageStrategy` or `NotificationStrategy`) and update the main application to include the new strategy.

