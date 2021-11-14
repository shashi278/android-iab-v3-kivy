# IABwrapper
#### Wrapper around anjlab's Android In-app Billing Version 3 to be used in Kivy apps

[![Build Status](https://app.travis-ci.com/shashi278/android-iab-v3-kivy.svg?branch=main)](https://app.travis-ci.com/shashi278/android-iab-v3-kivy) [![Python 3.6](https://img.shields.io/pypi/pyversions/kivymd)](https://www.python.org/downloads/release/python-360/) [![PyPI](https://img.shields.io/pypi/v/iabwrapper)](https://pypi.org/project/IABwrapper/) [![format](https://img.shields.io/pypi/format/iabwrapper)](https://pypi.org/project/IABwrapper/) [![downloads](https://img.shields.io/pypi/dm/iabwrapper)](https://pypi.org/project/iabwrapper/) [![code size](https://img.shields.io/github/languages/code-size/shashi278/android-iab-v3-kivy)]() [![repo size](https://img.shields.io/github/repo-size/shashi278/android-iab-v3-kivy)]()

#
### Install
```bash
pip install iabwrapper
```
#
### Important ( Add these into your buildozer.spec )
* Add `"mavenCentral()"` in `android.add_gradle_repositories`
* Add `com.anjlab.android.iab.v3:library:2.0.0` in `android.gradle_dependencies`

#
### Usage
```python
from iabwrapper import PythonBillingProcessor
```
You'll only be using the [`PythonBillingProcessor`](https://github.com/shashi278/android-iab-v3-kivy/blob/main/iabwrapper/main.py#L102) class so you can look at what all parameters are required for different methods from the source code for now.

To know about what a method does, please follow ![anjlab's android-inapp-billing-v3](https://github.com/anjlab/android-inapp-billing-v3) docs for reference. Docs about using this library will be updated.
