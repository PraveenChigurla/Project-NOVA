"""
OCR Benchmarking Tool.
Generates comprehensive benchmarks comparing preprocessing modes.
"""
import asyncio
import time
import cv2
import numpy as np
import os
import sys

from nova.providers.vision.ocr.provider import OCRProvider
from nova.providers.vision.ocr.models import OCRConfiguration, OCRMode
from nova.intelligence.vision.models import VisionRequest

def create_synthetic_image(path: str):
    """Creates a synthetic image with text to test OCR on."""
    img = np.zeros((500, 800, 3), dtype=np.uint8)
    # Add noisy background
    cv2.randn(img, (128, 128, 128), (50, 50, 50))
    # Add clear text
    cv2.putText(img, "Project NOVA Vision Pipeline Benchmark", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(img, "Running preprocessors...", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 2)
    cv2.putText(img, "Fast vs Accurate Mode", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imwrite(path, img)

async def run_benchmark():
    print("="*60)
    print("NOVA OCR Preprocessing Benchmark")
    print("="*60)
    
    test_image_path = "benchmark_test_image.png"
    create_synthetic_image(test_image_path)
    print(f"Created synthetic test image: {test_image_path}")
    
    configs = [
        ("Fast (No Preproc)", OCRConfiguration(mode=OCRMode.FAST, enable_preprocessing=False)),
        ("Standard (Scale 1x, No Denoise)", OCRConfiguration(mode=OCRMode.ACCURATE, scale_factor=1.0, enable_denoise=False)),
        ("Accurate (Scale 2x, Denoise)", OCRConfiguration(mode=OCRMode.ACCURATE, scale_factor=2.0, enable_denoise=True))
    ]
    
    print("\n{:<35} | {:<10} | {:<10} | {:<10} | {:<10}".format("Mode", "Pre (ms)", "Inf (ms)", "Post (ms)", "Total (ms)"))
    print("-" * 85)
    
    for name, config in configs:
        provider = OCRProvider(config=config)
        req = VisionRequest(image_path=test_image_path)
        
        # Warmup run (compilation/loading)
        await provider.process(req)
        
        # Measured run
        result = await provider.process(req)
        stats = provider._stats.metrics
        
        print("{:<35} | {:<10.2f} | {:<10.2f} | {:<10.2f} | {:<10.2f}".format(
            name, 
            stats.preprocessing_ms, 
            stats.inference_ms, 
            stats.postprocessing_ms, 
            stats.total_ms
        ))
        
    os.remove(test_image_path)
    print("\nBenchmark complete.")

if __name__ == "__main__":
    asyncio.run(run_benchmark())
