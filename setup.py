from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'sobits_tts'

data_files = [
    ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
    (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
(os.path.join('share', package_name, 'soundfile'), glob('soundfile/*')),
]

def add_recursive_files(src_dir, target_base):
    if os.path.exists(src_dir):
        for root, dirs, files in os.walk(src_dir):
            rel_path = os.path.relpath(root, src_dir)
            install_path = os.path.join(target_base, rel_path)
            
            file_list = [os.path.join(root, f) for f in files]
            if file_list:
                data_files.append((install_path, file_list))
add_recursive_files('install/supertonic', os.path.join('share', package_name, 'install/supertonic'))

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sobits',
    maintainer_email='f22hakuti@gmail.com',
    description='TTS package for ROS 2',
    license='BSD-3-Clause',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'tts_action_server = sobits_tts.tts_action_server:main',
            'tts_action_client = sobits_tts.tts_action_client:main',
        ],
    },
)