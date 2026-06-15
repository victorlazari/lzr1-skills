# Computer Vision

## Table of Contents
1. CV System Architecture
2. Image Classification
3. Object Detection
4. Segmentation
5. Multimodal Vision
6. Production CV Systems

---

## 1. CV System Architecture

### Standard CV Pipeline

```
Image/Video Input → Preprocessing → Feature Extraction → Model Inference → Post-processing → Output
```

### Preprocessing Best Practices

| Step | Purpose | Implementation |
|---|---|---|
| Resizing | Consistent input dimensions | Maintain aspect ratio, pad if needed |
| Normalization | Scale pixel values | ImageNet mean/std or model-specific |
| Augmentation | Increase training diversity | albumentations, torchvision.transforms |
| Color space | Task-specific representation | RGB, HSV, LAB depending on task |

### Data Augmentation Strategies

- **Geometric**: Rotation, flipping, scaling, cropping, affine transforms
- **Photometric**: Brightness, contrast, saturation, hue, noise injection
- **Advanced**: CutMix, MixUp, Mosaic, Random Erasing, AutoAugment
- **Domain-specific**: Medical (elastic deformation), satellite (rotation invariance), manufacturing (defect synthesis)

---

## 2. Image Classification

### Architecture Evolution

| Architecture | Year | Key Innovation | Use Case |
|---|---|---|---|
| ResNet | 2015 | Skip connections | General classification |
| EfficientNet | 2019 | Compound scaling | Mobile/edge |
| Vision Transformer (ViT) | 2020 | Attention for images | Large-scale |
| DINOv2 | 2023 | Self-supervised vision | Feature extraction |
| ConvNeXt V2 | 2023 | Modern ConvNet design | Efficient classification |
| SigLIP | 2023 | Sigmoid loss for CLIP | Vision-language |

### Transfer Learning Strategy

1. **Feature extraction**: Freeze backbone, train classifier head (small data, <1000 images)
2. **Fine-tuning**: Unfreeze top layers, lower learning rate (medium data, 1000-10000)
3. **Full fine-tuning**: Train all layers (large data, >10000 images)
4. **Foundation model**: Use DINOv2/CLIP features directly (zero-shot or few-shot)

### Classification Best Practices

- Use pretrained models; training from scratch rarely justified
- Apply progressive resizing during training (start small, increase)
- Use test-time augmentation (TTA) for critical predictions
- Implement class-weighted loss for imbalanced datasets
- Use label smoothing to prevent overconfidence
- Ensemble multiple models for production-critical applications

---

## 3. Object Detection

### Detection Architectures

| Architecture | Type | Speed | Accuracy | Use Case |
|---|---|---|---|---|
| YOLOv8/v9/v10 | One-stage | Very fast | Good | Real-time |
| RT-DETR | Transformer | Fast | Very good | Real-time + accuracy |
| DINO (DETR) | Transformer | Medium | Excellent | High accuracy |
| Faster R-CNN | Two-stage | Slow | Very good | Research baseline |
| GroundingDINO | Open-vocab | Medium | Good | Zero-shot detection |

### Detection Pipeline

```
Image → Backbone (feature extraction) → Neck (feature fusion) → Head (predictions) → NMS → Detections
```

### Key Concepts

- **Anchor-based vs Anchor-free**: Modern detectors trend toward anchor-free (FCOS, CenterNet)
- **FPN (Feature Pyramid Network)**: Multi-scale feature fusion for detecting objects at different sizes
- **NMS (Non-Maximum Suppression)**: Remove duplicate detections; consider Soft-NMS for crowded scenes
- **IoU (Intersection over Union)**: Primary metric for detection quality

### Detection Metrics

| Metric | Description | Standard |
|---|---|---|
| mAP@0.5 | Mean AP at IoU 0.5 | PASCAL VOC |
| mAP@0.5:0.95 | Mean AP averaged over IoU thresholds | COCO |
| AP per class | Per-category performance | Identify weak classes |
| FPS | Frames per second | Real-time requirement |

---

## 4. Segmentation

### Segmentation Types

| Type | Output | Use Case |
|---|---|---|
| Semantic | Per-pixel class label | Scene understanding |
| Instance | Per-object mask + class | Counting, tracking |
| Panoptic | Semantic + Instance combined | Full scene parsing |
| Interactive | User-guided segmentation | Annotation tools |

### Key Models

| Model | Type | Strengths |
|---|---|---|
| SAM 2 (Segment Anything 2) | Interactive/zero-shot | Universal segmentation, video |
| Mask2Former | Panoptic | Unified architecture |
| DeepLab V3+ | Semantic | Atrous convolutions |
| YOLO-Seg | Instance | Real-time |
| SegGPT | Few-shot | In-context segmentation |

### SAM 2 (Segment Anything Model 2)

Meta's SAM 2 (2024) provides:
- Zero-shot segmentation with point/box/mask prompts
- Video object segmentation with temporal consistency
- Foundation model for any segmentation task
- Use as annotation tool or production segmentation backbone

---

## 5. Multimodal Vision

### Vision-Language Models

| Model | Capabilities | Use Case |
|---|---|---|
| GPT-4V/4o | Image understanding, OCR, reasoning | General vision tasks |
| Claude 3.5 Vision | Document analysis, charts, diagrams | Document processing |
| Gemini Pro Vision | Multimodal reasoning | Complex visual QA |
| LLaVA | Open-source VLM | Self-hosted vision |
| CLIP | Image-text alignment | Zero-shot classification, search |
| Florence-2 | Multiple vision tasks | Unified vision model |

### Vision-Language Applications

- **Visual Question Answering (VQA)**: Answer questions about images
- **Image Captioning**: Generate natural language descriptions
- **Document Understanding**: Extract information from documents, forms, receipts
- **Visual Search**: Find images by text description
- **Chart/Diagram Understanding**: Extract data from visualizations
- **OCR + Understanding**: Read and comprehend text in images

### Multimodal RAG

Extend RAG to handle images, diagrams, and mixed content:
- Use vision models to generate text descriptions of images
- Store image embeddings (CLIP) alongside text embeddings
- Implement multi-modal retrieval (text query → image + text results)
- Use vision-language models for generation with image context

---

## 6. Production CV Systems

### Deployment Considerations

| Factor | Consideration | Solution |
|---|---|---|
| Latency | Real-time requirements | Model optimization, GPU inference |
| Throughput | Batch processing needs | Batched inference, async processing |
| Model size | Edge/mobile constraints | Quantization, distillation, pruning |
| Accuracy | Production quality bar | Ensemble, TTA, confidence thresholds |
| Cost | GPU compute costs | Right-size models, spot instances |

### Model Optimization for Production

- **TensorRT**: NVIDIA GPU optimization (2-5x speedup)
- **ONNX Runtime**: Cross-platform optimized inference
- **OpenVINO**: Intel hardware optimization
- **Core ML**: Apple device optimization
- **TFLite**: Mobile/edge deployment

### Video Processing Pipeline

```
Video Stream → Frame Extraction → Detection/Tracking → Post-processing → Output
```

- Use object tracking (ByteTrack, BoT-SORT) to maintain identity across frames
- Process keyframes only when full-frame analysis isn't needed
- Implement frame skipping based on motion detection
- Use temporal smoothing to reduce flickering predictions

### Data Pipeline for CV

- Implement efficient data loading (WebDataset, FFCV, tf.data)
- Use progressive loading for large datasets
- Implement online augmentation (not pre-computed)
- Store annotations in standard formats (COCO JSON, PASCAL VOC XML, YOLO txt)
- Version datasets with DVC or similar tools
- Implement annotation quality checks and inter-annotator agreement
