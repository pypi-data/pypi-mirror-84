from setuptools import setup

from os import path

def get_long_description():
    with open(
        path.join(path.dirname(path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()

setup(
    name="nb-tfjs_mnist",
    packages= ['tfjs_mnist'],
    include_package_data=True,
    package_data={
        "tfjs_mnist": ["static/index.html",
         "static/mnist_images.png",
         "static/mnist_labels_uint8",
         "static/mnist.js",
         "static/tufte.css"
         ],
    },
    install_requires=[
        'jupyter-server-proxy',
        'notebook'
    ],
    url="https://github.com/innovationOUtside/serverproxy_tfjs_demos",
    author='Tony Hirst',
    author_email='tony.hirst@open.ac.uk',
    description='Jupyter notebook server proxy extension for tfjs (MNIST)',
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    entry_points={
        'jupyter_serverproxy_servers': [
            'tfjs_mnist = tfjs_mnist:setup_tfjs_mnist',
        ]
    })