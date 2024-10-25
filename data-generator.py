# generate_data.py
import pandas as pd
import numpy as np
from scipy import stats
import os

def generate_missing_values(data, missing_rate=0.05):
    """Generate missing values randomly"""
    mask = np.random.random(len(data)) < missing_rate
    data[mask] = np.nan
    return data

def add_noise(data, noise_level=0.02):
    """Add Gaussian noise to the data"""
    noise = np.random.normal(0, noise_level * np.std(data), len(data))
    return data + noise

def add_outliers(data, outlier_rate=0.02, outlier_range=(-3, 3)):
    """Add outliers to the data"""
    mask = np.random.random(len(data)) < outlier_rate
    outliers = np.random.uniform(outlier_range[0], outlier_range[1], size=sum(mask))
    data[mask] = outliers * np.std(data) + np.mean(data)
    return data

def generate_stock_data(start_date, end_date):
    """Generate stock price data with realistic patterns"""
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    n_points = len(dates)
    
    # Base trend with momentum
    returns = np.random.normal(0.0002, 0.02, n_points)
    price = 100 * np.exp(np.cumsum(returns))
    
    # Add seasonality
    t = np.linspace(0, 1, n_points)
    weekly_pattern = 2 * np.sin(2 * np.pi * t * 52)  # Weekly seasonality
    monthly_pattern = 5 * np.sin(2 * np.pi * t * 12)  # Monthly seasonality
    
    values = price + weekly_pattern + monthly_pattern
    
    # Add noise and anomalies
    values = add_noise(values, 0.01)
    values = add_outliers(values, 0.01)
    values = generate_missing_values(values, 0.03)
    
    return pd.DataFrame({'date': dates, 'value': values})

def generate_sales_data(start_date, end_date):
    """Generate sales data with realistic patterns"""
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    n_points = len(dates)
    
    # Base trend (growing)
    t = np.linspace(0, 1, n_points)
    trend = 1000 + 500 * t
    
    # Seasonal components
    yearly = 200 * np.sin(2 * np.pi * t)  # Yearly seasonality
    weekly = 50 * np.sin(2 * np.pi * t * 52)  # Weekly seasonality
    
    # Special events (holidays, promotions)
    special_events = np.zeros(n_points)
    event_dates = np.random.choice(n_points, size=int(n_points * 0.05), replace=False)
    special_events[event_dates] = np.random.uniform(100, 300, len(event_dates))
    
    values = trend + yearly + weekly + special_events
    
    # Add noise and anomalies
    values = add_noise(values, 0.02)
    values = add_outliers(values, 0.02)
    values = generate_missing_values(values, 0.05)
    
    return pd.DataFrame({'date': dates, 'value': values})

def generate_weather_data(start_date, end_date):
    """Generate weather data with realistic patterns"""
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    n_points = len(dates)
    
    # Base temperature with yearly seasonality
    t = np.linspace(0, 1, n_points)
    yearly = 20 + 15 * np.sin(2 * np.pi * t)  # Temperature range: 5°C to 35°C
    
    # Add daily variations
    daily = 5 * np.sin(2 * np.pi * t * 365)
    
    # Add weather patterns (few days of consistent deviation)
    weather_patterns = np.zeros(n_points)
    pattern_length = 5  # 5-day weather patterns
    
    for i in range(0, n_points, pattern_length):
        pattern = np.random.normal(0, 2, pattern_length)
        weather_patterns[i:i+pattern_length] = pattern
    
    values = yearly + daily + weather_patterns
    
    # Add noise and anomalies
    values = add_noise(values, 0.01)
    values = add_outliers(values, 0.01)
    values = generate_missing_values(values, 0.02)
    
    return pd.DataFrame({'date': dates, 'value': values})

def main():
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate data for 3 years
    start_date = '2021-01-01'
    end_date = '2023-12-31'
    
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Generate and save stock data
    stock_data = generate_stock_data(start_date, end_date)
    stock_data.to_csv('data/stock_data.csv', index=False)
    print(f"Stock data generated: {stock_data.shape[0]} rows")
    
    # Generate and save sales data
    sales_data = generate_sales_data(start_date, end_date)
    sales_data.to_csv('data/sales_data.csv', index=False)
    print(f"Sales data generated: {sales_data.shape[0]} rows")
    
    # Generate and save weather data
    weather_data = generate_weather_data(start_date, end_date)
    weather_data.to_csv('data/weather_data.csv', index=False)
    print(f"Weather data generated: {weather_data.shape[0]} rows")

if __name__ == "__main__":
    main()
