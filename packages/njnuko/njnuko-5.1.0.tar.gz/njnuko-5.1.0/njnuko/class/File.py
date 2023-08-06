#!/usr/bin/python3
import json
import requests
import hashlib
import os
import exiftool
import datetime
import time
from PIL import Image
import imagehash
import shutil


class File:


    def __init__(self,file_loc):
        self.file_loc = file_loc
        self.b_name = os.path.basename(self.file_loc)
        self.dir_name = os.path.dirname(self.file_loc)

    
    def get_md5(self):
        the_md5=hashlib.md5()
        hash = ''
        with open(self.file_loc,'rb') as f:
            the_md5.update(f.read())
            hash = the_md5.hexdigest()
        return hash

    def get_metadata(self):
        """
        EXIF:Model
        File:MIMEType
        EXIF:Make
        """
        metadata = ""
        with exiftool.ExifTool() as et:
            metadata = et.get_metadata(self.file_loc)
        return metadata

    def get_maker(self):
        exif = self.get_metadata()
        if exif.get("EXIF:Make") is None:
                return "NON"
        else:
            return exif.get("EXIF:Make").strip().replace(" ","")+"-"+exif.get("EXIF:Model").strip().replace(" ","")


    def get_type(self):
        exif = self.get_metadata()
        if exif.get("File:FileType") is None:
            if os.path.splitext(self.b_name)[1][1:].upper() != "":
                return os.path.splitext(self.b_name)[1][1:].upper()
            else:
                return "NON"
        else:
            return exif.get("File:FileType")
        return "NON"



    def get_create_date(self):
        exif = self.get_metadata()
        if exif.get("EXIF:CreateDate"):
            a = exif.get("EXIF:CreateDate")[0:10]
            b = a.replace(":","-")
            return b
        elif exif.get("QuickTime:CreateDate"):
            a = exif.get("QuickTime:CreateDate")[0:10]
            b = a.replace(":","-")
            return b
        else:
            pass
        create_time =datetime.datetime.strptime(time.ctime(os.path.getctime(self.file_loc)), "%a %b %d %H:%M:%S %Y").strftime("%Y-%m-%d")
        return create_time

    def get_geo_address(self):
        dict={}
        exif = self.get_metadata()
        if exif.get("Composite:GPSLatitude") is not None:
            geo='{:.4f}'.format(exif.get("Composite:GPSLongitude"))+","+'{:.4f}'.format(exif.get("Composite:GPSLatitude"))
            gaode=json.load(open(os.path.join(os.path.dirname(os.getcwd()),"config","gaode.json")))
            base=gaode.get("base")
            key = gaode.get("key")
            parameters={"location":geo,"key":key}
            try:
                response = requests.get(base, parameters)
                if response.status_code == 200:
                    address = response.json()
                    dict["city"]=address.get("regeocode").get("addressComponent").get("city")
                    dict["province"]=address.get("regeocode").get("addressComponent").get("province")
                    dict["district"]=address.get("regeocode").get("addressComponent").get("district")
                    dict["country"]=address.get("regeocode").get("addressComponent").get("country")
                    dict["address"]=address.get("regeocode").get("formatted_address")
                else:
                    pass
            except:
                pass
            return dict
    def is_same(self,cmp_file):
        """
        返回same如果相同
        返回similar如果相似
        返回空如果不同
        """
        media2= File(cmp_file)
        hash2=media2.get_md5()
        hash1=self.get_md5()
        status = ""
        if hash1==hash2:
            status = "same"
        else:
            hash11 =  imagehash.average_hash(Image.open(self.file_loc))
            hash12 =  imagehash.average_hash(Image.open(cmp_file))
            if (hash11 == hash12):
                status = "similar"
        return status

    def move_to(self,dest):
        hash1=self.get_md5()
        log=""
        if os.path.exists(os.path.join(dest,self.b_name)):
            media2 = File(os.path.join(dest,self.b_name))
            hash2=media2.get_md5()
            if hash1 == hash2:
                log=['delete',self.b_name,self.file_loc,os.path.join(dest,self.b_name),os.path.getsize(self.file_loc),hash1]
                os.remove(self.file_loc)
            else:
                new_file_name  = os.path.join(dest,os.path.splitext(self.b_name)[0] + "_1" + os.path.splitext(self.b_name)[1])
                while os.path.exists(new_file_name):
                    new_file_name  = os.path.join(dest,os.path.splitext(os.path.basename(new_file_name))[0] + "_1" + os.path.splitext(new_file_name)[1])
                shutil.move(self.file_loc,os.path.join(new_file_name))
                print("shutil move,"+ "from,"+ self.file_loc + ",to,"+ new_file_name )
                log=['rename',self.b_name,self.file_loc,new_file_name,os.path.getsize(new_file_name),hash1]
        else:
            shutil.move(self.file_loc,os.path.join(dest,self.b_name))
            print("shutil move,"+ "from,"+ self.file_loc + ",to,"+ os.path.join(dest,self.b_name))
            log=['move',self.b_name,self.file_loc,os.path.join(dest,self.b_name),os.path.getsize(os.path.join(dest,self.b_name)),hash1]
        return log
