# Alert System Configuration

## Overview

The alert system monitors environmental conditions and triggers notifications based on predefined thresholds and anomaly detection.

## Alert Types

### 1. Threshold-based Alerts
```python
ALERT_THRESHOLDS = {
    'temperature': {'min': 18, 'max': 30},
    'humidity': {'min': 30, 'max': 70},
    'gas': {'min': 5000, 'max': 50000}
}
```

### 2. Anomaly-based Alerts
- Pattern deviation detection
- Sudden change alerts
- Trend deviation notifications

### 3. Predictive Alerts
- Trend-based warnings
- Maintenance predictions
- Capacity planning alerts

## Configuration

### Email Notifications
```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'port': 587,
    'username': 'your-email@gmail.com',
    'password': 'your-app-password',
    'from_addr': 'your-email@gmail.com',
    'to_addrs': ['alerts@yourcompany.com']
}
```

### Alert Levels
1. INFO: General information
2. WARNING: Attention needed
3. CRITICAL: Immediate action required

## Implementation

### Alert Manager Class
```python
class AlertManager:
    def __init__(self, config):
        self.thresholds = config['thresholds']
        self.email_config = config['email']
        self.alert_history = []

    def check_alerts(self, readings):
        alerts = []
        for metric, value in readings.items():
            if metric in self.thresholds:
                if value < self.thresholds[metric]['min']:
                    alerts.append(self._create_alert(metric, value, 'low'))
                elif value > self.thresholds[metric]['max']:
                    alerts.append(self._create_alert(metric, value, 'high'))
        return alerts
```

## Alert Formatting

### Example Alert Message
```
ALERT: High Temperature Detected
Timestamp: 2025-02-11 08:30:00
Value: 32.5°C
Threshold: 30°C
Location: Sensor-1
Recommended Action: Check ventilation system
```

## Integration

### With Neo4j
```cypher
CREATE (a:Alert {
    type: 'temperature_high',
    value: 32.5,
    threshold: 30,
    timestamp: datetime(),
    status: 'active'
})
```

### With Grafana
```python
def create_alert_panel(self):
    return {
        'title': 'Active Alerts',
        'type': 'table',
        'targets': [{
            'query': '''
            MATCH (a:Alert)
            WHERE a.status = 'active'
            RETURN a.type, a.value, a.timestamp
            ORDER BY a.timestamp DESC
            '''
        }]
    }
```

## Best Practices

1. Alert Throttling
   - Implement cooldown periods
   - Group similar alerts
   - Prevent alert storms

2. Alert Prioritization
   - Define clear severity levels
   - Set appropriate thresholds
   - Configure escalation paths

3. Alert Management
   - Track alert history
   - Monitor false positives
   - Regular threshold review

4. Response Procedures
   - Document response steps
   - Define escalation paths
   - Track resolution times

## Testing

### Alert Testing Script
```python
def test_alerts():
    manager = AlertManager(config)
    
    # Test temperature alert
    readings = {
        'temperature': 35,  # Above threshold
        'humidity': 50,
        'gas': 10000
    }
    
    alerts = manager.check_alerts(readings)
    assert len(alerts) > 0, 'Alert should be triggered'
```

## Maintenance

1. Regular Review
   - Threshold adjustments
   - Alert patterns analysis
   - False positive reduction

2. System Updates
   - Configuration updates
   - Alert rule refinement
   - Integration maintenance