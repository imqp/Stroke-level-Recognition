**How to Use PaddleOCR in Python with a Configuration File**

PaddleOCR provides flexibility to use its models directly in Python by loading configurations from a YAML config file. This approach allows you to customize the OCR process extensively and integrate it seamlessly into your Python applications.

Below is a comprehensive guide on how to use PaddleOCR in Python with a configuration file.

---

### **Step 1: Install PaddlePaddle and PaddleOCR**

Ensure you have Python 3.7 or later installed.

- **Install PaddlePaddle:**

  - **CPU Version:**

    ```bash
    pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
    ```

  - **GPU Version (if you have a compatible GPU):**

    ```bash
    pip install paddlepaddle-gpu -i https://mirror.baidu.com/pypi/simple
    ```

- **Install PaddleOCR:**

  ```bash
  pip install "paddleocr>=2.0.1"
  ```

For detailed installation instructions, refer to the [PaddlePaddle Installation Guide](https://www.paddlepaddle.org.cn/en/install/quick).

---

### **Step 2: Prepare Your Configuration File**

You can use an existing configuration file or create a custom one. Configuration files are in YAML format and define the model architecture, parameters, and other settings.

**Example Configuration File (`rec_config.yml`):**

```yaml
Global:
  use_gpu: false                      # Set to true if using GPU
  max_text_length: 25
  character_dict_path: ppocr/utils/en_dict.txt
  infer_img: ./test_images/           # Path to your images
  pretrained_model: ./pretrained_models/en_PP-OCRv3_rec_train/best_accuracy
  rec_image_shape: "3, 32, 320"       # Adjust based on your model
  rec_batch_num: 6

Architecture:
  model_type: rec
  algorithm: CRNN
  Transform:
  Backbone:
    name: MobileNetV3
    scale: 0.5
    model_name: small
  Neck:
    name: SequenceEncoder
    encoder_type: rnn
    hidden_size: 48
  Head:
    name: CTCHead

Loss:
  name: CTCLoss

PostProcess:
  name: CTCLabelDecode
  character_dict_path: ppocr/utils/en_dict.txt
  use_space_char: False

Metric:
  name: RecMetric
  main_indicator: acc

Eval:
  dataset:
    name: SimpleDataSet
    transforms:
      - DecodeImage:
          img_mode: 'RGB'
          channel_first: False
      - CTCLabelEncode:
      - RecResizeImg:
          image_shape: [3, 32, 320]
      - KeepKeys:
          keep_keys: ['image', 'label', 'length']
```

**Note:** Modify paths and parameters to match your environment and requirements.

---

### **Step 3: Load the Configuration in Python**

Use the `yaml` library to load the configuration file.

```python
import yaml

# Load the configuration file
config_path = 'rec_config.yml'
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)
```

---

### **Step 4: Build the Model Components**

PaddleOCR's internal modules can be used to build the model according to the configuration.

#### **Import Necessary Modules:**

```python
import sys
import os
import numpy as np
import paddle
from paddleocr.ppocr.modeling.architectures import build_model
from paddleocr.ppocr.utils.save_load import load_model
from paddleocr.ppocr.postprocess import build_post_process
from paddleocr.ppocr.data import create_operators, transform
from paddleocr.ppocr.utils.logging import get_logger
from paddleocr.ppocr.utils.utility import get_image_file_list
from PIL import Image
```

**Adjust Python Path if Necessary:**

If you have cloned the PaddleOCR repository and are running the script from outside its directory:

```python
sys.path.append('/path/to/PaddleOCR')
```

#### **Initialize Logger:**

```python
logger = get_logger()
```

#### **Build the Model:**

```python
# Build the model architecture
model = build_model(config['Architecture'])
```

#### **Load Pretrained Model Weights:**

```python
# Load the pretrained model
pretrained_model_path = config['Global']['pretrained_model']
if os.path.exists(pretrained_model_path):
    load_model(config, model, pretrained_model_path)
else:
    logger.error("Pretrained model not found at {}".format(pretrained_model_path))
    exit()
```

#### **Set Model to Evaluation Mode:**

```python
model.eval()
```

---

### **Step 5: Prepare Post-Processing and Data Transforms**

#### **Build the Post-Process Function:**

```python
post_process_class = build_post_process(config['PostProcess'], config['Global'])
```

#### **Create Data Operators:**

```python
transforms = []
ops = config['Eval']['dataset']['transforms']
global_ops = create_operators(ops, config['Global'])
```

---

### **Step 6: Load and Preprocess Images**

#### **Get the List of Images:**

```python
image_file_list = get_image_file_list(config['Global']['infer_img'])
```

#### **Process Each Image:**

```python
for image_file in image_file_list:
    # Load image
    img = Image.open(image_file).convert('RGB')
    img = np.array(img)

    # Create data dictionary
    data = {'image': img}

    # Apply transforms
    batch = transform(data, global_ops)

    # Prepare input tensor
    img_tensor = batch[0]['image']
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor = paddle.to_tensor(img_tensor)
```

---

### **Step 7: Run Inference and Post-Processing**

#### **Run the Model:**

```python
    # Forward pass
    preds = model(img_tensor)
```

#### **Apply Post-Processing:**

```python
    # Post-process the predictions
    post_result = post_process_class(preds)
```

#### **Print the Results:**

```python
    # Extract and print the recognized text and confidence score
    for rec_res in post_result:
        text = rec_res[0]
        confidence = rec_res[1]
        print('Predicts of {}: ({}, {:.4f})'.format(image_file, text, confidence))
```

---

### **Complete Python Script Example**

Here is the complete script combining all the steps:

```python
import sys
import os
import yaml
import numpy as np
import paddle
from paddleocr.ppocr.modeling.architectures import build_model
from paddleocr.ppocr.utils.save_load import load_model
from paddleocr.ppocr.postprocess import build_post_process
from paddleocr.ppocr.data import create_operators, transform
from paddleocr.ppocr.utils.logging import get_logger
from paddleocr.ppocr.utils.utility import get_image_file_list
from PIL import Image

# Adjust Python path if necessary
# sys.path.append('/path/to/PaddleOCR')

# Initialize logger
logger = get_logger()

# Load configuration
config_path = 'rec_config.yml'
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

global_config = config['Global']

# Build model architecture
model = build_model(config['Architecture'])

# Load pretrained model
pretrained_model_path = global_config['pretrained_model']
if os.path.exists(pretrained_model_path):
    load_model(config, model, pretrained_model_path)
else:
    logger.error("Pretrained model not found at {}".format(pretrained_model_path))
    exit()

# Set model to evaluation mode
model.eval()

# Build post-process function
post_process_class = build_post_process(config['PostProcess'], global_config)

# Create data operators
ops = config['Eval']['dataset']['transforms']
global_ops = create_operators(ops, global_config)

# Get list of images
image_file_list = get_image_file_list(global_config['infer_img'])

# Process images
for image_file in image_file_list:
    # Load image
    img = Image.open(image_file).convert('RGB')
    img = np.array(img)

    # Create data dictionary
    data = {'image': img}

    # Apply transforms
    batch = transform(data, global_ops)
    if batch is None:
        continue

    img_tensor = batch[0]['image']
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor = paddle.to_tensor(img_tensor)

    # Run inference
    preds = model(img_tensor)

    # Post-process the predictions
    post_result = post_process_class(preds)

    # Print the results
    for rec_res in post_result:
        text = rec_res[0]
        confidence = rec_res[1]
        print('Predicts of {}: ({}, {:.4f})'.format(image_file, text, confidence))
```

---

### **Step 8: Ensure All Dependencies Are Met**

- **Module Imports:**

  Ensure that all modules are correctly imported. If you encounter import errors, verify that you have the latest version of PaddleOCR and that you have cloned the repository if necessary.

- **PaddleOCR Repository:**

  If you have installed PaddleOCR via `pip`, some internal modules might not be accessible. In that case, clone the PaddleOCR repository:

  ```bash
  git clone https://github.com/PaddlePaddle/PaddleOCR.git
  ```

  Then, adjust your Python path:

  ```python
  sys.path.append('/path/to/PaddleOCR')
  ```

---

### **Additional Notes**

- **Adjust Configuration Parameters:**

  - **`use_gpu`:** Set to `true` if you have a compatible GPU and have installed the GPU version of PaddlePaddle.
  - **`character_dict_path`:** Ensure this path points to the correct character dictionary for your language.
  - **`pretrained_model`:** Specify the correct path to your pretrained recognition model.

- **Transformations:**

  - The transformations in the `Eval` section should match those used during training.

- **Batch Processing:**

  - The script processes images one by one. You can modify it to process images in batches by accumulating tensors and passing them together to the model.

- **Error Handling:**

  - Include checks to handle cases where images might not be processed correctly.

---

### **Alternative: Using PaddleOCR High-Level API with Parameters**

If you prefer a simpler approach without using the configuration file, you can use the high-level API and pass parameters directly.

```python
from paddleocr import PaddleOCR

# Initialize the OCR model with custom parameters
ocr_model = PaddleOCR(
    det=False,                   # Disable detection
    rec=True,                    # Enable recognition
    use_angle_cls=False,
    lang='en',
    rec_model_dir='./pretrained_models/en_PP-OCRv3_rec_train',  # Path to your model
    rec_char_dict_path='ppocr/utils/en_dict.txt',
    max_text_length=25,
    rec_image_shape="3, 32, 320",
    use_gpu=False                # Set to True if using GPU
)

# Recognize text from an image
result = ocr_model.ocr('test_images/word_1.jpg', cls=False)

# Print the recognized text
for line in result:
    text = line[1][0]
    confidence = line[1][1]
    print('Text: {}, Confidence: {:.4f}'.format(text, confidence))
```

---

### **Conclusion**

By following the steps above, you can use PaddleOCR in Python with a configuration file. This method gives you greater control over the OCR process and allows you to customize the model and parameters extensively.

**References:**

- **PaddleOCR GitHub Repository:** [https://github.com/PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- **PaddleOCR Documentation:** [https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_en/whl_en.md](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_en/whl_en.md)

---