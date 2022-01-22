from pathlib import Path

from setuptools import find_packages, setup

readme_file = Path(__file__).parent / 'README.md'
if readme_file.exists():
    with readme_file.open() as f:
        long_description = f.read()
else:
    # When this is first installed in development Docker, README.md is not available
    long_description = ''

setup(
    name='opengeo',
    version='0.2.0',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Apache 2.0',
    author='Kitware, Inc.',
    author_email='rgd@kitware.com',
    url='https://github.com/ResonantGeoData/ResonantGeoData',
    keywords='',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django :: 3.0',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python',
    ],
    python_requires='>=3.8',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django-configurations[database,email]>=0.19.2',
        'django-cleanup',
        'django-crispy-forms',
        'rules',
        # Production-only
        'django-composed-configuration[prod]>=0.16',
        'django-s3-file-field[minio]',
        'flower',
        'gunicorn',
        'pylibmc>=1.5.1',
        # RGD
        'django-rgd-3d==0.2.15',
        'django-rgd-fmv==0.2.15',
        'django-rgd-geometry==0.2.15',
        'django-rgd-imagery==0.2.15',
    ],
    extras_require={
        'dev': [
            'django-composed-configuration[dev]>=0.16',
            'django-debug-toolbar',
            'ipython',
            'tox',
        ],
        'worker': [
            'django-rgd-3d[worker]==0.2.15',
            'django-rgd-fmv[worker]==0.2.15',
            'django-rgd-geometry[worker]==0.2.15',
            'django-rgd-imagery[worker]==0.2.15',
        ],
        'fuse': [
            'django-rgd[fuse]==0.2.15',
        ],
    },
)
