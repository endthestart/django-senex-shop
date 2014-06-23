import os
from setuptools import find_packages
from setuptools import setup

from senex_shop import __version__

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(name='django-senex-shop',
      version=__version__,
      description='Senex Shop',
      long_description=README,
      classifiers=[
          'Environment :: Web Environment',
          'Framework :: Django',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
      ],
      keywords='django e-commerce online-shop',
      author='Michael Anderson',
      author_email='andermic@gmail.com',
      url='http://www.github.com/endthestart/django-senex-shop',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'Pillow==2.1.0',
          'South==0.8.4',
          'django-countries==2.1.2',
          'django-custom-auth==0.1',
          'django-localflavor==1.0',
          'easy-thumbnails==1.4',
          'requests==2.2.1',
          'stripe==1.9.8',
      ],
      )