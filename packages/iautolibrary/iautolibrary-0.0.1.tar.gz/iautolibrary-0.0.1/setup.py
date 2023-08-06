from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python'
]

setup(
    name = 'iautolibrary',
    version = '0.0.1',
    #description = 'intelligentAutomationLibraby',
    #long_description = open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url = '',
    author='Patrick Adu-Amankwah',
    author_email = '',
    license = 'MIT',
    classifiers=classifiers,
    keywords = '',
    packages=find_packages(),
    install_requires=['numpy', 'selenium', 'opencv-python', 'pyautogui', 'keyboard', 'pandas', 'requests', 'clipboard', 'tk']
)