import subprocess
import os
import math
import numpy as np
import random
import shutil
import json
from pathlib import Path

SEED=42

S_UNIWARD_PATH="/home/ilya/Documents/STEGO/S-UNIWARD/S-UNIWARD_linux_make_v10/executable/S-UNIWARD"
WOW_PATH="/home/ilya/Documents/STEGO/WOW/WOW_linux_make_v10/executable/WOW"
HUGO_PATH="/home/ilya/Documents/STEGO/HUGO/HUGO_like_linux_make_v10/executable/HUGO_like"

def apply_uniward(img_dir, out_dir, payload):
    full_path = os.path.abspath(img_dir)
    full_out_path = os.path.abspath(out_dir)
    
    cmd = f"{S_UNIWARD_PATH} -v -I {full_path} -O {full_out_path} -a {payload}"
    print(cmd)
    subprocess.run(cmd, shell=True)
    
    
def apply_wow(img_dir, out_dir, payload):
    full_path = os.path.abspath(img_dir)
    full_out_path = os.path.abspath(out_dir)
    
    cmd = f"{WOW_PATH} -v -I {full_path} -O {full_out_path} -a {payload}"
    print(cmd)
    subprocess.run(cmd, shell=True)
    
    
def apply_hugo(img_dir, out_dir, payload):
    full_path = os.path.abspath(img_dir)
    full_out_path = os.path.abspath(out_dir)
    
    cmd = f"{HUGO_PATH} -v -I {full_path} -O {full_out_path} -a {payload}"
    print(cmd)
    subprocess.run(cmd, shell=True)
    

def train_test_split(train_fraction, img_dir, out_dir):
    full_path = os.path.abspath(img_dir)
    full_out_path = os.path.abspath(out_dir)
    
    if not os.path.exists(full_out_path):
        os.mkdir(full_out_path)
    
    files = []    
    for filename in os.listdir(full_path):
        files.append(filename)
    random.Random(SEED).shuffle(files)
    
    train_dir = os.path.join(full_out_path, 'train')
    os.mkdir(train_dir)
    train_N = math.ceil(train_fraction * len(files))
    for filename in files[0:train_N]:
        shutil.copy(os.path.join(full_path, filename), train_dir)
        
    test_dir = os.path.join(full_out_path, 'test')
    os.mkdir(test_dir)
    for filename in files[train_N:len(files)]:
        shutil.copy(os.path.join(full_path, filename), test_dir)
        
        
# Generate a stego copy with 0.4 bpp payload for each image and assign labels for dataset in the following way:
#   dataset
#       cover          
#           1.pgm
#           2.pgm
#           ...
#       stego
#           1.pgm
#           2.pgm
#           ...
# 
def assign_labels(img_dir):
    payload = 0.4

    full_path = os.path.abspath(img_dir)
    stego_dir = os.path.join(full_path, 'stego')
    cover_dir = os.path.join(full_path, 'cover')
    
    if not os.path.exists(stego_dir): os.mkdir(stego_dir)
    if not os.path.exists(cover_dir): os.mkdir(cover_dir)
    
    uniward_dir = os.path.join(full_path, 'uniward')
    if not os.path.exists(uniward_dir): os.mkdir(uniward_dir)
    wow_dir = os.path.join(full_path, 'wow')
    if not os.path.exists(wow_dir): os.mkdir(wow_dir)
    hugo_dir = os.path.join(full_path, 'hugo')
    if not os.path.exists(hugo_dir): os.mkdir(hugo_dir)
    
    desc = {}
    r = random.Random(SEED)
    for filename in os.listdir(full_path):
        if os.path.isfile(os.path.join(full_path, filename)):
            shutil.copy(os.path.join(full_path, filename), cover_dir)
            
            dest_dir = r.choice([uniward_dir, wow_dir, hugo_dir])
            desc[filename] = {"algorithm": Path(dest_dir).stem, "payload": payload}
            shutil.move(os.path.join(full_path, filename), os.path.join(dest_dir, filename))
            
    apply_uniward(uniward_dir, stego_dir, payload)
    apply_wow(wow_dir, stego_dir, payload)
    apply_hugo(hugo_dir, stego_dir, payload)
    
    shutil.rmtree(uniward_dir)
    shutil.rmtree(wow_dir)
    shutil.rmtree(hugo_dir)               
    
    return desc
        
    f = open("description.json", "w")
    f.write(json.dumps(desc))
    f.close()


data_dir = "/home/ilya/Documents/STEGO/test_base"#"/home/ilya/Documents/STEGO/bossbase_1.01_divided"
out_dir = "/home/ilya/Documents/STEGO/test_dataset"
train_test_split(0.6, data_dir, out_dir)

d1 = assign_labels(os.path.join(out_dir, "train"))
f = open(os.path.join(out_dir, "train_description.json"), "w")
f.write(json.dumps(d1))
f.close()

d2 = assign_labels(os.path.join(out_dir, "test"))
f = open(os.path.join(out_dir, "test_description.json"), "w")
f.write(json.dumps(d2))
f.close()
