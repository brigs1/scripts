from coord import *
import re
#from body_base_table import *

# def treat_base_table(idir, image_full_path, new_coord_box, new_coord_line, up_limit, down_limit):


#     body_general_attr = {}
        
#     body_errors = []
#     build_name = []


#     print("이제 body_base_table로 분석합니다", "\n")

#     table_area_box = [] # 테이블 주변부까지 어느정도 포함됨
#     for ta in new_coord_box:
#         if up_limit < int(ta[0][1]) < down_limit:
#             if len(ta[5]) < 40: # 테이블 멤버의 글자수 제한
#                 table_area_box.append(ta)

#     #print("테이블 영역_박스", table_area_box, "\n")
#     print("\n")
#     #for tab in table_area_box:
#         #print("테이블 영역_박스", tab)
        

#     table_area_line = [] # 테이블 주변부까지 어느정도 포함됨
#     for ta in new_coord_line:
#         if up_limit < int(ta[0][1]) < down_limit:
#             if len(ta[5]) < 40: # 테이블 멤버의 글자수 제한
#                 table_area_line.append(ta)
#     #print("테이블 영역_라인", table_area_line, "\n")
#     print("\n")
#     #for tal in table_area_line:
#         #print("테이블 영역_라인", tal)




#     #key_merged_table_area = key_merge_raw_virtical(table_area)
#     #print("머징된 테이블 영역", key_merged_table_area)



#     ######### 박스모드 키항목 정돈 - start ################

#     key_letters = [] 
    
#     for letter in table_area_box:

#         if re.search("^[소재지]+", letter[5]):
#             if up_limit < letter[0][1] < down_limit - 200:
#                 key_letters.append(letter)
                
#         elif re.search("[건물명칭]+", letter[5]):
#             if up_limit < letter[0][1] < down_limit - 200:
#                 key_letters.append(letter)

#         elif re.search("[주용도]+", letter[5]):
#             if up_limit < letter[0][1] < down_limit:
#                 key_letters.append(letter)

#         elif re.search("^[사용승인일]+", letter[5]):
#             if up_limit < letter[0][1] < down_limit:
#                 key_letters.append(letter)

#         elif re.search("^[전유공용계약대지권면적]+", letter[5]):
#             if up_limit < letter[0][1] < down_limit:
#                 key_letters.append(letter)

#     #print("박스모드로 수집", key_letters, "\n")


#     NKL = []
#     for ek in key_letters:
#         nek = [ek[0], ek[1], ek[2], ek[3], ek[4], ek[5].replace(" ", "")]
#         NKL.append(nek)

#     #print("박스모드로 수집 후 가공", NKL, "\n")

#     key_body_base = {}  # 박스모드에서의 1차 모집
#     kbb_list = ["addr", "buildname", "builduse", "authordate", "privatearea", "publicarea", "contractarea", "landrightarea"]

#     for nk in NKL:
#         if re.search(".*소\s?재\s?지.*", nk[5]):
#             key_body_base["addr"] = nk
#             print("\n", "키목록 체크-1ㅠㅠ", key_body_base, "\n")
#         elif re.search("건물명.*", nk[5]):
#             key_body_base["buildname"] = nk

#         elif re.search("[주]?용도$", nk[5]):
#             key_body_base["builduse"] = nk

#         elif re.search("사용승인", nk[5]):
#             key_body_base["authordate"] = nk

#         elif re.search("^전[용유]$|전[용유]면적$|전[용유]면적[^\s가-힣]", nk[5]):
#             key_body_base["privatearea"] = nk

#         elif re.search("^공[용유]$|공[용유]면적$|공[용유]면적[^\s가-힣]", nk[5]):
#             key_body_base["publicarea"] = nk

#         elif re.search("^계약면.*", nk[5]):
#             key_body_base["contractarea"] = nk

#         elif re.search("^대지권$|^대지권.*", nk[5]):
#             key_body_base["landrightarea"] = nk

           
#     #print("박스에서 수집된 A형평가서의 키박스::", key_body_base, "\n")


#     unmet_keys = []
#     for kbb in kbb_list:
#         if not kbb in key_body_base.keys():
#             unmet_keys.append(kbb)

#     #print("박스모드 작업으로 채워지지 않은 키박스::", unmet_keys, "\n")



#     ############ 이제 라인모드로 키처리 ###################


#     ## A 양식의 키단어 모집을 위한 필터

#     K = []

#     for letter in new_coord_line:  # 키인식은 라인모드로 
#         if re.search("^[소재지]+", letter[5]):
#             if up_limit < letter[0][1] < down_limit - 200:
#                 K.append(letter)
                
#         elif re.search("^[건물명칭]+", letter[5]):
#             if up_limit < letter[0][1] < down_limit - 200:
#                 K.append(letter)

#         elif re.search("[주용도]+", letter[5]):
#             if up_limit < letter[0][1] < down_limit:
#                 key_letters.append(letter)

#         elif re.search("^[사용승인일]+", letter[5]):
#             if up_limit < letter[0][1] < down_limit:
#                 K.append(letter)

#         elif re.search("^[전유공용계약대지권면적]+", letter[5]):
#             if up_limit < letter[0][1] < down_limit:
#                 K.append(letter)

                
#     #print("라인모드로 A 형의 키를 모집 ", K, "\n")

#     #print("\n", "키목록 체크-1", key_body_base, "\n")
#     ## 박스모드에서도 일단 완전한 단어부터 골라야 하겠지??

#     del_1= []
#     for uk in unmet_keys:
#         for nk in NKL:

#             if uk == 'addr':
#                 if re.search(".*소\s?재\s?지.*", nk[5]):
#                     key_body_base["addr"] = nk
#                     del_1.append(nk)
#             elif uk == 'buildname':                    
#                 if re.search("건물명.*|명\s?칭", nk[5]):
#                     key_body_base["buildname"] = nk
#                     del_1.append(nk)

#             elif uk == 'buildname': 
#                 if re.search("[주]용도$", nk[5]):
#                     key_body_base["builduse"] = nk
#                     del_1.append(nk)


#             elif uk == 'authordate':
#                 if re.search("사용승인", nk[5]):
#                     key_body_base["authordate"] = nk
#                     del_1.append(nk)
#             elif uk == 'privatearea':
#                 if re.search("^전[용유]$|전[용유]면적$|전[용유]면적[^\s가-힣]", nk[5]): #전용률 이라는 단어가 혼선
#                     key_body_base["privatearea"] = nk
#                     del_1.append(nk)
#             elif uk == 'publicarea':
#                 if re.search("^공[용유]$|공[용유]면적$|공[용유]면적[^\s가-힣]", nk[5]):
#                     key_body_base["publicarea"] = nk
#                     del_1.append(nk)
#             elif uk == 'contractarea':
#                 if re.search("^계약면.*", nk[5]):
#                     key_body_base["contractarea"] = nk
#                     del_1.append(nk)
#             elif uk == 'landrightarea':
#                 if re.search("^대지권$|^대지권.*", nk[5]):
#                     key_body_base["landrightarea"] = nk
#                     del_1.append(nk)


#     K_1=[]
#     for kk in NKL:
#         if kk not in del_1:
#             K_1.append(kk)

                   
           
#     #print("박스모드에서 수집된 A형평가서의 키박스::", key_body_base, "\n")


#     unmet_keys_box = []
#     for kbb in kbb_list:
#         if not kbb in key_body_base.keys():
#             unmet_keys_box.append(kbb)

#     #print("박스모드 작업으로 채워지지 않은 키박스::", unmet_keys_box, "\n")

#     #print("작업벤치:K_1:", K_1, "\n")
#     #print("\n", "키목록 체크00", key_body_base, "\n")
#     ####################################################################################################
#     ## 온전한 단어는 다 살펴보았고, 이제는 낱글자들과 부서진 여러글자들을 모아 키를 조립해야함 ###

#     ### 1. 소재지 / 건물명 / 사용승인일의 낱글자 처리 == 3단계 조립
#     del_from_K_1= []
#     add_to_K_1 = []

                
#     for ukb in unmet_keys_box:
#         for bs1 in K_1:                    
#             for bs2 in K_1:
#                 for bs3 in K_1:
#                     if ukb == 'addr':                                    
                               
#                         if re.search("^소$", bs1[5]):
#                             if re.search("^재$", bs2[5]):
#                                 diff1 = bs2[0][0] - bs1[0][0]
#                                 if re.search("^지$", bs3[5]): ## 소 재 지 간의 간격이 균등함을 이용해 다른 '지'자 배제 
    
#                                     diff2 = (bs3[0][0] - bs2[0][0])
#                                     if abs(diff1-diff2) < 15:
#                                         addr = raw_x3_merge(bs1, bs2, bs3) 
                                            
#                                         key_body_base["addr"] = addr  ## 소재지가 완성된 경우,
#                                         del_from_K_1.append(bs1)
#                                         del_from_K_1.append(bs2)
#                                         del_from_K_1.append(bs3)

#                     elif ukb == 'buildname':
                          
#                         if re.search("^건$", bs1[5]): 
#                             if re.search("^물$", bs2[5]):     
#                                 if re.search("^명$", bs3[5]):
                                   
#                                     d1 = midpoint(bs1)[0] - midpoint(bs2)[0]
#                                     d2 = midpoint(bs2)[0] - midpoint(bs3)[0]

#                                     if abs(d1 - d2) < 10 and abs(midpoint(bs1)[1]-midpoint(bs2)[1]) < 10 and abs(midpoint(bs2)[1] - midpoint(bs3)[1])< 10:
                                            
#                                         use = raw_x3_merge(bs3, bs2, bs1) 
#                                         add_to_K_1.append(use)
#                                         del_from_K_1.append(bs1)
#                                         del_from_K_1.append(bs2)
#                                         del_from_K_1.append(bs3)                  
                                           

#                     elif ukb == 'authordate':
                          
#                         if re.search("^사$", bs1[5]): 
#                             if re.search("^승$", bs2[5]): 
#                                 if re.search("^일$", bs3[5]):
                                   
#                                     d1 = midpoint(bs1)[0] - midpoint(bs2)[0]
#                                     d2 = midpoint(bs2)[0] - midpoint(bs3)[0]

#                                     if abs(d1 - d2) < 10 and abs(midpoint(bs1)[1]-midpoint(bs2)[1]) < 10 and abs(midpoint(bs2)[1] - midpoint(bs3)[1])< 10:
                                            
#                                         use = raw_x3_merge(bs3, bs2, bs1) 
#                                         add_to_K_1.append(use)
#                                         del_from_K_1.append(bs1)
#                                         del_from_K_1.append(bs2)
#                                         del_from_K_1.append(bs3)    



#     for ek in add_to_K_1:
#         if ek not in K_1:
#             K_1.append(ek)

#     #print("지울거", del_from_K_1)                            
#     K_2 = []
#     for singj in K_1:
#         if singj not in del_from_K_1: ## 단어생성이 끝난 "소, 재, 지", 건, 물, 명, 사, 승, 일 제거
#             K_2.append(singj)
                                                                        
#     #print("K_2",K_2, "\n")
    

#     for ukb2 in unmet_keys_box:
                    
#         for nm1 in K_2:
#             for nm2 in K_2:
#                 for nm3 in K_2:

#                     if ukb2 == 'addr':
#                         if re.search("^소$", nm1[5]):
#                             if re.search("^재지$", nm2[5]):  
#                                 if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
#                                     key_body_base["addr"] = raw_x_merge(nm1, nm2)

#                         elif re.search("^소재$", nm1[5]):                                        
#                             if re.search("^지$", nm2[5]):                                           
#                                 if abs((nm2[0][0]-nm1[1][0]) - abs((nm1[1][0] - nm1[0][0]) - (nm2[1][0]-nm2[0][0])*2)) < 10 and abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
#                                     key_body_base["addr"] = raw_x_merge(nm1, nm2)   
                                        

#                     elif ukb2 == 'buildname':
#                         if re.search("^건물$", nm1[5]):
#                             if re.search("^명$", nm2[5]):                                    
#                                 if abs((nm2[0][0]-nm1[1][0]) - abs((nm1[1][0] - nm1[0][0]) - (nm2[1][0]-nm2[0][0])*2)) < 10 and abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
#                                     key_body_base["buildname"] = raw_x_merge(nm1, nm2)


#                         elif re.search("^건$", nm1[5]):
#                             if re.search("^물명$", nm2[5]):                                    
#                                 if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
#                                     key_body_base["buildname"] = raw_x_merge(nm1, nm2)


#                         elif re.search("^명$", nm1[5]):
#                             if re.search("^칭$", nm2[5]):                                    
#                                 if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
#                                     key_body_base["buildname"] = raw_x_merge(nm1, nm2)

#                     elif ukb2 == 'builduse':
#                         if re.search("^용$", nm1[5]):                                        
#                             if re.search("^도$", nm2[5]):                                            
#                                 if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
#                                     key_body_base["builduse"] = raw_x_merge(nm1, nm2)  

#                         elif re.search("^주용$", nm1[5]):                                        
#                             if re.search("^도$", nm2[5]):                                            
#                                 if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
#                                     key_body_base["builduse"] = raw_x_merge(nm1, nm2)  


#                     elif ukb2 == 'privatearea':
#                         if re.search("^전유$", nm1[5]):                                        
#                             if re.search("^면적", nm2[5]):                                            
#                                 if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
#                                     key_body_base["privatearea"] = raw_x_merge(nm1, nm2)  

#                                 elif abs(midpoint(nm1)[0] - midpoint(nm2)[0]) < 10:
#                                     key_body_base["privatearea"] = raw_y_merge(nm1, nm2)  


#                     elif ukb2 == 'publicarea':
#                         if re.search("^공용$", nm1[5]):                                        
#                             if re.search("^면적", nm2[5]):                                            
#                                 if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
#                                     key_body_base["publicarea"] = raw_x_merge(nm1, nm2)  

#                                 elif abs(midpoint(nm1)[0] - midpoint(nm2)[0]) < 10:
#                                     key_body_base["publicarea"] = raw_y_merge(nm1, nm2)  


#                     elif ukb2 == 'contractarea':
#                         if re.search("^계약$", nm1[5]):                                        
#                             if re.search("^면적", nm2[5]):                                            
#                                 if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
#                                     key_body_base["contractarea"] = raw_x_merge(nm1, nm2)  

#                                 elif abs(midpoint(nm1)[0] - midpoint(nm2)[0]) < 10:
#                                     key_body_base["contractarea"] = raw_y_merge(nm1, nm2)  

#                     elif ukb2 == 'landrightarea':
#                         if re.search("^대지권$", nm1[5]):                                        
#                             if re.search("^면적", nm2[5]):                                            
#                                 if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
#                                     key_body_base["landrightarea"] = raw_x_merge(nm1, nm2)  

#                                 elif abs(midpoint(nm1)[0] - midpoint(nm2)[0]) < 10:
#                                     key_body_base["landrightarea"] = raw_y_merge(nm1, nm2)  



#     unmet_keys_box_2 = []
#     for kb in kbb_list:
#         if not kb in key_body_base.keys():
#             unmet_keys_box_2.append(kb)


#     #print("미완성 키 박스 :", unmet_keys_box_2, "\n")

#     #print("\n", "키목록 체크", key_body_base, "\n")


#     #addr_Y = (key_body_base["addr"][1][1] + key_body_base["addr"][2][1])/2

#     ### 항목별 격벽의 좌표를 정해둠 ####     
#     print("\n", " "*20, ":"*10, "인식된 키박스(본문)", ":"*10, "\n")          
#     for key in key_body_base:

#         if key == "addr":
#             addr_L = key_body_base["addr"][0][0]
#             addr_R = key_body_base["addr"][1][0]
#             addr_Y = (key_body_base["addr"][1][1] + key_body_base["addr"][2][1])/2
#             print(" "*30, addr_L, key_body_base["addr"][5], addr_R)  

#         elif key == "buildname":
#             buildname_L = key_body_base["buildname"][0][0]
#             buildname_R = key_body_base["buildname"][1][0]
#             buildname_Y = (key_body_base["buildname"][1][1] + key_body_base["buildname"][2][1])/2
#             print(" "*30, buildname_L, key_body_base["buildname"][5], buildname_R)  

#         elif key == "builduse":
#             builduse_L = key_body_base["builduse"][0][0]
#             builduse_R = key_body_base["builduse"][1][0]
#             builduse_Y = (key_body_base["builduse"][1][1] + key_body_base["builduse"][2][1])/2
#             print(" "*30, builduse_L, key_body_base["builduse"][5], builduse_R)  


#         elif key == "authordate":
#             authordate_L = key_body_base["authordate"][0][0]
#             authordate_R = key_body_base["authordate"][1][0]
#             authordate_Y = (key_body_base["authordate"][1][1] + key_body_base["authordate"][2][1])/2
#             print(" "*30, authordate_L, key_body_base["authordate"][5], authordate_R, "Y:", authordate_Y)   

#         elif key == "privatearea":
#             privatearea_L = key_body_base["privatearea"][0][0]
#             privatearea_R = key_body_base["privatearea"][1][0]
#             privatearea_Y = (key_body_base["privatearea"][1][1] + key_body_base["privatearea"][2][1])/2
#             print(" "*30, privatearea_L, key_body_base["privatearea"][5], privatearea_R)  

#         elif key == "publicarea":
#             publicarea_L = key_body_base["publicarea"][0][0]
#             publicarea_R = key_body_base["publicarea"][1][0]
#             publicarea_Y = (key_body_base["publicarea"][1][1] + key_body_base["publicarea"][2][1])/2
#             print(" "*30, publicarea_L, key_body_base["publicarea"][5], publicarea_R)  

#         elif key == "contractarea":
#             contractarea_L = key_body_base["contractarea"][0][0]
#             contractarea_R = key_body_base["contractarea"][1][0]
#             contractarea_Y = (key_body_base["contractarea"][1][1] + key_body_base["contractarea"][2][1])/2
#             print(" "*30, contractarea_L, key_body_base["contractarea"][5], contractarea_R)   


#         elif key =="landrightarea":
#             landrightarea_L = key_body_base["landrightarea"][0][0]
#             landrightarea_R = key_body_base["landrightarea"][1][0]
#             landrightarea_Y = (key_body_base["landrightarea"][1][1] + key_body_base["landrightarea"][2][1])/2
#             print(" "*30, landrightarea_L, key_body_base["landrightarea"][5], landrightarea_R)  
#     print("\n", " "*20, ":"*30, "\n")
#     #print("\n", "키목록 체크", key_body_base, "\n")


#     #print("테이블 영역 텍스트 라인::",table_area_line) 
#     for vg in  table_area_line:
#         if "addr" in key_body_base:    
            
#             if  abs(addr_Y - midpoint(vg)[1]) < 50 or 0 <= (midpoint(vg)[0] - (addr_L+addr_R)/2) < 50:## 가로세로방향 정렬시
#                 body_general_attr["소재지"] = "{}".format(vg[5])
                        

#                 if re.search("^[가-힣]+\d*도$", vg[5]):   
#                     body_general_attr["도"] = "{}".format(vg[5])

#                 elif re.search("^[가-힣]+\d*시$", vg[5]):   
#                     body_general_attr["시"] = "{}".format(vg[5])
                    
#                 elif re.search("^[가-힣]+\d*[군구]$", vg[5]):
#                     body_general_attr["군구"] = "{}".format(vg[5])                        

#                 elif re.search("^[가-힣]+\d*[동]$", vg[5]):
#                     body_general_attr["동"] = "{}".format(vg[5])

#                 elif re.search("^[가-힣]+\d*[면]$", vg[5]):
#                     body_general_attr["면"] = "{}".format(vg[5])

#                 elif re.search("^[가-힣]+\d*[리]$", vg[5]):
#                     body_general_attr["리"] = "{}".format(vg[5])
                    
#                 # elif re.search("^[가-힣]+\d*[길로]$", vg[5]):
#                 #     body_general_attr.append(vg[5])

#                 # elif re.search("^\d{1,4}\-?\d{1,3}[길로]?$", vg[5]):
#                 #     body_general_attr.append(vg[5])  # 도로명 주소상 지번이므로 구분함



#             # if "소재지" not in body_general_attr:
#             #     body_general_attr["소재지"] = "{}".format(vg[5])

#         if "buildname" in key_body_base:
#             if re.search("\d+[동층호]", vg[5]):
#                 if  abs(buildname_Y - midpoint(vg)[1]) < 50 and buildname_R + 100 < midpoint(vg)[0]: 
#                     build_name.append(vg)
                
#                     print("건물명 check_point_1", vg)
#                     build_name.append(vg)               
#                     #if "건물명" not in body_general_attr:

#         #elif re.search("([가-힣]+[길로])\s?(\d+)", vg[5]):
#         #    if "도로명주소" not in body_general_attr:
#         #        body_general_attr["도로명주소"]= "{}".format(vg[5])  # 도로명 주소상 지번이므로 구분함


#         if "builduse" in key_body_base:
#             if re.search("도시형|^아파트$|^다세대|주택|공동|근린", vg[5]):
            
                      
#                 if (builduse_Y - midpoint(vg)[1]) < 20:  
#                     body_general_attr["용도"] = "{}".format(vg[5])

#         elif re.search("(19|20)(\d{2})[.,년]\s?\d{1,2}?[.,월]?", vg[5]): # 구버전 (19|20)\d{2}[.,]\s?\d{1,2}[.,]\s?\d{1,2}[.,]?
#             if "authordate" in key_body_base:                
#                 if abs(authordate_Y - midpoint(vg)[1]) < 20:  
#                     body_general_attr["사용승인일"] = "{}".format(vg[5])
#                 elif authordate_L < midpoint(vg)[0] < authordate_R and 20 < abs(authordate_Y - midpoint(vg)[1]) < 300:
#                     body_general_attr["사용승인일"] = "{}".format(vg[5])


#         elif re.search("^(\d{1,3}\,)*\d{1,3}.?\d+[-]?", vg[5]):
            
#             if "privatearea" in key_body_base:
#                 if privatearea_L < midpoint(vg)[0] < privatearea_R and 0 < (midpoint(vg)[1] - privatearea_Y) < 200:                 
#                     body_general_attr["전유면적"] = "{}".format(vg[5])

#             if "publicarea" in key_body_base:
#                 if publicarea_L < midpoint(vg)[0] < publicarea_R and 0 < (midpoint(vg)[1] - publicarea_Y) < 200:
#                     body_general_attr["공용면적"] = "{}".format(vg[5])

#             if "landrightarea" in key_body_base:
#                 if landrightarea_L < midpoint(vg)[0] < landrightarea_R and 0 < (midpoint(vg)[1] - landrightarea_Y) < 200:
#                     body_general_attr["대지권면적"] = "{}".format(vg[5])

#             if "contractarea" in key_body_base:
#                 if contractarea_L < midpoint(vg)[0] < contractarea_R and 0 < (midpoint(vg)[1] - contractarea_Y) < 200:
#                     body_general_attr["계약면적"] = "{}".format(vg[5])


#         #elif re.search(".+", vg[5]): #[가-힣]+(아파트|빌라)|([가-힣]+)\s?(.+[층동])\s?(\w+[층동호])\s?(\w+[호])?|[가-힣]+ #[^사용승인일]
#         #    if abs(buildname_Y - midpoint(vg)[1]) < 50 and buildname_R + 100 < midpoint(vg)[0]: 
#         #        print("건물명 check_point_2", vg)
#         #        build_name.append(vg)             

                        
#                     ### 참고 table_title = re.search("(?<=[\.\)\,-]).{2,25}", up[2]).group(0)
            
#     ## 건물명이 여러줄이거나 옆으로 긴 경우가 있어 모아서 따로 처리해준다 ##
#     new_build_name = []
#     build_name.sort(key=lambda t: t[0][1])
#     for bnm in build_name:
#         if bnm[5] not in new_build_name:
#             print("건물명 중복체크", bnm)
#             new_build_name.append(bnm[5])



            
#     # 수집된 각 항목의 리스트를 for 문 종료시 딕셔너리에 부가한다.
    

#     if len(new_build_name) > 0:
#         body_general_attr["건물명"] = ' '.join(new_build_name)
#     if len(body_general_attr) > 1:
#         body_general_attr["페이지 ID"] = image_full_path.split('/)[-1].split('.')[0]

#     #print("\n", "본문_일반항목", body_general_attr, "\n")


#     return body_general_attr




def top_gun_for_addr(idir, image_full_path, new_coord_box, new_coord_line, up_limit, down_limit):
    body_general_attr = {}
    addr = []
    

    for vg in new_coord_box:
        if up_limit < vg[0][1] < down_limit:
     
            if re.search("^[가-힣]+\d*도$", vg[5]):   
                addr.append(vg)
                #body_general_attr["도"] = "{}".format(vg[5])

            elif re.search("^[가-힣]+\d*시$", vg[5]):  
                addr.append(vg) 
                #body_general_attr["시"] = "{}".format(vg[5])
                
            elif re.search("^[가-힣]+\d*[군구]$", vg[5]):
                addr.append(vg)
                #body_general_attr["군구"] = "{}".format(vg[5])                        

            elif re.search("^[가-힣]+\d{1,2}[동]$|^[가-힣]{,4}동$", vg[5]):
                addr.append(vg)
                #body_general_attr["동"] = "{}".format(vg[5])

            elif re.search("^[가-힣]+\d*[면]$", vg[5]):
                addr.append(vg)
                #body_general_attr["면"] = "{}".format(vg[5])

            elif re.search("^[가-힣]+\d*[리]$", vg[5]):
                addr.append(vg)
                #body_general_attr["리"] = "{}".format(vg[5])  

            elif re.search("\d{,4}\-\d{,2}|^\d{,4}$", vg[5]):   #[가-힣]{3,20}|\d+[동]$
                addr.append(vg)
                #body_general_attr["지번"] = "{}".format(vg[5])

    ## 주소가 가로로 1열만 있는 경우##

    result_groups = []
    for ad in addr:
        found_group = False

        for group in result_groups:
            for end_member in group:
                if abs(end_member[0][1]-ad[0][1]) < 5:
                    group.append(ad)
                    found_group = True
                    break
                elif found_group:
                    break
        if not found_group:
            result_groups.append([ad])

    # new_addr = []    
    # if len(addr) > 1:
    #     print("주소가 가로로 1열이 있는 경우라 사료되는 경우", addr)
    #     for th, ne in this_and_next(addr):
    #         if th !=None and ne!=None:
            
    #             if abs(th[0][1] - ne[0][1]) < 5:
    #                 new_addr.append(th)
    #                 new_addr.append(ne)

    

    if len(result_groups) >= 1:
        #print("새 result_groups",result_groups)
        for group in result_groups:
            print("group", group)
            group_dict = {}
            for vg in group:
                
                if re.search("^[가-힣]+\d*도$", vg[5]):                       
                    group_dict["도"] = "{}".format(vg[5])
                    print("group_dict", group_dict)

                elif re.search("^[가-힣]+\d*시$", vg[5]):                       
                    group_dict["시"] = "{}".format(vg[5])
                    print("group_dict", group_dict)
                    
                elif re.search("^[가-힣]+\d*[군구]$", vg[5]):                    
                    group_dict["군구"] = "{}".format(vg[5]) 
                    print("group_dict", group_dict)                       

                elif re.search("^[가-힣]+\d{1,2}[동]$|^[가-힣]{,4}동$", vg[5]):                    
                    group_dict["동"] = "{}".format(vg[5])
                    print("group_dict", group_dict)

                elif re.search("^[가-힣]+\d*[면]$", vg[5]):                    
                    group_dict["면"] = "{}".format(vg[5])
                    print("group_dict", group_dict)

                elif re.search("^[가-힣]+\d*[리]$", vg[5]):                    
                    group_dict["리"] = "{}".format(vg[5])
                    print("group_dict", group_dict)  

                elif re.search("\d{,4}\-\d{,2}|^\d{,4}$", vg[5]):   #[가-힣]{3,20}|\d+[동]$                    
                    group_dict["지번"] = "{}".format(vg[5])
                    print("group_dict", group_dict)


            if "동" in group_dict and "지번" in group_dict:
                body_general_attr["페이지 ID"] = image_full_path.split('/')[-1].split('.')[0]
                body_general_attr.update(group_dict)
                print("body_general_attr", body_general_attr)
                return body_general_attr


def treat_body(idir, image_full_path, new_coord_line, new_coord_box):
    body_errors = []
    body_general_data = []
    #try:

    print("\n", "."*30, "본문표(=body_table) 처리 시작", "."*30, "\n")

    ### 소제목 라인들 리스트 구축  ###

    title_line = []
    breaker = False
    delete_from_mcl = []
    mid_coord_line = []
    for me in new_coord_line:
        ### 현페이지에서 소제목 형식을 갖는 라인 탐색
        ### 제목번호와 제목이 따로 떨어져 있는 버그를 찾아 붙여주기

        if re.search("^([\(])?([0-9가나다라마바사아자차ㄱㄴㄷIVXivx]*)([-\)\.\,])$",  me[5]) and not re.search("[)\]]?\s?감\s?정\s?평\s?가\s?명?\s?세?\s?표?$", me[5]) and me[0][1] < 400: # 페이지 상단부에서 찾기:

            for rest_me in new_coord_line: 
                if 175 < get_mid_angle(midpoint(me), midpoint(rest_me)) <= 180 or -180 < get_mid_angle(midpoint(me), midpoint(rest_me)) <= -175:
                    if get_mid_distance(midpoint(me), midpoint(rest_me)) <= 800:                               

                        delete_from_mcl.append(midpoint(me))
                        delete_from_mcl.append(midpoint(rest_me))
                        mid_coord_line.append(mid_merge(midpoint(me), midpoint(rest_me)))
                        breaker = True

                        break

        if breaker == True:
            break

    #print("소제목 정리한 라인들", new_new_coord_line) # 제목을 잘붙여서 정리해 두어야 어떤 표인지 추후에 명확히 필터링할 수 있다.    

    temp_coord_line = [t for t in new_coord_line if t not in delete_from_mcl]


    new_new_coord_line = []
    for mcl in temp_coord_line:
        if mcl not in new_new_coord_line:
            new_new_coord_line.append(mcl)

    for ind, ti in enumerate(new_new_coord_line):
        # 아래 주석처리부분 == 일반적인 제목을 고르는 필터
        if re.search("^([\(])?([0-9가나다라마바사아자차ㄱㄴㄷIVXivx]*)([-\)\.\,])\s?[그밖의사항월시임대공감정점수정지수인근지역거래사비교선정사정산출개요대상물건전유면적기타평가결정참고]|(평가)\s?(대상)$|(대상)$|(물건)$", ti[5]): 
            title_line.append(ti)            #소제목 y좌표와 텍스트정보
        
    title_line.sort(key=lambda t: t[0][1])
    #print("전체 표목록::", "\n", "\t",  title_line, "\n")

    # 소제목 단락별로 처리하기

    #if len(title_line) == 0:
        #print( "\n\n", "\t\t\t\t", ":::::소제목 없음:::::" "\n\n")

    if len(title_line) >= 1:
        for up, down in this_and_next(title_line):
            if down != None:
                print("\n\n", "    ", "소제목 구간: ", up[5], "~", down[5],  "\n\n")
                up_limit = int(up[0][1])
                down_limit = int(down[0][1])+50

                if re.search("^([\(])?([0-9가나다라마바사아자차ㄱㄴㄷIVXivx]*)([-\)\.\,])\s?(평가\s?대상|대상\s?물건|물건\s?개요)|(평가)\s?(대상)|(대상)|(물건)", up[5]): # 대상물건 개요표 처리  
                    print("대상물건표 처리시작:::")

                    body_general_attr = top_gun_for_addr(idir, image_full_path, new_coord_box, new_coord_line, up_limit, down_limit)
                    
                    # if len(body_general_attr) == 0:
                    #     print("body_general_attr 출력사항 없음")
                        
                    #     #continue

                    # else:
                    print("body_general_attr", body_general_attr)
                    body_general_data.append(body_general_attr)
                        
                #elif re.search("^([\(])?([0-9가나다라마바사아자차ㄱㄴㄷIVXivx]*)([-\)\.\,])\s?(비교|인근|유사).+(거래\s?사례$)", up[2]): # 거래사례표 처리
                #    treat_deal_case_table()
                #elif re.search("^([\(])?([0-9가나다라마바사아자차ㄱㄴㄷIVXivx]*)([-\)\.\,])\s?(가치|개별)?.+(요인\s?비교치?)", up[2]): # 개별요인비교표 처리
                #    treat_factor_comparison_table()
                #pass
                

            elif down == None:
                print("\n\n", "    ", "소제목 구간: ", up[5], "~", "페이지 끝", "\n\n")
                up_limit = int(up[0][1])
                down_limit = 2300
                if re.search("^([\(])?([0-9가나다라마바사아자차ㄱㄴㄷIVXivx]*)([-\)\.\,])\s?(평가\s?대상|대상\s?물건|물건\s?개요)|(평가)\s?(대상)|(대상)|(물건)", up[5]):  # 대상물건 개요표 처리
                    body_general_attr = top_gun_for_addr(idir, image_full_path, new_coord_box, new_coord_line, up_limit, down_limit)
                    


                    # if len(body_general_attr) == 0:
                    #     print("body_general_attr 항목이 발견되지 않음")
                    #     #continue
                    # else:
                    print("body_general_attr", body_general_attr)
                    body_general_data.append(body_general_attr)

                #elif re.search("^([\(])?([0-9가나다라마바사아자차ㄱㄴㄷIVXivx]*)([-\)\.\,])\s?(비교|인근|유사).+(거래\s?사례$)", up[2]): # 거래사례표 처리
                #    treat_deal_case_table()
                #elif re.search("^([\(])?([0-9가나다라마바사아자차ㄱㄴㄷIVXivx]*)([-\)\.\,])\s?(가치|개별)?.+(요인\s?비교치?)", up[2]): # 개별요인비교표 처리
                #    treat_factor_comparison_table()
                #pass
    print("\n", "."*30, "본문표(=body_table) 처리 끝", "."*30, "\n")     
    
    return body_general_data

    # except:
    #     body_errors.append(image_full_path)

    #     new_body_errors = []
    #     for nsg in body_errors:
    #         if nsg not in new_body_errors:
    #             new_body_errors.append(nsg)

    #     for sne in new_body_errors:
    #         with open(r"D:/results/var_2/body_errors.txt", 'a') as s:
    #             s.write("\n")
    #             s.write(str(sne))











































    #print("키가 못된 부스러기들", key_letters, "\n")

    #no2_key_letters = [] # 마구 중복된 키워드 파편들 정비
    #no2_key_letters = remove_duplicate_list(key_letters, no2_key_letters)

    ## 여기서 원래 table_area 에서 선별된 홑글자들은 제거
    
    #table_area = [tar for tar in table_area if tar not in key_letters]


    #key_gen = [] # 홑글자를 합하여 완성한 키를 모으는 곳            
            
    #for key_letter in no2_key_letters:                
    #    for other_letter in no2_key_letters:  

    #        if re.search("^소$", key_letter[5]):
    #            if re.search("^지$", other_letter[5]) and 0< (other_letter[0][0] - key_letter[0][0]) < 250 and abs(key_letter[0][1]-other_letter[0][1]) < 10:                            
    #                key_completion = [key_letter[0], other_letter[1], other_letter[2], key_letter[3], key_letter[4], "소재지"]
    #                key_gen.append(key_completion)                 


    #            elif re.search("^용$", key_letter[5]):
    #                if re.search("^도$", other_letter[5]) and 0< (other_letter[0][0] - key_letter[0][0]) < 150 and abs(key_letter[0][1]-other_letter[0][1]) < 10:                            
    #                    key_completion = [key_letter[0], other_letter[1], other_letter[2], key_letter[3], key_letter[4], key_letter[5]+other_letter[5]]
    #                    key_gen.append(key_completion)
                      

    #            elif re.search("^구$", key_letter[5]):
    #                if re.search("^조$", other_letter[5]) and 0< (other_letter[0][0] - key_letter[0][0]) < 150 and abs(key_letter[0][1]-other_letter[0][1]) < 10:                            
    #                    key_completion = [key_letter[0], other_letter[1], other_letter[2], key_letter[3], key_letter[4], key_letter[5]+other_letter[5]]
    #                    key_gen.append(key_completion)
                 

    #            elif re.search("^면$", key_letter[5]):
    #                if re.search("^적.{1,5}?$", other_letter[5]) and 0< (other_letter[0][0] - key_letter[0][0]) < 150 and abs(key_letter[0][1]-other_letter[0][1]) < 10:                            
    #                    key_completion = [key_letter[0], other_letter[1], other_letter[2], key_letter[3], key_letter[4], "면적(m)"]
    #                    key_gen.append(key_completion)
                  

    #            elif re.search("^지$", key_letter[5]):
    #                if re.search("^목$", other_letter[5]) and 0< (other_letter[0][0] - key_letter[0][0]) < 150 and abs(key_letter[0][1]-other_letter[0][1]) < 10:                            
    #                    key_completion = [key_letter[0], other_letter[1], other_letter[2], key_letter[3], key_letter[4], key_letter[5]+other_letter[5]]
    #                    key_gen.append(key_completion)
                     

    #for kgen in key_gen: ### 합일된 키 리스트에 넣어주기 ### 이제 노키레터에는 부스러기와 합일이 공존
    #    table_area.append(kgen)


    #table_area.sort(key=lambda t: t[0][1])    

    ### 아래위 덜 붙은 (m2) 같은 것들 붙여주기 >> 일단 사용보류. 밸류도 붙게 되고, 대지권 같은 경우는 그냥 "대지권?"으로 처리하려 함
    ##table_area = key_merge_raw_virtical(table_area)
                
    #box_mode_sp_lines = [] # 수평으로 존재하는 라인을 먼저 잡는 이유는 표의 정확한 아래 위 경계를 정하기 위함이다

    #for new_mem in table_area:
    #    found_line = False
    #    for sp_line in box_mode_sp_lines:
    #        for mem in sp_line:
    #            if abs(midpoint(mem)[1] - midpoint(new_mem)[1]) <= 30: # 중점은 10, 아래위로 40이하 
    #                sp_line.append(new_mem) 
    #                found_line = True
    #                break                           

    #            elif found_line:
    #                break

    #    if not found_line:
    #        box_mode_sp_lines.append([new_mem])

    #for esp in box_mode_sp_lines:
    #    esp.sort(key=lambda t: t[0][0]) 

    ##print("수정전__박스모드_ 수평라인들", "\n", box_mode_sp_lines, "\n") ##수평라인완성 >> 이를 통해 outliner를 식별


    ### 박스모드 수평라인에서 표자체의 상한값, 하한값을 얻기

    #range_y = []

    #if len(box_mode_sp_lines):
    #    for sp_line in box_mode_sp_lines: ## sp_line = [ [ 합계], [ 숫자], [숫자]]
            
    #        if len(sp_line) > 1: # 하나 이상의 멤버가 있는 라인의
    #            range_y.append(sp_line[0][0][1]) # y 요소를 상기 리스트에 넣기
    #else:
    #    pass

    #if len(range_y):
    #    box_mode_table_top = min(range_y)-40
    #    box_mode_table_bottom = max(range_y)+40

    #else:
    #    box_mode_table_top = 0
    #    box_mode_table_bottom = 2000 
    ################################################################################################

            

    ######## 2-1. 박스모드 table_area에서 수직라인도  지정 ########################################

    #table_area.sort(key=lambda t: t[0][0])            

    #box_mode_sj_lines = []

    #for sj_new_mem in table_area:
    #    if box_mode_table_top <= sj_new_mem[0][1] <= box_mode_table_bottom:
    #        found_line = False                    

    #        for j_line in box_mode_sj_lines:
    #            for sj_mem in j_line:                              

    #                    if abs(midpoint(sj_mem)[0] - midpoint(sj_new_mem)[0]) <= 30: # 중점은 10, 아래위로 40이하 
    #                        j_line.append(sj_new_mem)

    #                        found_line = True
    #                        break
      
    #                    elif found_line:
    #                        break

    #        if not found_line:
    #            box_mode_sj_lines.append([sj_new_mem])

    #for esj in box_mode_sj_lines:
    #    esj.sort(key=lambda t: t[0][0])        

    ##print("수정전 박스모드 수직라인들", "\n", box_mode_sj_lines, "\n")
    ################################################################################################

    #### 수평 수직라인에서 그룹에 속하지 못한 outliner 검출 #### >> 수평, 수직라인 라인에 끼지 못한 것들 검출

    #box_mode_outliners = []

    #for sp, p_line in enumerate(box_mode_sp_lines):
    #    if len(p_line) == 1 and box_mode_table_top <= p_line[0][0][1] <= box_mode_table_bottom:
    #        box_mode_outliners.append(p_line)

    #for sj, j_line in enumerate(box_mode_sj_lines):
    #    if len(j_line) == 1:
    #        box_mode_outliners.append(j_line)

    #no2_box_mode_outliners = []
    #for no in box_mode_outliners:
    #    if no not in no2_box_mode_outliners:
    #        no2_box_mode_outliners.append(no)

    ##print("\t@@", "no2_outliners", no2_box_mode_outliners, "\n")

    #######################################################################################


    ###### 출력하기 ############################                             

    #bm_sp_count = 0
    #for bm_sp_line in box_mode_sp_lines:
    #    if len(bm_sp_line) > 1:
    #        bm_sp_line.sort(key=lambda t: t[0][0])
    #        print("박스모드 수평라인", "\n", bm_sp_line, "\n")

    #        for i, bsp in enumerate(bm_sp_line):
    #            if re.search("건물명?", bm_sp_line[i][5]):
    #                for other_bsp in bm_sp_line[i+1:]:
    #                    if re.search("\w{2,}", other_bsp[5]):
    #                        #base_dict["건물명"] += [other_bsp[5]]
    #                        print("여기 다 모을 수 있나요", general_attr)




    #    elif len(bm_sp_line) == 1:
    #        bm_sp_count += 1
    ##print("박스모드 수평의 데브리스 갯수:", bm_sp_count)

 
    #bm_sj_count = 0
    #for bm_sj_line in box_mode_sj_lines:
    #    if len(bm_sj_line) > 1:
    #        bm_sj_line.sort(key=lambda t: t[0][1])
    #        print("박스모드 수직라인", "\n", bm_sj_line, "\n")

    #    elif len(bm_sj_line) == 1:
    #        bm_sj_count += 1
    ##print("박스모드 수직의 데브리스 갯수:", bm_sj_count)
    ###########################################################################


    ##### 딕셔너리에 넣기 ####
    #### 일단 수평항목에 존재할 확률이 높은 소재지, 건물명, 사용승인일, 구조, 용도를 찾아 넣기 ####

    
    
    
    
    #### 어떤 표이든 일단, 기호나 일련번호 아래로 몇개의 항목이 존재하며, 그 해당 y_level의 리스트를 모은다##





    #item_levels = []
    #for bsj in bm_sj_line:
    #    if re.search("기호|번호", bsj[5]):
    #        item_levels.append(midpoint(bsj)[1])

  



    ##### 주요 키 찾아 수평, 수직 구역 정해주고, 해당 영역에 원하는 형태의 밸류가 존재하면 바로 출력하기 ###
    
    #for can_key in table_area:
    #    for can_val in table_area:
    #        if abs(midpoint(can_key)[1]- midpoint(can_val)[1]) < 30 or abs(midpoint(can_key)[0]- midpoint(can_val)[0]) < 30:

    #            if re.search("기호|번호", can_key[5]):                
    #                if re.search("\d{1,3}$", can_val[5]):
    #                    base_dict["기호"] = can_val[5]

    #            elif re.search("소\s?재\s?지|주\s?소", can_key[5]):                
    #                if re.search("\w{1,5}도$", can_val[5]):
    #                    base_dict["도"] = can_val[5]

    #                elif re.search("\w{1,5}시$", can_val[5]):
    #                    base_dict["시"] = can_val[5]

    #                elif re.search("\w{1,5}[군구]$", can_val[5]):
    #                    base_dict["군구"] = can_val[5]

    #                elif re.search("^[가-힣]+\d{1,2}[동]$|^[가-힣]{,4}동$", can_val[5]):
    #                    base_dict["동"] = can_val[5]

    #                elif re.search("\w{1,8}[길로]$", can_val[5]):
    #                    base_dict["도로명"] = can_val[5]

    #            elif re.search("사용승인일", can_key[5]):                
    #                if re.search("[20]\d{2}[.,]\s?\d{1,2}[.,]\s?\d{1,2}[.,]?", can_val[5]):
    #                    base_dict["사용승인일"] = can_val[5]

    #            elif re.search("건물\s?명칭?", can_key[5]):                
    #                if re.search("\w+", can_val[5]):
    #                    base_dict["건물명"] = can_val[5]

    #            elif re.search("구조", can_key[5]):                
    #                if re.search("철근|콘크|지붕", can_val[5]):
    #                    base_dict["구조"] = can_val[5]

    #            elif re.search("^동$", can_key[5]):                
    #                if re.search("\d{1,3}", can_val[5]):
    #                    base_dict["동"] = can_val[5]

    #            elif re.search("층", can_key[5]):                
    #                if re.search("\d{1,3}", can_val[5]):
    #                    base_dict["층"] = can_val[5]

    #            elif re.search("호", can_key[5]):                
    #                if re.search("\d{1,3}", can_val[5]):
    #                    base_dict["호"] = can_val[5]

    #print("베이스 딕셔너리도 참고", base_dict, "\n")



