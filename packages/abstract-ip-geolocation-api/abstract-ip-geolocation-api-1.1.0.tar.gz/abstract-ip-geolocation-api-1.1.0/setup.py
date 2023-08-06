from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='abstract-ip-geolocation-api',
    version='1.1.0',
    description='IP Geolocation API from Abstract to geolocate any IP',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Eric Barns',
    author_email='eric@abstractapi.com',
    keywords=['IP geolocation', 'IP address', 'IP geolocation API', 'geolocation', 'ip location', 'geocoding'],
    url='https://github.com/geolocation-api/ip-geolocation-api-python/',
    download_url='https://pypi.org/project/abstract-ip-geolocation-api/'
)

install_requires = []

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
