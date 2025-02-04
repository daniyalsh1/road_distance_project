Road Distance Calculator

Overview

This project provides a Python-based solution to calculate distances between cities using various geolocation APIs. It is designed to integrate with Django and includes models for storing city and province data.

Features:

  Retrieve distance between two cities

  Support for multiple geolocation APIs (e.g., OpenCage, OpenRouteService)

  Django models for managing city and province data

  Easily extendable for additional distance calculation methods

Installation

  Clone the repository:

  git clone https://github.com/YOUR_USERNAME/road_distance_project.git
  cd road_distance_project

  Create and activate a virtual environment:

  python3 -m venv venv
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install dependencies:

  pip install -r requirements.txt


Example: Calculating Distance

from road_distance.distance import RouteInfo

distance_calculator = RouteInfo()
distance = distance_calculator.get_route('123456', '123123')  # Tehran: 123456 / Mashhad: 123123
print(f"Distance: {distance} km")

Configuration:

  API keys for geolocation services should be stored in environment variables or a configuration file.
  
  Django models (City, Province) can be migrated using:

  python manage.py makemigrations
  python manage.py migrate

License:

  This project is licensed under the MIT License.

Contributing:‌

  Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

