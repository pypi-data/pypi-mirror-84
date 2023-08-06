import os
import os.path
import csv
from File import File
import stat
import time
import sqlite3
import imagehash
#引入folder里面的通用函数，例如file_move,get_db,update_db


class Folder:
    """
    ### log 字段说明，从0到5
    ### ['duplicate',i,os.path.join(folder,i),'',os.path.getsize(os.path.join(folder,i)),hash]
    ### (action varchar(20),name varchar(200),source varchar(1000),dest varchar(1000),size varchar(50),md5 varchar(50))
    1. one_folder，把当前目录中所有子目录文件移动到根目录下，并删除空的文件夹
    2. check,检查当前目录中的所有文件，并删除重复文件（根据MD5值来判断）
    3. compare,比较当前folder和目标folder，如果文件存在于目标folder，则删除

    
    """
    global HASH_COLUMN
    HASH_COLUMN = 5
    global DEFAULT_LOC
    DEFAULT_LOC = os.path.join(os.environ['HOME'],".log")

    def __init__(self,folder_loc):
        self.folder_loc=folder_loc
        self.dir_name = os.path.dirname(folder_loc)

    def one_folder(self):
        folder = self.folder_loc
        one_log = self.init_log(os.path.basename(folder)+'_one.log')
        for i in os.listdir(folder):
            if os.path.isdir(os.path.join(folder,i)):
                if i[0] not in ['@','.']:
                    self.process_one(os.path.join(folder,i),folder,one_log)
        return one_log
    def process_one(self,folder,base_folder,log):
        for i in os.listdir(folder):
            if os.path.isdir(os.path.join(folder,i)):
                if i[0] not in ['@','.']:
                    self.process_one(os.path.join(folder,i),base_folder,log)
            else:
                check_file = File(os.path.join(folder,i))
                mov_log = check_file.move_to(self.folder_loc)
                with open(log,'a',newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(mov_log)
        if self.folder_loc != folder:
            os.rmdir(folder)

    def check(self):
        folder = self.folder_loc
        check_log = self.init_log(os.path.basename(folder)+'_check.log')
        global checking
        checking = []
        self.process_checking(check_log)
        #conn = self.init_db(DEFAULT_DB)
        #init_db_table(conn,os.path.basename(folder))
        #print(folder,check_log,conn)
        #update_db_record(os.path.basename(folder),check_log,conn)
        return check_log

    def process_checking(self,log):
        global checking
        folder = self.folder_loc
        for i in os.listdir(folder):            
            if os.path.isdir(os.path.join(folder,i)):
                if i[0] not in ['@','.']:
                    print(str(os.path.join(folder,i)) + " is not dummy folder")
                    self.process_checking(os.path.join(folder,i),log)
            else:
                media = File(os.path.join(folder,i))
                hash = media.get_md5()
                if hash is not None:
                    if hash in checking:
                        with open(log,'a',newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(['duplicate',i,os.path.join(folder,i),'',os.path.getsize(os.path.join(folder,i)),hash])
                        os.remove(os.path.join(folder,i)) 
                    else:
                        with open(log,'a',newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(['new',i,os.path.join(folder,i),'',os.path.getsize(os.path.join(folder,i)),hash])
                        checking.append(hash)
        return log

    def compare(self,std_folder):
        """
        用来对比文件夹cmp_folder和文件夹cmp_folder
        如果cmp_foler中的文件在ctd_folder中，则删除
        """
        global compare
        compare = []
        cmp_folder=self.folder_loc
        cmp_log = self.init_log(os.path.basename(cmp_folder)+'_comp.log')
        check_folder=Folder(std_folder)
        std_log = check_folder.check()
        self.process_comparing(self.folder_loc,std_log,cmp_log)
        return cmp_log

    def process_comparing(self,folder,std_log,cmp_log):
        global HASH_COLUMN
        for i in os.listdir(folder):
            if os.path.isdir(os.path.join(folder,i)):
                if i[0] not in ['@','.']:
                    print(str(os.path.join(folder,i)) + " is not dummy folder")
                    self.process_comparing(os.path.join(folder,i),std_log,cmp_log)
            else:
                media = File(os.path.join(folder,i))
                hash = media.get_md5()
                if hash is not None:
                    a = self.find_csv(std_log,hash,HASH_COLUMN)
                    if a is not None:
                        with open(cmp_log,'a',newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(['compare',i,os.path.join(folder,i),a[2],os.path.getsize(os.path.join(folder,i)),hash])
                        os.remove(os.path.join(folder,i))
                    else:
                        with open(cmp_log,'a',newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(['new',i,os.path.join(folder,i),'',os.path.getsize(os.path.join(folder,i)),hash])                   
                            compare.append(hash)  

    def class_bysize(self,dstfold,large=1):
        folder = self.folder_loc
        class_by_size_log = self.init_log(os.path.basename(folder)+'_class_by_size.log')
        if not os.path.exists(os.path.join(dstfold,"large")):
            os.makedirs(os.path.join(dstfold,"large"))
        if not os.path.exists(os.path.join(dstfold,"small")):
            os.makedirs(os.path.join(dstfold,"small"))
        if os.path.exists(class_by_size_log):
            os.remove(class_by_size_log)
        f = open(class_by_size_log,'w')
        f.close()  
        self.process_bysize(folder,dstfold,class_by_size_log,large)
        return class_by_size_log

    def process_bysize(self,folder,dstfold,log,large):

        for i in os.listdir(folder):
            if i[0] not in ['@','.']:
                if os.path.isdir(os.path.join(folder,i)):
                    self.process_bysize(os.path.join(folder,i),dstfold,log,large)
                else:
                    size = os.path.getsize(os.path.join(folder,i))
                    a = File(os.path.join(folder,i))
                    if size < large*1024*1024:
                        xx=a.move_to(os.path.join(dstfold,"small"))
                        with open(log,'a',newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(xx)
                            f.close()    
                    else:
                        xx=a.move_to(os.path.join(dstfold,"large"))
                        with open(log,'a',newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(xx)
                            f.close()     

    def class_bytype(self,dstfold):
        folder = self.folder_loc
        class_by_type_log = self.init_log(os.path.basename(folder)+'_class_by_type.log')
        self.process_bytype(folder,dstfold,class_by_type_log)
        return class_by_type_log

    def process_bytype(self,folder,dstfold,log):
        for i in os.listdir(folder):
            if i[0] not in ['@','.']:
                if os.path.isdir(os.path.join(folder,i)):
                    self.process_bytype(os.path.join(folder,i),dstfold,log)
                else:
                    media = File(os.path.join(folder,i))
                    type = media.get_type()
                    if not (os.path.exists(os.path.join(dstfold,type))):
                        os.makedirs(os.path.join(dstfold,type))
                    a=File(os.path.join(folder,i))
                    result=a.move_to(os.path.join(dstfold,type))
                    with open(log,'a',newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(result)
        

    def class_bytime(self,desfold):
        folder= self.folder_loc
        log = self.init_log(os.path.basename(folder)+'_class_bytime.log')
        self.process_bytime(folder,desfold,log)
        return log

    def process_bytime(self,folder,desfold,log):
        for i in os.listdir(folder):
            if i[0] not in ['@','.']:
                if os.path.isdir(os.path.join(folder,i)):
                    process_bytime(os.path.join(folder,i),desfold,log)
                else:
                    media = File(os.path.join(folder,i))
                    a = media.get_create_date()          
                    if not os.path.exists(os.path.join(desfold,a)):
                        os.makedirs(os.path.join(desfold,a))
                    cc = File(os.path.join(folder,i))
                    temp_log = cc.move_to(os.path.join(desfold,a))
                    with open(log,'a',newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(temp_log)

    def class_bymaker(self,desfold):
        folder = self.folder_loc
        log = self.init_log(os.path.basename(folder)+'_class_bymaker.log')
        self.process_bymaker(folder,desfold,log)
        return log

    def process_bymaker(self,folder,desfold,log):
        for i in os.listdir(folder):
            if i[0] not in ['@','.']:
                if os.path.isdir(os.path.join(folder,i)):
                    process_bymaker(os.path.join(folder,i),desfold,log)
                else:            
                    media = File(os.path.join(folder,i))
                    maker = media.get_maker()
                    if not os.path.exists(os.path.join(desfold,maker)):
                        os.makedirs(os.path.join(desfold,maker))
                    cc = File(os.path.join(folder,i))   
                    temp_log = cc.move_to(os.path.join(desfold,maker))   
                    with open(log,'a',newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(temp_log)       



    def init_log(self,logname):
        global DEFAULT_LOC
        if not os.path.exists(DEFAULT_LOC):
            os.mkdir(DEFAULT_LOC)
        if os.path.exists(os.path.join(DEFAULT_LOC,logname)):
            os.remove(os.path.join(DEFAULT_LOC,logname))
        f = open(os.path.join(DEFAULT_LOC,logname),'w')
        f.close() 
        return os.path.join(DEFAULT_LOC,logname)

    def find_csv(self,csv_file,key_words,column):
        with open(csv_file,'r') as f:
            reader = csv.reader(f,delimiter=",")
            for row in reader:
                if row[column] == key_words:
                    return row
        







        
