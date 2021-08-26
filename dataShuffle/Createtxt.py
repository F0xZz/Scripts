import os 
Path = "/home/ubuntu/20210701-/newfiredata/FurgFire_furg-fire-dataset-master/resultAug/Test/XML"
list = os.listdir(Path)
f = "text.txt"
for i in list :
    name = i.split(".")[0]
    with open(f,"a+") as file:   #”w"代表着每次运行都覆盖内容
        file.write(name+"\n")
    