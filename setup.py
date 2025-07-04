from setuptools import find_packages, setup
import os
from glob import glob   

package_name = 'sobits_tts'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'install'), glob('install/*.htsvoice')),
        (os.path.join('share', package_name, 'soundfile'), glob('soundfile/*.wav')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sobits',
    maintainer_email='f22hakuti@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'tts_action_server = sobits_tts.tts_action_server:main',
            'tts_action_client = sobits_tts.tts_action_client:main',
        ],
    },
)
