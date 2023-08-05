# Pydirbuster

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://github.com/Percyjackson235/pydirbuster.git)

Pydirbuster is a Python based Web Directory and File Brute Forcer.
# Installation
Pip:
```
$ pip3 install pydirbuster
```
Github:
```
$ git clone http://github.com/PercyJackson235/pydirbuster.git
$ cd pydirbuster
$ python3 setup.py install
```
# Usage
Package Style:
```
>>> import pydirbuster
>>> webbuster = pydirbuster.Pybuster(url="http://doctor/",
... wordfile="/root/HackTheBox/tools/short.txt", exts=['php','html'])
>>> webbuster.Run()
=================================================================
Pydirbuster v0.02
=================================================================
Url:                http://doctor/
Threads:            15
Wordlist:           /root/HackTheBox/tools/short.txt
Status Codes:       200,204,301,302,307,401,403
User Agent:         python-requests/2.23.0
Extensions:         php,html
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
```
Commandline Script Style:
```
(venv) root@kali:~/HackTheBox/tools/venv# pydirbuster -u http://cartoon.worker.htb -w ../short.txt -t 30 -z -x php,html
=================================================================
Pydirbuster v0.04
=================================================================
Url:                http://cartoon.worker.htb/
Threads:            30
Wordlist:           ../short.txt
Status Codes:       200,204,301,302,307,401,403
User Agent:         Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0;  Trident/5.0)
Extensions:         php,html
=================================================================
/Index.html (Status : 200)                                                                  
/Images (Status : 403)                                                                      
/css (Status : 403)                                                                         
/fonts (Status : 403)                                                                       
/images (Status : 403)                                                                      
/index.html (Status : 200)                                                                  
/index.html (Status : 200)                                                                  
/js (Status : 403)                                                                          
=================================================================                           
Time elapsed : 35.35524610700668                                                            
==================================================================================================================================
Time elapsed : 1.742801600979874
=================================================================                  
```
Commandline Module Style:
```
(venv) root@kali:~/HackTheBox/tools/venv# python -m pydirbuster -u http://cartoon.worker.htb -w ../short.txt -t 30 -z -x php,html
=================================================================
Pydirbuster v0.04
=================================================================
Url:                http://cartoon.worker.htb/
Threads:            30
Wordlist:           common.txt
Status Codes:       200,204,301,302,307,401,403
User Agent:         Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0;  Trident/5.0)
Extensions:         php,html
=================================================================
/Index.html (Status : 200)                                                                  
/Images (Status : 403)                                                                      
/css (Status : 403)                                                                         
/fonts (Status : 403)                                                                       
/images (Status : 403)                                                                      
/index.html (Status : 200)                                                                  
/index.html (Status : 200)                                                                  
/js (Status : 403)                                                                          
=================================================================                           
Time elapsed : 35.35524610700668                                                            
================================================================= 
```
# Options
Commandline Style:
```
usage: pydirbuster [-h] -u URL -w WORDFILE [--user USER] [--pass PASSWORD] [-x EXTS] [-t THREADS] [-o LOGFILE] [-s CODES] [-f] [-z [USER_AGENT]]

Python Web Directory and File Brute Forcer

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     The url to start brute foroce from.
  -w WORDFILE, --wordlist WORDFILE
                        The wordlist to use for brute force.
  --user USER           HTTP Username
  --pass PASSWORD       HTTP Password
  -x EXTS               File Extensions - must be commad delimited list
  -t THREADS, --threads THREADS
                        The amount of threads to use.
  -o LOGFILE, --output LOGFILE
                        File to log results.
  -s CODES              HTTP Status Codes to accept in a comma delimited list. Default - 200,204,301,302,307,401,403
  -f                    Force wildcard proccessing.
  -z [USER_AGENT], --user-agent [USER_AGENT]
                        Custom or random user agent. -z 'User-agent' for custom. -z for random
```
- All flags, except for `-u` and `-w`, for the url and wordlist respectively, are optional. The value for `-z`, the user agent, is optional because a naked `-z` will randomly select a user-agent instead of setting a custom one.

Package Style:
```
class Pybuster(builtins.object)
 |  Pybuster(url: str, wordfile: str, threads: int = 15, exts: list = [''], logfile: str = None, codes: list = [200, 204, 301, 302, 307, 401, 403], user: str = None, password: str = None, force: bool = False, user_agent: str = 'python-requests/2.23.0')
 |  
 |  The Pybuster class is the main interface for this website scanner.
 |  
 |  Pybuster Class:
 |  
 |  param: url - The website base url for scanning.
 |  type: str
 |  
 |  param: wordfile - The filepath, relative or absolute for wordlist.
 |  type: str
 |  
 |  param: threads - The number of threads for the scanner to run. Default = 15
 |  type: int
 |  
 |  param: exts - The list of file extensions to check. default = ['']
 |  It is best pass it a list, ie. ['php', 'html', 'png'], but it can be
 |  passed a comma delimited string ex., 'php,html,png'
 |  type: list
 |  
 |  param: logfile - The name of an output file write results to.
 |  type: str
 |  
 |  param: codes - The http status codes to accept in responses.
 |  Can be passed a list of numbers in either int or str forms, or a 
 |  comma delimited string. So ['200','204','301','302','307','401','403'],
 |  [200,204,301,302,307,401,403], and "200,204,301,302,307,401,403" are all
 |  valid, but the inner values must be able to converted to integers.
 |  Default = [200,204,301,302,307,401,403]
 |  param: user - HTTP username - Default = None
 |  type: list
 |  
 |  param: password - HTTP password - Default = None
 |  type: str
```
- The `url` and `wordfile` parameters are required for the Pybuster object, all other parameters are optional.
- Both the `exts` and `codes` parameters are better off being passed a list, but can take a comma delimited string, but the codes parameter requires that the values in the list or comma delimited string be valid integers.
- The Pybuster class expects the `user_agent` paramater to be a string or None. If it is passed None, the object will randomly select a user-agent to impersonate.
