from library import GET_REQUEST
from library import POST_REQUEST

def file_read(fname):
    with open (fname, "r") as myfile:
        data = myfile.readlines()
        data_final = map(str.rstrip, data)
        data1 = map(lambda x: x.replace("," ,"") ,data_final)
    return data1
def writeToFile(fname,data):
    with open(fname, "w") as myfile:
        myfile.writelines(data)


def getHostandParams(a):
    host=''
    parameters=''
    args=a.split(' ')
    link=''
    for str in args:
        if (('http://' in str) or ('https://'  in str) or ('www.'  in str) or (('\'' in str) and ('.' in str)) or (('.' in str) and (not ('.txt' in str))) and (not('url=' in str)) ):
            link=str
    link=link.strip('\"')
    list=link.split('/')
    pos=0
    for element in list:
        if(('.' in element) and (not 'redirect' in element)):
            host=element
            pos=link.index(host)
    parameters=link[pos+len(host):len(link)].strip('\'')
    # if(a.__contains__('get')or (not link.__contains__('post'))):
    #     for element in list:
    #         if(('.' in element) and (not 'redirect' in element)):
    #             host=element
    #             pos=link.index(host)
    #     parameters=link[pos+len(host):len(link)]
    # if(link.__contains__('post')):
    #     for element in list:
    #         if('.' in element):
    #             host=element.strip('/post')
    return [host,parameters]


def getheaders(a):
    headers = {}
    headstr=''
    for i, v0 in enumerate(a):
        if v0 is '-' and a[i + 1] is ('h' or 'H') and a[i+2] is ' ':
            i = i + 1
            isKey = True
            key = ""
            value = ""
            for v1 in a[i + 2:]:
                iscolon = False
                if v1 is ' ':
                    break
                if v1 is ':':
                    isKey = False
                    iscolon = True
                if isKey:
                    key = key + v1
                if not isKey and not iscolon:
                    value = value + v1
            if(key.__contains__('\"')):
                key=key.strip('\"')
            if(value.__contains__('\"')):
                value=value.strip('\"')
            headers[key] = value
    return headers

def createstr(headers):
    headstr=''
    len1=len(headers.keys())
    i=1
    for a in headers.keys():
        if(i==len1):
            headstr = headstr + a + ': ' + headers[a]
        else:
            headstr=headstr+a+': '+headers[a]+'\r\n'
        i=i+1
    return headstr
def removefromList(rem,list):
    for a in list:
        for b in rem:
            if a in b:
                rem.remove(b)
    return rem


def init():
    inputstr = input().strip()
    help_text = "httpc is a curl-like application but supports HTTP protocol only.\n" + "Usage:\n" + "    httpc command [arguments]\n" + "The commands are:\n" + "    get executes a HTTP GET request and prints the response.\n" + "    post executes a HTTP POST request and prints the response.\n" + "    help prints this screen.\n\n" + 'Use "httpc help [command]" for more information about a command\n'
    #print(help_text)
    help_get = "httpc help get\n\n" + "usage: httpc get [-v] [-h key:value] URL\n\n" + "Get executes a HTTP GET request for a given URL.\n\n" + "   -v Prints the detail of the response such as protocol, status,\n" + "and headers.\n" + "   -h key:value Associates headers to HTTP Request with the format\n" + "'key:value'."
    #print(help_get)
    help_post = "httpc help post\n\n" + "usage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL\n\n" + "Post executes a HTTP POST request for a given URL with inline data or from\n" + "file.\n\n" + "   -v Prints the detail of the response such as protocol, status,\n" + "and headers.\n" + "   -h key:value Associates headers to HTTP Request with the format\n" + "'key:value'.\n" + "   -d string Associates an inline data to the body HTTP POST request.\n" + "   -f file Associates the content of a file to the body HTTP POST\n" + "request.\n\n" + "Either [-d] or [-f] can be used but not both.\n"
    #print(help_post)
    redirectCount=0
    inputList=inputstr.split(" ")
    help_length = len(inputList)
    inputList2=inputstr.split('/')
    size=len(inputList2)
    remainingParams=inputList
    headers = {}
    headstr=''
    outputFile=''
    verbose=False
    hostnParam=''
    inlineData=''
    # getheaders(input)
    # hostandparam=getHostandParams(inputstr)
    # hostName=hostandparam[0]
    # param=hostandparam[1]
    # headers1=getheaders(inputstr)
    remainingParams.remove('httpc')
    if((len(inputList)<=3) and (inputstr.__contains__('get') or inputstr.__contains__('GET')) and (inputstr.__contains__('help') or inputstr.__contains__('HELP'))):
        print(help_get)
    elif((len(inputList)<=3) and (not(inputstr.__contains__('get') or inputstr.__contains__('GET'))) and (not(inputstr.__contains__('post') or inputstr.__contains__('POST'))) and (inputstr.__contains__('help') or inputstr.__contains__('HELP'))):
        print(help_text)
    elif((len(inputList)<=3) and (inputstr.__contains__('post') or inputstr.__contains__('POST')) and (inputstr.__contains__('help') or inputstr.__contains__('HELP'))):
        print(help_post)
    elif(inputstr.__contains__('get')):
        if (inputstr.__contains__("-h") or inputstr.__contains__("-H")):
            headers = getheaders(inputstr)
            headstr=createstr(headers)
            remainingParams=removefromList(remainingParams, headers.keys())
            remainingParams=removefromList(remainingParams, headers.values())
        if (inputstr.__contains__("-v") or inputstr.__contains__("-V")):
            verbose=True
            # if '-v' in remainingParams:
            #     remainingParams.remove('-v')
            # else:
            #     remainingParams.remove('-V')

        hostnParam=getHostandParams(inputstr)
        res=GET_REQUEST(hostnParam[0],hostnParam[1],verbose,headstr,inputstr,redirectCount)
        if (inputstr.__contains__("-o") or inputstr.__contains__("-O")):
            reslist = res.split('{', 1)
            b = inputList.index('-o')
            outputFile = inputList[b + 1]
            removefromList(remainingParams, ['-o', outputFile])
            writeToFile(outputFile, '{'+reslist[1])
            if (verbose):
                print(reslist[0])
        else:
            print(res)
    elif(inputstr.__contains__('post')):
        if (inputstr.__contains__("-h") or inputstr.__contains__("-H")):
            headers = getheaders(inputstr)
            headstr=createstr(headers)
            remainingParams=removefromList(remainingParams, headers.keys())
            remainingParams=removefromList(remainingParams, headers.values())
        if (inputstr.__contains__("-v") or inputstr.__contains__("-V")):
            verbose=True
            # if '-v' in remainingParams:
            #     remainingParams.remove('-v')
            # else:
            #      remainingParams.remove('-V')
        hostnParam=getHostandParams(inputstr)
        if (inputstr.__contains__("-d") or inputstr.__contains__("-D")):
            combined = '\t'.join(inputList)
            if ('-d' or '-D' in combined):
                b = inputList.index('-d')
                if(inputList[b+1].endswith('\'')):
                    inlineData=inputList[b+1]
                    inlineData=inlineData.strip('\'')
                else:
                    for inline in inputList[b+1:]:
                        if inline.startswith('\''):
                            if inline.endswith('\''):
                                inlineData=inline.strip('\'')
                                break
                            else:
                                inlineData=inline[1:]
                        elif inline.endswith('\''):
                            inlineData=inlineData+inline[:len(inline)-1]
                            break
                        else:
                            inlineData=inlineData+inline

            # final_list1 = inputList[b + 1].endswith('\'')
            # final_list = final_list1.replace("'", " ")
        elif (inputstr.__contains__("-f") or inputstr.__contains__("-F")):
            combined = '\t'.join(inputList)
            if ('-f' or '-F' in combined):
                b = inputList.index('-f')
                final_list1 = inputList[b + 1].strip("\n")
                new_Data = file_read(final_list1)
                final_list = ','.join(new_Data)
                inlineData=final_list.strip('\'')
        res=POST_REQUEST(hostnParam[0],hostnParam[1],verbose,headstr,inlineData,inputstr)
        if (inputstr.__contains__("-o") or inputstr.__contains__("-O")):
            reslist=res.split('{', 1)
            b = inputList.index('-o')
            outputFile = inputList[b + 1]
            removefromList(remainingParams,['-o',outputFile])
            writeToFile(outputFile,'{'+reslist[1])
            if(verbose):
                print(reslist[0])
        else:
            print(res)
init()