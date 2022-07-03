from treat_body import *

def treat_base_table(idir, image_full_path, new_coord_box, new_coord_line, up_limit, down_limit):


    body_general_attr = {}
        
    body_errors = []
    build_name = []


    print("이제 body_base_table로 분석합니다", "\n")

    table_area_box = [] # 테이블 주변부까지 어느정도 포함됨
    for ta in new_coord_box:
        if up_limit < int(ta[0][1]) < down_limit:
            if len(ta[5]) < 40: # 테이블 멤버의 글자수 제한
                table_area_box.append(ta)

    #print("테이블 영역_박스", table_area_box, "\n")
    print("\n")
    #for tab in table_area_box:
        #print("테이블 영역_박스", tab)
        

    table_area_line = [] # 테이블 주변부까지 어느정도 포함됨
    for ta in new_coord_line:
        if up_limit < int(ta[0][1]) < down_limit:
            if len(ta[5]) < 40: # 테이블 멤버의 글자수 제한
                table_area_line.append(ta)
    #print("테이블 영역_라인", table_area_line, "\n")
    print("\n")
    #for tal in table_area_line:
        #print("테이블 영역_라인", tal)




    #key_merged_table_area = key_merge_raw_virtical(table_area)
    #print("머징된 테이블 영역", key_merged_table_area)



    ######### 박스모드 키항목 정돈 - start ################

    key_letters = [] 
    
    for letter in table_area_box:

        if re.search("^[소재지]+", letter[5]):
            if up_limit < letter[0][1] < down_limit - 200:
                key_letters.append(letter)
                
        elif re.search("[건물명칭]+", letter[5]):
            if up_limit < letter[0][1] < down_limit - 200:
                key_letters.append(letter)

        elif re.search("[주용도]+", letter[5]):
            if up_limit < letter[0][1] < down_limit:
                key_letters.append(letter)

        elif re.search("^[사용승인일]+", letter[5]):
            if up_limit < letter[0][1] < down_limit:
                key_letters.append(letter)

        elif re.search("^[전유공용계약대지권면적]+", letter[5]):
            if up_limit < letter[0][1] < down_limit:
                key_letters.append(letter)

    #print("박스모드로 수집", key_letters, "\n")


    NKL = []
    for ek in key_letters:
        nek = [ek[0], ek[1], ek[2], ek[3], ek[4], ek[5].replace(" ", "")]
        NKL.append(nek)

    #print("박스모드로 수집 후 가공", NKL, "\n")

    key_body_base = {}  # 박스모드에서의 1차 모집
    kbb_list = ["addr", "buildname", "builduse", "authordate", "privatearea", "publicarea", "contractarea", "landrightarea"]

    for nk in NKL:
        if re.search(".*소\s?재\s?지.*", nk[5]):
            key_body_base["addr"] = nk
            print("\n", "키목록 체크-1ㅠㅠ", key_body_base, "\n")
        elif re.search("건물명.*", nk[5]):
            key_body_base["buildname"] = nk

        elif re.search("[주]?용도$", nk[5]):
            key_body_base["builduse"] = nk

        elif re.search("사용승인", nk[5]):
            key_body_base["authordate"] = nk

        elif re.search("^전[용유]$|전[용유]면적$|전[용유]면적[^\s가-힣]", nk[5]):
            key_body_base["privatearea"] = nk

        elif re.search("^공[용유]$|공[용유]면적$|공[용유]면적[^\s가-힣]", nk[5]):
            key_body_base["publicarea"] = nk

        elif re.search("^계약면.*", nk[5]):
            key_body_base["contractarea"] = nk

        elif re.search("^대지권$|^대지권.*", nk[5]):
            key_body_base["landrightarea"] = nk

           
    #print("박스에서 수집된 A형평가서의 키박스::", key_body_base, "\n")


    unmet_keys = []
    for kbb in kbb_list:
        if not kbb in key_body_base.keys():
            unmet_keys.append(kbb)

    #print("박스모드 작업으로 채워지지 않은 키박스::", unmet_keys, "\n")



    ############ 이제 라인모드로 키처리 ###################


    ## A 양식의 키단어 모집을 위한 필터

    K = []

    for letter in new_coord_line:  # 키인식은 라인모드로 
        if re.search("^[소재지]+", letter[5]):
            if up_limit < letter[0][1] < down_limit - 200:
                K.append(letter)
                
        elif re.search("^[건물명칭]+", letter[5]):
            if up_limit < letter[0][1] < down_limit - 200:
                K.append(letter)

        elif re.search("[주용도]+", letter[5]):
            if up_limit < letter[0][1] < down_limit:
                key_letters.append(letter)

        elif re.search("^[사용승인일]+", letter[5]):
            if up_limit < letter[0][1] < down_limit:
                K.append(letter)

        elif re.search("^[전유공용계약대지권면적]+", letter[5]):
            if up_limit < letter[0][1] < down_limit:
                K.append(letter)

                
    #print("라인모드로 A 형의 키를 모집 ", K, "\n")

    #print("\n", "키목록 체크-1", key_body_base, "\n")
    ## 박스모드에서도 일단 완전한 단어부터 골라야 하겠지??

    del_1= []
    for uk in unmet_keys:
        for nk in NKL:

            if uk == 'addr':
                if re.search(".*소\s?재\s?지.*", nk[5]):
                    key_body_base["addr"] = nk
                    del_1.append(nk)
            elif uk == 'buildname':                    
                if re.search("건물명.*|명\s?칭", nk[5]):
                    key_body_base["buildname"] = nk
                    del_1.append(nk)

            elif uk == 'buildname': 
                if re.search("[주]용도$", nk[5]):
                    key_body_base["builduse"] = nk
                    del_1.append(nk)


            elif uk == 'authordate':
                if re.search("사용승인", nk[5]):
                    key_body_base["authordate"] = nk
                    del_1.append(nk)
            elif uk == 'privatearea':
                if re.search("^전[용유]$|전[용유]면적$|전[용유]면적[^\s가-힣]", nk[5]): #전용률 이라는 단어가 혼선
                    key_body_base["privatearea"] = nk
                    del_1.append(nk)
            elif uk == 'publicarea':
                if re.search("^공[용유]$|공[용유]면적$|공[용유]면적[^\s가-힣]", nk[5]):
                    key_body_base["publicarea"] = nk
                    del_1.append(nk)
            elif uk == 'contractarea':
                if re.search("^계약면.*", nk[5]):
                    key_body_base["contractarea"] = nk
                    del_1.append(nk)
            elif uk == 'landrightarea':
                if re.search("^대지권$|^대지권.*", nk[5]):
                    key_body_base["landrightarea"] = nk
                    del_1.append(nk)


    K_1=[]
    for kk in NKL:
        if kk not in del_1:
            K_1.append(kk)

                   
           
    #print("박스모드에서 수집된 A형평가서의 키박스::", key_body_base, "\n")


    unmet_keys_box = []
    for kbb in kbb_list:
        if not kbb in key_body_base.keys():
            unmet_keys_box.append(kbb)

    #print("박스모드 작업으로 채워지지 않은 키박스::", unmet_keys_box, "\n")

    #print("작업벤치:K_1:", K_1, "\n")
    #print("\n", "키목록 체크00", key_body_base, "\n")
    ####################################################################################################
    ## 온전한 단어는 다 살펴보았고, 이제는 낱글자들과 부서진 여러글자들을 모아 키를 조립해야함 ###

    ### 1. 소재지 / 건물명 / 사용승인일의 낱글자 처리 == 3단계 조립
    del_from_K_1= []
    add_to_K_1 = []

                
    for ukb in unmet_keys_box:
        for bs1 in K_1:                    
            for bs2 in K_1:
                for bs3 in K_1:
                    if ukb == 'addr':                                    
                               
                        if re.search("^소$", bs1[5]):
                            if re.search("^재$", bs2[5]):
                                diff1 = bs2[0][0] - bs1[0][0]
                                if re.search("^지$", bs3[5]): ## 소 재 지 간의 간격이 균등함을 이용해 다른 '지'자 배제 
    
                                    diff2 = (bs3[0][0] - bs2[0][0])
                                    if abs(diff1-diff2) < 15:
                                        addr = raw_x3_merge(bs1, bs2, bs3) 
                                            
                                        key_body_base["addr"] = addr  ## 소재지가 완성된 경우,
                                        del_from_K_1.append(bs1)
                                        del_from_K_1.append(bs2)
                                        del_from_K_1.append(bs3)

                    elif ukb == 'buildname':
                          
                        if re.search("^건$", bs1[5]): 
                            if re.search("^물$", bs2[5]):     
                                if re.search("^명$", bs3[5]):
                                   
                                    d1 = midpoint(bs1)[0] - midpoint(bs2)[0]
                                    d2 = midpoint(bs2)[0] - midpoint(bs3)[0]

                                    if abs(d1 - d2) < 10 and abs(midpoint(bs1)[1]-midpoint(bs2)[1]) < 10 and abs(midpoint(bs2)[1] - midpoint(bs3)[1])< 10:
                                            
                                        use = raw_x3_merge(bs3, bs2, bs1) 
                                        add_to_K_1.append(use)
                                        del_from_K_1.append(bs1)
                                        del_from_K_1.append(bs2)
                                        del_from_K_1.append(bs3)                  
                                           

                    elif ukb == 'authordate':
                          
                        if re.search("^사$", bs1[5]): 
                            if re.search("^승$", bs2[5]): 
                                if re.search("^일$", bs3[5]):
                                   
                                    d1 = midpoint(bs1)[0] - midpoint(bs2)[0]
                                    d2 = midpoint(bs2)[0] - midpoint(bs3)[0]

                                    if abs(d1 - d2) < 10 and abs(midpoint(bs1)[1]-midpoint(bs2)[1]) < 10 and abs(midpoint(bs2)[1] - midpoint(bs3)[1])< 10:
                                            
                                        use = raw_x3_merge(bs3, bs2, bs1) 
                                        add_to_K_1.append(use)
                                        del_from_K_1.append(bs1)
                                        del_from_K_1.append(bs2)
                                        del_from_K_1.append(bs3)    



    for ek in add_to_K_1:
        if ek not in K_1:
            K_1.append(ek)

    #print("지울거", del_from_K_1)                            
    K_2 = []
    for singj in K_1:
        if singj not in del_from_K_1: ## 단어생성이 끝난 "소, 재, 지", 건, 물, 명, 사, 승, 일 제거
            K_2.append(singj)
                                                                        
    #print("K_2",K_2, "\n")
    

    for ukb2 in unmet_keys_box:
                    
        for nm1 in K_2:
            for nm2 in K_2:
                for nm3 in K_2:

                    if ukb2 == 'addr':
                        if re.search("^소$", nm1[5]):
                            if re.search("^재지$", nm2[5]):  
                                if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                    key_body_base["addr"] = raw_x_merge(nm1, nm2)

                        elif re.search("^소재$", nm1[5]):                                        
                            if re.search("^지$", nm2[5]):                                           
                                if abs((nm2[0][0]-nm1[1][0]) - abs((nm1[1][0] - nm1[0][0]) - (nm2[1][0]-nm2[0][0])*2)) < 10 and abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                    key_body_base["addr"] = raw_x_merge(nm1, nm2)   
                                        

                    elif ukb2 == 'buildname':
                        if re.search("^건물$", nm1[5]):
                            if re.search("^명$", nm2[5]):                                    
                                if abs((nm2[0][0]-nm1[1][0]) - abs((nm1[1][0] - nm1[0][0]) - (nm2[1][0]-nm2[0][0])*2)) < 10 and abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                    key_body_base["buildname"] = raw_x_merge(nm1, nm2)


                        elif re.search("^건$", nm1[5]):
                            if re.search("^물명$", nm2[5]):                                    
                                if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                    key_body_base["buildname"] = raw_x_merge(nm1, nm2)


                        elif re.search("^명$", nm1[5]):
                            if re.search("^칭$", nm2[5]):                                    
                                if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                    key_body_base["buildname"] = raw_x_merge(nm1, nm2)

                    elif ukb2 == 'builduse':
                        if re.search("^용$", nm1[5]):                                        
                            if re.search("^도$", nm2[5]):                                            
                                if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                    key_body_base["builduse"] = raw_x_merge(nm1, nm2)  

                        elif re.search("^주용$", nm1[5]):                                        
                            if re.search("^도$", nm2[5]):                                            
                                if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                    key_body_base["builduse"] = raw_x_merge(nm1, nm2)  


                    elif ukb2 == 'privatearea':
                        if re.search("^전유$", nm1[5]):                                        
                            if re.search("^면적", nm2[5]):                                            
                                if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                    key_body_base["privatearea"] = raw_x_merge(nm1, nm2)  

                                elif abs(midpoint(nm1)[0] - midpoint(nm2)[0]) < 10:
                                    key_body_base["privatearea"] = raw_y_merge(nm1, nm2)  


                    elif ukb2 == 'publicarea':
                        if re.search("^공용$", nm1[5]):                                        
                            if re.search("^면적", nm2[5]):                                            
                                if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                    key_body_base["publicarea"] = raw_x_merge(nm1, nm2)  

                                elif abs(midpoint(nm1)[0] - midpoint(nm2)[0]) < 10:
                                    key_body_base["publicarea"] = raw_y_merge(nm1, nm2)  


                    elif ukb2 == 'contractarea':
                        if re.search("^계약$", nm1[5]):                                        
                            if re.search("^면적", nm2[5]):                                            
                                if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                    key_body_base["contractarea"] = raw_x_merge(nm1, nm2)  

                                elif abs(midpoint(nm1)[0] - midpoint(nm2)[0]) < 10:
                                    key_body_base["contractarea"] = raw_y_merge(nm1, nm2)  

                    elif ukb2 == 'landrightarea':
                        if re.search("^대지권$", nm1[5]):                                        
                            if re.search("^면적", nm2[5]):                                            
                                if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                    key_body_base["landrightarea"] = raw_x_merge(nm1, nm2)  

                                elif abs(midpoint(nm1)[0] - midpoint(nm2)[0]) < 10:
                                    key_body_base["landrightarea"] = raw_y_merge(nm1, nm2)  



    unmet_keys_box_2 = []
    for kb in kbb_list:
        if not kb in key_body_base.keys():
            unmet_keys_box_2.append(kb)


    #print("미완성 키 박스 :", unmet_keys_box_2, "\n")

    #print("\n", "키목록 체크", key_body_base, "\n")


    #addr_Y = (key_body_base["addr"][1][1] + key_body_base["addr"][2][1])/2

    ### 항목별 격벽의 좌표를 정해둠 ####     
    print("\n", " "*20, ":"*10, "인식된 키박스(본문)", ":"*10, "\n")          
    for key in key_body_base:

        if key == "addr":
            addr_L = key_body_base["addr"][0][0]
            addr_R = key_body_base["addr"][1][0]
            addr_Y = (key_body_base["addr"][1][1] + key_body_base["addr"][2][1])/2
            print(" "*30, addr_L, key_body_base["addr"][5], addr_R)  

        elif key == "buildname":
            buildname_L = key_body_base["buildname"][0][0]
            buildname_R = key_body_base["buildname"][1][0]
            buildname_Y = (key_body_base["buildname"][1][1] + key_body_base["buildname"][2][1])/2
            print(" "*30, buildname_L, key_body_base["buildname"][5], buildname_R)  

        elif key == "builduse":
            builduse_L = key_body_base["builduse"][0][0]
            builduse_R = key_body_base["builduse"][1][0]
            builduse_Y = (key_body_base["builduse"][1][1] + key_body_base["builduse"][2][1])/2
            print(" "*30, builduse_L, key_body_base["builduse"][5], builduse_R)  


        elif key == "authordate":
            authordate_L = key_body_base["authordate"][0][0]
            authordate_R = key_body_base["authordate"][1][0]
            authordate_Y = (key_body_base["authordate"][1][1] + key_body_base["authordate"][2][1])/2
            print(" "*30, authordate_L, key_body_base["authordate"][5], authordate_R, "Y:", authordate_Y)   

        elif key == "privatearea":
            privatearea_L = key_body_base["privatearea"][0][0]
            privatearea_R = key_body_base["privatearea"][1][0]
            privatearea_Y = (key_body_base["privatearea"][1][1] + key_body_base["privatearea"][2][1])/2
            print(" "*30, privatearea_L, key_body_base["privatearea"][5], privatearea_R)  

        elif key == "publicarea":
            publicarea_L = key_body_base["publicarea"][0][0]
            publicarea_R = key_body_base["publicarea"][1][0]
            publicarea_Y = (key_body_base["publicarea"][1][1] + key_body_base["publicarea"][2][1])/2
            print(" "*30, publicarea_L, key_body_base["publicarea"][5], publicarea_R)  

        elif key == "contractarea":
            contractarea_L = key_body_base["contractarea"][0][0]
            contractarea_R = key_body_base["contractarea"][1][0]
            contractarea_Y = (key_body_base["contractarea"][1][1] + key_body_base["contractarea"][2][1])/2
            print(" "*30, contractarea_L, key_body_base["contractarea"][5], contractarea_R)   


        elif key =="landrightarea":
            landrightarea_L = key_body_base["landrightarea"][0][0]
            landrightarea_R = key_body_base["landrightarea"][1][0]
            landrightarea_Y = (key_body_base["landrightarea"][1][1] + key_body_base["landrightarea"][2][1])/2
            print(" "*30, landrightarea_L, key_body_base["landrightarea"][5], landrightarea_R)  
    print("\n", " "*20, ":"*30, "\n")
    #print("\n", "키목록 체크", key_body_base, "\n")


    #print("테이블 영역 텍스트 라인::",table_area_line) 
    for vg in  table_area_line:
        if "addr" in key_body_base:     
            if re.search("([가-힣]+\d*[시군구])|[가-힣]동|([가-힣]+[길로])\s?(\d+)", vg[5]): #
                if  abs(addr_Y - midpoint(vg)[1]) < 50 or 0 <= (midpoint(vg)[0] - (addr_L+addr_R)/2) < 50:## 가로세로방향 정렬시
                    body_general_attr["소재지"] = "{}".format(vg[5])
                         
                
                    if "소재지" not in body_general_attr:
                        body_general_attr["소재지"] = "{}".format(vg[5])

        if "buildname" in key_body_base:
            if re.search("\d+[동층호]", vg[5]):
                if  abs(buildname_Y - midpoint(vg)[1]) < 50 and buildname_R + 100 < midpoint(vg)[0]: 
                    build_name.append(vg)
                
                    print("건물명 check_point_1", vg)
                    build_name.append(vg)               
                    #if "건물명" not in body_general_attr:

        #elif re.search("([가-힣]+[길로])\s?(\d+)", vg[5]):
        #    if "도로명주소" not in body_general_attr:
        #        body_general_attr["도로명주소"]= "{}".format(vg[5])  # 도로명 주소상 지번이므로 구분함


        if "builduse" in key_body_base:
            if re.search("도시형|^아파트$|^다세대|주택|공동|근린", vg[5]):
            
                      
                if (builduse_Y - midpoint(vg)[1]) < 20:  
                    body_general_attr["용도"] = "{}".format(vg[5])

        elif re.search("(19|20)(\d{2})[.,년]\s?\d{1,2}?[.,월]?", vg[5]): # 구버전 (19|20)\d{2}[.,]\s?\d{1,2}[.,]\s?\d{1,2}[.,]?
            if "authordate" in key_body_base:                
                if abs(authordate_Y - midpoint(vg)[1]) < 20:  
                    body_general_attr["사용승인일"] = "{}".format(vg[5])
                elif authordate_L < midpoint(vg)[0] < authordate_R and 20 < abs(authordate_Y - midpoint(vg)[1]) < 300:
                    body_general_attr["사용승인일"] = "{}".format(vg[5])


        elif re.search("^(\d{1,3}\,)*\d{1,3}.?\d+[-]?", vg[5]):
            
            if "privatearea" in key_body_base:
                if privatearea_L < midpoint(vg)[0] < privatearea_R and 0 < (midpoint(vg)[1] - privatearea_Y) < 200:                 
                    body_general_attr["전유면적"] = "{}".format(vg[5])

            if "publicarea" in key_body_base:
                if publicarea_L < midpoint(vg)[0] < publicarea_R and 0 < (midpoint(vg)[1] - publicarea_Y) < 200:
                    body_general_attr["공용면적"] = "{}".format(vg[5])

            if "landrightarea" in key_body_base:
                if landrightarea_L < midpoint(vg)[0] < landrightarea_R and 0 < (midpoint(vg)[1] - landrightarea_Y) < 200:
                    body_general_attr["대지권면적"] = "{}".format(vg[5])

            if "contractarea" in key_body_base:
                if contractarea_L < midpoint(vg)[0] < contractarea_R and 0 < (midpoint(vg)[1] - contractarea_Y) < 200:
                    body_general_attr["계약면적"] = "{}".format(vg[5])


        #elif re.search(".+", vg[5]): #[가-힣]+(아파트|빌라)|([가-힣]+)\s?(.+[층동])\s?(\w+[층동호])\s?(\w+[호])?|[가-힣]+ #[^사용승인일]
        #    if abs(buildname_Y - midpoint(vg)[1]) < 50 and buildname_R + 100 < midpoint(vg)[0]: 
        #        print("건물명 check_point_2", vg)
        #        build_name.append(vg)             

                        
                    ### 참고 table_title = re.search("(?<=[\.\)\,-]).{2,25}", up[2]).group(0)
            
    ## 건물명이 여러줄이거나 옆으로 긴 경우가 있어 모아서 따로 처리해준다 ##
    new_build_name = []
    build_name.sort(key=lambda t: t[0][1])
    for bnm in build_name:
        if bnm[5] not in new_build_name:
            print("건물명 중복체크", bnm)
            new_build_name.append(bnm[5])



            
    # 수집된 각 항목의 리스트를 for 문 종료시 딕셔너리에 부가한다.
    

    if len(new_build_name) > 0:
        body_general_attr["건물명"] = ' '.join(new_build_name)
    if len(body_general_attr) > 1:
        body_general_attr["평가서 ID"] = idir

    #print("\n", "본문_일반항목", body_general_attr, "\n")


    return body_general_attr
