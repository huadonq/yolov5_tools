import os
import numpy as np
import json
import cv2
'''
data_dir:
    |--data 
    |--train
    |----images
    |------xxx1.png
    |------xxx2.png
    ...
    |----labels
    |------xxx1.txt
    |------xxx2.txt
'''
id_counter = 0 # To record the id
FILE_PATH = '/data_dir/labels' #####
out = {'annotations': [], 
           'categories': [{"id": 1, "name": "cancer", "supercategory": ""}], ##### change the categories to match your dataset!
           'images': [],
           'info': {"contributor": "", "year": "", "version": "", "url": "", "description": "", "date_created": ""},
           'licenses': {"id": 0, "name": "", "url": ""}
           }

def annotations_data(whole_path, image_id, height, width):
    # id, bbox, iscrowd, image_id, category_id
    global id_counter
    txt = open(whole_path,'r')
    for line in txt.readlines(): # if txt.readlines is null, this for loop would not run
        data = line.strip()
        data = data.split() 
        # convert the center into the top-left point!
        data[1] = float(data[1])* width - 0.5 * float(data[3])* width ##### change the 800 to your raw image width
        data[2] = float(data[2])* height - 0.5 * float(data[4])* height ##### change the 600 to your raw image height
        data[3] = float(data[3])* width ##### change the 800 to your raw image width
        data[4] = float(data[4])* height ##### change the 600 to your raw image height
        bbox = [data[1],data[2],data[3],data[4]]
        ann = {'id': id_counter,
            'bbox': bbox,
            'area': data[3] * data[4],
            'iscrowd': 0,
            'image_id': image_id,
            'category_id': int(data[0]) + 1            
        }
        out['annotations'].append(ann)
        id_counter = id_counter + 1 

def images_data(file_name,image_id,imgtype,height,width):
    file_name = file_name.split('.')[0]+imgtype
    id = image_id
    imgs = {'id': id,
            'height': height, 
            'width': width, 
            'file_name': file_name ,
            "coco_url": "", 
            "flickr_url": "", 
            "date_captured": 0, 
            "license": 0
    }
    out['images'].append(imgs)
           
    
            

if __name__ == '__main__':
    files = os.listdir(FILE_PATH)
    files.sort()
    tmp = 0
    height,width = 512,512
    imgtype = '.png' #change the imgtype to your raw image type example: .png .jpg .tif ...
    for file in files:
        if 'ipy' in file:
            continue
        whole_path = os.path.join(FILE_PATH,file)
        annotations_data(whole_path, tmp, height, width)
        images_data(file,tmp,imgtype,height,width)
        tmp+=1
    
    with open('xxx.json', 'w') as outfile: ##### change the str to the json file name you want
        json.dump(out, outfile, separators=(',', ':'))