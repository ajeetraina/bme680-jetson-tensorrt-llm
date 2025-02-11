import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class AdvancedAnalyzer:
    def __init__(self):
        self.scaler = StandardScaler()
        self.anomaly_detector = IsolationForest(
            contamination=0.1,
            random_state=42
        )
        self.pattern_memory = {}
        
    def analyze_sensor_data(self, readings_history):
        """Comprehensive analysis of sensor data"""
        try:
            # Basic statistical analysis
            stats = self._calculate_statistics(readings_history)
            
            # Pattern detection
            patterns = self._detect_patterns(readings_history)
            
            # Anomaly detection
            anomalies = self._detect_anomalies(readings_history)
            
            # Trend analysis
            trends = self._analyze_trends(readings_history)
            
            return {
                'statistics': stats,
                'patterns': patterns,
                'anomalies': anomalies,
                'trends': trends
            }
        except Exception as e:
            logger.error(f'Error in sensor data analysis: {e}')
            return None
    
    def _calculate_statistics(self, readings):
        """Calculate statistical measures from readings"""
        data = {
            'temperature': [r['temperature'] for r in readings],
            'humidity': [r['humidity'] for r in readings],
            'pressure': [r['pressure'] for r in readings],
            'gas': [r['gas'] for r in readings]
        }
        
        stats = {}
        for metric, values in data.items():
            stats[metric] = {
                'mean': np.mean(values),
                'std': np.std(values),
                'min': np.min(values),
                'max': np.max(values),
                'median': np.median(values)
            }
        
        return stats
    
    def _detect_patterns(self, readings):
        """Detect recurring patterns in sensor data"""
        # Extract hourly patterns
        hourly_patterns = self._analyze_hourly_patterns(readings)
        
        # Extract daily patterns
        daily_patterns = self._analyze_daily_patterns(readings)
        
        # Detect correlations
        correlations = self._analyze_correlations(readings)
        
        return {
            'hourly': hourly_patterns,
            'daily': daily_patterns,
            'correlations': correlations
        }
    
    def _analyze_hourly_patterns(self, readings):
        """Analyze patterns on hourly basis"""
        hours = [r['timestamp'].hour for r in readings]
        metrics = ['temperature', 'humidity', 'pressure', 'gas']
        
        patterns = {}
        for metric in metrics:
            hourly_avg = {}
            for hour, reading in zip(hours, readings):
                if hour not in hourly_avg:
                    hourly_avg[hour] = []
                hourly_avg[hour].append(reading[metric])
            
            patterns[metric] = {
                hour: np.mean(values)
                for hour, values in hourly_avg.items()
            }
        
        return patterns
    
    def _analyze_daily_patterns(self, readings):
        """Analyze patterns on daily basis"""
        days = [r['timestamp'].date() for r in readings]
        metrics = ['temperature', 'humidity', 'pressure', 'gas']
        
        patterns = {}
        for metric in metrics:
            daily_avg = {}
            for day, reading in zip(days, readings):
                if day not in daily_avg:
                    daily_avg[day] = []
                daily_avg[day].append(reading[metric])
            
            patterns[metric] = {
                str(day): np.mean(values)
                for day, values in daily_avg.items()
            }
        
        return patterns
    
    def _analyze_correlations(self, readings):
        """Analyze correlations between different metrics"""
        data = np.array([
            [r['temperature'], r['humidity'], r['pressure'], r['gas']]
            for r in readings
        ])
        
        corr_matrix = np.corrcoef(data.T)
        metrics = ['temperature', 'humidity', 'pressure', 'gas']
        
        correlations = {}
        for i, metric1 in enumerate(metrics):
            for j, metric2 in enumerate(metrics[i+1:], i+1):
                correlations[f'{metric1}_{metric2}'] = corr_matrix[i,j]
        
        return correlations
    
    def _detect_anomalies(self, readings):
        """Detect anomalies in sensor readings"""
        data = np.array([
            [r['temperature'], r['humidity'], r['pressure'], r['gas']]
            for r in readings
        ])
        
        # Scale the data
        scaled_data = self.scaler.fit_transform(data)
        
        # Detect anomalies
        predictions = self.anomaly_detector.fit_predict(scaled_data)
        
        # Get anomaly indices
        anomaly_indices = np.where(predictions == -1)[0]
        
        # Create detailed anomaly report
        anomalies = []
        for idx in anomaly_indices:
            anomalies.append({
                'timestamp': readings[idx]['timestamp'],
                'metrics': {
                    'temperature': readings[idx]['temperature'],
                    'humidity': readings[idx]['humidity'],
                    'pressure': readings[idx]['pressure'],
                    'gas': readings[idx]['gas']
                }
            })
        
        return anomalies
    
    def _analyze_trends(self, readings):
        """Analyze trends in sensor data"""
        metrics = ['temperature', 'humidity', 'pressure', 'gas']
        trends = {}
        
        for metric in metrics:
            values = [r[metric] for r in readings]
            if len(values) < 2:
                trends[metric] = 'Insufficient data'
                continue
            
            # Calculate overall trend
            trend = (values[-1] - values[0]) / len(values)
            
            # Determine trend direction and magnitude
            if abs(trend) < 0.1:
                direction = 'Stable'
            else:
                direction = 'Increasing' if trend > 0 else 'Decreasing'
                magnitude = 'Strong' if abs(trend) > 0.5 else 'Moderate'
                direction = f'{magnitude} {direction}'
            
            trends[metric] = direction
        
        return trends