"""
pydirbuster Module - Python Web Directory and File Brute Forcer
###############

pydirbuster is module for website file enumeration written in python3.
Basic Usage:
    >>> import pydirbuster
    >>> webbuster = pydirbuster.Pybuster(url="http://doctor/", wordfile="/root/HackTheBox/tools/short.txt",
    ... exts=['php','html'])
    >>> webbuster.Run()
    =================================================================
    Pydirbuster v0.02
    =================================================================
    Url:                http://doctor/
    Threads:            15
    Wordlist:           /root/HackTheBox/tools/short.txt
    Status Codes:       200,204,301,302,307,401,403
    User Agent:         python-requests/2.23.0
    =================================================================
    /.hta (Status : 403)
    /.htaccess.php (Status : 403)
    /.htaccess.html (Status : 403)
    /.hta.html (Status : 403)
    /.htpasswd (Status : 403)
    /.htpasswd.php (Status : 403)
    /.htpasswd.html (Status : 403)
    /.hta.php (Status : 403)
    /.htaccess (Status : 403)
    /index.html (Status : 200)
    =================================================================
    Time elapsed : 1.7652253159903921
    =================================================================

The Pybuster class takes at least a url and a valid wordfile name. The exts parameter
is optional but shown here for verbosity sake and and understanding of common use cases.
All paramters are documented under the Pybuster class.
"""

from . import utils
__version__ = "Pydirbuster v0.05"
from pydirbuster.main import Pybuster
