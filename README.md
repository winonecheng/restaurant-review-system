# Restaurant Review System API

A simple restaurant review system built with Django and Django Rest Framework.

## Setup and Installation

### Standard Setup

1. Clone the repository
2. Set up a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Apply migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Run the server: `python manage.py runserver`

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
4. The API will be available at http://localhost:8000
5. Create a superuser in the Docker container:
   ```
   docker exec -it $(docker ps -q --filter ancestor=restaurant-review-system) python manage.py createsuperuser
   ```

> **Note:** Mounting a volume for the SQLite database ensures your data persists even when the container is stopped or removed. Make sure your Django settings are configured to store the database file in the `/app/data` directory.

## API Documentation

### Authentication

The API uses Django's session authentication. You can log in via:
- Django admin interface at `/admin/`
- Django REST framework's browsable API at `/api-auth/login/`

### Restaurants

#### List all restaurants
- **GET** `/api/restaurants/`
- Query Parameters:
  - `cuisine_type`: Filter by cuisine type (e.g., Italian, Chinese)
  - `sort_by_score`: Set to any value to sort by average score

#### Get a specific restaurant
- **GET** `/api/restaurants/{id}/`

#### Create a new restaurant
- **POST** `/api/restaurants/`
- Authentication required
- Example request body:
```
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
```
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

## Feature Extensions (Optional)

### Restaurant Recommendation API

To implement a simple recommendation system, we could:

- **GET** `/api/recommendations/`
- Returns restaurants that match user preferences based on:
  - Previous high-rated restaurants
  - Cuisine types frequently rated highly
  - Restaurants highly rated by users with similar taste profiles