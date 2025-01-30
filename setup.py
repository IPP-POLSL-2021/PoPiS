from setuptools import setup, find_packages

setup(
    name='sejm_api_wrappers',
    version='0.1.0',
    description='Python API wrappers for the Polish Sejm (Parliament) API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/sejm-api-wrappers',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas',
        'numpy',
        'plotly',
        'streamlit-aggrid',
        'scipy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='sejm parliament api poland politics',
    python_requires='>=3.8',
)
