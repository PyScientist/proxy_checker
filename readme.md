## Proxy checker v1.0

Proxy checker writen on requests library and also includes pysocks extension.
This module provide functional to check availability of different types of proxies
(http, https, socks4, socks5) for particularly selected host

The list of proxies to check stored in file (proxies.txt).
The host provided inside script (line 139 of main.py). 

During the work of script each proy will be checked on availability and access to
particular host. As a result of check forming csv file with information concerning
availability of proxies and time for what the response received from hos through this proxy,
status code of response.

