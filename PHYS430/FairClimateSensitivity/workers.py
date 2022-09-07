import fair

import numpy as np


def simulate(tcrecs=np.array([1.6, 2.75])):
    sim_length = 736

    emissions = np.zeros(sim_length)
    emissions[125] = 278 * 2.2

    C_no_decay, F_no_decay, T_no_decay = fair.forward.fair_scm(
        emissions=emissions,
        useMultigas=False,
        tau=np.ones(4) * 1_000_000,
        tcrecs=tcrecs
    )

    emissions_with_decay = np.zeros(sim_length)
    emissions_with_decay[:125] = 10.0

    C_with_decay, F_with_decay, T_with_decay = fair.forward.fair_scm(
        emissions=emissions_with_decay,
        useMultigas=False,
        tcrecs=tcrecs
    )

    return C_no_decay, F_no_decay, T_no_decay, C_with_decay, F_with_decay, T_with_decay
