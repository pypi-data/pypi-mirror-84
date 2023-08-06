from torchvision import transforms
import albumentations as A
from albumentations.pytorch import ToTensorV2
import numpy as np


def transformations(transformations=None, augmentations=None):
    """Create data transformations

    Args:
       transformations: List of transformation transforms
       augmentations: List of Augumentation transforms

    Returns:
        Transform object containing defined data transformations.
    """
    transforms_list = [
        # convert the data to torch.FloatTensor with values within the range [0.0 ,1.0]
        transforms.ToTensor()
    ]

    if transformations is not None:
        transforms_list = transforms_list + transformations

    if augmentations is not None:
        transforms_list = augmentations + transforms_list

    return transforms.Compose(transforms_list)

def transforma_albumentation(transformations=None, augmentations=None):
        """Create data transformations

        Args:
           transformations: List of Albumentation transforms
           augmentations: List of Albumentation transforms

        Returns:
            Transform object containing defined data transformations.
        """
        transforms_list = []
        default_transforms_list = [
            # convert the data to torch.FloatTensor with values within the range [0.0 ,1.0]
            ToTensorV2()
        ]

        if transformations is not None:
            transforms_list = transformations + default_transforms_list

        if augmentations is not None:
            transforms_list = augmentations + transforms_list

        return A.Compose(transforms_list)
