# SecurePythonOpcUaServer
based on: https://github.com/FreeOpcUa/python-opcua

## Generate your own Certificate

* Step 1: Change ssl.conf (subjectAltname, country, organizationName, ...)
* Step 2: openssl genrsa -out pkey.pem 2048
* Step 3: openssl req -x509 -days 365 -new -out self-signed-certificate.pem -key pkey.pem -config ssl.conf
