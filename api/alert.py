from flask import Flask, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load the synthetic crime data
def load_crime_data():
    try:
        return pd.read_csv("synthetic_crime_data_mumbai.csv")
    except Exception as e:
        print("Error loading data:", e)
        return pd.DataFrame()  # Return an empty DataFrame if loading fails

crime_data = load_crime_data()

# Function to determine proximity to hotspots
def is_near_hotspot(user_location, crime_data, radius_threshold=0.02):
    user_lat = user_location['latitude']
    user_lon = user_location['longitude']
    
    if crime_data.empty:
        return []

    distances = np.sqrt((crime_data['latitude'] - user_lat)**2 + (crime_data['longitude'] - user_lon)**2)
    nearby_indices = distances[distances < radius_threshold].index
    nearby_incidents = crime_data.iloc[nearby_indices]
    return nearby_incidents.to_dict(orient='records')

# API endpoint for alerts
@app.route('/api/alert', methods=['GET'])
def get_alerts():
    try:
        user_lat = float(request.args.get('latitude'))
        user_lon = float(request.args.get('longitude'))
        nearby_incidents = is_near_hotspot({'latitude': user_lat, 'longitude': user_lon}, crime_data)
        return jsonify(nearby_incidents), 200
    except ValueError:
        return jsonify({"error": "Invalid input"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Local testing entry point
if __name__ == "__main__":
    app.run(debug=True)
