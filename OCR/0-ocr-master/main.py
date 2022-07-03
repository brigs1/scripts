
from pandas.core.frame import DataFrame
from SynapOCR import SynapOCR
from math import dist
#from operator import itemgetter
#from itertools import product, groupby
import re, os, glob
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

from spec_table_A import *
from spec_table_B import *
from base_0209 import *
from head_table import *
from treat_body import *

import time
import datetime

from itertools import count


start = time.time()

global new_coord_line, new_coord_box, spec_general_data, head_data, body_general, image_file, integral_attr



if __name__=='__main__':

    image_dir = r"D:/data/complex_specs/"
    #image_dir = r"C:/Users/brigs/Desktop/test_batch_whole/"
    #image_dir = r"C:/Users/brigs/Desktop/ERR_0214/unreadens/"
    #image_dir = r"C:/Users/brigs/Desktop/ERR_0214/0310/"

    target_img = r"D:/results/var_2/"
    target_js = r"D:/results/var_2/"

    new_head_data = [] # head_table에서 리턴되는 딕셔너리 수집

    new_spec_general_data = []
    new_spec_B = []
    new_spec_L = []
    
    for_json = []
     
    body_List=[]  # treat_body 에서 리턴되는 딕셔너리 수집

    

    for idir in os.listdir(image_dir): 
        print("\n\n\n\n", "@"*40,  "::::평가서 ID ::::", idir, "@"*40, "\n\n")

        ddir = os.listdir(image_dir + idir)
        ddir.sort(key = string_num_Sort) # string 으로 구성된 파일번호이므로, 숫자 순서대로 iteration 안되는 에러 보정
        
        number = count(1) ### 감정평가명세표의 순번을 할당하는 함수. 지목은 첫번째 명세표에서만 뽑고, 페이지가 변동시 발생하는 제반문제 처리

        for image_file in ddir:
            integral_attr = {}
            image_full_path = image_dir + idir +"/"+ image_file        
            print("\n\n\n", "-"*10, "::페이지 ID ::", image_full_path, "-"*10, "\n") 

            engine(image_full_path)
            new_coord_line, new_coord_box = coord(image_full_path)


            stop = False
                                        
            for head_title in new_coord_line: # 제목인식은 라인모드로    
                if head_title[0][1] < 400:

                    if re.search("[)\]]?\s?감\s?정\s?평\s?가\s?표?$|평\s?가\s?표?$", head_title[5]): # 페이지 상단부에서 찾기 
                        print("\n", " "*25,'"표종류"', ":", '"감정평가표"', head_title[5], "\n") 
                        head_data = head_table(idir, image_file, image_full_path, new_coord_line, new_coord_box)

                        shutil.copy2(image_full_path, target_img+image_file)

                        if head_data is not None:
                            for eh in head_data:
                                if eh not in new_head_data:
                                    new_head_data.append(eh)


                    elif re.search(".+명\s?세\s?표", head_title[5]) and head_title[0][1] < 400: # [)\]]?\s?감\s?정\s?평\s?가\s?명\s?세\s?표?$ 

                        for table_kind in new_coord_line:  #for m3 in new_coord_line:
                   
                                ## A형 ##
                            if re.search("일련|^지\s?번$", table_kind[5]) and table_kind[0][1] < 700:  ## A 형 감정평가명세표 #if re.search("^소", m3[5]) and m3[0][1] < 600: #if abs(table_kind[0][1] - m3[0][1]) < 50:
                                
                                print("\n", " "*25, '"표종류"', ":", '" A 형 감정평가명세표"', "\n")

                                try:
                                    spec_general_data, B_list, L_list, for_json_sta = spec_table_A(idir, image_file, image_full_path, new_coord_line, new_coord_box, next(number))

                                    shutil.copy2(image_full_path, target_img+image_file)
                                
                                    if spec_general_data != None:
                                        for sgd in spec_general_data:
                                            if sgd not in new_spec_general_data:
                                                new_spec_general_data.append(sgd)
                                                for_json.append(sgd)

                                    if B_list != None:
                                        #print("main에서 빌딩목록 확인", B_list)
                                        for bst in B_list:
                                            if bst not in new_spec_B:
                                                new_spec_B.append(bst)
                                                for_json.append(sgd)

                                    if L_list != None:
                                        #print("main에서 대지목록 확인", L_list)
                                        for elst in L_list:
                                            if elst not in new_spec_L:
                                                new_spec_L.append(elst) 
                                                for_json.append(sgd)
    

                                
                                except:
                                    print("\n", " "*30, "A형 감정평가명세표 리딩에러 >> 체크바랍니다", "\n\n")


                            elif re.search("건\s?물\s?명", table_kind[5]) and table_kind[0][1] < 700:  ## B 형 감정평가명세표 |\w+[시군]
                                print("\n", " "*25, '"표종류"', ":", '" B 형 감정평가명세표"', "\n")

                                try:#print(" 이 함수의 결과물 갯수는???", spec_general_data, B_list, L_list = spec_table_B(idir, image_full_path, new_coord_line, new_coord_box))
                                    spec_general_data, B_list, L_list = spec_table_B(idir, image_full_path, new_coord_line, new_coord_box, next(number))

                                    shutil.copy2(image_full_path, target_img+image_file)

                                    if spec_general_data != None:
                                        #print("BB main에서 일반목록 확인", spec_general_data)
                                        for sgd in spec_general_data:
                                            if sgd not in new_spec_general_data:
                                                new_spec_general_data.append(sgd)

                                    if B_list != None:
                                        #print("BB main에서 빌딩목록 확인", B_list)
                                        for bst in B_list:
                                            if bst not in new_spec_B:
                                                new_spec_B.append(bst)

                                    if L_list != None:
                                        #print("BB main에서 대지목록 확인", L_list)
                                        for elst in L_list:
                                            if elst not in new_spec_L:
                                                new_spec_L.append(elst)   
                                                

                                except:
                                    print("\n", " "*30, "B형 감정평가명세표 리딩에러 >> 체크바랍니다", "\n\n")

                        
                    else:
                        body_general_data = treat_body(idir, image_full_path, new_coord_line, new_coord_box)
                        

                        if body_general_data != None:
                            
                            for bg in body_general_data:
                                if bg not in body_List:
                                    body_List.append(bg)

            #df_gen_js = pd.DataFrame(for_json, columns = ['평가서 ID', "소재지",  '지번', '건물명_1',  '건물명_2', '이용상황',  '지상 층 수', '구조', '지붕'])
            #df_apec_general_js = df_gen_js.to_json(orient = 'columns', force_ascii=False)

            #with open(target_js+os.path.splitext(image_file)[0]+".json", 'w', encoding="UTF-8") as st:
            #    st.write(df_apec_general_js)


    df_head = pd.DataFrame(new_head_data, columns = ['평가서 ID', '평가목적', '기준시점'])
    print("\t", df_head)
    
    df_head.to_excel(r"D:/results/var_2/head.xlsx")  

    
    df_gen = pd.DataFrame(new_spec_general_data, columns = ['평가서 ID', "소재지",  '지번', '건물명_1',  '건물명_2', '이용상황',  '지상 층 수', '구조', '지붕', '도', '시', '군구', '동', '면', '리', '도로명']) #'도', '시', '군구', '동', '면', '리', '도로명'
    print("\t", df_gen)    
    df_gen.to_excel(r"D:/results/var_2/spec_general.xlsx") 

       
    df_spec_B = pd.DataFrame(new_spec_B, columns = ['평가서 ID', '일련번호_건물', '호', '층', '감정평가액', '공부_전유면적', '사정_전유면적',  '대지권면적_사정'])
    print("\t", df_spec_B)
    df_spec_B.to_excel(r"D:/results/var_2/spec_building.xlsx")       

    df_land = pd.DataFrame(new_spec_L, columns = ["평가서 ID", "일련번호_토지", "지목", "지번", "용도지역", "토지면적_해당필지"])
    print("\t", df_land)
    df_land.to_excel(r"D:/results/var_2/spec_land.xlsx")

    if body_List != None:
        print(body_List)

        df_body_gen = pd.DataFrame(body_List, columns = ["평가서 ID", "소재지",  "도로명주소", "건물명", "용도", "사용승인일", "전유면적", "공용면적", "대지권면적", "계약면적"])
        print("\t", " 이것이 본문에서 수집된 귀한 정보임!!!", df_body_gen)
        df_body_gen.to_excel(r"D:/results/var_2/body_general.xlsx")


    end = time.time()

    sec = (end - start) 
    result = datetime.timedelta(seconds=sec) 
    print("\n", "*"*48, "추출소요시간/건수", "*"*50)     
    #print("\n", "\t", result) 
    result_list = str(datetime.timedelta(seconds=sec)).split(".") 
    print("\n", " "*50, result_list[0])
    print("\n", " "*50, len(image_dir))
    print("\n", "X"*50, " THE END ", "X"*50) 
