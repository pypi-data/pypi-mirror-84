from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='abstract-ip-geolocation-api',
    version='1.5.1',
    description='IP Geolocation API from Abstract to geolocate any IP',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Eric Barns',
    author_email='eric@abstractapi.com',
    keywords=['IP geolocation', 'IP address', 'IP geolocation API', 'geolocation', 'ip location', 'geocoding'],
    download_url='https://pypi.org/project/abstract-ip-geolocation-api/',
    project_urls={
        'Documentation': 'https://www.abstractapi.com/ip-geolocation-api',
        'Source': 'https://github.com/geolocation-api/ip-geolocation-api-python/'
    }
)

install_requires = []

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
