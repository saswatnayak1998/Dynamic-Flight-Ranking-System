import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [departureCity, setDepartureCity] = useState('');
  const [destinationCity, setDestinationCity] = useState('');
  const [preferredAirline, setPreferredAirline] = useState('');
  const [enterprisePreferredAirline, setEnterprisePreferredAirline] = useState('');
  const [departureTime, setDepartureTime] = useState('');
  const [arrivalTime, setArrivalTime] = useState('');
  const [cabinClass, setCabinClass] = useState('');
  const [flightDate, setFlightDate] = useState('');
  const [userWeight, setUserWeight] = useState(0.5);
  const [enterpriseWeight, setEnterpriseWeight] = useState(0.5);
  const [inventoryWeight, setInventoryWeight] = useState(0);
  const [flightRecommendations, setFlightRecommendations] = useState([]);
  const [submitted, setSubmitted] = useState(false); // New state to track submission

  const airports = [
    { code: 'JFK', name: 'John F. Kennedy International Airport' },
    { code: 'LAX', name: 'Los Angeles International Airport' },
    { code: 'ORD', name: "Chicago O'Hare International Airport" },
    { code: 'DFW', name: 'Dallas/Fort Worth International Airport' },
    { code: 'SFO', name: 'San Francisco International Airport' },
  ];

  const airlines = ['United Airlines', 'Delta', 'American Airlines', 'Air Canada', 'Lufthansa'];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitted(true); // Set submitted to true when the form is submitted

    const preferences = {
      user_preferences: {
        departure_city: departureCity,
        destination_city: destinationCity,
        preferred_airline: preferredAirline,
        departure_time: departureTime,
        arrival_time: arrivalTime,
        cabin_class: cabinClass,
        date: flightDate,
        weight: userWeight,
      },
      enterprise_preferences: {
        preferred_airline: enterprisePreferredAirline,
        weight: enterpriseWeight,
      },
      inventory_weight: inventoryWeight,
    };

    try {
      const response = await axios.post('http://localhost:5000/rank_flightss', preferences);
      setFlightRecommendations(response.data);
    } catch (error) {
      console.error('Error fetching flight recommendations:', error);
    }
  };

  return (
    <div className="App">
      <h1>Flight Ranking System</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Departure City:
          <select value={departureCity} onChange={(e) => setDepartureCity(e.target.value)} required>
            <option value="">Select Departure City</option>
            {airports.map((airport) => (
              <option key={airport.code} value={airport.code}>
                {airport.name}
              </option>
            ))}
          </select>
        </label>
        <br />

        <label>
          Destination City:
          <select value={destinationCity} onChange={(e) => setDestinationCity(e.target.value)} required>
            <option value="">Select Destination City</option>
            {airports.map((airport) => (
              <option key={airport.code} value={airport.code}>
                {airport.name}
              </option>
            ))}
          </select>
        </label>
        <br />

        <label>
          Preferred Airline (User):
          <select value={preferredAirline} onChange={(e) => setPreferredAirline(e.target.value)}>
            <option value="">Select Preferred Airline</option>
            {airlines.map((airline, index) => (
              <option key={index} value={airline}>
                {airline}
              </option>
            ))}
          </select>
        </label>
        <br />

        <label>
          Preferred Airline (Enterprise):
          <select
            value={enterprisePreferredAirline}
            onChange={(e) => setEnterprisePreferredAirline(e.target.value)}
          >
            <option value="">Select Enterprise Preferred Airline</option>
            {airlines.map((airline, index) => (
              <option key={index} value={airline}>
                {airline}
              </option>
            ))}
          </select>
        </label>
        <br />

        <label>
          Flight Date:
          <input type="date" value={flightDate} onChange={(e) => setFlightDate(e.target.value)} required />
        </label>
        <br />

        <label>
          Departure Time:
          <input type="time" value={departureTime} onChange={(e) => setDepartureTime(e.target.value)} />
        </label>
        <br />

        <label>
          Arrival Time:
          <input type="time" value={arrivalTime} onChange={(e) => setArrivalTime(e.target.value)} />
        </label>
        <br />

        <label>
          Cabin Class:
          <select value={cabinClass} onChange={(e) => setCabinClass(e.target.value)}>
            <option value="">Select Cabin Class</option>
            <option value="Economy">Economy</option>
            <option value="Business">Business</option>
            <option value="First">First</option>
          </select>
        </label>
        <br />

        <label>
          User Preference Weight:
          <input
            type="number"
            step="0.1"
            value={userWeight}
            onChange={(e) => setUserWeight(parseFloat(e.target.value))}
          />
        </label>
        <br />

        <label>
          Enterprise Preference Weight:
          <input
            type="number"
            step="0.1"
            value={enterpriseWeight}
            onChange={(e) => setEnterpriseWeight(parseFloat(e.target.value))}
          />
        </label>
        <br />

        <label>
          Inventory Weight:
          <input
            type="number"
            step="0.1"
            value={inventoryWeight}
            onChange={(e) => setInventoryWeight(parseFloat(e.target.value))}
          />
        </label>
        <br />

        <button type="submit">Get Flight Recommendations</button>
      </form>

      <h2>Top 3 Flight Recommendations</h2>
      {submitted && flightRecommendations.length > 0 ? (
        <ul>
          {flightRecommendations.map((flight, index) => (
            <li key={index}>
              Flight {index + 1}: {flight.departure_city} to {flight.destination_city} on{' '}
              {flight.airline} at {flight.departure_time}, arriving at {flight.arrival_time}, Class:{' '}
              {flight.cabin_class}, price of {flight.price}
            </li>
          ))}
        </ul>
      ) : submitted ? (
        <p>No recommendations available.</p>
      ) : (
        <p>Please submit your preferences to see recommendations.</p>
      )}
    </div>
  );
}

export default App;
