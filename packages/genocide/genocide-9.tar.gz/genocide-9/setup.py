# GENOCIDE - the king of the netherlands commits genocide
#
# OTP-CR-117/19/001 otp.informationdesk@icc-cpi.int https://genocide.rtfd.io

__copyright__= "Public Domain"

import atexit, os

from setuptools import setup
from setuptools.command.install import install

servicetxt="""[Unit]
Description=GENOCIDE - the king of the netherlands commits genocide | OTP-CR-117/19/001 | otp.informationdesk@icc-cpi.| int https://genocide.rtfd.io
After=network-online.target

[Service]
Group=genocide
User=genocide
StandardOutput=append:/var/log/genocide/genocide.log
StandardError=append:/var/log/genocide/genocide.log
ExecStart=/usr/local/bin/genocide wd=/var/lib/genocide mods=irc,rss,udp -w

[Install]
WantedBy=multi-user.target
"""

class Install(install):
    def __init__(self, *args, **kwargs):
        super(Install, self).__init__(*args, **kwargs)
        atexit.register(postinstall)

def skipopen(txt, skip=["already"]):
    txt += " 2>&1"
    try:
        for line in os.popen(txt).readlines():
             pass
    except Exception as ex:
        for rej in skip:
           if rej in str(ex):
               return

def postinstall():
    skipopen("mkdir /var/lib/genocide")
    skipopen("mkdir /var/lib/genocide/mods")
    skipopen("mkdir /var/lib/genocide/store")
    skipopen("mkdir /var/log/genocide")
    skipopen("touch /var/log/genocide/genocide.log")
    skipopen("chown -R genocide:genocide /var/lib/genocide")
    skipopen("chown -R genocide:genocide /var/log/genocide")
    skipopen("chmod 700 /var/lib/genocide/")
    skipopen("chmod 700 /var/lib/genocide/mods")
    skipopen("chmod 700 /var/lib/genocide/store")
    skipopen("chmod -R 400 /var/lib/genocide/mods/*.py")
    skipopen("chmod 744 /var/log/genocide/")
    skipopen("groupadd genocide")
    skipopen("useradd genocide -g triple -d /var/lib/genocide")
    writeservice()

def writeservice():
    p = "/etc/systemd/system/genocide.service"
    if not os.path.exists(p):
        f = open(p, "w")
        f.write(servicetxt)
        f.close()

def mods():
    import os
    return [x[:-3] for x in os.listdir("genocide") if x.endswith(".py")]

def read():
    return open("README.rst", "r").read()

setup(
    name='genocide',
    version='9',
    url='https://github.com/bthate/genocide',
    author='Bart Thate',
    author_email='bthate@dds.nl', 
    description="GENOCIDE 9 TRIPLE 3 OTP-CR-117/19/001 otp.informationdesk@icc-cpi.int https://genocide.rtfd.io",
    long_description=read(),
    license='Public Domain',
    packages=["genocide", "triple"],
    namespace_packages=["genocide", "triple"],
    zip_safe=False,
    scripts=["bin/genocide"],
    cmdclass={'install': Install},
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
