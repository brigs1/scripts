from coord import *
import re, os, base


def spec_table_A(idir, image_file, image_full_path, new_coord_line, new_coord_box, order):
    target_js = r"D:/results/var_2/forDL/jsons/"
    
    print("\n", " "*20, "::: 감정평가명세표 A형 제 {}페이지 분석시작 :::".format(order), "\n\n")

      
   
    land_attr = {}     
    building_attr = {}
    
    B_list = []
    L_list = []
    spec_general_data = []

    spec_A_errors = []
    for_json_sta = {}

    #try:
    KL = []
    for letter in new_coord_line:  
        if re.search("일련|[기번호]", letter[5]):  ## "^[일련번기호]{1,4}$"
            if 300 < letter[0][1] < 600:   ## 양식A군은600내에 존재, B군은 700으로 내려옴
                KL.append(letter) 

        elif re.search("^[소재지]{1,3}$", letter[5]):
            if 300 < letter[0][1] < 600:
                KL.append(letter)

        elif re.search("^[지번]{1,2}$", letter[5]):
            if 300 < letter[0][1] < 600:
                KL.append(letter)

        elif re.search("[지목]{1,2}$|^[지목].{1,5}$", letter[5]): #지목?용도와 같은 변이까지 커버
            if 300 < letter[0][1] < 600:
                KL.append(letter)

        elif re.search("^[용도지역구조]{1,4}$", letter[5]):
            if 300 < letter[0][1] < 600:
                KL.append(letter)

        elif re.search("^[공부]{1,2}$", letter[5]):
            if 300 < letter[0][1] < 600:
                KL.append(letter)

        elif re.search("^[사정]{1,2}$", letter[5]):
            if 300 < letter[0][1] < 600:
                KL.append(letter)

        elif re.search("^[감정평단가격금액원\(\)]{1,8}", letter[5]): #감정평가액(원)
            if 300 < letter[0][1] < 600:
                KL.append(letter)
                        
        elif re.search("^[비고]{1,2}$", letter[5]):
            if 300 < letter[0][1] < 600:
                KL.append(letter)

    NKL = []
    for ek in KL:
        nek = [ek[0], ek[1], ek[2], ek[3], ek[4], ek[5].replace(" ", "")]
        NKL.append(nek)

    #print("A 형의 키모집을 위한 라인모드", NKL, "\n")

    key_blocks_A = {}  # 라인모드에서의 1차 모집
    kb_list = ["num", "addr", "addrnum", "landclass", "builduse", "buildstr", "areause", "paper", "estim", "price", "memo"]

    for nk in NKL:
        if re.search("^[기번]호$", nk[5]):
            key_blocks_A["num"] = nk

        elif re.search("^소재지$", nk[5]):
            key_blocks_A["addr"] = nk

        elif re.search("^지번$", nk[5]):
            key_blocks_A["addrnum"] = nk

        elif re.search("^(지목|용도).*(지목|용도)$|^지목$", nk[5]):
            key_blocks_A["landclass"] = nk

        elif re.search("^(지목|용도).*(지목|용도)$|^용도$", nk[5]):
            key_blocks_A["builduse"] = nk

        elif re.search("^(용도지역|구조).*(용도지역|구조)$|^용도지역$|^구조$", nk[5]):
            key_blocks_A["buildstr"] = nk

        elif re.search("^(용도지역|구조).*(용도지역|구조)$|^용도지역$|^구조$", nk[5]):
            key_blocks_A["areause"] = nk

        elif re.search("^공부$", nk[5]):
            key_blocks_A["paper"] = nk

        elif re.search("^사정$", nk[5]):
            key_blocks_A["estim"] = nk

        elif re.search("^^감정평가액$|^감정평가액(원)$|^평가금액$|^평가가격$", nk[5]):
            key_blocks_A["price"] = nk

        elif re.search("^비고$", nk[5]):
            key_blocks_A["memo"] = nk
           
    #print("라인에서 수집된 A형평가서의 키박스::", key_blocks_A, "\n")


    unmet_keys = []
    for kb in kb_list:
        if not kb in key_blocks_A.keys():
            unmet_keys.append(kb)

    #print("라인모드 작업으로 채워지지 않은 키박스::", unmet_keys, "\n")


    ############ 이제 박스모드로 키처리 ###################


    ## A 양식의 키단어 모집을 위한 필터

    K = []

    for letter in new_coord_box:  # 키인식은 박스모드로 
        if re.search("일련|[기번호]", letter[5]):  ## "^[일련번기호]{1,4}$"
            if 300 < letter[0][1] < 600:   ## 양식A군은600내에 존재, B군은 700으로 내려옴
                K.append(letter) 

        elif re.search("^[소재지]{1,3}$", letter[5]):
            if 300 < letter[0][1] < 600:
                K.append(letter)

        elif re.search("^[지번]{1,2}$", letter[5]):
            if 300 < letter[0][1] < 600:
                K.append(letter)

        elif re.search("[지목]{1,2}$|^[지목].{1,5}$", letter[5]): #지목?용도와 같은 변이까지 커버
            if 300 < letter[0][1] < 600:
                K.append(letter)

        elif re.search("^[용도지역구조]{1,4}$", letter[5]):
            if 300 < letter[0][1] < 600:
                K.append(letter)

        elif re.search("^[공부]{1,2}$", letter[5]):
            if 300 < letter[0][1] < 600:
                K.append(letter)

        elif re.search("^[사정]{1,2}$", letter[5]):
            if 300 < letter[0][1] < 600:
                K.append(letter)

        elif re.search("^[감정평단가격금액원\(\)]{1,8}", letter[5]): #감정평가액(원)
            if 300 < letter[0][1] < 600:
                K.append(letter)
                        
        elif re.search("^[비고]{1,2}$", letter[5]):
            if 300 < letter[0][1] < 600:
                K.append(letter)

                
    #print("박스모드로 A 형의 키를 모집 ", K, "\n")

    ## 박스모드에서도 일단 완전한 단어부터 골라야 하겠지??

    del_1= []
    for uk in unmet_keys:
        for nk in K:
            if uk == 'num':
                if re.search("^[기번]호$", nk[5]):
                    key_blocks_A["num"] = nk
                    del_1.append(nk)
            elif uk == 'addr':
                if re.search("^소재지$", nk[5]):
                    key_blocks_A["addr"] = nk
                    del_1.append(nk)
            elif uk == 'addrnum':                    
                if re.search("^지번$", nk[5]):
                    key_blocks_A["addrnum"] = nk
                    del_1.append(nk)
            elif uk == 'landclass':
                if re.search("^(지목|용도).*(지목|용도)$|^지목$", nk[5]):
                    key_blocks_A["landclass"] = nk
                    del_1.append(nk)
            elif uk == 'builduse':
                if re.search("^(지목|용도).*(지목|용도)$|^용도$", nk[5]):
                    key_blocks_A["builduse"] = nk
                    del_1.append(nk)
            elif uk == 'areause':
                if re.search("^(용도지역|구조).*(용도지역|구조)$|^용도지역$", nk[5]):
                    key_blocks_A["areause"] = nk
                    del_1.append(nk)
            elif uk == 'buildstr':
                if re.search("^(용도지역|구조).*(용도지역|구조)$|^구조$", nk[5]):
                    key_blocks_A["buildstr"] = nk
                    del_1.append(nk)
            elif uk == 'paper':
                if re.search("^공부$", nk[5]):
                    key_blocks_A["paper"] = nk
                    del_1.append(nk)
            elif uk == 'estim':
                if re.search("^사정$", nk[5]):
                    key_blocks_A["estim"] = nk
                    del_1.append(nk)
            elif uk == 'price':                
                if re.search("^감정평가액.{1,3}$|^감정평가액(원)$|^평가금액$|^평가가격$", nk[5]):
                    key_blocks_A["price"] = nk
                    del_1.append(nk)
            elif uk == 'memo':
                if re.search("^비고$", nk[5]):
                    key_blocks_A["memo"] = nk
                    del_1.append(nk)

    K_1=[]
    for kk in K:
        if kk not in del_1:
            K_1.append(kk)

                 
           
    #print("박스모드에서 수집된 A형평가서의 키박스::", key_blocks_A, "\n")


    unmet_keys_box = []
    for kb in kb_list:
        if not kb in key_blocks_A.keys():
            unmet_keys_box.append(kb)

    #print("박스모드 작업으로 채워지지 않은 키박스::", unmet_keys_box, "\n")

    #print("작업벤치:K_1:", K_1, "\n")

    ####################################################################################################
    ## 온전한 단어는 다 살펴보았고, 이제는 낱글자들과 부서진 여러글자들을 모아 키를 조립해야함 ###

               

    ### 1. 소재지 / 감정평가액의 낱글자 처리 == 3단계 조립
    del_from_K_1= []
    add_to_K_1 = []

                
    for ukb in unmet_keys_box:
        for bs1 in K_1:                    
            for bs2 in K_1:
                for bs3 in K_1:
                    if ukb == 'addr':                                    
                            ## 소재지와 '지번'이 붙는 경우가 많아 조립에 방해가 되므로, 낱글자로 이들부터 떼 내겠음 ##
                        if re.search("^소$", bs1[5]):
                            if re.search("^재$", bs2[5]):
                                diff1 = bs2[0][0] - bs1[0][0]
                                if re.search("^지$", bs3[5]): ## 소 재 지 간의 간격이 균등함을 이용해 다른 '지'자 배제 
    
                                    diff2 = (bs3[0][0] - bs2[0][0])
                                    if abs(diff1-diff2) < 15:
                                        addr = raw_x3_merge(bs1, bs2, bs3) 
                                            
                                        key_blocks_A["addr"] = addr  ## 소재지가 완성된 경우, 일찌감치 fin으로 보낸다.
                                        del_from_K_1.append(bs1)
                                        del_from_K_1.append(bs2)
                                        del_from_K_1.append(bs3)

                    elif ukb == 'builduse' or ukb == 'areause':
                        #print("## '용도지역'과 '용도'가 혼재하므로 미리 정리해줌 ", bs1)
                        
                        if re.search("^지$", bs1[5]): 
                            if re.search("^도$", bs2[5]): ## 용도지역 간의 간격이 균등함을 이용해 다른 '지'자 배제     
                                if re.search("^용$", bs3[5]):
                                   
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
        if singj not in del_from_K_1: ## 단어생성이 끝난 "소, 재, 지"를 제거
            K_2.append(singj)
                                                                        
    #print("K_2",K_2, "\n")


    for ukb2 in unmet_keys_box:
                    
        for nm1 in K_2:
            for nm2 in K_2:
                for nm3 in K_2:

                    if ukb2 == 'num':
                        if re.search("^[기번]", nm1[5]):
                            if re.search("호$", nm2[5]):
                                if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                    key_blocks_A["num"] = raw_x_merge(nm1, nm2)
                                elif abs(midpoint(nm1)[0] - midpoint(nm2)[0]) < 10:
                                    key_blocks_A["num"] = raw_y_merge(nm1, nm2)

                    elif ukb2 == 'addr':
                        if re.search("^소$", nm1[5]):
                            if re.search("^재지$", nm2[5]):  
                                if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                    key_blocks_A["addr"] = raw_x_merge(nm1, nm2)

                        elif re.search("^소재$", nm1[5]):                                        
                            if re.search("^지$", nm2[5]):                                           
                                if abs((nm2[0][0]-nm1[1][0]) - abs((nm1[1][0] - nm1[0][0]) - (nm2[1][0]-nm2[0][0])*2)) < 10 and abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                    key_blocks_A["addr"] = raw_x_merge(nm1, nm2)         

                    elif ukb2 == 'landclass':
                        if re.search("^목$", nm1[5]):
                            if re.search("^지$", nm3[5]):                                    
                                if abs(midpoint(nm1)[1] - midpoint(nm3)[1]) < 10 and 0 < (nm1[0][0] - nm3[0][0]):
                                    key_blocks_A["landclass"] = raw_x_merge(nm3, nm1)

                    elif ukb2 == 'areause':
                        if re.search("^용도지$", nm1[5]):                                        
                            if re.search("^역$", nm2[5]):                                            
                                if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                    key_blocks_A["areause"] = raw_x_merge(nm1, nm2)  
                        elif re.search("^도지역$", nm1[5]):
                            if re.search("^용$", nm2[5]):                                           
                                if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                    if abs((nm1[0][0] - nm2[1][0]) - ((nm1[1][0]-nm1[0][0])-(nm2[1][0]-nm2[0][0])*3)/2) < 10:
                                        key_blocks_A["areause"] = raw_x_merge(nm2, nm1)

                             
                    elif ukb2 == 'builduse':
                        if re.search("^용$", nm1[5]):                                       
                            if re.search("^도$", nm2[5]):                                         
                                if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                    key_blocks_A["builduse"] = raw_x_merge(nm1, nm2) 

                                        
                    elif ukb2 == 'buildstr':
                        if re.search("^구$", nm1[5]):
                            if re.search("^조$", nm2[5]):
                                if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                    key_blocks_A["buildstr"] = raw_x_merge(nm1, nm2) 
                                    

                    elif ukb2 == 'paper':
                        if re.search("^공$", nm1[5]):
                            if re.search("^부$", nm2[5]):
                                if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                    key_blocks_A["paper"] = raw_x_merge(nm1, nm2) 

                    elif ukb2 == 'estim':               
                        if re.search("^사$", nm1[5]):
                            if re.search("^정$", nm2[5]):
                                if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                    key_blocks_A["estim"] = raw_x_merge(nm1, nm2) 

                    elif ukb2 == 'price':                
                        if re.search("^감", nm1[5]):
                            if re.search("액$", nm2[5]):
                                if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                    key_blocks_A["price"] = raw_x_merge(nm1, nm2) 


                    elif ukb2 == 'memo':                
                        if re.search("^비$", nm1[5]):
                            if re.search("^고$", nm2[5]):
                                if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                    key_blocks_A["memo"] = raw_x_merge(nm1, nm2) 
                                                
                    elif ukb2 == 'addrnum' or ukb == 'landclass':   
                        if re.search("^지$", nm1[5]):
                            if re.search("^번$", nm2[5]):
                                if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                    if 0 < (nm2[0][0] - nm1[0][0]):
                                        key_blocks_A["addrnum"] = raw_x_merge(nm1, nm2) 
                                                    
                                    elif  (nm2[0][0] - nm1[0][0]) < 0: # '번'자 다음에 오는 '지'자이면
                                        if re.search("^목$", nm3[5]):
                                            key_blocks_A["landclass"] = raw_x_merge(nm1, nm3)
                                            print("지목 : 추가작업으로 완성")

    unmet_keys_box_2 = []
    for kb in kb_list:
        if not kb in key_blocks_A.keys():
            unmet_keys_box_2.append(kb)


    print("미완성 키 박스 :", unmet_keys_box_2, "\n")

    #print("최종 키박스::", key_blocks_A, "\n")