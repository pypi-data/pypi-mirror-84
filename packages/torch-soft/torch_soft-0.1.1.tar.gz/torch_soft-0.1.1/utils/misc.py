from utils.config import *
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR,ReduceLROnPlateau,OneCycleLR
from torchsummary import summary
import torch.nn as nn



def get_model_summary(model, input_size):
    """ Print the model summary """
    print(summary(model, input_size))


def cross_entropy_loss_fn():
    return nn.CrossEntropyLoss()


def nll_loss():
    return nn.NLLLoss()


def sgd_optimizer(model, lr=LEARNING_RATE, momentum=MOMENTUM, l2_factor=0):
    """

    :param model: Network model
    :param lr: learning rate
    :param momentum: momentum of previous history to be taken
    :param l2_factor:

    :return: SGD optimizer instance
    """
    return optim.SGD(model.parameters(), lr=lr, momentum=momentum, weight_decay=l2_factor)


def StepLR_scheduler(optimizer, step_size=STEP_SIZE, gamma=0.1):
    """

    :param optimizer: model optimizer
    :param step_size: frequency after which lr is updated
    :param gamma: factor by which lr is updated.

    :return: sterLR instance
    """
    return StepLR(optimizer, step_size=step_size, gamma=gamma)

def ReduseLR_onplateau(optimizer, patience = 2, verbose = False):
    """

    :param optimizer (torch.optim) : Model optimizer
    :param patience (int): Number of epochs to wait before updating the lr when metrix doesnt update
    :param verbose (bool): print the log?

    :return: ReduseLR_onplateau instance
    """
    return ReduceLROnPlateau(optimizer, patience=patience, verbose=verbose)


def one_cycle_lr(
        optimizer, max_lr, epochs, steps_per_epoch, pct_start=0.5, div_factor=10.0, final_div_factor=10000
):
    """Create One Cycle Policy for Learning Rate.
    Args:
        optimizer (torch.optim): Model optimizer.
        max_lr (float): Upper learning rate boundary in the cycle.
        epochs (int): The number of epochs to train for. This is used along with
            steps_per_epoch in order to infer the total number of steps in the cycle.
        steps_per_epoch (int): The number of steps per epoch to train for. This is
            used along with epochs in order to infer the total number of steps in the cycle.
        pct_start (float, optional): The percentage of the cycle (in number of steps)
            spent increasing the learning rate. (default: 0.5)
        div_factor (float, optional): Determines the initial learning rate via
            initial_lr = max_lr / div_factor. (default: 10.0)
        final_div_factor (float, optional): Determines the minimum learning rate via
            min_lr = initial_lr / final_div_factor. (default: 1e4)

    Returns:
        OneCycleLR instance.
    """

    return OneCycleLR(
        optimizer, max_lr, epochs=epochs, steps_per_epoch=steps_per_epoch,
        pct_start=pct_start, div_factor=div_factor, final_div_factor=final_div_factor
    )

def set_seed(seed, cuda):
    """ Setting the seed makes the results reproducible. """
    torch.manual_seed(seed)
    if cuda:
        torch.cuda.manual_seed(seed)


def initialize_device(seed):
    """ checking the cuda avalibility and sedding based on it"""

    # Check CUDA availability
    cuda = torch.cuda.is_available()
    print('GPU Available?', cuda)

    # Initialize seed
    set_seed(seed, cuda)

    # Set device
    device = torch.device("cuda" if cuda else "cpu")

    return cuda, device








