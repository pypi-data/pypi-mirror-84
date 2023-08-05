#!/usr/bin/env python
"""vzt-cdp-chaos-poc extension builder and installer"""

import setuptools

name = 'vztcdpchaos-network'
desc = 'Extension for creating network faults'

classifiers = [
    'License :: Freely Distributable',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: Implementation',
    'Programming Language :: Python :: Implementation :: CPython'
]
author = "vzt-cdp"
license = 'Apache License Version 2.0'
packages = [
    'cdpchaosnetwork',
    'cdpchaosnetwork.dns',
    'cdpchaosnetwork.latency',
    'cdpchaosnetwork.packetloss'


]


setup_params = dict(
    name=name,
    version='1.6.3',
    description=desc,

    classifiers=classifiers,
    author=author,

    license=license,
    packages=packages,
    include_package_data=True,
    install_requires=['chaostoolkit-lib>=1.7.0',
                      'cdpchaostoolkit',
    'logzero',
    'psutil'],
    python_requires='>=3.5.*'
)


def main():
    """Package installation entry point."""
    setuptools.setup(**setup_params)


if __name__ == '__main__':
    main()
