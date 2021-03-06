#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup_requirements = ['pytest-runner']

with open('requirements.txt') as f:
    requirements = list(f.readlines())

test_requirements = ['pytest']

setup(
    author="Andre Kahles",
    author_email='andre.kahles@inf.ethz.ch',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="This project contains genomics scripts and utilities used in the Ratschlab",
    entry_points={
        'console_scripts': [
            'count_expression=gromics.counting.count_expression:main',
            'count_expression_prep_anno=gromics.counting.count_expression_prep_anno:main',
            'compute_lib_size=gromics.counting.compute_lib_size:main',
            'collect_counts=gromics.counting.collect_counts:main',
            'count_hdf2tsv=gromics.counting.count_hdf2tsv:main',
            'splice_burden_project=gromics.splice_burden.splice_burden_project:main',
            'splice_burden_compute=gromics.splice_burden.splice_burden_compute:main',
            'splice_burden_plot_tcga=gromics.splice_burden.splice_burden_plot_tcga:main',
            'genename_to_HUGO=gromics.tcga_boxplot:main'
        ],
    },
    scripts=[
        'scripts/difftest/deseq2.R',
        'scripts/difftest/Limma.R',
        'scripts/hypoxia/tupro_pipeline_hypoxia.R',
        'scripts/hypoxia/hypoxia_plots.r',
        'scripts/tcga_boxplot/variant_expression_context.TCGA.list_of_genes.R',
        'scripts/tcga_boxplot/parse_rna_tcga_pat_data.r',
        'scripts/tcga_boxplot/quartile_norm.pl',
        'scripts/tcga_boxplot/filter_genes.py'
    ],
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='gromics',
    name='gromics',
    packages=find_packages(include=['gromics']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ratschlab/gromics',
    version='0.1.0',
    zip_safe=False,
)
