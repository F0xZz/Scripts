import os
import re
def get_depends(Dic_lib,file_root):
    command_base = "apt-get download "
    command_cd_base = "cd "
    for key in Dic_lib:
        for value_name in Dic_lib[key]:
            save_path = os.path.join(file_root,key)
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            # command_cd = command_cd_base+save_path
            os.chdir(save_path)
            command_get_dep = command_base+value_name
            os.system(command_get_dep)  
    return 0
def get_bool_to_next_layer(dic):
    for name in dic :
        command_dep = "apt-cache depends"+" "+name
        bool_sel = "  Depends"
        pip_line_dic = os.popen(command_dep)
        pipline = pip_line_dic.readlines()
        value_ass = False
        for l in pipline:
            if bool_sel==l.split(":")[0]:
                value_ass = True
                print("this is true ")
                break        
    return value_ass
def get_dep_name(dic):
    for name in dic:
        command_get = "apt-cache depends"+" "+name
        pip_line_dic = os.popen(command_get)
        pipline = pip_line_dic.readlines()
        name_list = []
        for line in pipline:
            #this will convert 
            pattern = re.compile("\s\sDepends:\s\S*\n")
            re_need = pattern.findall(line)
            if len(re_need):
                # this will return the depends the name 
                re_com =re_need[0].split(":")[-1].replace(" ","").replace("\n","")
                name_list.append(re_com)
    return name_list
def re_make_(Dic_lib,dic):
    bool_value = False
    for value in Dic_lib:
        if value in dic:
            bool_value = True
    return bool_value
if __name__=="__main__":
    dic = ["gcc"]
    # this is the set of you wanna download the file
    # command_dep = "apt-cache depends"+" "+name
    # this is the set of the apt-cache depends 
    # return list of depends gcc suggests
    '''
    ['gcc\n', '  Depends: cpp\n', '  Depends: gcc-7\n', '  Conflicts: gcc-doc\n', ' |Recommends: libc6-dev\n', '  
    Recommends: <libc-dev>\n', '    libc6-dev\n', '  Suggests: gcc-multilib\n', '  Suggests: make\n', '    
    make-guile\n', '  Suggests: manpages-dev\n', '  Suggests: autoconf\n', '  Suggests: automake\n', ' 
    Suggests: libtool\n', '  Suggests: flex\n', '   
    flex:i386\n', '  Suggests: bison\n', '    bison:i386\n', '  Suggests: gdb\n', '  
    Suggests: gcc-doc\n']
    '''
    # pip_line_dic = os.popen(command_dep)
    # pipline = pip_line_dic.readlines()
    # pipline = ['gcc\n', '  Depends: cpp\n', '  Depends: gcc-7\n', '  Conflicts: gcc-doc\n', ' |Recommends: libc6-dev\n', '  Recommends: <libc-dev>\n', '    libc6-dev\n', '  Suggests: gcc-multilib\n', '  Suggests: make\n', '    make-guile\n', '  Suggests: manpages-dev\n', '  Suggests: autoconf\n', '  Suggests: automake\n', '  Suggests: libtool\n', '  Suggests: flex\n', '    flex:i386\n', '  Suggests: bison\n', '    bison:i386\n', '  Suggests: gdb\n', '  Suggests: gcc-doc\n']
    # bool_sel = "  Depends:*\n"
    # print(type(pipline))
    # if  bool_sel in pipline.:
    #     print("this is right command")
    Dic_lib = {}
    root = os.getcwd()
    file_root = os.path.join(root,"gcc")
    if not os.path.exists(file_root):
        os.makedirs(file_root)
    i = 0
    while (get_bool_to_next_layer(dic)):
        dic = get_dep_name(dic)
        i += 1
        layer = "layer"+str(i)
        Dic_lib[layer]=dic
        if (i>1):
            pre_layer = "layer"+str(i-1)
            if(re_make_(Dic_lib[pre_layer],dic)):
                break      
    print(Dic_lib)
    
    get_depends(Dic_lib,file_root)


    
   
   
   
            