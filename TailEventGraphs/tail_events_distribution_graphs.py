import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


def calculate_tails(mean, std):
    """Calculate the location of the tails for a density function.
    :param mean: a float, mean of distribution
    :param std:  a float, standard deviation of distribution
    :return: left and right locations of the tail events
    """
    return mean - 3 * std, mean + 3 * std


def calculate_xrange(mean, std):
    """ Calculate the plotting range for a probability distribution.
    Take the mean - 4 times the standard deviation as lower bound
    and mean + 4 times the standard deviation as upper bound.

    :param mean: a float, mean of distribution
    :param std: a float, standard deviation of distribution
    :return:
    """
    return mean - 4 * std, mean + 4 * std


def plot_tail_events(distribution, n=100, tail_color="#ff0000", center_color="#e6ffff", **params):
    """
    Plot a probability density function (pdf) and color the tails.

    Arguments
    ---------
    distribution: str
        The distribution to be plotted. Has to be either 'normal', 'uniform', 'laplace', or 'exponential'.

    n : int (default: 100)
        The number of values on the x axis used for plotting.

    tail_color: str (default: '#ff0000')
        Hex code for the tails.

    center_color: str (default: '#e6ffff')
        Hex code for the remainder of the area under the pdf.

    **params: floats, optional
        Parameters of the probability distribution, for example 'loc' or 'scale'.

    Returns
    -------
    fig, ax:
        Matplotlib figure and axis objects.
    """

    # Define the distribution:
    distributions = {
        "normal": stats.norm,
        "uniform": stats.uniform,
        "Laplace": stats.laplace,
        "exponential": stats.expon
    }
    assert distribution in distributions.keys(), \
        "Please specify a valid value for 'distribution'. \
        Valid values are 'normal', 'uniform', 'Laplace', and 'exponential'."
    dist = distributions[distribution](**params)

    # Get the expected value and standard deviation:
    mean = dist.mean()
    std = dist.std()

    # Define the x-range:
    x_min, x_max = calculate_xrange(mean, std)

    # Create the x vector and calculate corresponding values of y:
    x = np.linspace(x_min, x_max, n)
    y = dist.pdf(x)

    # Calculate the locations of the tails:
    tails = calculate_tails(mean, std)

    # Create the figure and axis objects:
    fig, ax = plt.subplots(1, 1, figsize=(9, 6))

    # Plot the distribution and fill the tails:
    ax.fill_between(x, 0, y, facecolor=center_color, interpolate=True)
    ax.fill_between(x, 0, y, where=x < tails[0], facecolor=tail_color, interpolate=True)
    ax.fill_between(x, 0, y, where=x > tails[1], facecolor=tail_color, interpolate=True)

    # Plot stylistics:
    plt.title("Tail events for {0} distribution".format(distribution), fontsize=16)
    plt.xlabel("x", fontsize=14)
    plt.ylabel("f(x)", fontsize=14)
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(14)
    ax.set_yticks([])

    for tail in list(zip(list(tails) + [mean], ['-', '-', '--'])):
        plt.axvline(x=tail[0], color='black', linestyle=tail[1], linewidth=1)

    plt.ylim(0, 1.2 * max(y))

    return fig, ax

if __name__ == '__main__':
    distribution = sys.argv[1]
    print("Creating plot for {0} distribution.".format(*[distribution]))
    fix, ax = plot_tail_events(distribution, n=100, tail_color="#ff0000", center_color="#e6ffff")
    plt.savefig(distribution)