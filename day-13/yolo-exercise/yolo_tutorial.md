# YOLO Tutorial

Below is a practical, opinionated path that gets you from zero to a
trained, evaluated, and deployed YOLO model---plus just enough history
to understand why things look the way they do today.

------------------------------------------------------------------------

## 1) What is YOLO, really?

**YOLO (You Only Look Once)** is a family of real-time object detectors.
Instead of first proposing regions and then classifying them (two-stage
detectors like Faster R-CNN), YOLO **predicts bounding boxes and class
probabilities directly** from the image in a single forward pass. That
makes it **fast**, hardware-friendly, and great for applications like
traffic monitoring, retail analytics, robotics, and video understanding.

**Key ideas** - **Single shot**: One network, one pass → boxes +
classes. - **Dense prediction**: Predicts on a grid / feature pyramid. -
**Post-processing**: Non-Max Suppression (NMS) prunes overlapping
boxes. - **Speed/accuracy trade-offs** controlled by model size
(n/s/m/l/x) and input resolution.

------------------------------------------------------------------------

## 2) A quick YOLO timeline (why so many versions?)

-   **YOLOv1 (2016, Redmon et al.)**: End-to-end detector, grid-based,
    blazing fast, modest accuracy.
-   **YOLOv2 / YOLO9000 (2017)**: Anchors + multi-scale training, big
    jump in accuracy.
-   **YOLOv3 (2018)**: Feature pyramid (FPN) + residual backbone
    (Darknet-53). A durable classic.
-   **YOLOv4 (2020, Bochkovskiy et al.)**: "Bag of freebies/tricks"
    (Mosaic aug, CIoU, etc.) + CSPDarknet.
-   **Scaled-YOLOv4 (2020)**: Scaling laws across
    depth/width/resolution.
-   **YOLOv5 (2020+, community/Ultralytics)**: PyTorch rewrite, simple
    training UX, massive adoption.
-   **YOLOv7 (2022)**: Strong accuracy/speed; extended training
    techniques.
-   **YOLOv8 (2023+, Ultralytics)**: Modernized pipeline (anchor-free by
    default), simple CLI, tasks beyond detection (seg, pose).
-   **...and many research offshoots (v6, v9, v10, etc.)** exploring
    anchors vs. anchor-free, new losses, efficient decoders.\
    **Takeaway:** multiple "YOLOs" exist, but **Ultralytics YOLO**
    provides the most beginner-friendly, batteries-included path today,
    with competitive accuracy and great tooling.

------------------------------------------------------------------------

## 3) The YOLO architecture in 90 seconds

-   **Backbone**: Extracts features (e.g., CSPDarknet, CSP-like, or
    Mobile edge backbones).
-   **Neck**: Merges multi-scale features (FPN/PAN/BiFPN).
-   **Head**: Predicts per-cell **(box, objectness, class probs)**.
    -   **Anchor-based** heads (v3/v4/v5): predict offsets to preset
        anchor boxes.
    -   **Anchor-free** heads (e.g., v8): predict box sides or centers
        directly.
-   **Losses**: Box regression (GIoU/DIoU/CIoU), objectness,
    classification.
-   **NMS**: Greedy filtering to keep best boxes.

------------------------------------------------------------------------

## 4) Install the tooling

We'll use **Ultralytics** (PyTorch under the hood) because it's simple
and production-ready.

``` bash
# Python 3.9–3.11 recommended; use a venv/conda environment
pip install --upgrade pip
pip install ultralytics  # installs CLI + Python API
# (Optional) GPU support: install a CUDA-enabled torch per pytorch.org instructions
```

Verify:

``` bash
yolo check
python -c "import torch; print(torch.cuda.is_available())"
```

------------------------------------------------------------------------

## 5) Understand the data format

YOLO expects images + **YOLO text labels** (per image) like:

    <class_id> <x_center> <y_center> <width> <height>

All values are **normalized** to \[0,1\] relative to image size. One
line per object.

**Folder layout (Ultralytics)**:

    dataset/
      images/
        train/  # .jpg/.png
        val/
      labels/
        train/  # .txt, same filename as image
        val/

**Dataset config YAML (example `data.yaml`):**

``` yaml
path: dataset           # root of your dataset
train: images/train
val: images/val
names:
  0: person
  1: helmet
  2: vest
```

**How to annotate**\
Use tools like **LabelImg**, **Label Studio**, **Roboflow Annotate**, or
**CVAT**. Export in YOLO format.

------------------------------------------------------------------------

## 6) Train a custom YOLO model (CLI)

Pick a model size (n/s/m/l/x). Start small for speed; scale later.

``` bash
# Train detection with YOLOv8-style model
yolo detect train   model=yolov8n.pt   data=data.yaml   imgsz=640   epochs=100   batch=16   project=runs_yolo   name=helmet_det_v1
```

What happens: - Ultralytics downloads the base weights. - Trains on your
dataset. - Saves best/last checkpoints + metrics to
`runs_yolo/detect/helmet_det_v1/`.

**Useful switches** - `patience=20` early stopping - `lr0=0.01` base
LR - `optimizer=sgd|adam|adamw` - `augment=True` (on by default)\
- `device=0` (select GPU) or `device=cpu`

------------------------------------------------------------------------

## 7) Validate & test

Validation runs during training, but you can run it explicitly:

``` bash
yolo detect val   model=runs_yolo/detect/helmet_det_v1/weights/best.pt   data=data.yaml   imgsz=640
```

You'll get **mAP@0.5** and **mAP@0.5:0.95**, plus per-class
precision/recall.\
High-level guidance: - If **precision high, recall low** → model is
conservative; consider lowering confidence at inference or training
longer. - If **recall high, precision low** → model too eager; consider
higher conf/NMS thresholds or better labels/augmentations.

------------------------------------------------------------------------

## 8) Inference (images, video, webcam)

``` bash
# Single image or folder
yolo detect predict   model=runs_yolo/detect/helmet_det_v1/weights/best.pt   source="test_images"   imgsz=640   conf=0.25   iou=0.7

# Webcam (0) or RTSP/MP4
yolo detect predict model=... source=0
```

Outputs go to `runs_yolo/detect/predict…/` with rendered boxes.

------------------------------------------------------------------------

## 9) Use the Python API (batch, custom post-processing)

``` python
from ultralytics import YOLO

model = YOLO("runs_yolo/detect/helmet_det_v1/weights/best.pt")
results = model.predict(source="test_images", conf=0.25, iou=0.7, imgsz=640)

for r in results:
    # r.boxes.xyxy, r.boxes.conf, r.boxes.cls
    for box, cls, conf in zip(r.boxes.xyxy, r.boxes.cls, r.boxes.conf):
        x1,y1,x2,y2 = box.tolist()
        print(int(cls.item()), float(conf.item()), [x1,y1,x2,y2])
```

------------------------------------------------------------------------

## 10) Fine-tuning tips that matter

-   **Start with small models** (`n`/`s`) to shake out bugs quickly.
-   **Input size**: 640 is a good default; larger boosts accuracy but
    costs memory/speed.
-   **Class balance**: If some classes are rare, add more examples or
    use class weighting.
-   **Augmentations**: Mosaic, random crop, flips help; too much can
    hurt small objects.
-   **Box quality**: Tight, consistent annotations are the biggest ROI.
-   **Warmup & LR**: If training is unstable, lower `lr0` (e.g., 0.005)
    or extend warmup.
-   **Freeze backbone** for very small datasets: `freeze=10` (first 10
    layers).

------------------------------------------------------------------------

## 11) Advanced: segmentation & pose

Ultralytics supports **instance segmentation** and **pose** with similar
flows:

``` bash
# Segmentation
yolo segment train model=yolov8n-seg.pt data=data.yaml imgsz=640

# Pose (keypoints)
yolo pose train model=yolov8n-pose.pt data=pose_data.yaml imgsz=640
```

------------------------------------------------------------------------

## 12) Export for deployment (ONNX, TensorRT, CoreML, etc.)

``` bash
# Common formats: onnx, openvino, tflite, tfjs, coreml, engine (TensorRT)
yolo export model=best.pt format=onnx opset=12
yolo export model=best.pt format=engine  # TensorRT (needs CUDA/TensorRT)
```

**Minimal ONNXRuntime inference (Python):**

``` python
import onnxruntime as ort
import cv2, numpy as np

sess = ort.InferenceSession("best.onnx", providers=["CPUExecutionProvider"])
inp_name = sess.get_inputs()[0].name

img = cv2.imread("test.jpg")
im = cv2.resize(img, (640, 640))
im = im[:, :, ::-1].transpose(2,0,1) / 255.0
im = np.expand_dims(im.astype(np.float32), 0)

outputs = sess.run(None, {inp_name: im})
# Post-process outputs similar to YOLO head (or reuse Ultralytics postprocess utilities if available)
```

------------------------------------------------------------------------

## 13) Deploy in a tiny FastAPI service

``` python
# app.py
from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
import cv2, numpy as np

app = FastAPI()
model = YOLO("best.pt")

@app.post("/predict")
async def predict(file: UploadFile = File(...), conf: float = 0.25):
    data = await file.read()
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    results = model.predict(img, conf=conf)[0]
    dets = []
    for b, c, p in zip(results.boxes.xyxy.tolist(),
                       results.boxes.cls.tolist(),
                       results.boxes.conf.tolist()):
        dets.append({"xyxy": b, "cls": int(c), "conf": float(p)})
    return {"detections": dets}
```

Run:

``` bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

------------------------------------------------------------------------

## 14) Evaluate like you mean it

-   **mAP@0.5**: forgiving IoU threshold; **mAP@0.5:0.95**: stricter,
    COCO-style.
-   **PR curves**: spot precision/recall trade-offs per class.
-   **Conf/iou sweeps**: Choose thresholds that match business needs
    (e.g., false-negatives are costly → lower `conf`).
-   **Latency & throughput**: Measure end-to-end, not just model FPS.
    Include decode/resize/NMS/IO.

------------------------------------------------------------------------

## 15) Troubleshooting & gotchas

-   **"It runs but finds nothing"**: wrong label paths, class names out
    of sync, tiny objects at too-low resolution, `conf` too high.
-   **CUDA OOM**: reduce `batch`, `imgsz`, or use a smaller model.
-   **Class bleeding**: improve labeling consistency; check
    augmentations.
-   **Domain shift**: collect **validation/test** data that matches
    production (lighting, camera, motion blur).
-   **Video jitter**: apply simple **temporal smoothing** (e.g., track
    by IoU or a lightweight tracker like ByteTrack/OC-SORT).

------------------------------------------------------------------------

## 16) YOLO in production: practical checklist

-   [ ] Pin versions of `ultralytics`, `torch`, and CUDA.
-   [ ] Export to a portable format (ONNX/TensorRT) where possible.
-   [ ] Add **health** and **warm-up** endpoints to your service.
-   [ ] Monitor **data drift** and **latency**.
-   [ ] Keep a **feedback loop**: store low-confidence or disagreed
    predictions to retrain.
-   [ ] Automate training/eval/export in CI with fixed seeds for
    reproducibility.

------------------------------------------------------------------------

## 17) Minimal "from scratch" training script (Python API)

``` python
# train_yolo.py
from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO("yolov8n.pt")  # base weights
    model.train(
        data="data.yaml",
        epochs=100,
        imgsz=640,
        batch=16,
        patience=20,
        optimizer="adamw",
        project="runs_yolo",
        name="exp_from_script"
    )
    metrics = model.val(data="data.yaml", imgsz=640)
    print(metrics)  # dict with mAP etc.

    # Predict one folder after training
    model.predict(source="test_images", conf=0.25, iou=0.7)
```

------------------------------------------------------------------------

## 18) Suggested learning path (fast track)

1.  Train **yolov8n** on a tiny custom dataset (100--500 images) → ship
    a demo.
2.  Scale to **yolov8s/m** and higher `imgsz` once pipeline is reliable.
3.  Try **segmentation** if masks matter; **pose** for keypoints.
4.  Export **ONNX** and measure latency on target hardware.
5.  Add **tracking** for video stability.
6.  Iterate with **active learning** on edge cases.

------------------------------------------------------------------------

## 19) References & further reading (start here)

-   **YOLOv1**: Redmon et al., "You Only Look Once: Unified, Real-Time
    Object Detection" (2016).\
-   **YOLOv2/YOLO9000**: Redmon & Farhadi (2017).\
-   **YOLOv3**: Redmon & Farhadi (2018).\
-   **YOLOv4**: Bochkovskiy, Wang, Liao (2020).\
-   **Scaled-YOLOv4**: Wang et al. (2020).\
-   **YOLOv5**: Ultralytics repository & docs (PyTorch implementation
    and training ecosystem).\
-   **YOLOv7**: Wang et al. (2022).\
-   **Ultralytics YOLO (YOLOv8+)**: Official Ultralytics docs &
    tutorials.\
-   **Losses**: Rezatofighi et al., "Generalized Intersection over
    Union" (GIoU); Zheng et al., "Distance-IoU Loss".\
-   **Trackers**: ByteTrack (Y.-F. Zhang et al., 2021), OC-SORT (C.-H.
    Cao et al., 2022).

*(Tip: search each title to find the official arXiv page or docs.)*

------------------------------------------------------------------------

## 20) What you can do next

-    Refer **yolo_datasets.md**. Pick a dataset and train a YOLO model
