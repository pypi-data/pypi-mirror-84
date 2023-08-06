from typing import Union

import numpy as np

Numerical = Union[float, np.ndarray]


def _haaland_dimless(rey_num: Numerical, epsilon_r: Numerical) -> Numerical:
    """
    Haaland approximation of the Colebrook equation,
    https://en.wikipedia.org/wiki/Darcy_friction_factor_formulae#Haaland_equation.

    Args:
        rey_num (float or np.ndarray): Reynolds number = rho*u*D/mu
        epsilon_r (float or np.ndarray): Pipe's relative roughness, given as pipe effective
            roughness (epsilon) scaled with the pipe diameter (D) - epsilon_r = epsilon / D

    Returns:
        darcy_friction, f (float or np.ndarray): The Darcy-Weisbach friction factor for a full-flowing circular pipe.

    """
    flow_rough = (epsilon_r / 3.7) ** 1.11
    flow_smooth = 6.9 / rey_num
    denom = -1.8 * np.log10(flow_rough + flow_smooth)
    f = (1 / denom) ** 2
    return f
