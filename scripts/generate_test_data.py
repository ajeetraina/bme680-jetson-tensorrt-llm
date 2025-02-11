import random
from datetime import datetime, timedelta
from neo4j import GraphDatabase
import time

class Neo4jDataGenerator:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def generate_sensor_data(self):
        return {
            'temperature': round(random.uniform(20.0, 30.0), 2),  # 20-30°C
            'humidity': round(random.uniform(30.0, 70.0), 2),     # 30-70%
            'pressure': round(random.uniform(980.0, 1020.0), 2),  # 980-1020 hPa
            'gas_resistance': round(random.uniform(5000, 50000), 2)  # 5k-50k Ω
        }

    def store_reading(self, reading):
        with self.driver.session() as session:
            session.run("""
            CREATE (r:Reading {
                timestamp: datetime(),
                temperature: $temperature,
                humidity: $humidity,
                pressure: $pressure,
                gas_resistance: $gas_resistance
            })
            """, reading)

    def continuous_generation(self, interval=5):
        try:
            while True:
                reading = self.generate_sensor_data()
                self.store_reading(reading)
                print(f"Stored reading: {reading}")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nStopping data generation...")
        finally:
            self.driver.close()

if __name__ == "__main__":
    generator = Neo4jDataGenerator(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"  # Replace with your password
    )
    
    print("Starting data generation. Press Ctrl+C to stop.")
    generator.continuous_generation()
