import os
import sys
from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '600')
root_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.join(root_dir, "libs", "applibs"))

import json  # NOQA: E402
import traceback  # NOQA: E402

from kivy.factory import Factory  # NOQA: E402
from cnpm import CNPM  # NOQA: E402

__version__ = "0.1"

"""
Registering factories from factory.json.
"""
r = Factory.register

with open("factory_registers.json") as fd:
    custom_widgets = json.load(fd)
    for module, _classes in custom_widgets.items():
        for _class in _classes:
            r(_class, module=module)


try:
    CNPM().run()
except Exception:
    error = traceback.format_exc()

    """
    If the app encounters an error it automatically saves the
    error in a file called ERROR.log.
    You can use this for BugReport purposes.
    """
    with open("ERROR.log", "w") as error_file:
        error_file.write(error)

    print(error)
