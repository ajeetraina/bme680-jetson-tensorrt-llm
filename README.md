# BME680 Sensor Monitoring with TensorRT-LLM on Jetson

This project integrates BME680 environmental sensor monitoring with advanced AI analytics using TensorRT-LLM on NVIDIA Jetson platforms. It provides real-time analysis, predictive insights, and automated alerts based on sensor data.

## Features

### Core Functionality
- Real-time BME680 sensor data collection
- TensorRT-LLM based environmental analysis
- Advanced anomaly detection
- Predictive analytics
- Neo4j database integration
- Grafana visualization
- Email alert system

### Model Optimization
- FP16 and INT8 quantization support
- Calibration data generation
- Optimized for Jetson platform
- Memory usage optimization

### Analysis Capabilities
- Temperature trend analysis
- Humidity pattern detection
- Air quality assessment
- Anomaly detection
- Predictive maintenance

## Prerequisites

- NVIDIA Jetson device (Nano/Xavier/Orin)
- BME680 sensor
- Python 3.8+
- TensorRT-LLM
- Neo4j Database
- Grafana

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/ajeetraina/bme680-jetson-tensorrt-llm.git
cd bme680-jetson-tensorrt-llm
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Optimize the LLM model:
```bash
# Generate calibration data
python scripts/calibration_data_generator.py --output calibration.pt

# Optimize model with FP16
python scripts/optimize_model.py --model_path /path/to/model --output_path optimized_model --precision fp16

# Or with INT8 quantization
python scripts/optimize_model.py --model_path /path/to/model --output_path optimized_model --precision int8 --calibration_data calibration.pt
```

4. Configure settings in `config.py`

5. Start the monitoring system:
```bash
python src/main.py
```

## Project Structure

```
bme680-jetson-tensorrt-llm/
├── scripts/
│   ├── optimize_model.py
│   └── calibration_data_generator.py
├── src/
│   ├── bme680_sensor.py
│   ├── tensorrt_analyzer.py
│   ├── advanced_analysis.py
│   ├── alert_manager.py
│   ├── neo4j_client.py
│   ├── grafana_dashboard.py
│   └── main.py
├── config.py
└── requirements.txt
```

## Documentation

- [Model Optimization Guide](docs/model_optimization.md)
- [Analysis Features](docs/analysis.md)
- [Alert Configuration](docs/alerts.md)
- [Dashboard Setup](docs/dashboard.md)

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT

## Acknowledgments

- Original BME680 integration based on work by the Collabnix team
- TensorRT-LLM optimization techniques from NVIDIA