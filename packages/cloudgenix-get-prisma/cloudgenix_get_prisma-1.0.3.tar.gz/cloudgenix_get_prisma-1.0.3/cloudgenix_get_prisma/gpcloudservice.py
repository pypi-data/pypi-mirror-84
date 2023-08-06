import cloudgenix
import tempfile
import atexit
import logging

logger = logging.getLogger(__name__)
APP_NAME = "Get Prisma Servicelinks"
APP_VERSION = "1.0.3"
APP_BUILD = "b1"

API_GPC_ROOT = bytes("""
-----BEGIN CERTIFICATE-----
MIIEsTCCAxmgAwIBAgIQHdh5ZM7HY7FADUlEJ3DTUTANBgkqhkiG9w0BAQwFADBc
MQswCQYDVQQGEwJVUzEgMB4GA1UEChMXUGFsbyBBbHRvIE5ldHdvcmtzIEluYy4x
KzApBgNVBAMTIlBhbG8gQWx0byBOZXR3b3JrcyBJbmMuLVJvb3QtQ0EgRzEwHhcN
MTcwNTI0MjE0NTUwWhcNMjcwNTI0MjE1NDQyWjBcMQswCQYDVQQGEwJVUzEgMB4G
A1UEChMXUGFsbyBBbHRvIE5ldHdvcmtzIEluYy4xKzApBgNVBAMTIlBhbG8gQWx0
byBOZXR3b3JrcyBJbmMuLVJvb3QtQ0EgRzEwggGiMA0GCSqGSIb3DQEBAQUAA4IB
jwAwggGKAoIBgQDCuGMVA+NHFzgdNjxAmXpTkC9X75g+OQ8Vl9skYn3GCSz0gc7P
zTtS1DFB+35s0xAAh7N4+NVFKHIjdn9sTEEw4ka2junqACbjq0aSqRYfiAJ8iwAB
bebltlf/fBQqz8BTAD+aqq7YPRHtBBLu6gPRKc6Ue+4PtL6LzqB7/IbVM3pCkrzb
hwxhFcnya0fHZgTBCTUJn11+Le7iaQzjI7x4JRbT/iPPcXtT5mtcDbeIh+MbYRlO
1aGVCZ5ietJS6447Gma2smmZ9O8XZin2BDktKqbPdFtiXEs8eYf9SFSoB5GgRvjJ
7XLDX7jdh/ao0e1+eNiMu1JFk4dtFgeE4551jbfLV42RMGF2tTcMCVE87otcqMkA
Vd7Tq9H6/8GUsyRJHd/zbZ9WscvDt4xWwU6bg+21v7tzEe1kzhLWVZ0/VKG6sJT4
Twjjza1StjMxAMJu3pmK/IBOU4PuqiMz7jT3g2eD1YNYctUIhB5YhN+lA2R4INEh
KtQTnOsZo8woUUcCAwEAAaNvMG0wDgYDVR0PAQH/BAQDAgEGMA8GA1UdEwEB/wQF
MAMBAf8wHQYDVR0OBBYEFM9d98m/4sLyezm2ThN4ZnimwuvzMBAGCSsGAQQBgjcV
AQQDAgEAMBkGA1UdIAQSMBAwDgYMKwYBBAGBxnUDAQECMA0GCSqGSIb3DQEBDAUA
A4IBgQBPT3zJZ9QHlpQtptbZis99etFK2ysJZ5RPnH7mygX5hNKtMm4SHiSjBx+c
1KG3o6GypKvglAnTiZdcFoIFL24B2h81hYlKngLxshNUD/D3NrFjyLOEB7vChUtf
x/VTCRIhKGXe/4daPaGRWNaP6Cta9p/lDipRwaGP7iDiejkVDhBYGMhsSxgnU1vp
PjCFkdqKgo145KSNEnU2L3/qB9+V4m4GPz3y695yEPulEqIQfZLUNzK8Fuo0V1xF
pFrUuJD4JfTdOMd3k39WZY1SYmk0CLt9buFQskf4DbWZoaVa59+tp0g2jVgDPZrR
cXTtNC82D0dzW1a9U7DSX8jm96IQJwIl4hxjHqOWRRcTQP7pNZz20/vXK97/XDFp
4PM2mL/jEP779bBqPRtLB1VPT2ksk1zREeVxhjwnEXNbNn3lUhuKEvaA21syq/Wz
2LeM8BTkwb/MGHsmbPPQS0TMjn0oB6pUq2n07TSNmHYtHsf/3PEY/MJyOSymlUHl
aSmTrfI=
-----END CERTIFICATE-----
 1 s:/C=US/O=Palo Alto Networks Inc./CN=Palo Alto Networks Inc.-SJC-Issuing-CA G1
   i:/C=US/O=Palo Alto Networks Inc./CN=Palo Alto Networks Inc.-Intermediate-SJC-CA G1
-----BEGIN CERTIFICATE-----
MIIFhjCCA+6gAwIBAgITcQAAAAU5SM2ZvK7zBgAAAAAABTANBgkqhkiG9w0BAQwF
ADBoMQswCQYDVQQGEwJVUzEgMB4GA1UEChMXUGFsbyBBbHRvIE5ldHdvcmtzIElu
Yy4xNzA1BgNVBAMTLlBhbG8gQWx0byBOZXR3b3JrcyBJbmMuLUludGVybWVkaWF0
ZS1TSkMtQ0EgRzEwHhcNMTcwNTI1MDAwMzIyWhcNMjAwNTI0MDAwMzIyWjBjMQsw
CQYDVQQGEwJVUzEgMB4GA1UEChMXUGFsbyBBbHRvIE5ldHdvcmtzIEluYy4xMjAw
BgNVBAMTKVBhbG8gQWx0byBOZXR3b3JrcyBJbmMuLVNKQy1Jc3N1aW5nLUNBIEcx
MIIBojANBgkqhkiG9w0BAQEFAAOCAY8AMIIBigKCAYEA5hsQLsPUDh1gb7mvL5dw
5Xq8W6XDGYYGR/fGAROMRhSbKf2xhja9IfxWzN7IScWabZWASWLB/irPTnHU1jqY
kAY6m0f+U19Z9JoXl8KD3Xe/947diBp0p78eAOVqsf/7FKYRRzOWLO/uLCi1eN86
5ToqBXzYAR2qW3INl3t7k6u+/yUs7ScEDh8Mc3yP+WyBY05MilBVp7dI+ZOmYb6u
wOkbGjjzS3ZPWvKRe2Z+Ue9I7BAaMpIyQM2UsEqUEdsyR+0nuYNo71Vdh8130njL
el9Xus42kMtud6BkbddE2WJ9DXZvZv1kQhCXSIqfrr1am3as1EUEGTZqy6PJpYjC
UBtQAjswflUWNE3H3sVQn7AzCLKdPqDKKeHkCv6QOvMqvbKWy/iHy+ornGpiB/Jo
71ivVaWm4EMIroE+hyS+RrygYg9oHr4L4ciqDV+6R1MnGafjM+I2hkbpT/t7btdl
a6HeYtVnozoIQyeNCNi1bOKbkRpxLj0Sm6hA8AxzP/VFAgMBAAGjggEsMIIBKDAd
BgNVHQ4EFgQUtVHCA6aanx4HKr0VQ6lNZz2nxBYwHwYDVR0jBBgwFoAUSUWPnY8T
ktNlKGTVu6Ij8cvb2OEwTAYDVR0fBEUwQzBBoD+gPYY7aHR0cDovL2NybC5wYWxv
YWx0b25ldHdvcmtzLmNvbS9wYW4taW50ZXJtZWRpYXRlLXNqYy1jYS5jcmwwVwYI
KwYBBQUHAQEESzBJMEcGCCsGAQUFBzAChjtodHRwOi8vY3JsLnBhbG9hbHRvbmV0
d29ya3MuY29tL3Bhbi1pbnRlcm1lZGlhdGUtc2pjLWNhLmNydDAPBgNVHRMBAf8E
BTADAQH/MA4GA1UdDwEB/wQEAwIBBjAeBgNVHSABAf8EFDASMBAGDisGAQQBgcZ1
AwEBAgEBMA0GCSqGSIb3DQEBDAUAA4IBgQAzvBuR9L2D7tfmx7Q73Teg34I+4HbF
+Lsn9YAX9aEGUFmGsRppiDah6tX9YeVYQlL0dwML8Y7iVbfcpQWKGR4em4qtf2EZ
LAlXItRuX5U3vWINxcndy/GRm81j9thkttikMwkvEv/opqXPMNI8AyO6zKbTfijM
CeHfKbRWjiKLKgTk4iN7rzYLBXCJUS9foPBCl15jACAiCJ/AKqITjVVjCl5zPYOX
xjNhr2EeEBfwddXFxUEeiRxoRTufOeM6o0a3wc+bF4PrxkJgbA3fod8AzO5l/m/U
bpVRoL1MreEXwUWErh5EB6in7A9vG+G8vkS/PuDqnt8oeYi9SQC25K0lEOL3R9Ub
agZH3r7GK65Dd6Pr06mW6mupWf0iipxV2z20opLqWf7nYZXB2j13CMUTHAsPYh2u
syUCXbm4zYfRy7+ptTNacBIVfgVre0e8PGvxmlRjZkzZtniXLdv2aAQySL7ysElt
JSEiyuQzUzFHgSOZEHQqWmHRrXT+yXBQre0=
-----END CERTIFICATE-----
 2 s:/C=US/O=Palo Alto Networks Inc./CN=Palo Alto Networks Inc.-Intermediate-SJC-CA G1
   i:/C=US/O=Palo Alto Networks Inc./CN=Palo Alto Networks Inc.-Root-CA G1
-----BEGIN CERTIFICATE-----
MIIFkDCCA/igAwIBAgITcwAAAAbXyU1KxVhaCwAAAAAABjANBgkqhkiG9w0BAQwF
ADBcMQswCQYDVQQGEwJVUzEgMB4GA1UEChMXUGFsbyBBbHRvIE5ldHdvcmtzIElu
Yy4xKzApBgNVBAMTIlBhbG8gQWx0byBOZXR3b3JrcyBJbmMuLVJvb3QtQ0EgRzEw
HhcNMTcwNTI0MjM0ODQyWhcNMjcwNTI0MjE1NDQyWjBoMQswCQYDVQQGEwJVUzEg
MB4GA1UEChMXUGFsbyBBbHRvIE5ldHdvcmtzIEluYy4xNzA1BgNVBAMTLlBhbG8g
QWx0byBOZXR3b3JrcyBJbmMuLUludGVybWVkaWF0ZS1TSkMtQ0EgRzEwggGiMA0G
CSqGSIb3DQEBAQUAA4IBjwAwggGKAoIBgQDGaidD3ZZKy4DSX8mmHvfw2RRlgukS
ArirG3330+eyvTEjfouZWsM3kRXdxqmNmBhVWUyDQL/17a0yEAaHT5frJQFPbm0K
3Bmg+r+qxLAC/nu0Daw3gGcur9FvvCx1jEhnsoPTq9u3QQgUPB1qfOHzmNQxEh5b
oBBHzqpv0vebPKsDptBuM7WqcS2zkbr37W8VRD6Xa8pNUVEUFWezcYmuOpE52tga
HrWPE9rYl3LgUcUtrLALsWeEViJzGZXM9CMHflk34UU6DlIUatK1GIAALPXZmGll
4fXx5MBKf5HEKo7SZDk1Lj6tEaqf72fAPbjF6CI+i94VN7kdwutKUgV5SIIPTYYH
TOTSW4eLZuctL3y+2jSievSy6di4bK5/4oh8Ybl9PtUWiS/O+IDrs+UfU1WEk8BI
27sX5+bpJJeg63S2+LQkAUnx+aPcinptGPker/2gShT3iN3cimELdoD7tT2f7gU7
QXlLIOrXtFnKDQyFGrV62sitcwMZaNF3pmkCAwEAAaOCAT0wggE5MA4GA1UdDwEB
/wQEAwIBBjAQBgkrBgEEAYI3FQEEAwIBADAdBgNVHQ4EFgQUSUWPnY8TktNlKGTV
u6Ij8cvb2OEwGgYDVR0gBBMwETAPBg0rBgEEAYHGdQMBAQIBMBkGCSsGAQQBgjcU
AgQMHgoAUwB1AGIAQwBBMA8GA1UdEwEB/wQFMAMBAf8wHwYDVR0jBBgwFoAUz133
yb/iwvJ7ObZOE3hmeKbC6/MwQAYDVR0fBDkwNzA1oDOgMYYvaHR0cDovL2NybC5w
YWxvYWx0b25ldHdvcmtzLmNvbS9wYW4tcm9vdC1jYS5jcmwwSwYIKwYBBQUHAQEE
PzA9MDsGCCsGAQUFBzAChi9odHRwOi8vY3JsLnBhbG9hbHRvbmV0d29ya3MuY29t
L3Bhbi1yb290LWNhLmNydDANBgkqhkiG9w0BAQwFAAOCAYEAmR2rhG14c3c7erp4
bx85YyPavPw574eisixGupm4a2vtrbfPQKL1aAcfUurhgx4ZqD9wncvSyIy8vh6P
MvjGmZw5OxbdErwpitvFPuUSxj45EsdVSK4k26O/G04PqOqs2LCNcT6Dq0IZeoeo
yvPCz0yW5OiWhey2fF6pYdUoP1uTg/GHum6/ETY6XLVgXlCnReznciPz/sYYpPpe
ZC8COawgbf5ke6/cUHU2LHAldODUJ/Ila4m3fiExFaEHXI+xtAklqsXRiHAz8dCS
10PlUCEy3HvgonKRftx6IiyHCdHjIhkI/9FYRfpIFBgqXPUlsjzOYyRoO1onXww2
g1hu4pOORRl0sgtuQO9IA4lvxJO8sO8yk60lZuqfSugUg71FexFUVqZpWV5hDmPR
OFqfi4oVsHW2Zx99yGDwij5YsslXHm8RC8xAzNFnnbVIUAucLv6uXwesDXh9jOTg
a9VvjNwAZRBjsvbls5iKtIFYINpPhaAY0GMAGlod5mJB4G0c
-----END CERTIFICATE-----
 3 s:/C=US/O=Palo Alto Networks Inc./CN=Palo Alto Networks Inc.-Root-CA G1
   i:/C=US/O=Palo Alto Networks Inc./CN=Palo Alto Networks Inc.-Root-CA G1
-----BEGIN CERTIFICATE-----
MIIEsTCCAxmgAwIBAgIQHdh5ZM7HY7FADUlEJ3DTUTANBgkqhkiG9w0BAQwFADBc
MQswCQYDVQQGEwJVUzEgMB4GA1UEChMXUGFsbyBBbHRvIE5ldHdvcmtzIEluYy4x
KzApBgNVBAMTIlBhbG8gQWx0byBOZXR3b3JrcyBJbmMuLVJvb3QtQ0EgRzEwHhcN
MTcwNTI0MjE0NTUwWhcNMjcwNTI0MjE1NDQyWjBcMQswCQYDVQQGEwJVUzEgMB4G
A1UEChMXUGFsbyBBbHRvIE5ldHdvcmtzIEluYy4xKzApBgNVBAMTIlBhbG8gQWx0
byBOZXR3b3JrcyBJbmMuLVJvb3QtQ0EgRzEwggGiMA0GCSqGSIb3DQEBAQUAA4IB
jwAwggGKAoIBgQDCuGMVA+NHFzgdNjxAmXpTkC9X75g+OQ8Vl9skYn3GCSz0gc7P
zTtS1DFB+35s0xAAh7N4+NVFKHIjdn9sTEEw4ka2junqACbjq0aSqRYfiAJ8iwAB
bebltlf/fBQqz8BTAD+aqq7YPRHtBBLu6gPRKc6Ue+4PtL6LzqB7/IbVM3pCkrzb
hwxhFcnya0fHZgTBCTUJn11+Le7iaQzjI7x4JRbT/iPPcXtT5mtcDbeIh+MbYRlO
1aGVCZ5ietJS6447Gma2smmZ9O8XZin2BDktKqbPdFtiXEs8eYf9SFSoB5GgRvjJ
7XLDX7jdh/ao0e1+eNiMu1JFk4dtFgeE4551jbfLV42RMGF2tTcMCVE87otcqMkA
Vd7Tq9H6/8GUsyRJHd/zbZ9WscvDt4xWwU6bg+21v7tzEe1kzhLWVZ0/VKG6sJT4
Twjjza1StjMxAMJu3pmK/IBOU4PuqiMz7jT3g2eD1YNYctUIhB5YhN+lA2R4INEh
KtQTnOsZo8woUUcCAwEAAaNvMG0wDgYDVR0PAQH/BAQDAgEGMA8GA1UdEwEB/wQF
MAMBAf8wHQYDVR0OBBYEFM9d98m/4sLyezm2ThN4ZnimwuvzMBAGCSsGAQQBgjcV
AQQDAgEAMBkGA1UdIAQSMBAwDgYMKwYBBAGBxnUDAQECMA0GCSqGSIb3DQEBDAUA
A4IBgQBPT3zJZ9QHlpQtptbZis99etFK2ysJZ5RPnH7mygX5hNKtMm4SHiSjBx+c
1KG3o6GypKvglAnTiZdcFoIFL24B2h81hYlKngLxshNUD/D3NrFjyLOEB7vChUtf
x/VTCRIhKGXe/4daPaGRWNaP6Cta9p/lDipRwaGP7iDiejkVDhBYGMhsSxgnU1vp
PjCFkdqKgo145KSNEnU2L3/qB9+V4m4GPz3y695yEPulEqIQfZLUNzK8Fuo0V1xF
pFrUuJD4JfTdOMd3k39WZY1SYmk0CLt9buFQskf4DbWZoaVa59+tp0g2jVgDPZrR
cXTtNC82D0dzW1a9U7DSX8jm96IQJwIl4hxjHqOWRRcTQP7pNZz20/vXK97/XDFp
4PM2mL/jEP779bBqPRtLB1VPT2ksk1zREeVxhjwnEXNbNn3lUhuKEvaA21syq/Wz
2LeM8BTkwb/MGHsmbPPQS0TMjn0oB6pUq2n07TSNmHYtHsf/3PEY/MJyOSymlUHl
aSmTrfI=
-----END CERTIFICATE-----
""", 'utf-8')


class GPCloudServiceOperations(object):
    """
    Object to interact with api.gpcloudservice.com endpoint
    """
    api_key = None
    session = None
    api_endpoint = None
    ca_verify_filename = None
    _ca_verify_file_handle = None
    debug_level = 0

    def __init__(self, api_key, api_endpoint="https://api.gpcloudservice.com", ssl_verify=None):
        """
        Build the GPCS api interaction object
        :param api_key: API Key from Panorama's CloudService config.
        :param api_endpoint: URL for endpoint - default set if not specified.
        :param ssl_verify: Verify SSL behavior. If not set, creates a temp file and uses API_GPC_ROOT cert
                           from default_data.py. Any other value is passed directly to requests.Session.verify
        """
        # create a requests.session object - reuse requests import from CloudGenix SDK.
        self.session = cloudgenix.requests.Session()
        # disable URLLIB3 warnings on SAN by default, as GPCS cert has no SAN :(
        cloudgenix.urllib3.disable_warnings(cloudgenix.urllib3.exceptions.SubjectAltNameWarning)
        # program other optional values
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        # update user agent for GPCS logging.
        user_agent = self.session.headers.get('User-Agent')
        user_agent += ' ({0} v{1}-{2})'.format(APP_NAME, APP_VERSION, APP_BUILD)
        # add auth header
        self.session.headers.update({
            'User-Agent': str(user_agent),
            "header-api-key": api_key
        })
        if ssl_verify is None:
            # set up SSL verification using a tempfile containing the api.gpcloudservice.com root cert.
            self._ca_verify_file_handle = tempfile.NamedTemporaryFile()
            self._ca_verify_file_handle.write(API_GPC_ROOT)
            self._ca_verify_file_handle.flush()
            self.ca_verify_filename = self._ca_verify_file_handle.name
            # register cleanup function for temp file.
            atexit.register(self._ca_verify_file_handle.close)
            self.session.verify = self.ca_verify_filename
        else:
            # set verification custom
            self.session.verify = ssl_verify
        return

    def set_debug(self, debug_level):
        """
        Set debug level
        :param debug_level: Int, 0-1
        :return: No return
        """
        if isinstance(debug_level, int):
            self.debug_level = debug_level
        else:
            # no debug if invalid.
            self.debug_level = 0

    def rest_worker(self, method, path, params=None):
        """
        Quick REST Worker wrapper around the requests.Session object
        :param method: HTTP Method
        :param path: URL Path
        :param params: Any URL Parameters in dict (key/value) format
        :return: requests.Response object
        """
        response = self.session.request(method=method,
                                        url=str(self.api_endpoint) + path,
                                        params=params)
        if self.debug_level > 0:
            # Print request info, reuse cloudgenix.jdout_detailed logic.
            jdout = cloudgenix.jdout
            try:
                # try to be super verbose.
                output = "REQUEST: {0} {1}; ".format(response.request.method, response.request.path_url)
                output += "REQUEST HEADERS: "
                for key, value in response.request.headers.items():
                    # look for sensitive values
                    if key.lower() in ['header-api-key']:
                        output += " {0}: {1} ".format(key, "<SENSITIVE - NOT SHOWN BY DEFAULT>")
                    else:
                        output += " {0}: {1} ".format(key, value)
                # if body not present, output blank.
                if not response.request.body:
                    output += "; REQUEST BODY: {0}  ".format({})
                else:
                    try:
                        # Attempt to load JSON from string to make it look beter.
                        output += "REQUEST BODY: {0}  ".format(jdout(response.request.body))
                    except (TypeError, ValueError, AttributeError):
                        # if pretty call above didn't work, just toss it to jdout to best effort it.
                        output += "REQUEST BODY: {0}  ".format(jdout(response.request.body))
                output += "; RESPONSE: {0} {1} ".format(response.status_code, response.reason)
                output += "; RESPONSE HEADERS: "
                for key, value in response.headers.items():
                    output += " {0}: {1} ".format(key, value)
                output += "; RESPONSE DATA: {0}".format(jdout(response.content))
            except (TypeError, ValueError, AttributeError, UnicodeDecodeError):
                # cgx_content did not exist, or was not JSON serializable. Try pretty output the base obj.
                try:
                    output = jdout(response)
                except (TypeError, ValueError, AttributeError):
                    # Same issue, just raw output the passed data. Let any exceptions happen here.
                    output = response
            # print debug
            print("GPCS API REQUEST to {0}: {1}".format(self.api_endpoint, output))
        return response

    def get_addr_list(self, fwtype="", addrtype=""):
        """
        Get address lists from GPCS. Allows passing fwtype/addrtype
        :param fwtype: fw type string
        :param addrtype: addr type string
        :return:
        """
        parameters = {
            "fwType": fwtype,
            "addrType": addrtype
        }
        return self.rest_worker('get', '/getAddrList/latest', params=parameters)

    def remote_gw_addr_dicts(self):
        """
        Create a pair of GPCS remote network dicts. Name to IP, and IP to name dicts.
        :return: Tuple (Tunnel Name to IP, and IP to tunnel name dicts.)
        """
        remoteaddr_n2ip = {}
        remoteaddr_ip2n = {}
        # get raw address list filtered.
        response = self.get_addr_list(fwtype="gpcs_remote_network", addrtype="public_ip")
        try:
            goodresponse = response.json()
        except ValueError:
            # was not JSON
            raise GPCloudServiceError("Bad Response or non-JSON response from {0}: ({1}) {2}"
                                      "".format(self.api_endpoint, response.status_code, response.content))
        # extract good response
        status = goodresponse.get('status')
        # set boolean return_status based on success
        return_status = False
        if status:
            if status.lower() in 'success':
                return_status = True
        result = goodresponse.get('result', {})
        addrlist = result.get('addrList', [])
        # check for a message
        message = goodresponse.get('message')
        for addrstring in addrlist:
            # split apart the list at ':', first is tunnel name(s), 2nd is IP.
            host_ips = addrstring.split(':')
            # get the tunnel names without whitespace.
            tunnelname_list = list(map(str.strip, host_ips[0].split(',')))
            ip_addr = host_ips[1]
            logger.debug("IP: %s  TUNNEL NAMES: %s", ip_addr, tunnelname_list)
            if ip_addr and tunnelname_list:
                remoteaddr_ip2n[ip_addr] = tunnelname_list
                for tunnelname in tunnelname_list:
                    remoteaddr_n2ip[tunnelname] = ip_addr
        # return what we got
        return return_status, remoteaddr_n2ip, remoteaddr_ip2n, message


class GPCloudServiceError(Exception):
    """
    Custom exception for errors when not exiting.
    """
    pass
