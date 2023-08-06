# author: Daniel Burkhardt <daniel.burkhardt@yale.edu>
# (C) 2017 Krishnaswamy Lab GPLv2

from __future__ import print_function, division
import warnings
import scprep


def library_size_normalize(data, verbose=False):
    """magic.preprocessing is deprecated. Please use scprep.normalize instead.
    Read more at http://scprep.readthedocs.io/
    """
    raise RuntimeError(
        "magic.preprocessing is deprecated. Please use scprep.normalize instead. "
        "Read more at http://scprep.readthedocs.io",
        FutureWarning,
    )
