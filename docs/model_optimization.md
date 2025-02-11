# Model Optimization Guide for BME680 Analysis

This guide explains how to optimize and quantize your LLM models for use with TensorRT-LLM on NVIDIA Jetson platforms.

## Model Options

For environmental data analysis, we recommend using one of these models:

1. Small models (suitable for Jetson Nano):
   - BERT-tiny (4.4M parameters)
   - DistilBERT (66M parameters)
   - GPT-2 small (117M parameters)

2. Medium models (suitable for Jetson Xavier/Orin):
   - BERT-base (110M parameters)
   - GPT-2 medium (345M parameters)
   - T5-small (60M parameters)

## Optimization Process

### 1. FP16 Optimization

```bash
# Basic FP16 optimization
python scripts/optimize_model.py \
    --model_path /path/to/model \
    --output_path optimized_model \
    --precision fp16
```

### 2. INT8 Quantization

```bash
# Generate calibration data
python scripts/calibration_data_generator.py \
    --output calibration.pt \
    --samples 1000

# Perform INT8 quantization
python scripts/optimize_model.py \
    --model_path /path/to/model \
    --output_path quantized_model \
    --precision int8 \
    --calibration_data calibration.pt
```

## Memory Optimization

1. Set appropriate batch size:
```python
config = ModelConfig(
    max_batch_size=1,  # Adjust based on your needs
    max_input_len=512,
    max_output_len=128
)
```

2. Enable attention caching:
```python
builder_config = {
    'enable_attention_caching': True,
    'attention_cache_size': 1024
}
```

3. Use workspace size limits:
```python
builder.max_workspace_size = 4 * 1024 * 1024 * 1024  # 4GB
```

## Performance Comparison

Typical performance metrics on Jetson platforms:

| Model Size | Precision | Memory Usage | Inference Time | Accuracy |
|------------|-----------|--------------|----------------|----------|
| Small      | FP16      | 500MB       | 50ms          | 95%      |
| Small      | INT8      | 250MB       | 30ms          | 93%      |
| Medium     | FP16      | 2GB         | 150ms         | 98%      |
| Medium     | INT8      | 1GB         | 80ms          | 96%      |

## Best Practices

1. Start with FP16 precision for development
2. Use INT8 quantization for deployment
3. Monitor memory usage during inference
4. Use appropriate batch sizes
5. Enable attention caching for longer sequences
6. Profile your model with different configurations

## Troubleshooting

### Common Issues

1. Out of Memory (OOM)
   - Reduce batch size
   - Use INT8 quantization
   - Reduce model size

2. Slow Inference
   - Enable FP16 or INT8
   - Optimize attention caching
   - Check system resources

3. Accuracy Issues
   - Validate calibration data
   - Try different quantization methods
   - Adjust model architecture
