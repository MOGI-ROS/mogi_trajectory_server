from setuptools import find_packages, setup

package_name = 'mogi_trajectory_server'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='David Dudas',
    maintainer_email='david.dudas@outlook.com',
    description='ROS2 trajectory server',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'mogi_trajectory_server = mogi_trajectory_server.trajectory:main',
            'mogi_trajectory_server_topic_based = mogi_trajectory_server.trajectory_topic_based:main'
        ],
    },
)
