from distutils.core import setup

with open("README.md", "r") as f:
  _long_description = f.read()


setup(
  name = 'shary',
  packages = ['shary'],
  version = '0.0.1',
  license='GNU General Public License Version 3',
  description = 'API Wrapper around several File Hosting Services',
  long_description = _long_description,
  long_description_content_type='text/markdown',
  author = 'Aaron Levi Can (aaronlyy)',
  author_email = 'aaronlevican@gmail.com',
  url = 'https://github.com/aaronlyy/shary',
  download_url = 'https://github.com/aaronlyy/levish/archive/v0.0.1.tar.gz',
  keywords = ['api', 'wrapper', 'files', 'hosting', 'filehosting'],
  install_requires=[
        "requests"
      ],
)