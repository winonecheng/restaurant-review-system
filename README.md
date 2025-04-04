# Restaurant Review System API

A simple restaurant review system built with Django and Django Rest Framework.

## Setup and Installation

### Standard Setup

1. Clone the repository
2. Set up a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create migrations for each app:
   ```
   python manage.py makemigrations users
   python manage.py makemigrations restaurants
   python manage.py makemigrations reviews
   ```
6. Apply migrations: `python manage.py migrate`
7. Create a superuser: `python manage.py createsuperuser`
8. Run the server: `python manage.py runserver`

### Docker Setup

You can also run this application using Docker:

1. Make sure Docker is installed on your system
2. Build the Docker image:
   ```
   docker build -t restaurant-review-system .
   ```
3. Run the container with a volume mount for the database:
   ```
   docker run -d -p 8000:8000 -v $(pwd)/data:/app/data restaurant-review-system
   ```
   This mounts a local `data` directory to `/app/data` in the container, where SQLite database will be stored.
ˋ. Create a superuser in the Docker container:
   ```
   docker exec -it $(docker ps -q --filter ancestor=restaurant-review-system) python manage.py createsuperuser
   ```

## API Documentation

### Authentication

The API supports token-based authentication. You can obtain a token via:

#### Register a new user
- **POST** `/api/auth/register/`
- Example request body:
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "securepassword"
}
```
- Example response:
```json
{
  "token": "your_auth_token",
  "user_id": 1,
  "username": "newuser",
  "email": "user@example.com"
}
```

#### Login with existing user
- **POST** `/api/auth/login/`
- Example request body:
```json
{
  "username": "existinguser",
  "password": "yourpassword"
}
```
- Example response:
```json
{
  "token": "your_auth_token",
  "user_id": 1,
  "username": "existinguser",
  "email": "user@example.com"
}
```

#### Using the token
Include the token in the Authorization header for authenticated requests:
```
Authorization: Token your_auth_token
```

### Restaurants

#### List all restaurants
- **GET** `/api/restaurants/`
- Query Parameters:
  - `cuisine_type`: Filter by cuisine type (e.g., Italian, Chinese)
  - `sort_by_score`: Set to any value to sort by average score
  - `search`: Search restaurants by name or address

#### Get a specific restaurant
- **GET** `/api/restaurants/{id}/`

#### Create a new restaurant
- **POST** `/api/restaurants/`
- Authentication required
- Example request body:
```json
{
  "name": "Restaurant Name",
  "address": "123 Main St",
  "cuisine_type": "Italian"
}
```

#### Update a restaurant
- **PUT/PATCH** `/api/restaurants/{id}/`
- Authentication required

#### Delete a restaurant
- **DELETE** `/api/restaurants/{id}/`
- Authentication required

### Reviews

#### List all reviews
- **GET** `/api/reviews/`
- Query Parameters:
  - `restaurant`: Filter by restaurant ID
  - `user`: Filter by user ID
  - `restaurant_id`: Alternative filter by restaurant ID
  - `user_id`: Alternative filter by user ID
  - `ordering`: Order by field (e.g., `created_at`, `-score`)

#### Get a specific review
- **GET** `/api/reviews/{id}/`

#### Create a new review
- **POST** `/api/reviews/`
- Authentication required
- Body:
```json
{
  "restaurant": 1,
  "score": 5,
  "comment": "Great food and service!"
}
```

#### Update a review
- **PUT/PATCH** `/api/reviews/{id}/`
- Authentication required
- Only the owner of the review can update it

#### Delete a review
- **DELETE** `/api/reviews/{id}/`
- Authentication required
- Only the owner of the review can delete it

## Testing with cURL

Here are some examples of how to test the API with cURL:

### Authentication
```bash
# Register a new user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123", "email": "test@example.com"}'

# Login to get token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'

# Save token for later use
export TOKEN="your_token_here"
```

### Restaurants
```bash
# List all restaurants
curl -X GET http://localhost:8000/api/restaurants/

# Create a new restaurant
curl -X POST http://localhost:8000/api/restaurants/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Italian Bistro",
    "address": "123 Pasta Avenue, Food City",
    "cuisine_type": "Italian"
  }'

# Get a specific restaurant
curl -X GET http://localhost:8000/api/restaurants/1/

# Update a restaurant
curl -X PATCH http://localhost:8000/api/restaurants/1/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Restaurant Name"}'

# Delete a restaurant
curl -X DELETE http://localhost:8000/api/restaurants/1/ \
  -H "Authorization: Token $TOKEN"
```

### Reviews
```bash
# List all reviews
curl -X GET http://localhost:8000/api/reviews/

# Create a review
curl -X POST http://localhost:8000/api/reviews/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "restaurant": 1,
    "score": 4,
    "comment": "Great food and service!"
  }'

# Update your review
curl -X PATCH http://localhost:8000/api/reviews/1/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"score": 5, "comment": "Updated: The food was amazing!"}'

# Delete your review
curl -X DELETE http://localhost:8000/api/reviews/1/ \
  -H "Authorization: Token $TOKEN"
```
