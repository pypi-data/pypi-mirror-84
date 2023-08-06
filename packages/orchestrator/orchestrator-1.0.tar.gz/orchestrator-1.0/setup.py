from setuptools import setup

with open('version.txt') as f:
    ver = f.read().strip()

setup(name='orchestrator',
    version=ver,
    description='Process orchestrator',
    author='Vinogradov D',
    author_email='dmitrij.vinogradov@se.com',
    license='MIT',
    packages=['orchestrator'],
    zip_safe=False
)
