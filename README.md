# Gracehopper API

## Purpose
This project is part of the Gracehopper AI Software Engineer Internship. It aims to develop an API backend using Django, Django REST Framework, and Redis to handle product and category data, with features such as caching, filtering, and efficient querying.

## Features
- **Product and Category Management**: Endpoints for creating, retrieving, updating, and deleting product and category entries.
- **Caching with Redis**: Utilizes Django Redis for caching frequently accessed data, improving response times.
- **Django Filters**: Implements filtering for product and category lists for easy data retrieval.
- **Unit Testing**: Comprehensive unit tests to ensure functionality and correctness of the API endpoints.

## Project Structure
```
.
├── apps
│   ├── api
│   │   └── v1
│   │       └── category
│   │       └── product
│   │       └── tests
│   ├── config
│   │   └── asgi.py
│   │   └── settings.py
│   │   └── urls.py
│   │   └── wsgi.py
├── requirements.txt
├── manage.py
└── README.md
```

- `apps/api/v1`: Contains the core API functionality, including the `category` and `product` modules for handling data.
- `apps/config`: Contains configurations such as settings and database configurations.
  
## Postman Documentation
For detailed API documentation, you can find the Postman collection [here](https://github.com/algavania/gracehopper_api/blob/main/postman_collection.json).

## Unit Testing
Unit tests have been implemented for both the `category` and `product` modules to ensure the API endpoints work as expected. The tests include:
- Verifying the correct retrieval of data.
- Testing Redis cache for performance.
- Checking API responses against various edge cases.

To run tests, use the following command:
```
python3 manage.py test apps.api.v1.tests
```

## Redis Configuration

To configure Redis, go to `config/settings.py` and locate the `# Redis cache configuration` section. Update the `LOCATION` field to match your Redis server URL and port:

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',  # Update this with your Redis URL and port
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'TIMEOUT': 300,  # 5 minutes
    }
}
```

## Installing and Running Redis

### On Mac (Using Homebrew)

1. Install Redis via Homebrew:
   ```
   brew install redis
   ```

2. Start Redis:
   ```
   redis-server
   ```

   This will start Redis on the default port `6379`. You can verify it's running by checking if it's listening on that port:
   ```
   redis-cli ping
   ```

3. If you need to stop Redis, run:
   ```
   redis-server stop
   ```

### On Linux (Using apt)

1. Install Redis:
   ```
   sudo apt update
   sudo apt install redis-server
   ```

2. Start Redis:
   ```
   sudo systemctl start redis-server
   ```

3. Verify Redis is running:
   ```
   redis-cli ping
   ```

4. If you want Redis to start automatically on boot:
   ```
   sudo systemctl enable redis-server
   ```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/algavania/gracehopper_api.git
   ```

2. Install dependencies:
   ```
   pip3 install -r requirements.txt
   ```

3. Run the development server:
   ```
   python3 manage.py runserver
   ```

4. Ensure Redis is running locally on the default port or update the settings if necessary.
