# -*- coding: utf-8 -*-
"""ultrasound

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/#fileId=https%3A//storage.googleapis.com/kaggle-colab-exported-notebooks/ultrasound-ff373ebc-ebe0-4fa5-9227-7fccea123160.ipynb%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com/20240930/auto/storage/goog4_request%26X-Goog-Date%3D20240930T140943Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D13eba6d4fd843cc9a396d645182d92ba2c19aae94f3206ca07e58b47862bb2f1ea8183c17c2e762d850b60a6b39c1d30af79e56eee98056b0622ecd3b38ff660efae872cd9afc78ba94db60ec08834a1f91c41905c0480fe94918aac42b00fc70977c8eb7d04d3c057cf71b2a881ae45071f901fe574adae933398ef6fdfe7cf7089edf1914bb00a82996e67a45e7b89a2b03e542ab1a2742abccc5269dc654bd1b9e20bf67f5321b8b1c44a2bbb82a5fffc4c78e5d7bb7b412b1e140a6c5d0c41ebb159163de93e6f8c7a8f3ed0bc31f9df6d365a73a9a91592996b1572416e68298e9031429606dc8a5f5814a19fd97e9f81d49083103afc5ae89391aa10b9
"""

# IMPORTANT: RUN THIS CELL IN ORDER TO IMPORT YOUR KAGGLE DATA SOURCES
# TO THE CORRECT LOCATION (/kaggle/input) IN YOUR NOTEBOOK,
# THEN FEEL FREE TO DELETE THIS CELL.
# NOTE: THIS NOTEBOOK ENVIRONMENT DIFFERS FROM KAGGLE'S PYTHON
# ENVIRONMENT SO THERE MAY BE MISSING LIBRARIES USED BY YOUR
# NOTEBOOK.

import os
import sys
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from urllib.parse import unquote, urlparse
from urllib.error import HTTPError
from zipfile import ZipFile
import tarfile
import shutil

CHUNK_SIZE = 40960
DATA_SOURCE_MAPPING = 'breast-ultrasound-images-dataset:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F2952181%2F5084161%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240930%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240930T140942Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3Dc20d6efa41ca2d52e83eb27916cab9307572045dec654667fd8e66e8c57d0a9712a7f2c518c7e1fc316320e0fe17ba9096e6609c76279e7d521fa555032700a8b96226673e4b640c9383c9efffc6c2f17108839c8d8c853050fed2f5700c0380fba54b97785eab45c35a91d3ae93557a1e2bdfc6683603f11fb50afd14622bb86b0b9a5778d1a5a289b7555b845b37c4f04fa65802e6db2569b41df440ce2b91205da6267203f9bad79056a7bcfbbca2a8384e1b89d5bdf35a2d862abb27023cb08feb2b929b108eb7ca36dbb5453ab2451ec0bf8360089c81e9c277dbf58a6f72bc881a9d8489868d05261b941b28d1866e376617c2e48be51a4343659578d7,dl3_res/pytorch/default/1:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-models-data%2F104393%2F124025%2Fbundle%2Farchive.tar.gz%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240930%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240930T140942Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3Da835f3d022781a1d8320fbcccdb350d5f533c06c135c06397e4cc969794d533252c4dc706cefd326806d3f52bf60bdd3d1b16392aa27c821cbae9a7c9c7bf62e8307ea0c24cb73de49e51b82308f674455be87041c02ee586d278799d6fe8af57dafca33e49ae2de849927164f9c3993d2520537d62dbd9b7ef73b5d825d5d008e783c124e590413cc38ac27ca5efdd2ff6ff03117ce6c49e1350e947b54a22032c9bb3dfa02ab44fef769693129eac8d0eeff3f1810d8d4bdcd3321d4e52eda15c5460451eb00deea5c6408b9ddcc22687c031cd6173aa9ef3218ff909ee6017cc0872709892ee11fa71bd48f70ac7a545f60a04964450a88b54b328c7a59a4'

KAGGLE_INPUT_PATH='/kaggle/input'
KAGGLE_WORKING_PATH='/kaggle/working'
KAGGLE_SYMLINK='kaggle'

!umount /kaggle/input/ 2> /dev/null
shutil.rmtree('/kaggle/input', ignore_errors=True)
os.makedirs(KAGGLE_INPUT_PATH, 0o777, exist_ok=True)
os.makedirs(KAGGLE_WORKING_PATH, 0o777, exist_ok=True)

try:
  os.symlink(KAGGLE_INPUT_PATH, os.path.join("..", 'input'), target_is_directory=True)
except FileExistsError:
  pass
try:
  os.symlink(KAGGLE_WORKING_PATH, os.path.join("..", 'working'), target_is_directory=True)
except FileExistsError:
  pass

for data_source_mapping in DATA_SOURCE_MAPPING.split(','):
    directory, download_url_encoded = data_source_mapping.split(':')
    download_url = unquote(download_url_encoded)
    filename = urlparse(download_url).path
    destination_path = os.path.join(KAGGLE_INPUT_PATH, directory)
    try:
        with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:
            total_length = fileres.headers['content-length']
            print(f'Downloading {directory}, {total_length} bytes compressed')
            dl = 0
            data = fileres.read(CHUNK_SIZE)
            while len(data) > 0:
                dl += len(data)
                tfile.write(data)
                done = int(50 * dl / int(total_length))
                sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl} bytes downloaded")
                sys.stdout.flush()
                data = fileres.read(CHUNK_SIZE)
            if filename.endswith('.zip'):
              with ZipFile(tfile) as zfile:
                zfile.extractall(destination_path)
            else:
              with tarfile.open(tfile.name) as tarfile:
                tarfile.extractall(destination_path)
            print(f'\nDownloaded and uncompressed: {directory}')
    except HTTPError as e:
        print(f'Failed to load (likely expired) {download_url} to path {destination_path}')
        continue
    except OSError as e:
        print(f'Failed to load {download_url} to path {destination_path}')
        continue

print('Data source import complete.')

import os
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader

class BreastUltrasoundDataset(Dataset):
    def __init__(self, root_dir, classes=['benign', 'malignant'], transform_image=None, transform_mask=None):
        self.root_dir = root_dir
        self.classes = classes
        self.transform_image = transform_image  # Separate transformation for images
        self.transform_mask = transform_mask  # Separate transformation for masks
        self.image_paths = []
        self.mask_paths = []

        # Loop through the classes and load image and mask paths
        for cls in self.classes:
            image_dir = os.path.join(root_dir, cls)
            for filename in os.listdir(image_dir):
                if filename.endswith(".png") and "_mask" not in filename:
                    image_path = os.path.join(image_dir, filename)
                    mask_path = os.path.join(image_dir, filename.replace(".png", "_mask.png"))
                    self.image_paths.append(image_path)
                    self.mask_paths.append(mask_path)

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx]).convert("RGB")  # Convert image to RGB
        mask = Image.open(self.mask_paths[idx]).convert("L")  # Convert mask to grayscale (L mode)

        # Apply transformations (if any)
        if self.transform_image:
            image = self.transform_image(image)  # Apply the image transformations

        if self.transform_mask:
            mask = self.transform_mask(mask)  # Apply the mask transformations

        return image, mask

dataset = BreastUltrasoundDataset(root_dir="/kaggle/input/breast-ultrasound-images-dataset/Dataset_BUSI_with_GT")

dataset

from torch.utils.data import DataLoader
import torchvision.transforms as transforms

transform_image = transforms.Compose([
    transforms.Resize((256, 256)),  # Resize all images to the same size
    transforms.ToTensor(),  # Convert PIL images to PyTorch tensors
])

transform_mask = transforms.Compose([
    transforms.Resize((256, 256)),  # Resize masks to the same size as images
    transforms.ToTensor(),  # Convert PIL masks to PyTorch tensors (grayscale)
])

transform_normal = transforms.Compose([
    transforms.Resize((256, 256)),  # Resize normal to the same size as images
    transforms.ToTensor(),  # Convert PIL masks to PyTorch tensors (grayscale)
])

dataset = BreastUltrasoundDataset(
    root_dir="/kaggle/input/breast-ultrasound-images-dataset/Dataset_BUSI_with_GT",
    classes=['benign', 'malignant'],
    transform_image=transform_image,
    transform_mask=transform_mask
)

from torch.utils.data import DataLoader

train_loader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=4)

# Example usage: Iterate through the DataLoader
for images, masks in train_loader:
    print(images.shape, masks.shape)  # Check the shape of a batch
    break  # Just to test one batch

!pip install segmentation_models_pytorch

x, y = next(iter(train_loader))

x.shape, y.shape

!pip install catalyst

from catalyst.runners import SupervisedRunner
from catalyst.callbacks import CheckpointCallback
from catalyst.contrib.schedulers import OneCycleLR

# experiment setup
num_epochs = 300  # Set the number of epochs you want to run
logdir = "./logs/segmentation_notebook"

# Define the loaders for training and validation
loaders = {
    "train": train_loader
}

import pytorch_lightning as pl
import torch
import torch.nn as nn
import torch.optim as optim

import segmentation_models_pytorch as smp

# Create the model
model = smp.DeepLabV3Plus(
    encoder_name="resnet152",
    encoder_weights="imagenet",
    in_channels=3,
    classes=1
)

dice_loss = smp.losses.DiceLoss(mode='binary')
bce_loss = nn.BCEWithLogitsLoss()

class SegmentationModel(pl.LightningModule):
    def __init__(self, model, dice_loss, bce_loss):
        super(SegmentationModel, self).__init__()
        self.model = model
        self.dice_loss = dice_loss
        self.bce_loss = bce_loss

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        images, masks = batch
        predictions = self(images)

        # Compute Dice Loss and BCE Loss
        loss_dice = self.dice_loss(predictions, masks)
        loss_bce = self.bce_loss(predictions, masks)

        # Combine the two losses
        loss = loss_dice + loss_bce

        self.log('train_loss', loss)
        return loss

    def configure_optimizers(self):
        optimizer = optim.Adam([
            {'params': self.model.decoder.parameters(), 'lr': 1e-4},
            {'params': self.model.encoder.parameters(), 'lr': 1e-6},
        ])
        return optimizer

lightning_model = SegmentationModel(model=model, dice_loss=dice_loss, bce_loss=bce_loss)

import matplotlib.pyplot as plt
import pytorch_lightning as pl

class LossTracker(pl.Callback):
    def __init__(self):
        super().__init__()
        self.train_losses = []

    # Track training loss at the end of each batch
    def on_train_batch_end(self, trainer, pl_module, outputs, batch, batch_idx):
        loss = outputs['loss'].item()
        self.train_losses.append(loss)

    # Plot the loss curve after training ends
    def on_train_end(self, trainer, pl_module):
        plt.figure(figsize=(10, 5))
        plt.plot(self.train_losses, label="Training Loss")
        plt.title("Loss Curve")
        plt.xlabel("Batches")
        plt.ylabel("Loss")
        plt.legend()
        plt.show()

from pytorch_lightning.callbacks import EarlyStopping
early_stopping = EarlyStopping(
    monitor='train_loss',  # Metric to monitor (can be any logged metric, like 'val_loss')
    patience=15,  # Number of epochs to wait before stopping when no improvement
    verbose=True,  # Whether to print early stopping information
    mode='min'  # 'min' for metrics like loss where lower is better, 'max' for accuracy, etc.
)

from pytorch_lightning.loggers import CSVLogger
from pytorch_lightning import Trainer

# Set up CSVLogger to log the metrics to a CSV file
csv_logger = CSVLogger("logs", name="my_model_logs")

import pytorch_lightning as pl
from pytorch_lightning.loggers import TensorBoardLogger

loss_tracker = LossTracker()

# Trainer setup with logger and live loss tracking
trainer = Trainer(
    max_epochs=num_epochs,  # Define how many epochs you want to run
    accelerator="gpu" if torch.cuda.is_available() else "cpu",  # Use GPU or CPU
    devices=1 if torch.cuda.is_available() else None,  # Number of GPUs (set None if using CPU)
    log_every_n_steps=10,  # Log every 10 steps
    logger=csv_logger,  # Add  logger
    callbacks=[loss_tracker, early_stopping]
)

# Train the model
trainer.fit(lightning_model, train_loader)

import numpy as np
import matplotlib.pyplot as plt
import torch

# Prediction function using lightning_model for the first 16 images
def predict16(valMap, lightning_model, shape=256):
    # Extract the first 16 images and masks from the DataLoader batch
    img = valMap['img'][:16]
    mask = valMap['mask'][:16]

    # Move images to the same device as the model
    img = img.to(lightning_model.device)

    # Set model to evaluation mode
    lightning_model.eval()

    # Use the forward method for predictions
    with torch.no_grad():
        predictions = lightning_model(img)

    # Apply sigmoid and threshold for binary mask predictions
    predictions = torch.sigmoid(predictions)
    predictions = (predictions > 0.8).float()

    # Move predictions, images, and masks to CPU and convert to NumPy for plotting
    predictions = predictions.cpu().numpy()
    img = img.cpu().numpy()
    mask = mask.cpu().numpy()

    return predictions, img, mask

# Plot function to visualize the images, predicted masks, and ground truth masks
def Plotter(img, predMask, groundTruth):
    plt.figure(figsize=(9, 9))

    plt.subplot(1, 3, 1)
    plt.imshow(np.transpose(img, (1, 2, 0)))  # Convert CHW to HWC for plotting
    plt.title('Image')

    plt.subplot(1, 3, 2)
    plt.imshow(predMask.squeeze(), cmap='gray')  # Predicted mask
    plt.title('Predicted Mask')

    plt.subplot(1, 3, 3)
    plt.imshow(groundTruth.squeeze(), cmap='gray')  # Ground truth mask
    plt.title('Ground Truth')

    plt.show()

# Example usage
# Assuming you have a DataLoader `train_loader` and a trained Lightning model `lightning_model`

# Loop through the train_loader
for batch in train_loader:
    valMap = {'img': batch[0], 'mask': batch[1]}

    # Predict on the entire batch from the training set using lightning_model
    sixteenPrediction, actuals, masks = predict16(valMap, lightning_model)

    # Visualize each image, predicted mask, and ground truth mask for the entire batch
    for i in range(len(actuals)):
        print(f"Visualizing image {i+1}/{len(actuals)}")  # Optional: Progress output
        Plotter(actuals[i], sixteenPrediction[i], masks[i])

    break  # Process only one batch, remove this if you want to go through all batches

# torch.save(lightning_model.model.state_dict(), "/kaggle/working/dl3_res.pth")

# segment_image("/kaggle/input/breast-ultrasound-images-dataset/Dataset_BUSI_with_GT/malignant/malignant (103)_mask.png")

import torch
import segmentation_models_pytorch as smp

# Function to load the trained model
def load_model():
    model = smp.DeepLabV3Plus(
        encoder_name="resnet152",  # This should match the encoder you used during training
        encoder_weights=None,     # No pretrained weights, since we are loading trained model weights
        in_channels=3,            # RGB images
        classes=1                 # Binary segmentation (1 class)
    )
    # Load your trained weights into the model
    model.load_state_dict(torch.load("/kaggle/input/dl3_res/pytorch/default/1/dl3_res.pth", weights_only=True))
    model.eval()  # Set the model to evaluation mode
    return model

load_model();

import os
from PIL import Image
from torch.utils.data import Dataset
import torchvision.transforms as transforms

class BreastUltrasoundImagesDataset(Dataset):
    def __init__(self, root_dir, classes=['benign', 'malignant'], transform_image=None):
        self.root_dir = root_dir
        self.classes = classes
        self.transform_image = transform_image
        self.image_paths = []
        self.class_labels = []

        # Loop through the classes and load image paths
        for cls in self.classes:
            image_dir = os.path.join(root_dir, cls)
            for filename in os.listdir(image_dir):
                if filename.endswith(".png") and "_mask" not in filename:
                    image_path = os.path.join(image_dir, filename)
                    self.image_paths.append(image_path)
                    self.class_labels.append(cls)  # Store whether it's benign or malignant

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        class_label = self.class_labels[idx]
        image = Image.open(image_path).convert("RGB")  # Convert image to RGB

        # Apply transformations (if any)
        if self.transform_image:
            image = self.transform_image(image)

        return image, image_path, class_label

# Prediction function for images
def predict_and_store_images(dataset, model):
    results = []

    # Iterate over the dataset
    for i in range(len(dataset)):
        image, image_path, class_label = dataset[i]
        image_tensor = image.unsqueeze(0)  # Add batch dimension

        # Move image to model device
        with torch.no_grad():
            prediction = model(image_tensor)  # Get model output
            prediction = torch.sigmoid(prediction)
            prediction = (prediction > 0.6).float()  # Threshold to get binary mask

        # Store the input image, prediction, and file name
        results.append({
            "image": image,
            "prediction": prediction.squeeze().cpu().numpy(),  # Convert prediction to NumPy
            "file_name": os.path.basename(image_path),
            "class_label": class_label
        })

    return results

!rm -rf /kaggle/working/*

import os
import shutil  # For deleting directories
import numpy as np
from PIL import Image
import torchvision.transforms as transforms

# Function to delete existing directories and save new predictions and input images
def save_predictions(results):
    # Define directory paths
    benign_dir = "/kaggle/working/benign"
    malignant_dir = "/kaggle/working/malignant"

    # Delete the directories if they exist
    if os.path.exists(benign_dir):
        shutil.rmtree(benign_dir)  # Remove benign directory and all its contents
    if os.path.exists(malignant_dir):
        shutil.rmtree(malignant_dir)  # Remove malignant directory and all its contents

    # Re-create the directories
    os.makedirs(benign_dir, exist_ok=True)
    os.makedirs(malignant_dir, exist_ok=True)

    # Save each prediction and input image
    for result in results:
        input_image = result["image"]
        prediction_mask = result["prediction"]
        file_name = result["file_name"]
        class_label = result["class_label"]

        # Determine the save path based on class label
        save_dir = benign_dir if class_label == "benign" else malignant_dir
        input_image_save_path = os.path.join(save_dir, file_name)  # Save input image with original name
        prediction_save_path = os.path.join(save_dir, file_name.replace(".png", "_pred.png"))  # Save prediction

        # Save the input image (convert tensor back to PIL image)
        input_image_pil = transforms.ToPILImage()(input_image)  # Convert tensor to PIL image if it's a tensor
        input_image_pil.save(input_image_save_path)

        # Save the prediction mask as an image
        pred_image = Image.fromarray((prediction_mask * 255).astype(np.uint8))  # Convert mask to an image
        pred_image.save(prediction_save_path)

        print(f"Saved input image: {input_image_save_path}")
        print(f"Saved prediction: {prediction_save_path}")

transform_image = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
])

image_dataset = BreastUltrasoundImagesDataset(
    root_dir="/kaggle/input/breast-ultrasound-images-dataset/Dataset_BUSI_with_GT",
    transform_image=transform_image
)

# results = predict_and_store_images(image_dataset, model)

# save_predictions(results);

import matplotlib.pyplot as plt
import numpy as np

# Function to visualize input images and predictions
def visualize_malignant_predictions(results, num_samples=5):
    count = 0
    for result in results:
        if result["class_label"] == "malignant":
            image = result["image"].permute(1, 2, 0).cpu().numpy()  # Convert tensor to image format (H, W, C)
            prediction = result["prediction"]

            # Plot the original image and prediction mask side by side
            plt.figure(figsize=(10, 5))
            plt.subplot(1, 2, 1)
            plt.imshow(image)
            plt.title(f"Malignant Image: {result['file_name']}")

            plt.subplot(1, 2, 2)
            plt.imshow(prediction, cmap='gray')
            plt.title(f"Prediction for: {result['file_name']}")

            plt.show()

            count += 1
            if count >= num_samples:
                break

# Example usage:
# Filter the results for malignant images and visualize them
visualize_malignant_predictions(results, num_samples=5)  # Change num_samples to view more

# import shutil

# # Zip the benign directory
# shutil.make_archive("/kaggle/working/benign", 'zip', "/kaggle/working/benign")

# # Zip the malignant directory
# shutil.make_archive("/kaggle/working/malignant", 'zip', "/kaggle/working/malignant")

!pip install gradio

