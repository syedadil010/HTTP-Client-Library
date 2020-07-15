# HTTP-Client-Library

The httpc is a cURL like command-line application that supports HTTP protocol with additional specifications like Redirection and an option to write the body of the response to a file.


The implemented client is httpc (the name of the produced executable).

* The following presents the options of your final command line:

**httpc (get|post) [-v] (-h "k:v")* [-d inline-data] [-f file] URL**


# Redirection Specification
The Redirection specification allows your HTTP client to follow the first request with
another one to new URL if the client receives a redirection code (numbers starts with 3xx).
This option is useful when the HTTP client deal with temporally or parental moved URLs. 


# Usage

 **httpc help**

httpc is a curl-like application but supports HTTP protocol only.

**httpc command [arguments]**
The commands are:
 get executes a HTTP GET request and prints the response.
 post executes a HTTP POST request and prints the response.
 help prints this screen.

Use "httpc help [command]" for more information about a command.

**Get Usage**

httpc help get

**usage**: httpc get [-v] [-h key:value] URL
Get executes a HTTP GET request for a given URL.
 -v Prints the detail of the response such as protocol, status,
and headers.
 -h key:value Associates headers to HTTP Request with the format
'key:value'.

**Post Usage**

httpc help post

**usage**: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL
Post executes a HTTP POST request for a given URL with inline data or from
file.
 -v Prints the detail of the response such as protocol, status,
and headers.
 -h key:value Associates headers to HTTP Request with the format
'key:value'.
 -d string Associates an inline data to the body HTTP POST request.
 -f file Associates the content of a file to the body HTTP POST
request.
Either [-d] or [-f] can be used but not both.

**save to file**
add -o filename to the httpc commandline.
