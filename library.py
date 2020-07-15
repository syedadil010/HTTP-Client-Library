import socket
#from httpc import getHostandParams

target_port=80
count=0
def GET_REQUEST(host,params,verbose,headers,inputstr,redirectCount):
    # ////////////////////GET Starts///////////////////#
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, target_port))
    # payload = {'assignment': '1','course': 'networking'}
 #   inputString = "GET " + params + " HTTP/1.0"+headers+"\r\nHost: " + host + "\r\n\r\n"
    inputString = "GET %s HTTP/1.0\r\nHost: %s\r\n%s\r\n\r\n" % (params, host, headers)
    s.sendall(bytes(inputString, 'UTF-8'))
    result = s.recv(10000)
    a = result.decode('UTF-8')
    outputList=a.split(" ")
    outputList2=[s.strip() for s in a.splitlines()]
    if( outputList.__contains__('301') or outputList.__contains__('302') or outputList.__contains__('303') or outputList.__contains__('304')):
        if (verbose):
            print(a)
        else:
            # if val.__contains__('://'):
            #     hostandpar = getHostandParams(val)
            # else:
            #     i = val.index('Location: ')
            #     host = val[i + 10:]
            aList = a.split('{', 1)
            print("{", aList[1])
            newhost=''
        for val in outputList2:
            if 'Location:' in val:
                #i=val.index('http://')
                hostandpar=getHostandParams(val)
                # i=val.index('//')
                # newhost1=val[i+2:len(val)]
                # if newhost1[len(newhost1)-1] is '/':
                #     newhost=newhost1[:len(newhost1)-1]
                if(redirectCount<6):
                    redirectCount=redirectCount+1
                    a=REDIRECT(hostandpar[0],hostandpar[1],verbose,headers,inputstr,redirectCount)
    if (verbose):
         return a
    else:
        aList = a.split('{', 1)
        s.close
        return '{'+aList[1]


def POST_REQUEST(host,params,verbose,user_headers,body,inputstr):
    target_port = 80  # create a socket object
    target_host = host
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host, target_port))
    contentlength="Content-Length: "+str(len(body))
    payload="POST %s HTTP/1.0\r\nHost: %s\r\n%s\r\n%s\r\n\r\n%s"%(params,host,user_headers,contentlength,body)

#     headers = """\
# POST /post HTTP/1.0\r
    # Content-Length: {content_length}\r
# Host: {target_host}\r
# \r\n"""
#     body1 = body
#     body_bytes = body1.encode('ascii')
#     header_bytes = headers.format(
# #        content_type="application/json",
#         content_length=len(body_bytes),
#         user_agent="Concordia-HTTP/1.0",
#         target_host=str(target_host) + ":" + str(target_port)
#     ).encode('iso-8859-1')
#
#     payload = header_bytes + body_bytes
    client.send(payload.encode('utf-8'))
    response1 = client.recv(4096)
    # pp.pprint("response1: {}".format(response1))
    d = response1.decode('UTF-8')
    if (verbose):
        return d
    else:
        dList = d.split('{', 1)
        return "{"+dList[1]

def REDIRECT(host,params,verbose,headers,inputstr,redirectCount):
    return GET_REQUEST(host,params,verbose,headers,inputstr,redirectCount)


def getHostandParams(a):
    host=''
    parameters=''
    args=a.split(' ')
    link=''
    for str in args:
        if (('http://' in str) or ('https://'  in str) or ('www.'  in str) or (('\'' and '.') in str) or ('.' in str)):
            link=str
    list=link.split('/')
    pos=0
    if((a.__contains__('get')) or (not a.__contains__('post'))):
        for element in list:
            if('.' in element):
                host=element
                pos=link.index(host)
        parameters=link[pos+len(host):len(link)]
    if(a.__contains__('post')):
        for element in list:
            if('.' in element):
                host=element.strip('/post')
    return [host,parameters]