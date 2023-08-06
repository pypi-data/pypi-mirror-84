import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='cas',
    version='1.0.0',
    author='Chaos Initiative',
    author_email='contact@chaosinitiative.com',
    description='Chaos Automation System',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ChaosInitiative/CAS',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.7'
)
