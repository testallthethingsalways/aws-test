from setuptools import setup
try:
    # for pip >= 10
    from pip._internal import req
except ImportError:
    # for pip <= 9.0.3
    from pip import req

install_reqs = req.parse_requirements('requirements.txt', session=False)

reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='aws-test',
    version='1.0',
    install_requires=reqs,
)
