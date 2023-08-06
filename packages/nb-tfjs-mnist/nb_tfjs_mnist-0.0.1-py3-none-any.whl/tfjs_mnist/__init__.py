"""
Return config on servers to start for tfjs_mnist
See https://jupyter-server-proxy.readthedocs.io/en/latest/server-process.html
for more information.
"""

__version__="0.0.1"

import os
import pkg_resources

def setup_tfjs_mnist():
    fpath = pkg_resources.resource_filename('tfjs_mnist', 'static/')
    return {
        'command': ["python", "-m", "http.server", "--directory", fpath, "{port}"],
        'environment': {},
        'launcher_entry': {
            'title': 'tfjs_mnist',
            'icon_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons', 'tfjs_mnist.svg')
        }
    }