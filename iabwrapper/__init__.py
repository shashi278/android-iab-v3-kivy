from kivy.logger import Logger
from kivy.utils import platform

__version__ = "0.0.1"
_log_message = ("IABwrapper:"
                + f" {__version__}"
                + f' (installed at "{__file__}")'
                )

Logger.info(_log_message)

if platform == "android":
    from main import PythonBillingProcessor

else:
    Logger.error("IABwrapper: This module is only available on Android")