import asyncio
import logging
from datetime import datetime
from config import (
    MODEL_CONFIG,
    SENSOR_CONFIG,
    NEO4J_CONFIG,
    GRAFANA_CONFIG,
    ALERT_CONFIG,
    MONITORING_CONFIG
)
from tensorrt_analyzer import SensorAnalyzer
from advanced_analysis import AdvancedAnalyzer
from alert_manager import AlertManager
from bme680_sensor import BME680Sensor
from neo4j_client import Neo4jClient
from grafana_dashboard import GrafanaDashboard

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedMonitor:
    def __init__(self):
        logger.info('Initializing Enhanced Monitoring System')
        
        # Initialize components
        self.sensor = BME680Sensor(**SENSOR_CONFIG)
        self.analyzer = SensorAnalyzer(MODEL_CONFIG['model_path'])
        self.advanced_analyzer = AdvancedAnalyzer()
        self.alert_manager = AlertManager(ALERT_CONFIG)
        self.neo4j = Neo4jClient(**NEO4J_CONFIG)
        self.grafana = GrafanaDashboard(**GRAFANA_CONFIG)
        
        # Track last analysis times
        self.last_analysis = datetime.now()
        self.last_trend_analysis = datetime.now()
        
    async def sensor_reading_cycle(self):
        """Regular sensor reading cycle"""
        try:
            readings = self.sensor.get_readings()
            
            # Check for alerts
            alerts = self.alert_manager.check_alerts(readings)
            if alerts:
                logger.warning(f'Alerts triggered: {alerts}')
            
            # Store in Neo4j
            self.neo4j.store_readings(readings)
            
            return readings
            
        except Exception as e:
            logger.error(f'Error in sensor reading cycle: {e}')
            return None
    
    async def analysis_cycle(self, readings):
        """Regular analysis cycle"""
        try:
            if readings:
                # Get real-time analysis
                analysis = self.analyzer.analyze_current_readings(readings)
                
                # Store analysis
                self.neo4j.store_analysis(analysis)
                
                # Update Grafana
                self.grafana.update_current_analysis(analysis)
                
        except Exception as e:
            logger.error(f'Error in analysis cycle: {e}')
    
    async def trend_analysis_cycle(self):
        """Periodic trend analysis cycle"""
        try:
            # Get historical readings
            readings_history = self.neo4j.get_historical_readings(hours=24)
            
            # Perform trend analysis
            trends = self.analyzer.analyze_trends(readings_history)
            patterns = self.advanced_analyzer.analyze_patterns(readings_history)
            
            # Check for anomalies
            anomalies = self.advanced_analyzer.detect_anomalies(readings_history)
            if anomalies:
                logger.info(f'Anomalies detected: {anomalies}')
            
            # Store results
            self.neo4j.store_trend_analysis(trends, patterns)
            
            # Update Grafana
            self.grafana.update_trend_analysis(trends, patterns)
            
        except Exception as e:
            logger.error(f'Error in trend analysis cycle: {e}')
    
    async def run(self):
        """Main monitoring loop"""
        logger.info('Starting monitoring system')
        
        while True:
            try:
                # Regular sensor reading
                readings = await self.sensor_reading_cycle()
                
                # Regular analysis if interval elapsed
                now = datetime.now()
                if (now - self.last_analysis).seconds >= MONITORING_CONFIG['analysis']:
                    await self.analysis_cycle(readings)
                    self.last_analysis = now
                
                # Trend analysis if interval elapsed
                if (now - self.last_trend_analysis).seconds >= MONITORING_CONFIG['trend_analysis']:
                    await self.trend_analysis_cycle()
                    self.last_trend_analysis = now
                
                # Wait for next cycle
                await asyncio.sleep(MONITORING_CONFIG['sensor_reading'])
                
            except Exception as e:
                logger.error(f'Error in main monitoring loop: {e}')
                await asyncio.sleep(5)  # Wait before retry

async def main():
    monitor = EnhancedMonitor()
    await monitor.run()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Monitoring system stopped by user')
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
