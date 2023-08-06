import torch
import numpy as np

def get_stats(dataset):

    """
    Args
    ----
    dataset: torch Dataset
    """

    if type(dataset.data) == np.ndarray:
        dset = torch.tensor(dataset.data, dtype=torch.float)
    else:
        dset = dataset.data

    n_channels = dset.shape[-1]

    if dset.max().item() == 255:
        dset.div_(255.0)

    d_mean = [round(dset[..., channel].mean().item(), 4) for channel in list(range(n_channels))]
    d_std = [round(dset[..., channel].std().item(), 4) for channel in list(range(n_channels))]

    return tuple(d_mean), tuple(d_std)

