
def getProp(file_name):
    pre_file = open(file_name,'r',encoding='utf-8')
    prop={}
    try:
        for line in pre_file:
            if line.find('=') > 1:
                str=line.replace('\n','').split('=')
                prop[str[0]]=str[1]
    except Exception as e:
        raise e
    finally:
        pre_file.close()
    return prop