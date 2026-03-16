"""
ImprovedCNNEmotion model architecture for facial emotion recognition.

This model was designed for the FER2013 dataset with 7 emotion classes.
Extracted from the original Streamlit dashboard for reusability across
Flask API and Streamlit implementations.

Architecture:
- 4 Convolutional blocks (32→64→128→256 channels)
- Double convolution per block with BatchNorm + ReLU
- Progressive dropout (0.05→0.10→0.15→0.20)
- Global Average Pooling (GAP)
- FC layers: 256→128→7 classes
- Input: 48x48 grayscale images
- Output: 7 emotion classes (Angry, Disgust, Fear, Happy, Neutral, Sad, Surprise)

Performance: 65.9% accuracy on FER2013 test set
"""

import torch
import torch.nn as nn


class ImprovedCNNEmotion(nn.Module):
    """
    Improved CNN architecture for emotion detection from facial images.

    Args:
        num_classes (int): Number of emotion classes (default: 7 for FER2013)
        dropout_head (float): Dropout rate for the classification head (default: 0.5)
    """

    def __init__(self, num_classes=7, dropout_head=0.5):
        super().__init__()

        def conv_block(in_ch, out_ch, p_drop=0.0):
            """
            Creates a double-convolution block with BatchNorm, ReLU, and MaxPooling.

            Args:
                in_ch (int): Input channels
                out_ch (int): Output channels
                p_drop (float): Dropout probability (applied before MaxPool)

            Returns:
                nn.Sequential: The convolutional block
            """
            layers = [
                nn.Conv2d(in_ch, out_ch, kernel_size=3, padding=1, bias=False),
                nn.BatchNorm2d(out_ch),
                nn.ReLU(inplace=True),

                nn.Conv2d(out_ch, out_ch, kernel_size=3, padding=1, bias=False),
                nn.BatchNorm2d(out_ch),
                nn.ReLU(inplace=True),
            ]
            if p_drop > 0:
                layers.append(nn.Dropout2d(p_drop))
            layers.append(nn.MaxPool2d(2, 2))
            return nn.Sequential(*layers)

        # Convolutional feature extractor
        self.features = nn.Sequential(
            conv_block(1,   32, p_drop=0.05),  # 48x48 -> 24x24
            conv_block(32,  64, p_drop=0.10),  # 24x24 -> 12x12
            conv_block(64, 128, p_drop=0.15),  # 12x12 -> 6x6
            conv_block(128, 256, p_drop=0.20), # 6x6   -> 3x3
        )

        # Global Average Pooling (reduces parameters, prevents overfitting)
        self.gap = nn.AdaptiveAvgPool2d((1, 1))

        # Classification head
        self.classifier = nn.Sequential(
            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout_head),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        """
        Forward pass through the network.

        Args:
            x (torch.Tensor): Input tensor of shape (batch_size, 1, 48, 48)

        Returns:
            torch.Tensor: Logits of shape (batch_size, num_classes)
        """
        x = self.features(x)
        x = self.gap(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x
