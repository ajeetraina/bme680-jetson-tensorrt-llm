# TensorRT-LLM Configuration
MODEL_CONFIG = {
    'model_path': '/path/to/optimized_model',
    'max_batch_size': 1,
    'max_sequence_length': 512,
    'precision': 'fp16',  # or 'int8'
    'workspace_size': 8 * 1024 * 1024 * 1024  # 8GB
}

# BME680 Sensor Configuration
SENSOR_CONFIG = {
    'i2c_addr': 0x77,
    'i2c_bus': 1,
    'temperature_offset': 0,
    'humidity_baseline': 40,
    'pressure_baseline': 1013.25
}

# Neo4j Database Configuration
NEO4J_CONFIG = {
    'uri': 'bolt://localhost:7687',
    'user': 'neo4j',
    'password': 'your_password'
}

# Grafana Configuration
GRAFANA_CONFIG = {
    'host': 'localhost:3000',
    'api_key': 'your_api_key',
    'dashboard_uid': 'bme680_analysis'
}

# Alert Configuration
ALERT_CONFIG = {
    'thresholds': {
        'temperature': {'min': 18, 'max': 30},
        'humidity': {'min': 30, 'max': 70},
        'gas': {'min': 5000, 'max': 50000}
    },
    'email': {
        'smtp_server': 'smtp.gmail.com',
        'port': 587,
        'username': 'your-email@gmail.com',
        'password': 'your-app-password',
        'from_addr': 'your-email@gmail.com',
        'to_addrs': ['alerts@yourcompany.com']
    }
}

# Monitoring Intervals (in seconds)
MONITORING_CONFIG = {
    'sensor_reading': 60,  # Read sensor every minute
    'analysis': 300,      # Run analysis every 5 minutes
    'trend_analysis': 3600,  # Run trend analysis every hour
    'alert_check': 60     # Check for alerts every minute
}
