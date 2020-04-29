from glob import glob
import cv2,os
import numpy as np

def pHash(img):
    img = cv2.resize(img,(32, 32))#interpolation=cv2.INTER_CUBIC
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)# 转换为灰度图
    dct = cv2.dct(np.float32(gray))# 将灰度图转为浮点型，再进行dct变换
    dct_roi = dct[0:8, 0:8]#opencv实现的掩码操作
    hash = []
    avreage = np.mean(dct_roi)
    for i in range(dct_roi.shape[0]):
        for j in range(dct_roi.shape[1]):
            if dct_roi[i, j] > avreage:
                hash.append(1)
            else:
                hash.append(0)
    #print("hash:"+str(hash))
    return hash

def dHash(img):
    img=cv2.resize(img,(9,8))#缩放8*8
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#转换灰度图
    hash_str=''#每行前一个像素大于后一个像素为1，相反为0，生成哈希
    for i in range(8):
        for j in range(8):
            if gray[i,j]>gray[i,j+1]:
                hash_str=hash_str+'1'
            else:
                hash_str=hash_str+'0'
    #print("hash:" + str(hash_str))
    return hash_str

def campHash(hash1, hash2):
    n = 0
    if len(hash1) != len(hash2):
        return -1
    for i in range(len(hash1)):
        if hash1[i] != hash2[i]:
            n = n + 1
    return n

if __name__ == '__main__':
    filefloders = os.listdir("./")
    for filefloadername in filefloders:
        if len(filefloadername)!=2:
            filefloders.remove(filefloadername)
    file_list=[]
    #file_list=glob("./1619672/*.jpg")
    for fders in filefloders:
        path="./"+str(fders)+"/*.jpg"
        file_list.extend(glob(path))
    filelist=glob("./1619672/*.jpg")
    #print(filelist)
    for flst in filelist:
        for fl_st in file_list:
            imgA=cv2.imread(flst)
            imgB=cv2.imread(fl_st)
            res=campHash(pHash(imgA),pHash(imgB))
            if res==0:
                if flst!=fl_st:
                    print(str(flst) + "已存在相似图片,相似图片为" + str(fl_st))
                    pass