from distutils.core import setup
setup(
  name = 'pymeteobridgeio',
  packages = ['pymeteobridgeio'],
  package_data={
    "": ["*.md"],
    "pymeteobridgeio": ["translations/*.json"],
  },
  version = '0.21.5',
  license='MIT',
  description = 'Python Wrapper for Meteobridge Data Logger', 
  author = 'Bjarne Riis',
  author_email = 'bjarne@briis.com',
  url = 'https://github.com/briis/pymeteobridgeio',
  keywords = ['Meteobridge', 'Python'],
  install_requires=[
          'aiohttp',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers', 
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)