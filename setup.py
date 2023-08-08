from setuptools import setup, find_packages

setup(
    name='zoom_video_migrator',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'update_users=zoom_video_migrator.update_users:main',
            'collect_legacy_data=zoom_video_migrator.collect_legacy_data:main',
            'collect_weekly_data=zoom_video_migrator.collect_weekly_data:main',
            'batch_job=zoom_video_migrator.batch_job:main'
        ]
    },
    install_requires=[
        'requests',
        'zoomus',
        'google-auth',
        'google-auth-oauthlib',
        'google-auth-httplib2',
        'google-api-python-client',
        'python-dotenv'
    ]
)