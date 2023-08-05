#!/usr/bin/env python
# coding: utf-8

# In[6]:


import numpy as np
import pandas as pd
import os
import cv2
from keras.preprocessing.image import ImageDataGenerator,array_to_img,img_to_array,load_img


# In[3]:

class Process:
    def create_color_data(self,IMG_SIZE,training_data,Data_train,CATEGORIES):
        
        for category in CATEGORIES:
            c_path = os.path.join(Data_train,category)
            class_num = CATEGORIES.index(category)
            for img in os.listdir(c_path):
                try:
                    img_array = cv2.imread(os.path.join(c_path,img))
                    new_array = cv2.resize(img_array,(IMG_SIZE,IMG_SIZE)) 
                    training_data.append([new_array,class_num])
                except Exception as e:
                    pass


    # In[47]:


    def create_gray_data(self,IMG_SIZE,training_data,Data_train,CATEGORIES):
        for category in CATEGORIES:
            path = os.path.join(Data_train,category)
            class_num = CATEGORIES.index(category)
            for img in os.listdir(path):
                try:
                    img_array = cv2.imread(os.path.join(path,img),cv2.IMREAD_GRAYSCALE)
                    new_array = cv2.resize(img_array,(IMG_SIZE,IMG_SIZE)) 
                    training_data.append([new_array,class_num])
                except Exception as e:
                    pass


    # In[48]:


    def idg(self,Data_path,CATEGORIES,Data_out):
        datagen = ImageDataGenerator(shear_range=0.1,
                                 zoom_range=0.1,
                                 horizontal_flip=True,
                                 fill_mode='wrap')
        for category in CATEGORIES:
            path = os.path.join(Data_path,category)
            out_path=os.path.join(Data_out,category)
            for img in os.listdir(path):
                image = load_img(os.path.join(path,img))
                x = img_to_array(image)
                x = x.reshape((1,)+x.shape)
                i=0
                for batch in datagen.flow(x,batch_size=1,save_to_dir=out_path,save_prefix='gen',save_format='jpeg'):
                    i=i+1
                    if i>10:
                        break


