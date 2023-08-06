#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
import subprocess
from rsactftool.lib.timeout import timeout
from rsactftool.lib.keys_wrapper import PrivateKey
from rsactftool.lib.utils import rootpath

__SAGE__ = True

logger = logging.getLogger("global_logger")


def attack(attack_rsa_obj, publickey, cipher=[]):
    """binary polinomial factoring
        """
    try:
        sageresult = str(
            subprocess.check_output(
                [
                    "sage",
                    "%s/sage/binary_polinomial_factoring.sage" % rootpath,
                    str(publickey.n),
                ],
                timeout=attack_rsa_obj.args.timeout,
            )
        ).split(" ")

    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return (None, None)

    try:
        p = int(sageresult[0])
    except ValueError:
        return (None, None)

    if p > 0:
        q = publickey.n // p
        priv_key = PrivateKey(int(p), int(q), int(publickey.e), int(publickey.n))
        return (priv_key, None)
    else:
        return (None, None)
