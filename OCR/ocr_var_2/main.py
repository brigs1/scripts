
from pandas.core.frame import DataFrame
from SynapOCR import SynapOCR
#from math import dist
#from operator import itemgetter
#from itertools import product, groupby
import re, os, glob, sys
import statistics
#import cv2
#from pdf2image import convert_from_bytes, convert_from_path
import shutil
import itertools
#import openpyxl
#from openpyxl import Workbook
import numpy as np
import pandas as pd
from coord import *
from DL_forms import DL_specA

from MOD_spec_table_A import ComBld

#from spec_table_B import *
from base_0209 import *
from head_table import *
from treat_body_advanced import *

import time
import datetime

from itertools import count

start = time.time()

#global new_coord_line, new_coord_box, spec_general_data, head_data, body_general, image_file



if __name__=='__main__':

    ## 작업 디렉터리 지정    
    image_dir = r"/media/y/850EVO/data/test_batch_5/"

    target_img = r"/media/y/850EVO/results/var/"

    trg_head = "head/"
    trg_body = "body/"
    trg_spec_A = "spec_A/"
    trg_spec_B = "spec_B/"


    ### 자료 reservoir 지정


    master_list = []

    new_head_info = [] # head_table에서 리턴되는 딕셔너리 수집
    Bld_dict = {}
    body_Bld_info=[]  # treat_body 에서 리턴되는 딕셔너리 수집


    Bld_info_integral = []

    no2_body_Bld_info = []
    no2_specA_Bld_info = []
    no2_specB_Bld_info = []
    
    #new_spec_L = []
    


    for idir in os.listdir(image_dir): 
        print("\n\n\n\n", "@"*40,  "::::평가서 ID ::::", idir, "@"*40, "\n\n")

        Bld_dict = {"평가서 ID":"{}".format(idir)}
        ddir = os.listdir(image_dir + idir)
        ddir.sort(key = string_num_Sort) # string 으로 구성된 파일번호이므로, 숫자 순서대로 iteration 안되는 에러 보정
        
        number = count(1) ### 감정평가명세표의 순번을 할당하는 함수. 지목은 첫번째 명세표에서만 뽑고, 페이지가 변동시 발생하는 제반문제 처리
        
        for image_file in ddir:
            
            image_full_path = image_dir + idir +"/"+ image_file        
            print("\n\n\n", "-"*10, "::페이지 ID ::", image_full_path.split('/')[-1].split('.')[0], "-"*10, "\n") 
            # 구체적인 숫자가 지속적으로 들어와 CB라는, 구체화된, ComBld의 인스턴스를 찍어냄

            engine(image_full_path)
            new_coord_line, new_coord_box = coord(image_full_path)
            
            up_limit, down_limit = 0, 0
            CB = ComBld(idir, image_file, image_full_path, new_coord_line, new_coord_box, next(number), Bld_dict, up_limit, down_limit) 
            
            
            stop = False
                                        
            for head_title in new_coord_line: # 제목인식은 라인모드로    
                if head_title[0][1] < 400:

                    if re.search("[)\]]?\s?감\s?정\s?평\s?가\s?표?$|평\s?가\s?표?$", head_title[5]): # 페이지 상단부에서 찾기 
                        print("\n", " "*25,'"표종류"', ":", '"감정평가표"', head_title[5], "\n") 
                        CB.head_table() #

                        #shutil.copy2(image_full_path, target_img + trg_head + image_file)

                        # if head_info is not None:
                        #     for eh in head_info:
                        #         if eh not in new_head_info:
                        #             new_head_info.append(eh)


                    elif re.search(".+명\s?세\s?표", head_title[5]) and head_title[0][1] < 400: # [)\]]?\s?감\s?정\s?평\s?가\s?명\s?세\s?표?$ 

                        for table_kind in new_coord_line:  #for m3 in new_coord_line:
                   
                                ## A형 ##
                            if re.search("일련|^지\s?번$", table_kind[5]) and table_kind[0][1] < 700:  ## A 형 감정평가명세표 #if re.search("^소", m3[5]) and m3[0][1] < 600: #if abs(table_kind[0][1] - m3[0][1]) < 50:
                                
                                print("\n", " "*25, '"표종류"', ":", '" A 형 감정평가명세표"', "\n")
                                CB.spec_table_A()
                                # ComBld.Bld_dict, specA_Bld_info, L_list, num_checked_coord_box = CB.spec_table_A()
                                # print("모아진 건물의 정보 ComBld.Bld_dict::(main)::::::", ComBld.Bld_dict)
                                # #shutil.copy2(image_full_path, target_img + trg_spec_A + image_file)
                                # specA_Bld_info = [i for i in specA_Bld_info if i] # empty dict 제거
                                

                                # for bst in specA_Bld_info:  # specA_Bld_info 에서 중복제거
                                #     if bst not in no2_specA_Bld_info:
                                #         no2_specA_Bld_info.append(bst)

                                #print("모아진 건물의 정보 Bld_info_no2::::::", Bld_info_no2)
                                ## spec_A에서 읽은 빌딩정보는 리스트(Bld_info_no2)로 준비가 완료됨

                                # if len(Bld_info_no2) != 0: # 여기서 바디에서 올라온 것과 같이 비교하자




                                #     for elem_dict in Bld_info_no2:


                                #         if "페이지 ID" in elem_dict: 
                                #             Bld_data["페이지 ID"]=elem_dict["페이지 ID"]

                                #         if "도" in elem_dict: 
                                #             Bld_data["도"]=elem_dict["도"]

                                #         if "시" in elem_dict: 
                                #             Bld_data["시"]=elem_dict["시"]

                                #         if "군구" in elem_dict: 
                                #             Bld_data["군구"]=elem_dict["군구"]                                            

                                #         if "동" in elem_dict: 
                                #             Bld_data["동"]=elem_dict["동"]

                                #         if "면" in elem_dict: 
                                #             Bld_data["면"]=elem_dict["면"]

                                #         if "리" in elem_dict: 
                                #             Bld_data["리"]=elem_dict["리"]

                                #         if "지번" in elem_dict: 
                                #             Bld_data["지번"]=elem_dict["지번"]

                                #         if "건물명_1" in elem_dict: 
                                #             Bld_data["건물명_1"]=elem_dict["건물명_1"]

                                #         if "건물동" in elem_dict: 
                                #             Bld_data["건물동"]=elem_dict["건물동"]                                            

                                #         if "층" in elem_dict: 
                                #             Bld_data["층"]=elem_dict["층"]

                                #         if "호" in elem_dict: 
                                #             Bld_data["호"]=elem_dict["호"]

                                #         if "감정평가액" in elem_dict: 
                                #             Bld_data["감정평가액"]=elem_dict["감정평가액"]


                                #         if "소재지" in elem_dict: 
                                #             Bld_data["소재지"]=elem_dict["소재지"]



                                # if L_list != None:
                                #     print("main에서 대지목록 확인", L_list)
                                #     for elst in L_list:
                                #         if elst not in new_spec_L:
                                #             new_spec_L.append(elst) 
                                #             


                            elif re.search("건\s?물\s?명", table_kind[5]) and table_kind[0][1] < 700:  ## B 형 감정평가명세표 |\w+[시군]
                                print("\n", " "*25, '"표종류"', ":", '" B 형 감정평가명세표"', "\n")
                                
                                #try:#print(" 이 함수의 결과물 갯수는???", spec_general_data, specA_Bld_info, L_list = spec_table_B(idir, image_full_path, new_coord_line, new_coord_box))
                                # specB_Bld_info, L_list = spec_table_B(idir, image_full_path, new_coord_line, new_coord_box, next(number))

                                # shutil.copy2(image_full_path, target_img + trg_spec_B +image_file)

                                # if spec_general_data != None:
                                #     #print("BB main에서 일반목록 확인", spec_general_data)
                                #     for sgd in spec_general_data:


                                # if specB_Bld_info != None:
                                #     #print("BB main에서 빌딩목록 확인", specB_Bld_info)
                                #     for bst in specB_Bld_info:
                                #         if bst not in Bld_info_merged:
                                #             Bld_info_merged.append(bst)

                                # if L_list != None:
                                #     #print("BB main에서 대지목록 확인", L_list)
                                #     for elst in L_list:
                                #         if elst not in new_spec_L:
                                #             new_spec_L.append(elst)   
                                                

                                # except:
                                #     print("\n", " "*30, "B형 감정평가명세표 리딩에러 >> 체크바랍니다", "\n\n")

                        
                    else:
                        CB.treat_body() #image_full_path, new_coord_line, new_coord_box
                        # body_Bld_info = treat_body(idir, image_full_path, new_coord_line, new_coord_box)
                        # print("바디에서 뽑은 것 제대로 메인으로 전달되나", body_Bld_info)
                        
                        # if body_Bld_info != None:
                        #     #shutil.copy2(image_full_path, target_img + trg_body +image_file)
                        #     for bg in body_Bld_info:
                        #         if bg not in no2_body_Bld_info:
                        #             no2_body_Bld_info.append(bg)

                        # print("바디정보 중복제거한거 제대로 있나", no2_body_Bld_info)


    
        master_list.append(CB.dict_ejector())
    print("이것이 어떻게 나오는지 봐야함", master_list)# idir는 보고서단위>> 취합된 케이스_딕트들의 리스트가 나온다면, 
        # 
        # 메인에서는 이들 리스트를 합하기만 하면 데이터프레임이 될 것임. 

    #df_head = pd.DataFrame(new_head_info, columns = ['페이지 ID', '법인명', '평가목적', '기준시점'])
    #print("\t", df_head)    

    #df_head.to_excel(r"/media/y/850EVO/results/head.xlsx")  
    # print("\t", "집합건물 specA 입니다", no2_specA_Bld_info) 
    # print("\t", "집합건물 body 입니다", no2_body_Bld_info) 
       
    # Bld_info_integral = no2_specA_Bld_info + no2_body_Bld_info
    print("\t", "집합건물 정보_최종입니다", master_list)  
    #Bld_info_integral = filter(None, Bld_info_integral) # Nontype object 제거
    df_Bld = pd.DataFrame(master_list, columns = ['평가서 ID', '페이지 ID', '법인명', '평가목적', '기준시점', "소재지",  '도', '시', '군구', '동', '면', '리', '지번', '건물명_1', '건물동', '층', '호', '감정평가액']) #, '공부_전유면적', '사정_전유면적',  '대지권면적_사정', '이용상황',  '지상 층 수', '구조', '지붕', '건물명_2','도로명',
      
    df_Bld.to_excel(r"/media/y/850EVO/results/spec_building.xlsx")       

    # # df_land = pd.DataFrame(new_spec_L, columns = ["페이지 ID", "일련번호_토지", "지목", "지번", "용도지역", "토지면적_해당필지"])
    # # print("\t", df_land)
    # # df_land.to_excel(r"/media/y/850EVO/results/spec_land.xlsx")

    # eu_body_List = []
    # for bl in body_Bld_info:
    #     if bl != None:
    #         print(bl)
    #         eu_body_List.append(bl)

    # df_body_gen = pd.DataFrame(eu_body_List, columns = ["페이지 ID", "시", "군구", "동", "지번", "건물동", "층", "호"]) #["페이지 ID", "소재지",  "도로명주소", "건물명", "용도", "사용승인일", "전유면적", "공용면적", "대지권면적", "계약면적"])
    # print("\t", " 본문에서 건물정보!!!", df_body_gen)
    # df_body_gen.to_excel(r"/media/y/850EVO/results/body_Bld.xlsx")





    # os.system("cd ~")
    # os.system("source ~/anaconda3/etc/profile.d/conda.sh")
    
    
    # os.system("conda init bash")
    

    # import sys  
    # print(*sys.path, sep='\n')

    # sys.path.append('/home/y/anaconda3/envs/fineOCR/lib/python3.7/site-packages')

    # print("sys.path 변경후---------")
    # print(*sys.path, sep='\n')

    # dir_path="/media/y/850EVO/tries/once/yolov5/"
    # terminal_command = f"cd {dir_path}" 
    # os.system(terminal_command)
    # #os.system("conda activate fineOCR")
    # #os.system('python detect.py --weights /media/y/850EVO/tries/once/yolov5/runs/train/exp/weights/last.pt --img 1024 --conf 0.05 --source "/media/y/850EVO/LABELED_DATA/train/images/D18100118_4.jpg"')

    










    end = time.time()

    sec = (end - start) 
    result = datetime.timedelta(seconds=sec) 
    print("\n", "*"*48, "추출소요시간/건수", "*"*50)     
    #print("\n", "\t", result) 
    result_list = str(datetime.timedelta(seconds=sec)).split(".") 
    print("\n", " "*50, result_list[0])
    print("\n", " "*50, len(image_dir))
    print("\n", "X"*50, " THE END ", "X"*50) 
