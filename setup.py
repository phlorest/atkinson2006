from setuptools import setup


setup(
    name='cldfbench_atkinson2006',
    py_modules=['cldfbench_atkinson2006'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'atkinson2006=cldfbench_atkinson2006:Dataset',
        ]
    },
    install_requires=[
        'cldfbench',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
