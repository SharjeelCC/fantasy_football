# Fantasy Football Platform

This project is a case study implementation of a Fantasy Football Platform using Django. It simulates the management of football teams, player transfers, and transaction history. The project follows a Design-Driven Design (DDD) inspired structure in most of the APIs, providing a well-organized and modular codebase.

## Features

- **User Registration and Profile Management:** Users can register, update their profiles, and manage their teams.
- **Team Management:** When a user registers, a new team is automatically created for them. The team is populated with 20 players divided into different positions: Goalkeepers, Defenders, Midfielders, and Forwards.
- **Player Management:** Players are randomly assigned to teams and can be listed for sale or transferred between teams.
- **Transfer Market:** Users can list players for sale, view players available for sale, and transfer players to other teams.
- **Transaction History:** Keeps a log of player transfers and their associated transaction details.

## Installation

To get the project running on your local machine, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/SharjeelCC/fantasy_football.git

2. **Navigate to the Project Directory:**
   ```bash
   cd fantasy_football

3. **Create a Virtual Environment:**
   ```bash
   python -m venv venv

4. **Activate the Virtual Environment:**

      **On Windows:**
       ```bash
       venv\Scripts\activate

     **On Unix or MacOS:**
         ```bash
         source venv/bin/activate

5. **Install the Requirements:**
   ```bash
   pip install -r requirements.txt

6. **Apply Migrations:**
   ```bash
   python manage.py migrate

7. **Create a Superuser:**
   ```bash
   python manage.py createsuperuser

8. **Run the Development Server:**
   ```bash
   python manage.py runserver

## Usage
  1. **Register a User:** Access the registration endpoint to create a new user. This will automatically create a new team and assign 20 players to it.
  2. **Manage Team:** Use the API to update the team's name, capital, and other details.
  3. **List a Player for Sale:** Players can be listed for sale using the ListPlayerForSaleView API.
  4. **Transfer a Player:** Users can purchase players listed for sale and transfer them to their team using the PlayerTransferView API.
  5. **View Transaction History:** The TransactionHistoryView API allows users to see the history of player transfers.

## API Endpoints
  ## User Endpoints
    1. POST /api/register/ - Register a new user.
    2. GET /api/profile/ - Retrieve user profile.
    3. PUT /api/profile/ - Update user profile.

  ## Team Endpoints
    1. GET /api/teams/ - List all teams.
    2. PUT /api/teams/<team_id>/ - Update team information.

  ## Player Endpoints
    1. POST /api/players/<player_id>/list_for_sale/ - List a player for sale.
    2. POST /api/players/transfer/<player_id>/ - Transfer a player to another team.
    3. GET /api/players/for_sale/ - View players available for sale.

  ## Transaction Endpoints
    1. GET /api/transactions/ - List transaction history.

  ## Design-Driven Design (DDD) Inspired Structure
    We used a Design-Driven Design (DDD) inspired approach in structuring the project. This involves:
    1. Organizing the codebase by domain areas (e.g., Users, Teams, Players).
    2. Creating services for business logic (e.g., list_player_for_sale, transfer_player).
    3. Following clear boundaries between different layers of the application (e.g., views, serializers, models).

  ## Running Tests
    We used pytest for testing the application. To run the tests, follow these steps:

  1. **Install pytest:**
     ```bash
      pip install pytest

  2. **Run the tests:**
     ```bash
     pytest

## Technologies Used
  1. **Backend Framework:** Django, Django REST Framework
  2. **Database:** SQLite (default), can be replaced with PostgreSQL or another database
  3. **Testing:** pytest
  4. **Authentication:** JWT with Django REST Framework Simple JWT
  5. **Containerization:** Docker

## Dockerization
1. **Build the Docker image:** 
    ```bash
    docker build -t fantasy-football
2. **Build the Docker image:** 
    ```bash
    docker-compose up

## Additional Considerations

    1. Robust error handling and data validation are implemented.
    2. Performance optimizations for handling large datasets can be considered for future enhancements.

## Code Style

    This project uses `flake8` to ensure PEP 8 compliance.
    To check your code for PEP 8 violations, run:

    ```bash
    flake8 .

## Folder Structure
  ```bash
  fantasy_football/
├── players/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── services.py
│   └── tests/
├── teams/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── tests/
├── users/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── signals.py
│   └── tests/
└── fantasy_football/
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    └── asgi.py




    






