import os
import shutil
import argparse
import time
import zipfile
def Get_thevalue():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-absroot",type=str,default="./",help=
    "set the root you wanna to restore the img just like /home/ubuntu/xxx "
    "defalut value is currently root")
    parser.add_argument("-startdata",type=str,default="",help=
    "please set up the data that you wanna to save just like"
    " 2021-06-03 default is NONE this will set the currenty day")
    parser.add_argument("-enddata",type=str,default="",help=
    "please set up the data that you wanna to save just like"
    " 2021-06-05 default is NONE this will set the currenty day")
    parser.add_argument("-timelow",type=int,default="00",help=
    "please set up the lower limited time that you wanna to save just like"
    " 13 defalut value is 00 ")
    parser.add_argument("-timeup",type=int,default="24",help=
    "please set up the superior limited time that you wanna to save just like"
    " 24 default value is 24")
    parser.add_argument("-savepath",type=str,default="defalutfloder",help=
    "please set up the savepath that you wanna to save just like"
    " /home/ubuntu/0605/ default value is ./defalutfloder")
    return parser
def Move_img():
    strtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()).split(" ")[0]
    if(args.startdata==""):
        args.startdata =strtime
    if(args.enddata==""):
        args.enddata = strtime
    selectUp_Month = int(args.enddata.split("-")[1])
    selectUp_Days = int(args.enddata.split("-")[2])
    selectDown_Month = int(args.startdata.split("-")[1])
    selectDown_Days = int(args.startdata.split("-")[2])
    if(os.path.exists(args.savepath)==False):
        os.makedirs(args.savepath)
    for root in os.listdir(args.absroot):
        if(os.path.isfile(root)==False and root!=args.savepath):
            for filename in os.listdir(os.path.join(args.absroot,root)):
                Data_entire = filename.split(" ")[0]
                Time_entire = filename.split(" ")[1]
                Data_Month = int(Data_entire.split("-")[1])
                Data_Days = int(Data_entire.split("-")[2])
                Time_hours = int(Time_entire.split(":")[0])
                # print(Data_Days)
                if(Data_Month<=selectUp_Month and Data_Month>=selectDown_Month):
                    if(Data_Days<=selectUp_Days and Data_Days>=selectDown_Days):
                        if(Time_hours<=args.timeup and Time_hours>=args.timelow):
                            src_path = os.path.join(args.absroot,root,filename)
                            dst_path = os.path.join(args.savepath,root,filename)
                            # print(os.path.exists(os.path.join(args.savepath,root)))
                            if(os.path.exists(os.path.join(args.savepath,root))==False):
                                print(os.path.join(args.savepath,root))
                                os.makedirs(os.path.join(args.savepath,root),exist_ok=True)
                            shutil.copy(src_path,dst_path)
                            
    # for root, dirs, files in os.walk(args.absroot):  
        # print(root) #当前目录路径  
        # print(dirs) #当前路径下所有子目录  
        # print(files) #当前路径下所有非目录子文件
    return 0
def zip(file):
    zipfile_name = os.path.basename(file) + '.zip'
    with zipfile.ZipFile(zipfile_name, 'w') as zfile:
        for foldername, subfolders, files in os.walk(file):
            zfile.write(foldername)
            for i in files:
                zfile.write(os.path.join(foldername, i))
        zfile.close()

if __name__=="__main__":
    parser = Get_thevalue()
    args = parser.parse_args()
    Move_img()
    zip(args.savepath)
    # zip_filename = (args.enddata)+".zip"
    # with zipfile.ZipFile(zip_filename,"w") as zfile:
    #     zfile.write(args.savepath)

    # os.path.exists(os.path.join())