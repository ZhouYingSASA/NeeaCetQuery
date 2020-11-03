#!/usr/bin/python3

import os
from app import create_app
from flask_script import Manager, Shell

config = os.getenv("FLASK_CONFIG", "default")
app = create_app(config)
manager = Manager()

if __name__ == '__main__':
    print("config: %s" % config)
    manager.run()
