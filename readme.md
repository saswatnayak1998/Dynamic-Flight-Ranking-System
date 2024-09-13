# Flight Ranking System

## Overview

The Flight Ranking System is a web application that generates optimized flight recommendations based on user and enterprise preferences. The system dynamically balances these preferences using a sophisticated multi-factor ranking algorithm, making it adaptable to changing priorities.

## Key Features

- **Dynamic Weighting System**: Balances user and enterprise preferences with real-time adjustability.
- **Multi-Criteria Decision Analysis (MCDA)**: Scores flights based on a combination of user, enterprise, and inventory preferences.
- **Interactive Frontend**: Built with React, the frontend allows users to input flight preferences and see top recommendations.

## How It Works

1. **User Preferences**: The user specifies their flight criteria such as departure time, arrival time, preferred airline, departure city, destination city, and cabin class.
2. **Enterprise Preferences**: The enterprise can specify its preferred airlines and set cost-saving priorities.
3. **Dynamic Scoring**: A dynamic weighting system balances user and enterprise needs, adjusting the flight scores based on their weights.
4. **Flight Recommendation**: The top 3 flights are recommended based on the combined scores.

## Backend Workflow

1. **Input Processing**:

   - The backend receives user and enterprise preferences, along with weights for each scoring category.
   - The weights determine the importance of each preference in the overall ranking.

2. **Data Filtering**:

   - The backend fetches flight data from the MySQL database based on the user's selected departure time, destination city, departure city, and date with a time buffer.

3. **Scoring Logic**:

   - Each flight is scored using a formula that balances user and enterprise preferences:

     ```
     score = (user_weight * user_preference_score) +
             (enterprise_weight * enterprise_preference_score) +
             (inventory_weight * inventory_score)
     ```

4. **Ranking Flights**:
   - The flights are sorted based on their total score, and the top 3 flights are returned as recommendations.

## Scoring Mechanism Explained

### 1. User Preference Score Calculation

- **Departure Time**: Flights closer to the preferred time receive higher scores. For instance, if the preferred time is 7:00 PM, a flight at 6:30 PM will score `(240 - 30) / 240`.
- **Arrival Time**: Similar to departure time, flights arriving closer to the preferred arrival time receive higher scores.
- **Preferred Airline**: A score of `1` is given if the flight matches the user's preferred airline, otherwise `0`.
- **Cabin Class**: A score of `1` is given if the cabin class matches the user's preference, otherwise `0`.

### 2. Enterprise Preference Score Calculation

- **Preferred Airline**: Enterprise preferences are considered by giving a score of `1` if the airline matches the enterprise's preferred airline.
- **Price Optimization**: Lower-priced flights score higher. The score is calculated as `(max_price - flight_price) / (max_price - min_price)`.

### 3. Inventory Score

- The inventory score is currently set to `0` but can be adjusted in the future to factor in inventory-based optimizations.

## Frontend (React)

The React frontend provides a user-friendly interface to input preferences and displays the top flight recommendations based on the calculated scores.

### Key Components:

- **Form Inputs**: Users can select departure city, destination city, preferred airlines, departure and arrival times, and other flight details.
- **Interactive Controls**: Allows real-time adjustments to the weights of user and enterprise preferences.
- **Dynamic Display**: Shows the top 3 flight recommendations with a visually appealing list format.

### How to Run the Application

1. **Backend**:

   - Ensure MySQL is running with the appropriate schema set up.
   - Run the Flask backend:
     ```bash
     python backend.py
     ```

2. **Frontend**:
   - Navigate to the frontend directory and start the React app:
     ```bash
     npm start
     ```

## Conclusion

The Flight Ranking System balances multiple factors to provide the most relevant flight recommendations. By dynamically adjusting to user and enterprise needs, the system ensures that the best options are always displayed.

For further improvements, consider integrating caching mechanisms, support for round-trip itineraries, and real-time data from external APIs.
