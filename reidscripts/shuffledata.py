
#wanna to return the train ,gallery,query data the ratio is 0.35:0.55:0.1

import os 
import cv2 
import numpy.random as npr
import shutil
import glob
import random
import shutil
import Augmentor as p
import re 

def pro_extend_earsing(imgpath):
    imgpiple = p.Pipeline(imgpath)
    # print(imgpath)
    imgpiple.rotate(probability=0.7, max_left_rotation=10, max_right_rotation=10)
    imgpiple.zoom(probability=0.5, min_factor=1.1, max_factor=1.5)
    imgpiple.random_erasing(probability=1,rectangle_area=0.5)
    # imgpiple.crop_random(probability=0.2, percentage_area=0.5)
    # img = cv2.imread(imgpath)
    # imgHir = cv2.flip(img,1,dst = None)
    imgpiple.sample(10)
    # imgpiple.process()
    return 0
def data_augmentor(data_name):
    root =os.path.join(os.getcwd(),data_name)
    print(root)
    Person_list = os.listdir(root)
    for P_ID in Person_list:
        frame_file = os.path.join(root,P_ID)
        frame_list = os.listdir(frame_file)
        if (len(frame_list)<20 and len(frame_list)>0):
            print("where is error")
            print(frame_file)
            pro_extend_earsing(frame_file)
            out_put_file = os.path.join(frame_file,"output")
            out_put_frame_list = os.listdir(out_put_file)
            # print(out_put_frame_list)
            for outputframe in out_put_frame_list:
                
                # print(outputframe)
                
                pattern = re.compile("\d{4}_c\ds\d_\d*_\d*")
                out = pattern.search(outputframe)[0]
                re_name_frame = out.split("_")[-2]
                re_name_id = out.split("_")[0]
                re_name_cs = out.split("_")[1]
                elderpath = os.path.join(out_put_file,outputframe)
                newname = str(re_name_id)+"_"+str(re_name_cs)+"_"+str(int(re_name_frame)+npr.randint(1,20))+"_01.jpg"
                newerpath = os.path.join(frame_file,newname)
                shutil.copy(elderpath,newerpath)
            # os.removedirs(out_put_file)
            shutil.rmtree(out_put_file)
            
            
        # for frame_name in frame_list:

        #     if frame_name.endswith(".jpg") or frame_name.endswith(".png"):
        #         # print("1")
    return 0
            
def remove_same_list(person_ID,train_ID):
    for i in train_ID:
        person_ID.remove(i) 
    return person_ID
# def get_selected_img(personID,mixdatapath,keywords):
#     get_slt_img = []
#     select_num = 30
#     if keywords =="query":
#         select_num = 6
#     for ID in personID:
#         frame_path = os.path.join(mixdatapath,ID)
#         # this will return the /root/sepimage/personID
#         Camera_list_dir = os.listdir(frame_path)
#         # this will return the /root/sepimage/personID/CamID/
#         for Camera_ID in Camera_list_dir:
#             seq = int(select_num/len(Camera_list_dir))
#             abs_path_frame = os.path.join(frame_path,Camera_ID)
#             # print(abs_path_frame)
#             list_frame = os.listdir(abs_path_frame)
#             if (len(list_frame)<=seq):
#                 selected_frame_list = random.sample(list_frame,0.6*(len(list_frame))) 
#                 print("the label dataset is too smaller ")
#             if (len(list_frame)>seq):     
#                 print("there is normal datasets ")
#                 selected_frame_list = random.sample(list_frame,seq)

#                 for selected_frame in selected_frame_list:
#                     selected_dir_list = os.path.join(frame_path,Camera_ID,selected_frame)
#                     get_slt_img.append(selected_dir_list)
#             # get_slt_img = get_slt_img+selected_frame_list
#     return get_slt_img


def get_selected_img(person_ID,mixdatapath,keywords):
    get_slt_img = []
    select_num = 30
    if keywords =="query":
        select_num = 6
        for ID in person_ID:
            if(int(ID)!=0):
                name_path = os.path.join(mixdatapath,ID)
                # print(name_path)
                frame_list = os.listdir(name_path)
                # print(frame_list)
                if(len(frame_list)>30):
                    selected_frame_list = random.sample(frame_list,int(0.1*(len(frame_list)))) 
                    for selected_frame in selected_frame_list:
                        selected_dir_list = os.path.join(mixdatapath,ID,selected_frame)
                        get_slt_img.append(selected_dir_list)
                else:
                    if(len(frame_list)<select_num):
                        select_num = len(frame_list)-1
                    selected_frame_list = random.sample(frame_list,select_num)
                    for selected_frame in selected_frame_list:
                        selected_dir_list = os.path.join(mixdatapath,ID,selected_frame) 
                        get_slt_img.append(selected_dir_list)
    else:
        for ID in person_ID:
            if(int(ID)!=0):
                name_path = os.path.join(mixdatapath,ID)
                # print(name_path)
                frame_list = os.listdir(name_path)
                # print(frame_list)
                if(len(frame_list)>30):
                    
                    selected_frame_list = random.sample(frame_list,int(0.6*(len(frame_list)))) 
                    for selected_frame in selected_frame_list:
                        selected_dir_list = os.path.join(mixdatapath,ID,selected_frame)
                        get_slt_img.append(selected_dir_list)
                else:
                    selected_frame_list = frame_list
                    
                    for selected_frame in selected_frame_list:
                        selected_dir_list = os.path.join(mixdatapath,ID,selected_frame) 
                        get_slt_img.append(selected_dir_list)
            #set this in the person id 
        
    return get_slt_img
def save_img_path(person_frame_list,keywords,recount_id):
    # for
    save_name = [] 
    
    for img_list in person_frame_list:
        save_name=img_list.split('/')[-1]
        if(recount_id!=1):
            pattern = re.compile("\d{4}_c\ds\d_\d*_\d*")
            out = pattern.findall(save_name)[0]
            re_name_frame = out.split("_")[-2]
            re_name_id = out.split("_")[0]
            re_name_cs = out.split("_")[1]
            camer_id = int(re_name_cs.split("c")[-1].split("s")[0])+6
            ser_id = int(re_name_cs.split("c")[-1].split("s")[1])
            # elderpath = os.path.join(out_put_file,outputframe)
            newname = str(int(re_name_id)+recount_id).zfill(4)+"_"+"c"+str(camer_id)+"s"+str(ser_id)+"_"+str(int(re_name_frame))+"_00.jpg"
            save_name = newname
        save_path = os.path.join(os.getcwd(),keywords)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        save_file_dir = os.path.join(save_path,save_name)
        shutil.copyfile(img_list,save_file_dir)
        # cv2.imwrite(save_path,)
    return 0
def get_query_from_gallerypath(afterpath,mixdatapath):

    return 0

if __name__=='__main__':
    
    mixdataname = "cropmix"

    trainwords = "train"
    gallerywords = "gallery"
    querywords = "query"
    data_augmentor_choose = True
    # this is set for the re_count_id
    recount_id = 1501
    # re_make =True
    if data_augmentor_choose:
        data_augmentor(mixdataname)
    # if re_make: 
    
    mixdatapath = os.path.join(os.getcwd(),mixdataname)

    # print(mixdatapath)
    personidlist = os.listdir(mixdatapath) # get the pid list
    train_person_ID = random.sample(personidlist,int(0.7*(len(personidlist)))) 
    # this will return the train personID 
    af_person_ID = remove_same_list(personidlist,train_person_ID)
    # this will return remove the train_person_ID from the sourceID  
    back_get_img = get_selected_img(train_person_ID,mixdatapath,trainwords)
    # this method will return the imglist path

    # print(back_get_img[:10])

    save_img_path(back_get_img,trainwords,recount_id)
    # this will save image
    back_get_gallery_img = get_selected_img(af_person_ID,mixdatapath,gallerywords)
    # print(len(back_get_gallery_img))
    save_img_path(back_get_gallery_img,gallerywords,recount_id)
    # get the list of frame
    back_get_query_img = get_selected_img(af_person_ID,mixdatapath,querywords)
    save_img_path(back_get_query_img,querywords,recount_id)
    
    
    '''
    this can solve to get the train label
    '''
    
    
