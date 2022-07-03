from coord import *
import re, os


def spec_table_A(idir, image_file, image_full_path, new_coord_line, new_coord_box, order):
    target_js = r"D:/results/var_2/"
    
    print("\n", " "*20, "::: 감정평가명세표 A형 제 {}페이지 분석시작 :::".format(order), "\n\n")

    land_attr = {}     
    building_attr = {}
    general_attr = {}
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


    #print("미완성 키 박스 :", unmet_keys_box_2, "\n")

    #print("최종 키박스::", key_blocks_A, "\n")

    ### 항목별 격벽의 좌표를 정해둠 ####        
    print("\n", " "*20, ":"*10, "인식된 키박스(A형)", ":"*10, "\n")       
    for key in key_blocks_A:
        if key == "num":
            num_L = key_blocks_A["num"][0][0]
            num_R = key_blocks_A["num"][1][0]
            print(" "*30, num_L,key_blocks_A["num"][5], num_R)

        elif key == "addr":
            addr_L = key_blocks_A["addr"][0][0]
            addr_R = key_blocks_A["addr"][1][0]
            print(" "*30, addr_L, key_blocks_A["addr"][5], addr_R)  

        elif key == "addrnum":
            addrnum_L = key_blocks_A["addrnum"][0][0]
            addrnum_R = key_blocks_A["addrnum"][1][0]
            print(" "*30, addrnum_L, key_blocks_A["addrnum"][5],  addrnum_R)

        elif key == "landclass":
            landclass_L = key_blocks_A["landclass"][0][0]
            landclass_R = key_blocks_A["landclass"][1][0]
            print(" "*30, landclass_L, key_blocks_A["landclass"][5],  landclass_R)

        elif key == "builduse":
            builduse_L = key_blocks_A["builduse"][0][0]
            builduse_R = key_blocks_A["builduse"][1][0]
            print(" "*30, builduse_L, key_blocks_A["builduse"][5], builduse_R)

        elif key == "buildstr":
            buildstr_L = key_blocks_A["buildstr"][0][0]
            buildstr_R = key_blocks_A["buildstr"][1][0]
            print(" "*30, buildstr_L, key_blocks_A["buildstr"][5], buildstr_R)

        elif key == "areause":
            areause_L = key_blocks_A["areause"][0][0]
            areause_R = key_blocks_A["areause"][1][0]
            print(" "*30, areause_L, key_blocks_A["areause"][5], areause_R)

        #elif not key_blocks_A["areause"]:
        #    areause_L = buildstr_L
        #    areause_R = buildstr_R
        #    print(" "*30, areause_L, "areause", areause_R)

        elif key =="paper":
            paper_L = key_blocks_A["paper"][0][0]
            paper_R = key_blocks_A["paper"][1][0]
            paper_Y = key_blocks_A["paper"][2][1]
            print(" "*30, paper_L, key_blocks_A["paper"][5], paper_R)

        elif key == "estim":
            estim_L = key_blocks_A["estim"][0][0]
            estim_R = key_blocks_A["estim"][1][0]
            print(" "*30, estim_L, key_blocks_A["estim"][5], estim_R)

        elif key =="price":
            price_L = key_blocks_A["price"][0][0]
            price_R = key_blocks_A["price"][1][0]
            print(" "*30, price_L, key_blocks_A["price"][5], price_R)

        elif key == "memo":
            memo_L = key_blocks_A["memo"][0][0]
            memo_R = key_blocks_A["memo"][1][0]
            memo_Y = key_blocks_A["memo"][2][1]
            print(" "*30, memo_L, key_blocks_A["memo"][5], memo_R)
    print("\n", " "*25, ":"*30, "\n")

                
    ## 공부와 사정은 중점좌표로 누락됨이 많아, 바로 위에서 새로정리된 기준으로 잡는다.
    ## 그런데, 공부와 사정이 1)소수점을 기준으로 분리된 것들이 많고, 하이픈(-)과 같은 찌꺼기가 소수점 뒤에 붙어 있는 misreads 들이 존재
    ## 이를 바로잡는다.
    if "price" in key_blocks_A:
        departed = []

        for value in new_coord_box:
                    
            if paper_L < midpoint(value)[0] < price_R or price_L < value[0][0] < price_R:
                if re.search("(\d+\,)*(\d+[.,]$)", value[5]): ## 쉼표로 끝나면서 허리잘린 통화표현을 선택하되, '000,'과 같이 숫자 중간에서 떨어져 나온 것은 배제
                    departed.append(value)  # 리스트에 넣기

                
        no2_departed = []
        for drp in departed:
            if drp not in no2_departed:
                no2_departed.append(drp)
        #print("쪼개진 숫자들 1111", no2_departed, "\n")

        ### '감정평가액의 마지막 000과 '비준가액'이 붙어버린 경우가 있어 수정함

        amended_pr_values = []
        del_pr_val = []
        for apv in new_coord_box:
            if price_L < apv[0][0] < (price_R+memo_L)/2:
                if re.search("(\d+\,)*(\d+,?)(?=[가-힣]+)", apv[5]):
                    new_num = re.search("(\d+\,)*(\d+,?)(?=[가-힣]+)", apv[5]).group(0)
                    new_price_part = [apv[0], [(price_R+memo_L)/2-20, apv[1][1]], [(price_R+memo_L)/2-20, apv[2][1]], apv[3], apv[4], new_num]
                    amended_pr_values.append(new_price_part)
                    del_pr_val.append(apv)

        for ap in del_pr_val:
            new_coord_box.remove(ap)

        for apr in amended_pr_values:
            new_coord_box.append(apr)
                
        #for r2 in new_coord_box:
        #    print('이상한 좌표 생성 체크 1', r2)
    ####################################################################

        ## 깨진 화폐의 중간파트가 새로운 그룹을 만들도록 해서는 안되므로, 처리함
        boss_groups = []
                
        for dp in no2_departed: 
            boss_groups.append(dp)

        #print("보스들만 오셔", boss_groups, "\n")

        new_boss = []
        del_boss = []
        for bsg in boss_groups:
            for obsg in boss_groups:
                #print("누가 보스가 될 것인가", bsg, obsg)
                if 0 < (obsg[0][0] - bsg[1][0]) < 20 and 0<= abs(bsg[1][1] - obsg[1][1]) < 10:
                    new_bsg = raw_num_x_merge(bsg, obsg)
                    #print("내 밑으로 와라", new_bsg)
                    del_boss.append(obsg)
                    del_boss.append(bsg)
                    new_boss.append(new_bsg)

        new_no2_departed = [nn for nn in boss_groups if nn not in del_boss]
        for new_bo in new_boss:
            if new_bo not in new_no2_departed:
                new_no2_departed.append(new_bo)


        for nb in new_boss:
            if nb not in new_no2_departed:
                new_no2_departed.append(nb)

        #print("중간보스들 병합완료 ~~", new_no2_departed, "\n")
        ###################################################################
        #for r2 in new_coord_box:
        #    print('이상한 좌표 생성 체크 2', r2)


        ############ 이제 보스는 깨진 숫자의 맨처음이므로, 주변에 존재하는 residue들을 병합합니다 ######
        del_from_new_coord_box = []  #나중에 제거해야함
        completed_groups = []
        for nnd in new_no2_departed:
            completed_groups.append([nnd]) # 신규 그룹생성

            for num_residue in new_coord_box: 
                
                if midpoint(num_residue)[0] < (price_R + memo_L)/2:
                    for group in completed_groups: # 그룹선택
                        if 0 < (num_residue[0][0] - group[-1][1][0]) < 20 and abs(num_residue[1][1] - group[-1][1][1]) < 10: # 면접~~
                            group.append(num_residue) # 그룹합류 및 모집단에서 제외
                            #print("새로 생긴 팀입니다", price_R, memo_L, group)
                            del_from_new_coord_box.append(num_residue)
                            group.sort(key=lambda t: t[0][0])
                            break # 신규 멤버
                        else:
                            continue # 조건에 맞는 그룹없음. 다른 그룹으로.

        merged_comp = []
        for sub_comp in completed_groups:
            sub_comp.sort(key=lambda t: t[0][0])

                    
            if len(sub_comp) == 2:                                               
                sub_c = raw_num_x_merge(sub_comp[0], sub_comp[1])
                merged_comp.append(sub_c)

            if len(sub_comp) == 3:
                sub_c = raw_num_x_merge(sub_comp[0], sub_comp[1])
                sub_d = raw_num_x_merge(sub_c, sub_comp[2])
                merged_comp.append(sub_d)

        #print("머지된 최종그룹입니다~~", merged_comp, "\n")
    ###################################################################################################


                               

        num_checked_coord_box_1 = [gg for gg in new_coord_box if gg not in no2_departed] #  깨진 숫자들에서 빼는 것은 당연~~

        #중간에 밸류에서 병합에 참여한 인자들도 모두 빼줘야 함~~

        num_checked_coord_box = [yy for yy in num_checked_coord_box_1 if yy not in del_from_new_coord_box]

        for mg in merged_comp:
            if mg not in new_coord_box:
                num_checked_coord_box.append(mg)

        #print("최종그룹들 제거하고, 조합된 숫자들까지 모두 첨가~", num_checked_coord_box, "\n")
        #XXXXXXXXXXXXXXXXXXXXXXXXXXX A형 reading pool 정비 완료 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
               










        #OOOOOOOOOOOOOOOOOOOOOOOOOOO 중요 y축 레벨 추출 OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO  
         
        landclass_level = []  # 중요기준 1: 지목정보  y 좌표
        price_level = []    # 중요기준 2: 평가액정보 y 좌표
        daejikwon_level = []  # 중요기준 3: 대지권정보 y 좌표
        soyoukwon_level = []  # 중요기준 4: 소유권정보 y 좌표


        for v_1 in  num_checked_coord_box:                
            if re.search("^전$|^답$|^대$", v_1[5]):   ## 향후 다양한 지목 평가시 추가"[적묘원용]지$|^도로$|\w+[야전장방천거장]$"
                if landclass_L < midpoint(v_1)[0] < landclass_R:                        
                    landclass_level.append(midpoint(v_1)[1])

        for v_2 in  num_checked_coord_box:
            for v_2a in  num_checked_coord_box:
                for v_3a in num_checked_coord_box:
                    if re.search("^(\d{1,3}\,)*\d{1,3}.?\d+[-]?", v_2[5]) and re.search("^(\d{1,3}\,)*\d{1,3}.?\d+[-]?", v_2a[5]):
                        # 공부, 사정의 전유면적 일치라인을 price_level로 잡음 
                        if buildstr_R < midpoint(v_2)[0] < estim_L and estim_L < midpoint(v_2a)[0] < price_L:   #수평으로 위치  
                            
                            if list(v_2[5])[:1] == list(v_2a[5])[:1] and list(v_2[5])[-1:] == list(v_2a[5])[-1:]: #abs(v_2[0][1] - v_2a[0][1]) < 30: # and 
                                
                                if price_L < v_3a[0][0] < price_R and re.search("^(\d{1,3}\,)+\d{1,3}$", v_3a[5]):                                    
                                    if abs(v_2[0][1] - v_3a[0][1]) < 30:                                        
                                        price_level.append(midpoint(v_2)[1])
                
        for v_3 in num_checked_coord_box:
            if landclass_R < midpoint(v_3)[0] < paper_L:   # "용도지역_구조" 항목칸에서                                                                     
                if re.search("대지권", v_3[5]):            # "대지권" 또는 "소유권" 이라는 말 중 더 아래에 있는 것이
                    daejikwon_level.append(midpoint(v_3)[1])           # 그 y값이 "대지권 레벨인데,
                if re.search("소유권", v_3[5]):            # "대지권" 또는 "소유권" 이라는 말 중 더 아래에 있는 것이
                    soyoukwon_level.append(midpoint(v_3)[1])                             
                            
                                
        ## 평가액 레벨과 지목레벨, 대지권 레벨 중복제거하고, 크기순으로 정렬

        no2_landclass_level = []
        if len(landclass_level) == 0:
            err_note = "파일명: {}__ 지목 레벨이 없습니다::".format(image_full_path)
            with open(r"D:/results/var_2/spec_errors_landclass_level.txt", 'a') as f:
                f.write("\n")
                f.write(err_note)
        else:
            for d2 in landclass_level:
                if d2 not in no2_landclass_level:
                    no2_landclass_level.append(d2)
            no2_landclass_level.sort(key=lambda t: t)
        print("\n", "지목 레벨::", no2_landclass_level, "\n")


        no2_price_level = []
        if len(price_level) == 0:
            err_note = "파일명: {}__ 평가액 레벨이 없습니다::".format(image_full_path)
            with open(r"D:/results/var_2/spec_errors_price_level.txt", 'a') as f:
                f.write("\n")
                f.write(err_note)
        else:
            for p2 in price_level:
                if p2 not in no2_price_level:
                    no2_price_level.append(p2)
            no2_price_level.sort(key=lambda t: t)
        print("\n", "평가액 레벨::", no2_price_level, "\n")



        no2_daejikwon_level = []
        if len(daejikwon_level) == 0:
            err_note = "파일명: {}__ 대지권 레벨이 없습니다::".format(image_full_path)
            with open(r"D:/results/var_2/spec_errors_daejikwon_level.txt", 'a') as f:
                f.write("\n")
                f.write(err_note)  
        else:
            for j2 in daejikwon_level:
                if j2 not in no2_daejikwon_level:
                    no2_daejikwon_level.append(j2)
            no2_daejikwon_level.sort(key=lambda t: t)
        print("\n", "대지권 레벨::", no2_daejikwon_level, "\n")


        no2_soyoukwon_level = []
        if len(soyoukwon_level) == 0:
            err_note = "파일명: {}__ 소유권 레벨이 없습니다::".format(image_full_path)
            with open(r"D:/results/var_2/spec_errors_soyoukwon_level.txt", 'a') as f:
                f.write("\n")
                f.write(err_note)
        else:
            for s2 in soyoukwon_level:
                if s2 not in no2_soyoukwon_level:
                    no2_soyoukwon_level.append(s2)
            no2_soyoukwon_level.sort(key=lambda t: t)




        ############################### 일반항목(general_attr) 추출#######################################

        
        #if order == 1: # 일반항목은 감정평가명세표 첫장에서만 추출 >> 여러건 평가하고도 하나의 파일속에 있는 경우가 있어 폐기함
        print("일반항목추출 시작")
        addr = []
        addrnum = []
        b_name_1 = []
        b_name_2 = []
        use_mode = []
        road_addr = []
        floor_num = []

        if len(no2_landclass_level) > 0:
            for vg in  num_checked_coord_box:
                #print("en22", vg)
                if addr_L < midpoint(vg)[0] < addr_R and memo_Y + 50 < midpoint(vg)[1] < no2_landclass_level[0]:
                    #if re.search(".+", vg[5]):    
                    addr.append(vg)
                
                    general_attr["소재지"] = "{}".format(vg[5])


                    if re.search("^[가-힣]+\d*도$", vg[5]):   
                       general_attr["도"] = "{}".format(vg[5])

                    elif re.search("^[가-힣]+\d*시$", vg[5]):   
                       general_attr["시"] = "{}".format(vg[5])
                        
                    elif re.search("^[가-힣]+\d*[군구]$", vg[5]):
                       general_attr["군구"] = "{}".format(vg[5])                        

                    elif re.search("^[가-힣]+\d*[동]$", vg[5]):
                       general_attr["동"] = "{}".format(vg[5])

                    elif re.search("^[가-힣]+\d*[면]$", vg[5]):
                       general_attr["면"] = "{}".format(vg[5])

                    elif re.search("^[가-힣]+\d*[리]$", vg[5]):
                       general_attr["리"] = "{}".format(vg[5])
                        
                    elif re.search("^[가-힣]+\d*[길로]$", vg[5]):
                       road_addr.append(vg[5])

                    elif re.search("^\d{1,4}\-?\d{1,3}[길로]?$", vg[5]):
                       road_addr.append(vg[5])  # 도로명 주소상 지번이므로 구분함
  
                       
                ## 건물명은 소재지에도 있고, 지번에도 있다.
                ## 소재지의 경우에는, 동명 아래에 따라오고,
                ## 지번의 경우에는 지번 숫자를 제외하면 된다.

                elif addrnum_L < midpoint(vg)[0] < addrnum_R:

                    if memo_Y + 50 < midpoint(vg)[1] < no2_landclass_level[0]:  ## 지번 속 건물명 넣기
                        if re.search("(^\d+\-?\d*)", vg[5]):   #[가-힣]{3,20}|\d+[동]$
                            addrnum.append(vg)
                            #general_attr["지번"] = "{}".format(vg[5])

                        if re.search("[가-힣]+", vg[5]):
                            b_name_1.append(vg)
                    else:
                        if memo_Y + 50 < midpoint(vg)[1] < 1000:  ## 지번 속 건물명 넣기
                            if re.search("(\d+\-?\d*)", vg[5]):   #[가-힣]{3,20}|\d+[동]$
                                addrnum.append(vg)
                                #general_attr["지번"] = "{}".format(vg[5])

                            if re.search("[가-힣]+", vg[5]):
                                b_name_1.append(vg)

                elif landclass_L < midpoint(vg)[0] < landclass_R:
                    
                    if paper_Y  < midpoint(vg)[1] < no2_landclass_level[0]:  
                        if re.search("도시형|^다세대|주택|공동|근린|업무", vg[5]):   
                            use_mode.append(vg[5])
                        else:
                            if re.search(".+", vg[5]):   #[가-힣]{3,20}|\d+[동]$
                                b_name_2.append(vg)
                                    

                    else:
                        if memo_Y + 50 < midpoint(vg)[1] < 1000:  ## 지번 속 건물명 넣기
                            if re.search("도시형|^다세대|주택|공동|근린|업무", vg[5]):   
                                use_mode.append(vg[5])
                            else:
                                if re.search(".+", vg[5]):   #[가-힣]{3,20}|\d+[동]$
                                    b_name_2.append(vg)
                                    

                elif landclass_R < midpoint(vg)[0] < paper_L:
                    if re.search("\w+조$|철근\w+조$|콘크\w+조$|크리\w+조$|세멘\w+조$|시멘\w+조$|시맨\w+조$", vg[5]):   
                        general_attr["구조"] = "{}".format(vg[5])
                        for_json_sta["구조"] = "{}".format(vg[5])

                    elif re.search("\w+붕|슬라브\w+붕$|경사\w+붕$", vg[5]):   
                        general_attr["지붕"] = "{}".format(vg[5])
                        for_json_sta["지붕"] = "{}".format(vg[5])
                    elif re.search("\d{1,3}층", vg[5]): 
                        floor_n = re.search("\d{1,3}(?=층)", vg[5]).group(0)
                        floor_num.append(floor_n)
                        
                        ### 참고 table_title = re.search("(?<=[\.\)\,-]).{2,25}", up[2]).group(0)
            
        ### 건물명은 조금 복잡해서 따로 처리해준다 ##
        if len(b_name_1) > 0:
            new_b_name_1 = []
            b_name_1.sort(key=lambda t: t[0][1])
            for bnm1 in b_name_1:
                if bnm1[5] not in new_b_name_1:
                    new_b_name_1.append(bnm1[5])
                #if 600 < bnm[0][1] < no2_landclass_level[0]:
            general_attr["건물명_1"] = ' '.join(new_b_name_1)
            for_json_sta["건물명_1"] = ' '.join(new_b_name_1)
                    
        if len(b_name_2) > 0:
            new_b_name_2 = []
            b_name_2.sort(key=lambda t: t[0][1])
            general_attr["건물명_2"] = ' '.join(new_b_name_2)



            groups = []
            brk = False
            for bnm2 in b_name_2:   
                for group in groups:        
                    if 0 < (bnm2[1][1] - group[-1][1][1]) < 100:
                        group.append(bnm2)            
                        brk = True 
                        continue

                    elif brk:
                        break                       
            
                if not brk:
                    groups.append([bnm2]) 

            if len(groups) > 0:
                new_bn_2 = []
                groups[0].sort(key=lambda t: t[0][1])
                for nadm in groups[0]:
                    if nadm[5] not in new_bn_2:
                        new_bn_2.append(nadm[5])
                general_attr["건물명_bn"] = ' '.join(new_bn_2)        


        if len(use_mode) > 0:
            new_use_mode = []
            for adm in use_mode:
                if adm not in new_use_mode:
                    new_use_mode.append(adm)
            general_attr["이용상황"] = ' '.join(new_use_mode)
            for_json_sta["이용상황"] = ' '.join(new_use_mode)

        if len(addr) > 0:
            new_addr = []
            addr.sort(key=lambda t: t[0][1])
            for adm in addr:
                if adm[5] not in new_addr:
                    new_addr.append(adm[5])
                #if 600 < adm[0][1] < no2_landclass_level[0]:
            general_attr["소재지"] = ' '.join(new_addr)
            for_json_sta["소재지"] = ' '.join(new_addr)
                    
        if len(addrnum) > 0:
            new_addrnum = []
            addrnum.sort(key=lambda t: t[0][1])
            for nadm in addrnum:
                if nadm[5] not in new_addrnum:
                    new_addrnum.append(nadm[5])
                #if 600 < adm[0][1] < no2_landclass_level[0]:
            general_attr["지번"] = ' '.join(new_addrnum)
            for_json_sta["지번"] = ' '.join(new_addrnum)
            
        # 수집된 각 항목의 리스트를 for 문 종료시 딕셔너리에 부가한다.
        general_attr["평가서 ID"] = idir

        #general_attr["도로명"] = ' '.join(road_addr)
        #for_json_sta["도로명"] = ' '.join(road_addr)
        
        

        if len(floor_num) > 0:            
            floor_num.sort(key=int) # 층수는 string이므로 이와 같이 "정수기준이라면"으로 정렬후 가장 큰 마지막 숫자 선택
            general_attr["지상 층 수"] = int(floor_num[-1])
            for_json_sta["지상 층 수"] = int(floor_num[-1])


        if len(general_attr) > 0:
            print("\n", "일반항목", general_attr, "\n")

            spec_general_data.append(general_attr)


        ####################################################################################



               
                
        ############ 지목레벨에서 뽑을 것 = 지목 / 지번 / 공부_면적 ###########################################

        if len(no2_landclass_level) > 0: # 토지속성도 지목레벨이 존재할때만 뽑음

            breaker = False       
            for ue in no2_landclass_level: # 지목에 대해 여러개인 경우까지 순회하며 각각의 데이터를 모음
                for ind, va in  enumerate(num_checked_coord_box):
                    #print(va, "이것과 비교", ue)

                    if abs(midpoint(va)[1] - ue) < 50:
                        #print("지목 레벨과 유사한 값::", va, ue)

                        if  num_L < midpoint(va)[0] < num_R:
                            if re.search("\w{1,3}", va[5]):
                                land_attr["일련번호_토지"] = "{}".format(va[5]) 
                                for_json_sta["일련번호_토지"] = "{}".format(va[5]) 
                                #print(land_attr)
                            #else:
                                #land_attr["일련번호_토지"] = "Not Found" 

                        elif  landclass_L < midpoint(va)[0] < landclass_R:
                            if re.search("^전$|답$|대$|\w+[지원야전장로방천거장]$", va[5]):
                                land_attr["지목"] = "{}".format(va[5])      
                                for_json_sta["지목"] = "{}".format(va[5]) 
                                #print(land_attr)

                        elif  addrnum_L < midpoint(va)[0] < addrnum_R:
                            if re.search("\d+\-?\d+", va[5]):
                                if "지번" not in land_attr:
                                    land_attr["지번"] = "{}".format(va[5])
                                    for_json_sta["지번"] = "{}".format(va[5]) 
                                elif "지번" not in general_attr:
                                    general_attr["지번"] = "{}".format(va[5])
                                    for_json_sta["지번"] = "{}".format(va[5]) 
                                #print(general_attr)
                                #print(general_attr, "general에 지번 들어감")

                        elif  landclass_R < midpoint(va)[0] < paper_L: ### "구조
                            if re.search("제?[123]종|일주|상업|공업|자연", va[5]):
                                land_attr["용도지역"] = "{}".format(va[5])
                                for_json_sta["용도지역"] = "{}".format(va[5]) 
                                #print(land_attr)

                        elif  buildstr_R < midpoint(va)[0] < estim_L:
                            if re.search("\d+$", va[5]):
                                land_attr["토지면적_해당필지"] = "{}".format(va[5])
                                for_json_sta["토지면적_해당필지"] = "{}".format(va[5]) 
                                #print(land_attr)
                            else:
                                land_attr["토지면적_해당필지"] = "Not Found" 
                                for_json_sta["토지면적_해당필지"] = "{}".format(va[5]) 
                                
                    elif ind == len(num_checked_coord_box)-1:   ## 밸류항목을 한번탐색                     
                        breaker = True
                        break

                if breaker:
                    land_attr["평가서 ID"] = idir
                    land_attr_copy = land_attr.copy() # 딕셔너리는 키밸류 integrity를 위해 append 시 카피본을 넣음                    
                    L_list.append(land_attr_copy)
                    
                    land_attr.clear()

        print(" 토지속성::", L_list, "\n")

        #########################################################################################################




        ###################### 평가액레벨에서 뽑을 것 = 평가액 / 전유면적_공부, 사정 / 층/호 / 일련번호 ############################
        if len(no2_daejikwon_level) == 0 and len(no2_price_level) > 0:
            p_breaker = False

            for p, pr in enumerate(no2_price_level):
               
                for ind, vn in enumerate(num_checked_coord_box):
                    
                    if abs(midpoint(vn)[1]- pr) < 50: #  vn은 평가액라인 속으로 좁힘. 
                        

                        if price_L < vn[0][0] < price_R:  
                            if re.search("^(\d{1,3}\,)+\d{1,3}$", vn[5]):
                                building_attr["감정평가액"] =  "{}".format(vn[5])
                                for_json_sta["감정평가액"] = "{}".format(vn[5])                                 
                                #print("감정평가액::", vn[5])
             
                        if num_L < midpoint(vn)[0] < num_R:
                            if re.search("\w{1,3}", vn[5]):
                                building_attr["일련번호_건물"] = "{}".format(vn[5])   
                                for_json_sta["일련번호_건물"] = "{}".format(vn[5])  
                                #print("일련번호_건물::", vn[5])


                        if paper_L < midpoint(vn)[0] < estim_L:       
                            if re.search("^(\d{1,3}\,)*\d{1,3}.?\d+[-]?$", vn[5]):
                                building_attr["공부_전유면적"] =  "{}".format(vn[5]) 
                                for_json_sta["공부_전유면적"] = "{}".format(vn[5])  
                                #print("공부_전유면적::", vn[5])

                        if estim_L < midpoint(vn)[0] < price_L:       
                            if re.search("^(\d{1,3}\,)*\d{1,3}.?\d+[-]?$", vn[5]):
                                building_attr["사정_전유면적"] =  "{}".format(vn[5])  
                                for_json_sta["사정_전유면적"] = "{}".format(vn[5])  

                        if landclass_R < midpoint(vn)[0] < buildstr_R:       
                            if re.search("호$", vn[5]):
                                building_attr["호"] =  "{}".format(vn[5])  
                                for_json_sta["호"] = "{}".format(vn[5])

                            if re.search("층$", vn[5]):
                                building_attr["층"] =  "{}".format(vn[5]) 
                                for_json_sta["층"] = "{}".format(vn[5])

                        if addrnum_L < midpoint(vn)[0] < buildstr_L:       
                            if re.search("호$", vn[5]):
                                building_attr["호"] =  "{}".format(vn[5])  
                                for_json_sta["호"] = "{}".format(vn[5])

                            if re.search("층$", vn[5]):
                                building_attr["층"] =  "{}".format(vn[5]) 
                                for_json_sta["층"] = "{}".format(vn[5])

                    if ind == len(num_checked_coord_box)-1:   ## 밸류항목에 대한 한번 순회   
                        p_breaker = True
                        break

                if p_breaker:
                    building_attr["평가서 ID"] = idir #image_file # # #
                    building_attr["대지권면적_사정"] = "대지권 면적 없음"
                    building_attr_copy = building_attr.copy()
                    B_list.append(building_attr_copy) 
                    
                    building_attr.clear()

                    #############################
        if len(no2_daejikwon_level) == 1 and len(no2_price_level) == 1:
            p_breaker = False
            for ind, vn in enumerate(num_checked_coord_box):

                for v_5 in num_checked_coord_box:
                    
                    if abs(midpoint(vn)[1]- no2_price_level[0]) < 50: #  vn은 평가액라인 속으로 좁힘.                         

                        if price_L < vn[0][0] < price_R:  
                            if re.search("^(\d{1,3}\,)+\d{1,3}$", vn[5]):
                                building_attr["감정평가액"] =  "{}".format(vn[5])
                                for_json_sta["감정평가액"] = "{}".format(vn[5])                                 
                                #print("감정평가액::", vn[5])
             
                        if num_L < midpoint(vn)[0] < num_R:
                            if re.search("\w{1,3}", vn[5]):
                                general_attr["일련번호_건물"] = "{}".format(vn[5])   
                                for_json_sta["일련번호_건물"] = "{}".format(vn[5])  
                                #print("일련번호_건물::", vn[5])


                        if paper_L < midpoint(vn)[0] < estim_L:       
                            if re.search("^(\d{1,3}\,)*\d{1,3}.?\d+[-]?$", vn[5]):
                                building_attr["공부_전유면적"] =  "{}".format(vn[5]) 
                                for_json_sta["공부_전유면적"] = "{}".format(vn[5])  
                                #print("공부_전유면적::", vn[5])

                        if estim_L < midpoint(vn)[0] < price_L:       
                            if re.search("^(\d{1,3}\,)*\d{1,3}.?\d+[-]?$", vn[5]):
                                building_attr["사정_전유면적"] =  "{}".format(vn[5])  
                                for_json_sta["사정_전유면적"] = "{}".format(vn[5])  

                                if re.search("^(\d{1,3}\,)*\d{1,3}.?\d+[-]?$", v_5[5]) and estim_L < midpoint(v_5)[0] < price_L:
 
                                    if no2_price_level[0] + 50 < v_5[0][1]:
                                        building_attr["대지권면적_사정"] = "{}".format(v_5[5]) ## 사정_전유면적 아래에 존재하는 수
                                        for_json_sta["대지권면적_사정"] = "{}".format(v_5[5])
                                        #print("대지권면적_사정::", v_5[5])

                        if landclass_R < midpoint(vn)[0] < buildstr_R:       
                            if re.search("호$", vn[5]):
                                building_attr["호"] =  "{}".format(vn[5])  
                                for_json_sta["호"] = "{}".format(vn[5])

                            if re.search("층$", vn[5]):
                                building_attr["층"] =  "{}".format(vn[5]) 
                                for_json_sta["층"] = "{}".format(vn[5])

                        if addrnum_L < midpoint(vn)[0] < buildstr_L:       
                            if re.search("호$", vn[5]):
                                building_attr["호"] =  "{}".format(vn[5])  
                                for_json_sta["호"] = "{}".format(vn[5])

                            if re.search("층$", vn[5]):
                                building_attr["층"] =  "{}".format(vn[5]) 
                                for_json_sta["층"] = "{}".format(vn[5])

                    if ind == len(num_checked_coord_box)-1:   ## 밸류항목에 대한 한번 순회   
                        p_breaker = True 
                        break

                if p_breaker:
                    building_attr["평가서 ID"] = idir #image_file # # #
                   
                    building_attr_copy = building_attr.copy()
                    B_list.append(building_attr_copy) 
                    
                    building_attr.clear()


        ## 대지권 레벨 = 대지권면적 / 전체 토지면적 ############################################################


        if len(no2_daejikwon_level) > 1 and len(no2_price_level) > 1:
            #no2_price_level.sort(key=lambda t: t)
            #no2_daejikwon_level.sort(key=lambda t: t)

            d_breaker = False
            for thp, nep in this_and_next(no2_price_level):
                
                for thd, ned in this_and_next(no2_daejikwon_level):
                    
                    for ind, vn in enumerate(num_checked_coord_box):
                        
                        for v_5 in num_checked_coord_box:
                                
                            if abs(midpoint(vn)[1]- thp) < 50: #  vn은 평가액라인 속으로 좁힘. 
                                
                                if price_L < vn[0][0] < price_R:  
                                    if re.search("^(\d{1,3}\,)+\d{1,3}$", vn[5]):
                                        building_attr["감정평가액"] =  "{}".format(vn[5])  
                                        for_json_sta["감정평가액"] = "{}".format(vn[5])
                                        
             
                                elif num_L < midpoint(vn)[0] < num_R:
                                    if re.search("\w{1,3}", vn[5]):
                                        building_attr["일련번호_건물"] = "{}".format(vn[5])   
                                        for_json_sta["일련번호_건물"] = "{}".format(vn[5])
                                        

                                elif paper_L < midpoint(vn)[0] < estim_L:       
                                    if re.search("^(\d{1,3}\,)*\d{1,3}.?\d+[-]?$", vn[5]):
                                        building_attr["공부_전유면적"] =  "{}".format(vn[5])
                                        for_json_sta["공부_전유면적"] = "{}".format(vn[5])
                                        #print("공부_전유면적::", vn[5])

                                elif estim_L < midpoint(vn)[0] < price_L:       
                                    if re.search("^(\d{1,3}\,)*\d{1,3}.?\d+[-]?$", vn[5]):
                                        building_attr["사정_전유면적"] =  "{}".format(vn[5]) 
                                        for_json_sta["사정_전유면적"] = "{}".format(vn[5])

                                        if re.search("^(\d{1,3}\,)*\d{1,3}.?\d+[-]?$", v_5[5]) and estim_L < midpoint(v_5)[0] < price_L:
                                            if nep != None:
                                                if thp + 50 < v_5[0][1] < nep - 50 :
                                                    building_attr["대지권면적_사정"] = "{}".format(v_5[5]) ## 사정_전유면적 아래에 존재하는 수
                                                    for_json_sta["대지권면적_사정"] = "{}".format(v_5[5])
                                                    #print("대지권면적_사정::", v_5[5])


                                elif landclass_R < midpoint(vn)[0] < buildstr_R:       
                                    if re.search("호$", vn[5]) and abs(midpoint(v_5)[1] - thp) < 100:
                                        building_attr["호"] =  "{}".format(vn[5])  
                                        for_json_sta["호"] = "{}".format(vn[5])

                                    elif re.search("층$", vn[5]) and abs(midpoint(v_5)[1] - thp) < 100:
                                        building_attr["층"] =  "{}".format(vn[5]) 
                                        for_json_sta["층"] = "{}".format(vn[5])

                                elif addrnum_L < midpoint(vn)[0] < buildstr_L:       
                                    if re.search("호$", vn[5]) and abs(midpoint(v_5)[1] - thp) < 100:
                                        building_attr["호"] =  "{}".format(vn[5])  
                                        for_json_sta["호"] = "{}".format(vn[5])

                                    elif re.search("층$", vn[5]):
                                        building_attr["층"] =  "{}".format(vn[5])
                                        for_json_sta["층"] = "{}".format(vn[5])

                                elif landclass_R < midpoint(v_5)[0] < paper_L:       
                                    if re.search("호", v_5[5]) and abs(midpoint(v_5)[1] - thp) < 100:
                                        building_attr["호"] =  "{}".format(v_5[5])  
                                        for_json_sta["호"] = "{}".format(vn[5])

                                    elif re.search("층", v_5[5])and abs(midpoint(v_5)[1] - thp) < 100:
                                        building_attr["층"] =  "{}".format(v_5[5]) 
                                        for_json_sta["층"] = "{}".format(vn[5])
            

                            if ind == len(num_checked_coord_box)-1:   ## 밸류항목에 대한 한번 순회   
                                
                                d_breaker = True
                                break

                if d_breaker:
                    building_attr["평가서 ID"] = idir #image_file # # #
                    building_attr_copy = building_attr.copy()
                    B_list.append(building_attr_copy) 
                    
                    general_attr.clear()

        print("\n", "딥러닝 학습 데이터로 사용 항목", for_json_sta, target_js + os.path.splitext(image_file)[0], "\n")

        
        with open(target_js + os.path.splitext(image_file)[0]+".json", 'w', encoding="UTF-8") as st: #"
            st.write(str(for_json_sta))



        ####################################################################################################
        print("빌딩속성", B_list, "\n")

        if len(B_list)==0:
            print("건물속성이 모아지지 않았습니다")
            berr_note = "파일명: {}__ 건물속성이 모아지지 않았습니다::".format(idir)
            with open(r"D:/results/var_2/spec_general_attr_errors.txt", 'a') as f:
                f.write("\n")
                f.write(berr_note)


                  
    return (spec_general_data, B_list, L_list, for_json_sta)

    #except:
    #    spec_A_errors.append(image_full_path)

    #    new_spec_A_errors = []
    #    for nsg in spec_A_errors:
    #        if nsg not in new_spec_A_errors:
    #            new_spec_A_errors.append(nsg)

    #    for sne in new_spec_A_errors:
    #        with open(r"C:/Users/brigs/Desktop/results/spec_A_errors.txt", 'a') as s:
    #            s.write("\n")
    #            s.write(str(sne))
    