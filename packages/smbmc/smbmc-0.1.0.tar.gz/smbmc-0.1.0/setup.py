# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['smbmc']

package_data = \
{'': ['*']}

install_requires = \
['defusedxml>=0.6.0,<0.7.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'smbmc',
    'version': '0.1.0',
    'description': 'Supermicro BMC interface',
    'long_description': 'SMBMC\n=====\n\nAn unofficial Python interface for obtaining metrics from Supermicro BMCs.\n\nThe following metrics are accessible:\n\n- Sensor: Temperature, Fan, Voltage, etc.\n- PMBus: Power Consumption, Fan, Temperature, etc.\n\n**Note:** This library depends on the BMC web-interface being available.\n\nUsage\n-----\n\n::\n\n    # smbmc_example.py\n    from smbmc import Client\n\n    # initialise client with connection details\n    c = Client(IPMI_SERVER, IPMI_USER, IPMI_PASS)\n\n    # retrieve session token\n    c.login()\n\n    # obtain sensor metrics\n    sensors = c.get_sensor_metrics()\n\n    # and pmbus metrics\n    power_supplies = c.get_pmbus_metrics()\n\n    # or, retrieve all known metrics\n    metrics = c.get_metrics()\n\nContributing\n------------\n\nThis library has been tested on a system with the following components:\n\n- Chassis: SC846 (unknown revision; possibly 846BA-R920B)\n- Motherboard: CSE-PTJBOD-CB3\n- Power Supply: PWS-920P-SQ\n- Backplane: BPN-SAS2-846EL1\n- Power Distribution Board: PDB-PT846-2824\n\nIf there are any errors or additional functionality for other components, please file an issue with as *much* detail as you can!\n\nLegal\n-----\n\nThis library is not associated with Super Micro Computer, Inc.\n\nSupermicro have released some `BMC/IPMI <https://www.supermicro.com/wftp/GPL/SMT/SDK_SMT_X9_317.tar.gz>`_ code under the GPL, which has been used as a reference. Therefore, this library is licensed as GPLv3.\n',
    'author': 'George Rawlinson',
    'author_email': 'george@rawlinson.net.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/grawlinson/smbmc',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
