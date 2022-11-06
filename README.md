# ztStatus

Simple monitoring of your ZeroTier network

## Prerequisites:

* Python 3.7+
* [requests](https://pypi.org/project/requests/)
* [colorama](https://pypi.org/project/colorama/) (for the console version)
* [rich](https://pypi.org/project/rich/) (for the "GUI" version)

## Usage:

Mark as executable and run either `./ztconsole.py` for the console version or `./ztGUI.py` for the "GUI" version.
Configuration requirements are provided by the application.

### Console version

One-off printout of all your networks and the status of their members.

### "GUI" version

Live monitoring of one of your networks with all its members. Refreshes once a minute.