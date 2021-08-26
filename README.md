# Scripts Mix
Autor Fox 

Target: Use to get the my custom data and modify the data 

Begin: 2021-03

LastEditor: 2021-08

## Use Doc

1. **XMLUse** Folder: Use for test For Create and Add the node to the xml file （用于测试对XML文件的生成测试和节点添加测试，里面有测试用于视频数据标签生成VOC格式的样本的脚本）

2. **VOCAug** Folder: Use for Augment the VOC datasets to create small object by using copypaste method ，and also create the new XML file (通过对VOC数据格式的样本进行特定的数据增强，使用简易的复制粘贴的方式随机生成小目标并同时生成XML标注文件)
3. **reidscripts** Folder : Use for create Person Reid datasets Scripts by the **darklabel** toolkit and the label "frame id x y  w h " in the one txt（用于生成通过darklabel标注完成的Reid数据，并且还配合shuffle方式和数据增强方式）
4. **augDataset** Folder : waiting for done 
5. **dataShuffle** Folder : Using for the data shuffle the VOC datasets (用于打乱VOC数据集)

