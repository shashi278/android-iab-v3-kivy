from kivy.logger import Logger
from kivy.utils import platform

__version__ = "1.0.0"
lib_name = "iabwrapper"
_log_message = (f"{lib_name}:"
                + f" {__version__}"
                + f' (installed at "{__file__}")'
                )

Logger.info(_log_message)

if platform == "android":
    from iabwrapper.wrapper import BillingProcessor

else:
    Logger.error(f"{lib_name}: This module is only available on Android")
