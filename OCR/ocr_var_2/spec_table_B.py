import re
from coord import *
import shutil




def spec_table_B(idir, image_full_path, new_coord_line, new_coord_box, order):

    print("\n", " "*20, "::: 감정평가명세표 B형 제 {} 페이지 분석시작 :::".format(order), "\n\n")

    land_attr = {}     
    building_attr = {}
    general_attr = {}
    B_list = []
    L_list = []
    spec_general_data = []

    spec_B_errors = []

    #try:
                        
    BL = []
    for letter in new_coord_line:  

        if re.search("^[기번호]$", letter[5]):  ## "^[일련번기호]{1,4}$"
            if 200 < letter[0][1] < 1000:   ## 양식A군은600내에 존재, B군은 700으로 내려옴
                BL.append(letter) 

        if re.search("^소\s?재\s?지$", letter[5]):
            if 200 < letter[0][1] < 1000:
                BL.append(letter)

        if re.search("^건\s?물\s?명$", letter[5]):
            if 200 < letter[0][1] < 1000:
                BL.append(letter)

        if re.search("^지\s?목$", letter[5]): #지목?용도와 같은 변이까지 커버
            if 200 < letter[0][1] < 1000:
                BL.append(letter)

        if re.search("^용\s?도$", letter[5]):
            if 200 < letter[0][1] < 1000:
                BL.append(letter)

        if re.search("^공\s?부$", letter[5]):
            if 200 < letter[0][1] < 1000:
                BL.append(letter)

        if re.search("^사\s?정$", letter[5]):
            if 200 < letter[0][1] < 1000:
                BL.append(letter)

        if re.search("^감\s?정\s?평\s?가\s?액$|^감\s?정\s?평\s?가\s?액\s?(원)$", letter[5]): #감정평가액(원)
            if 200 < letter[0][1] < 1000:
                BL.append(letter)
                        
        if re.search("^비\s?고$", letter[5]):
            if 200 < letter[0][1] < 1000:
                BL.append(letter)

    NBL = []
    for ek in BL:
        nek = [ek[0], ek[1], ek[2], ek[3], ek[4], ek[5].replace(" ", "")]
        NBL.append(nek)

    #print("B 형의 키모집을 위한 라인모드", NBL, "\n")

    key_blocks_B = {}  # 라인모드에서의 1차 모집
    bb_list = ["num", "addr", "buildname", "generalinfo", "landclass", "builduse", "paper", "estim", "price", "memo"]

    for nk in NBL:
        if re.search("^[기번]호$", nk[5]):
            key_blocks_B["num"] = nk

        if re.search("^소재지$", nk[5]):
            key_blocks_B["addr"] = nk

        if re.search("^건물명$", nk[5]):
            key_blocks_B["buildname"] = nk

        if re.search("^구분$", nk[5]):
            key_blocks_B["generalinfo"] = nk


        if re.search("^(지목|용도).*(지목|용도)$|^지목$", nk[5]):
            key_blocks_B["landclass"] = nk

        if re.search("^(지목|용도).*(지목|용도)$|^용도$", nk[5]):
            key_blocks_B["builduse"] = nk


        if re.search("^공부$", nk[5]):
            key_blocks_B["paper"] = nk

        if re.search("^사정$", nk[5]):
            key_blocks_B["estim"] = nk

        if re.search("^감정평가액$|^감정평가액(원)$|^평가금액$|^평가가격$", nk[5]):
            key_blocks_B["price"] = nk

        if re.search("^비고$", nk[5]):
            key_blocks_B["memo"] = nk
           
    #print("라인에서 수집된 B형평가서의 키박스::", key_blocks_B, "\n")


    unmet_keysb = []
    for bb in bb_list:
        if not bb in key_blocks_B.keys():
            unmet_keysb.append(bb)

    #print("라인모드 작업으로 채워지지 않은 키박스::", unmet_keysb, "\n")


    ############ 이제 박스모드로 키처리 ###################


    ## B 양식의 키단어 모집을 위한 필터

    B = []

    for letter in new_coord_box:  # 키인식은 박스모드로 
        if re.search("[기번호]", letter[5]):  ## "^[일련번기호]{1,4}$"
            if 200 < letter[0][1] < 700:   ## 양식A군은600내에 존재, B군은 700으로 내려옴
                B.append(letter) 

        if re.search("^[소재지]$", letter[5]):
            if 200 < letter[0][1] < 700:
                B.append(letter)

        if re.search("^[건물명]$", letter[5]):
            if 200 < letter[0][1] < 700:
                B.append(letter)

        if re.search("^[구분]{1,2}$", letter[5]):
            if 200 < letter[0][1] < 700:
                B.append(letter)

        if re.search("[지목]{1,2}$|^[지목].{1,5}$", letter[5]): #지목?용도와 같은 변이까지 커버
            if 200 < letter[0][1] < 700:
                B.append(letter)

        if re.search("^[용도]{1,2}$", letter[5]):
            if 200 < letter[0][1] < 700:
                B.append(letter)

        if re.search("^[공부]{1,2}$", letter[5]):
            if 200 < letter[0][1] < 700:
                B.append(letter)

        if re.search("^[사정]{1,2}$", letter[5]):
            if 200 < letter[0][1] < 700:
                B.append(letter)

        if re.search("^[감정평단가격금액원\(\)]{1,8}", letter[5]): #감정평가액(원)
            if 200 < letter[0][1] < 700:
                B.append(letter)
                        
        if re.search("^[비고]{1,2}$", letter[5]):
            if 200 < letter[0][1] < 700:
                B.append(letter)

                
    #print("박스모드로 B 형의 키를 모집 ", B, "\n")

    ## 박스모드에서도 일단 완전한 단어부터 골라야 하겠지??

    del_1= []
    for uk in unmet_keysb:
        for nk in B:
            if uk == 'num':
                if re.search("^[기번]호$", nk[5]):
                    key_blocks_B["num"] = nk
                    del_1.append(nk)
            if uk == 'addr':
                if re.search("^소재지$", nk[5]):
                    key_blocks_B["addr"] = nk
                    del_1.append(nk)
            if uk == 'buildname':                    
                if re.search("^건물명$", nk[5]):
                    key_blocks_B["buildname"] = nk
                    del_1.append(nk)
            if uk == 'generalinfo':
                if re.search("^구분$", nk[5]):
                    key_blocks_B["generalinfo"] = nk
                    del_1.append(nk)

            if uk == 'landclass':
                if re.search("^(지목|용도).*(지목|용도)$|^지목$", nk[5]):
                    key_blocks_B["landclass"] = nk
                    del_1.append(nk)
            if uk == 'builduse':
                if re.search("^(지목|용도).*(지목|용도)$|^용도$", nk[5]):
                    key_blocks_B["builduse"] = nk
                    del_1.append(nk)

            if uk == 'paper':
                if re.search("^공부$", nk[5]):
                    key_blocks_B["paper"] = nk
                    del_1.append(nk)
            if uk == 'estim':
                if re.search("^사정$", nk[5]):
                    key_blocks_B["estim"] = nk
                    del_1.append(nk)
            if uk == 'price':
                if re.search("^감정평가액$|^감정평가액(원)$|^평가금액$|^평가가격$", nk[5]):
                    key_blocks_B["price"] = nk
                    del_1.append(nk)
            if uk == 'memo':
                if re.search("^비고$", nk[5]):
                    key_blocks_B["memo"] = nk
                    del_1.append(nk)



    B_1=[]
    for kk in B:
        if kk not in del_1:
            B_1.append(kk)

                   
           
    #print("박스모드에서 수집된 B형평가서의 키박스::", key_blocks_B, "\n")


    unmet_keys_box_b = []
    for kb in bb_list:
        if not kb in key_blocks_B.keys():
            unmet_keys_box_b.append(kb)

    #print("박스모드 작업으로 채워지지 않은 키박스::", unmet_keys_box_b, "\n")

    #print("작업벤치:B_1:", B_1, "\n")

    ####################################################################################################
    ## 온전한 단어는 다 살펴보았고, 이제는 낱글자들과 부서진 여러글자들을 모아 키를 조립해야함 ###

               

    ### 1. 소재지 / 건물명의 낱글자 처리 == 3단계 조립
    del_from_B_1= []
    add_to_B_1 = []

                
    for ukb in unmet_keys_box_b:
        for bs1 in B_1:                    
            for bs2 in B_1:
                for bs3 in B_1:
                    if ukb == 'addr':                                    
                            ## 소재지와 '지번'이 붙는 경우가 많아 조립에 방해가 되므로, 낱글자로 이들부터 떼 내겠음 ##
                        if re.search("^소$", bs1[5]):
                            if re.search("^재$", bs2[5]):
                                diff1 = bs2[0][0] - bs1[0][0]
                                if re.search("^지$", bs3[5]): ## 소 재 지 간의 간격이 균등함을 이용해 다른 '지'자 배제 
    
                                    diff2 = (bs3[0][0] - bs2[0][0])
                                    if abs(diff1-diff2) < 15:
                                        addr = raw_x3_merge(bs1, bs2, bs3) 
                                            
                                        key_blocks_B["addr"] = addr  ## 소재지가 완성된 경우, 일찌감치 fin으로 보낸다.
                                        del_from_B_1.append(bs1)
                                        del_from_B_1.append(bs2)
                                        del_from_B_1.append(bs3)

                    elif ukb == 'buildname':                        
                        if re.search("^건$", bs1[5]): 
                            if re.search("^물$", bs2[5]): ## 용도지역 간의 간격이 균등함을 이용해 다른 '지'자 배제     
                                if re.search("^명$", bs3[5]):
                                   
                                    d1 = midpoint(bs1)[0] - midpoint(bs2)[0]
                                    d2 = midpoint(bs2)[0] - midpoint(bs3)[0]

                                    if abs(d1 - d2) < 10 and abs(midpoint(bs1)[1]-midpoint(bs2)[1]) < 10 and abs(midpoint(bs2)[1] - midpoint(bs3)[1])< 10:
                                            
                                        buildn = raw_x3_merge(bs1, bs2, bs3) 
                                        key_blocks_B["buildname"] = buildn
                                        del_from_B_1.append(bs1)
                                        del_from_B_1.append(bs2)
                                        del_from_B_1.append(bs3)                  
                                           
    for ek in add_to_B_1:
        if ek not in B_1:
            B_1.append(ek)

    #print("지울거", del_from_K_1)                            
    B_2 = []
    for singj in B_1:
        if singj not in del_from_B_1: ## 단어생성이 끝난 "소, 재, 지"를 제거
            B_2.append(singj)
                                                                        
    #print("B_2",B_2, "\n")


    for ukb2 in unmet_keys_box_b:
                    
        for nm1 in B_2:
            for nm2 in B_2:

                if ukb2 == 'num':
                    if re.search("^[기번]", nm1[5]):
                        if re.search("호$", nm2[5]):
                            if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                key_blocks_B["num"] = raw_x_merge(nm1, nm2)
                            if abs(midpoint(nm1)[0] - midpoint(nm2)[0]) < 10:
                                key_blocks_B["num"] = raw_y_merge(nm1, nm2)

                elif ukb2 == 'addr':
                    if re.search("^소$", nm1[5]):
                        if re.search("^재지$", nm2[5]):  
                            if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                key_blocks_B["addr"] = raw_x_merge(nm1, nm2)

                    elif re.search("^소재$", nm1[5]):                                        
                        if re.search("^지$", nm2[5]):                                           
                            if abs((nm2[0][0]-nm1[1][0]) - abs((nm1[1][0] - nm1[0][0]) - (nm2[1][0]-nm2[0][0])*2)) < 10 and abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                key_blocks_B["addr"] = raw_x_merge(nm1, nm2)         

                elif ukb2 == 'generalinfo':
                    if re.search("^구$", nm1[5]):
                        if re.search("^분$", nm2[5]):
                            if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10 and 0 < (nm2[0][0] - nm1[0][0]):
                                key_blocks_B["generalinfo"] = raw_x_merge(nm1, nm2)

                        
                elif ukb2 == 'builduse':
                    if re.search("^용$", nm1[5]):                                       
                        if re.search("^도$", nm2[5]):                                         
                            if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                key_blocks_B["builduse"] = raw_x_merge(nm1, nm2) 


                elif ukb2 == 'paper':
                    if re.search("^공$", nm1[5]):
                        if re.search("^부$", nm2[5]):
                            if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                key_blocks_B["paper"] = raw_x_merge(nm1, nm2) 

                elif ukb2 == 'estim':               
                    if re.search("^사$", nm1[5]):
                        if re.search("^정$", nm2[5]):
                            if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                key_blocks_B["estim"] = raw_x_merge(nm1, nm2) 

                elif ukb2 == 'price':                
                    if re.search("^감", nm1[5]):
                        if re.search("액$", nm2[5]):
                            if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                key_blocks_B["price"] = raw_x_merge(nm1, nm2) 


                elif ukb2 == 'memo':                
                    if re.search("^비$", nm1[5]):
                        if re.search("^고$", nm2[5]):
                            if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                key_blocks_B["memo"] = raw_x_merge(nm1, nm2) 
                                                
                elif ukb == 'landclass':   
                    if re.search("^지$", nm1[5]):
                        if re.search("^목$", nm2[5]):
                            if abs(midpoint(nm1)[1] - midpoint(nm2)[1]) < 10:
                                key_blocks_B["landclass"] = raw_x_merge(nm1, nm2) 


    unmet_keys_box_b2 = []
    for kb in bb_list:
        if not kb in key_blocks_B.keys():
            unmet_keys_box_b2.append(kb)


    #print("아직도 채워지지 않은 키박스??????????: 2 :", unmet_keys_box_b2, "\n")

    #print("최종 키박스::", key_blocks_B, "\n")

    ### 항목별 격벽의 좌표를 정해둠 ####       
    print("\n", " "*20, ":"*10, "인식된 키박스(B형)", ":"*10, "\n")         
    for key in key_blocks_B:
        if key == "num":
            num_L = key_blocks_B["num"][0][0]
            num_R = key_blocks_B["num"][1][0]
            print(" "*30, num_L,key_blocks_B["num"][5], num_R)

        if key == "addr":
            addr_L = key_blocks_B["addr"][0][0]
            addr_R = key_blocks_B["addr"][1][0]
            addr_Y = midpoint(key_blocks_B["addr"])[1]
            print(" "*30, addr_L, key_blocks_B["addr"][5], addr_R)  

        if key == "buildname":
            buildname_L = key_blocks_B["buildname"][0][0]
            buildname_R = key_blocks_B["buildname"][1][0]
            buildname_Y = midpoint(key_blocks_B["buildname"])[1]
            print(" "*30, buildname_L, key_blocks_B["buildname"][5],  buildname_R)

        if key == "landclass":
            landclass_L = key_blocks_B["landclass"][0][0]
            landclass_R = key_blocks_B["landclass"][1][0]
            print(" "*30, landclass_L, key_blocks_B["landclass"][5],  landclass_R)

        if key == "builduse":
            builduse_L = key_blocks_B["builduse"][0][0]
            builduse_R = key_blocks_B["builduse"][1][0]
            print(" "*30, builduse_L, key_blocks_B["builduse"][5], builduse_R)


        if key == "generalinfo":
            generalinfo_L = key_blocks_B["generalinfo"][0][0]
            generalinfo_R = key_blocks_B["generalinfo"][1][0]
            print(" "*30, generalinfo_L, key_blocks_B["generalinfo"][5], generalinfo_R)

        if key =="paper":
            paper_L = key_blocks_B["paper"][0][0]
            paper_R = key_blocks_B["paper"][1][0]
            print(" "*30, paper_L, key_blocks_B["paper"][5], paper_R)

        if key == "estim":
            estim_L = key_blocks_B["estim"][0][0]
            estim_R = key_blocks_B["estim"][1][0]
            estim_Y = midpoint(key_blocks_B["estim"])[1]
            print(" "*30, estim_L, key_blocks_B["estim"][5], estim_R)

        if key =="price":
            price_L = key_blocks_B["price"][0][0]
            price_R = key_blocks_B["price"][1][0]
            print(" "*30, price_L, key_blocks_B["price"][5], price_R)

        if key == "memo":
            memo_L = key_blocks_B["memo"][0][0]
            memo_R = key_blocks_B["memo"][1][0]
            print(" "*30, memo_L, key_blocks_B["memo"][5], memo_R)

    print("\n", " "*35, ":"*30, "\n") 
       
    ## 공부와 사정은 중점좌표로 누락됨이 많아, 바로 위에서 새로정리된 기준으로 잡는다.
    ## 그런데, 공부와 사정이 1)소수점을 기준으로 분리된 것들이 많고, 하이픈(-)과 같은 찌꺼기가 소수점 뒤에 붙어 있는 misreads 들이 존재
    ## 이를 바로잡는다.
    if "price" in key_blocks_B:
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


        ############ 이제 보스는 깨진 숫자의 맨처음이므로, 주변에 존재하는 residue들을 병합합니다 ######
        del_from_new_coord_box = []  #나중에 제거해야함
        completed_groups = []
        for nnd in new_no2_departed:
            completed_groups.append([nnd]) # 

            for num_residue in new_coord_box: # 

                if midpoint(num_residue)[0] < (price_R + memo_L)/2:
                    for group in completed_groups: # 
                        if 0 < (num_residue[0][0] - group[-1][1][0]) < 20 and abs(num_residue[1][1] - group[-1][1][1]) < 10: # 면접~~
                            group.append(num_residue) # 

                            del_from_new_coord_box.append(num_residue)
                            group.sort(key=lambda t: t[0][0])
                            break # 
                        else:
                            continue # 

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

        #print("최종그룹들 제거하고, 조합된 숫자들까지 모두 첨가::", num_checked_coord_box, "\n")
        #XXXXXXXXXXXXXXXXXXXXXXXXXXX B형 reading pool 정비 완료 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX




        #OOOOOOOOOOOOOOOOOOOOOOOOOOO 중요 y축 레벨 추출 OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO  

        landclass_level = []  # 중요기준 1: 지목정보  y 좌표
        price_level = []    # 중요기준 2: 평가액정보 y 좌표
        daejikwon_level = []  # 중요기준 3: 대지권정보 y 좌표
        soyoukwon_level = []  # 중요기준 4: 소유권정보 y 좌표


        for v_1 in  num_checked_coord_box:                
            if re.search("^전$|^답$|^대$", v_1[5]):   ## 향후 다양한 지목 평가시 추가"[적묘원용]지$|^도로$|\w+[야전장방천거장]$"
                if v_1[0][1] > estim_Y: # '소재지' 상의 지번 등이 교란을 일으키므로 차단
                    if "landclass" in key_blocks_B:
                        if landclass_L < midpoint(v_1)[0] < landclass_R:                        
                            landclass_level.append(midpoint(v_1)[1])

                    elif "builduse" in key_blocks_B:
                        if builduse_L < midpoint(v_1)[0] < builduse_R:                        
                            landclass_level.append(midpoint(v_1)[1])


        for v_2 in  num_checked_coord_box:
            for v_2a in  num_checked_coord_box:
                if re.search("^(\d{1,3}\,)*\d{1,3}.?\d+[-]?", v_2[5]) and re.search("^(\d{1,3}\,)*\d{1,3}.?\d+[-]?", v_2a[5]):
                    if v_2[0][1] >estim_Y and v_2a[0][1] > estim_Y:
                        # 공부, 사정의 전유면적 일치라인을 price_level로 잡음 
                        if paper_L < midpoint(v_2)[0] < estim_L and estim_L < midpoint(v_2a)[0] < price_L:   #수평으로 위치                              
                            if abs(v_2[0][1] - v_2a[0][1]) < 10 and list(v_2[5])[:1] == list(v_2a[5])[:1] and list(v_2[5])[-1:] == list(v_2a[5])[-1:]:
                                price_level.append(midpoint(v_2a)[1])
                                
                  
                
        for v_3 in num_checked_coord_box:
            if v_3[0][1] > estim_Y:
                if generalinfo_L < midpoint(v_3)[0] < generalinfo_R:   # "구분"칸에서                                                        
                    if re.search("대지권", v_3[5]):            # "대지권" 또는 "소유권" 이라는 말 중 더 아래에 있는 것이
                        daejikwon_level.append(midpoint(v_3)[1])           # 그 y값이 "대지권 레벨인데,
                    if re.search("소유권", v_3[5]):            # "대지권" 또는 "소유권" 이라는 말 중 더 아래에 있는 것이
                        soyoukwon_level.append(midpoint(v_3)[1])                             

                            
                                
        ## 평가액 레벨과 지목레벨, 대지권 레벨 중복제거하고, 크기순으로 정렬
        #if order == 1:
        no2_landclass_level = []
        
        if len(landclass_level) == 0:
            err_note = "파일명: {}__ 지목 레벨이 없습니다::".format(image_full_path)
            with open(r"D:/results/spec_errors_landclass_level.txt", 'a') as f:
                f.write("\n")
                f.write(err_note)
        else:
            for d2 in landclass_level:
                if d2 not in no2_landclass_level:
                    no2_landclass_level.append(d2)
            no2_landclass_level.sort(key=lambda t: t)


        no2_price_level = []
        if len(price_level) == 0:
            err_note = "파일명: {}__ 평가액 레벨이 없습니다::".format(image_full_path)
            with open(r"D:/results/spec_errors_price_level.txt", 'a') as f:
                f.write("\n")
                f.write(err_note)
        else:
            for p2 in price_level:
                if p2 not in no2_price_level:
                    no2_price_level.append(p2)
            no2_price_level.sort(key=lambda t: t)
            print("\n", "평가액 레벨::", no2_price_level, "\n")
            if len(no2_price_level) > 1:
                shutil.copy2(image_full_path, "D:/data/complex_specs/")


        no2_daejikwon_level = []
        if len(daejikwon_level) == 0:
            err_note = "파일명: {}__ 대지권 레벨이 없습니다::".format(image_full_path)

            with open(r"D:/results/spec_errors_daejikwon_level.txt", 'a') as f:
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
            with open(r"D:/results/spec_errors_soyoukwon_level.txt", 'a') as f:
                f.write("\n")
                f.write(err_note)
        else:
            for s2 in soyoukwon_level:
                if s2 not in no2_soyoukwon_level:
                    no2_soyoukwon_level.append(s2)
            no2_soyoukwon_level.sort(key=lambda t: t)

   

        ## Harvesting 시작 ##


        #### 일반속성 >>>> 감정평가명세표 첫장만############
        #if order == 1: # 한 파일에 여러물건 평가경우가 있어 폐기함

        b_name = []
        use_mode = []
        road_addr = []
        floor_num = []
        addr = []
        
        for adr in num_checked_coord_box:
            if abs(midpoint(adr)[1] - addr_Y) < 30 and addr_R < midpoint(adr)[0]: #'소재지'의 수평선상
                addr.append(adr)
                #if re.search(".+", adr[5]):
                    #general_attr["소재지"] = "{}".format(adr[5])

                #if re.search("^[가-힣]+\d*도$", adr[5]):   
                #    general_attr["도"] = "{}".format(adr[5])
                #    #print("도", general_attr)
                    
                #elif re.search("^[가-힣]+\d*시$", adr[5]):   
                #    general_attr["시"] = "{}".format(adr[5])
                #    #print("시", general_attr)

                        
                #elif re.search("^[가-힣]+\d*[군구]$", adr[5]):
                #    general_attr["군구"] = "{}".format(adr[5])    
                #    #print("군구", general_attr)


                #elif re.search("^[가-힣]+\d*[동]$", adr[5]):
                #    general_attr["동"] = "{}".format(adr[5])
                #    #print("동", general_attr)

                #elif re.search("^[가-힣]+\d*[면]$", adr[5]):
                #    general_attr["면"] = "{}".format(adr[5])

                #elif re.search("^[가-힣]+\d*[리]$", adr[5]):
                #    general_attr["리"] = "{}".format(adr[5])

                        
                #elif re.search("(?<=[\(\[]).+[길로]", adr[5]): # or re.search("\w+[로길]", adr[5]) : #|\w+[로길]
                #    r_name = re.search("(?<=[\(\[]).+[길로]", adr[5]).group(0)
                #    road_addr.append(r_name)

                #elif re.search("^[가-힣]+\d*[길로]", adr[5]):
                #    road_addr.append(adr[5])

                #elif re.search("\d+(?=[\)\]])", adr[5]):
                #    r_name = re.search("\d+(?=[\)\]])", adr[5]).group(0)
                #    road_addr.append(r_name)

                #elif re.search("^\d{1,4}\-?\d{1,3}$", adr[5]):
                #    general_attr["지번"] = "{}".format(adr[5])
                #    #road_addr.append(adr[5])
                #    #print("지번", general_attr)

            if abs(midpoint(adr)[1] - buildname_Y) < 30 and buildname_R < adr[0][0]:  # "건물명"의 우측 수평
                #if re.search(".+", adr[5]):
                    #general_attr["건물명"] = "{}".format(adr[5])
                b_name.append(adr)
                    

        if len(landclass_level) > 0:
            for ddr in num_checked_coord_box:
                if buildname_Y + 80 < midpoint(ddr)[1] < min(landclass_level):
                    if "landclass" in key_blocks_B:
                        if landclass_L < midpoint(ddr)[0] < landclass_R: #지목 및 용도로서 건물명보다 아래값들
                            if re.search("도시형|[아파트다세주택공동근린생활설형단지오피]{2,20}", ddr[5]):   
                                use_mode.append(ddr[5])

                        if num_R < midpoint(ddr)[0] < landclass_L:
                            if re.search("철근\w+조$|콘크\w+조$|크리\w+조$|세멘\w+조$|시멘\w+조$|시맨\w+조$", ddr[5]):   
                                general_attr["구조"] = "{}".format(ddr[5])

                            if re.search("\w+지붕|슬라브\w+붕$|경사\w+붕$", ddr[5]):   
                                general_attr["지붕"] = "{}".format(ddr[5])

                            if re.search("\d{1,3}층", ddr[5]): 
                                floor_n = re.search("\d{1,3}(?=층)", ddr[5]).group(0)
                                floor_num.append(floor_n)


                    elif "builduse" in key_blocks_B:
                        if builduse_L < midpoint(ddr)[0] < builduse_R:
                            if re.search("도시형|[아파트다세주택공동근린생활설형단지오피]{2,20}", ddr[5]):   
                                use_mode.append(ddr[5])

                        if num_R < midpoint(ddr)[0] < builduse_L:
                            if re.search("철근\w+조$|콘크\w+조$|크리\w+조$|세멘\w+조$|시멘\w+조$|시맨\w+조$", ddr[5]):   
                                general_attr["구조"] = "{}".format(ddr[5])

                            if re.search("\w+지붕|슬라브\w+붕$|경사\w+붕$", ddr[5]):   
                                general_attr["지붕"] = "{}".format(ddr[5])

                            if re.search("\d{1,3}층", ddr[5]): 
                                floor_n = re.search("\d{1,3}(?=층)", ddr[5]).group(0)
                                floor_num.append(floor_n)
                        
                    ### 참고 table_title = re.search("(?<=[\.\)\,-]).{2,25}", up[2]).group(0)

    
        ### 건물명은 조금 복잡해서 따로 처리해준다 ##
        if len(b_name) > 0:
            new_b_name = []
            b_name.sort(key=lambda t: t[0][0])
            for bnm in b_name:
                new_b_name.append(bnm[5])

        if len(addr) > 0:
            new_addr = []
            addr.sort(key=lambda t: t[0][0])
            for anm in addr:
                new_addr.append(anm[5])

        #new_road_addr = []
        #road_addr.sort(key=lambda t: t[0][0])
        #for rnm in road_addr:
        #    new_road_addr.append(rnm[5])
        #print(new_road_addr)
        # 수집된 각 항목의 리스트를 for 문 종료시 딕셔너리에 부가한다.
            

        if len(new_b_name) > 0:
            general_attr["건물명_1"] = ' '.join(new_b_name)

        if len(use_mode) > 0:
            general_attr["이용상황"] = ' '.join(use_mode)

        if len(road_addr) > 0:
            general_attr["도로명"] = ' '.join(road_addr)
        
        if len(new_addr) > 0:
            general_attr["소재지"] = ' '.join(new_addr)
                
        if len(floor_num) > 0:
            floor_num.sort(key=int) # 층수는 string이므로 이와 같이 "정수기준이라면"으로 정렬후 가장 큰 마지막 숫자 선택
            general_attr["지상 층 수"] = int(floor_num[-1])

        general_attr["페이지 ID"] = image_full_path.split('/')[-1].split('.')[0]
        spec_general_data.append(general_attr)
            

        print("\n\n", "    B형_일반속성", general_attr, "\n")

            ##############################################################





        ##  지목과 수평라인으로 토탈면적과 일련번호를 뽑는다 ## 
        if len(no2_landclass_level) > 0: # 토지속성도 지목레벨이 존재할때만 뽑음
            breaker = False       
            for ue in no2_landclass_level: # 지목에 대해 여러개인 경우까지 순회하며 각각의 데이터를 모음
                for ind, va in  enumerate(num_checked_coord_box):
         
                    if abs(midpoint(va)[1] - ue) < 100:

                        #print("지목 레벨과 유사한 값::", va, ue)

                        if  num_L < midpoint(va)[0] < generalinfo_L:
                            if re.search("\w{1,3}", va[5]):
                                land_attr["일련번호_토지"] = "{}".format(va[5]) 
                                #print(land_attr, L_list)
                        if "landclass" in key_blocks_B:
                            if  landclass_L < midpoint(va)[0] < landclass_R:
                                if re.search("^전$|답$|대$|\w+[지원야전장로방천거장]$", va[5]):
                                    land_attr["지목"] = "{}".format(va[5])                           
                                    #print(land_attr,  L_list)

                            if  landclass_R < midpoint(va)[0] < estim_L:
                                if re.search("\d+$", va[5]):
                                    land_attr["토지면적_해당필지"] = "{}".format(va[5])
                                    #print(land_attr)

                            if  generalinfo_L < midpoint(va)[0] < landclass_L:
                                if re.search("^\d{1,4}\-?\d{1,3}$", va[5]):
                                    land_attr["지번"] = "{}".format(va[5])
                                    general_attr["지번"] = "{}".format(va[5])
                                    #print(land_attr)   

                        elif "builduse" in key_blocks_B:
                            if  builduse_L < midpoint(va)[0] < builduse_R:
                                if re.search("^전$|답$|대$|\w+[지원야전장로방천거장]$", va[5]):
                                    land_attr["지목"] = "{}".format(va[5])                           
                                    #print(land_attr,  L_list)

                            if  builduse_R < midpoint(va)[0] < estim_L:
                                if re.search("\d+$", va[5]):
                                    land_attr["토지면적_해당필지"] = "{}".format(va[5])
                                    #print(land_attr)

                            if  generalinfo_L < midpoint(va)[0] < builduse_L:
                                if re.search("^\d{1,4}\-?\d{1,3}$", va[5]):
                                    land_attr["지번"] = "{}".format(va[5])
                                    general_attr["지번"] = "{}".format(va[5])
                                    #print(land_attr)  

                            
                    elif ind == len(num_checked_coord_box)-1:   ## 밸류항목을 한번탐색                     
                        breaker = True
                        break

                if breaker:
                    land_attr["페이지 ID"] = image_full_path.split('/')[-1].split('.')[0]
                    land_attr["용도지역"] = "B형은 미기재"
                    land_attr_copy = land_attr.copy() # 딕셔너리는 키밸류 integrity를 위해 append 시 카피본을 넣음                    
                    L_list.append(land_attr_copy)
                    
                    land_attr.clear()
                                             
     
        print("\n", "    B형_토지속성 ::", L_list,  "\n")

        #######################################################################################






        ###################### 빌딩 속성 추출 ############################################


        ###### 대지권 레벨이 없는 경우      

        if len(no2_daejikwon_level) == 0:
            p_breaker = False
            for dp, dpr in enumerate(no2_price_level):
                for inv1, vn in enumerate(num_checked_coord_box):

                    if abs(midpoint(vn)[1]- dpr) < 50: #  vn은 평가액라인 속으로 좁힘. 
                        
                        if price_L < vn[0][0] < price_R:       
                            if re.search("^(\d{1,3}\,)+\d{1,3}$", vn[5]):
                                building_attr["감정평가액"] =  "{}".format(vn[5])                                                      
                                #print("감정평가액::", vn[5], building_attr, B_list)

                        if midpoint(vn)[0] < generalinfo_L:
                            #print("일련번호_건물::", vn[5])
                            if re.search("\w{1,3}", vn[5]):
                                building_attr["일련번호_건물"] = "{}".format(vn[5])    
                                #print("일련번호_건물::", building_attr, B_list)

                        if paper_L < vn[0][0] < (paper_R + estim_L)/2:       
                            if re.search("^(\d{1,3}\,)*\d{1,3}.?\d+[-]?$", vn[5]):
                                building_attr["공부_전유면적"] =  "{}".format(vn[5]) 

                        if estim_L < vn[0][0] < (estim_R + price_L)/2:       
                            if re.search("^(\d{1,3}\,)*\d{1,3}.?\d+[-]?$", vn[5]):
                                building_attr["사정_전유면적"] =  "{}".format(vn[5]) 
                                    
                        if num_R < midpoint(vn)[0] < landclass_L:       
                            if re.search("호$", vn[5]):
                                building_attr["호"] =  "{}".format(vn[5])  
                                #print("호::", building_attr, B_list)

                            if re.search("층$", vn[5]):
                                building_attr["층"] =  "{}".format(vn[5]) 
                                #print("층::", building_attr, B_list)
                       

                    if inv1 == len(num_checked_coord_box)-1:   ## 밸류항목에 대한 한번 순회로 위 필터에 다 걸리게 되어 있다.       
                        #print("한 번 순회 완료")
                        p_breaker = True
                        break

                if p_breaker:
                    building_attr["페이지 ID"] = image_full_path.split('/')[-1].split('.')[0]
                    building_attr["대지권면적_사정"] = "대지권 항목 없음"
                    building_attr_copy = building_attr.copy()
                    B_list.append(building_attr_copy) 
                    
                    building_attr.clear()
 

 
        ###### 대지권 레벨이 있는 경우    
                    
        if len(no2_daejikwon_level) > 0:

            p_breaker = False
            for dp, dpr in enumerate(no2_price_level):
                for da, dae in enumerate(no2_daejikwon_level):
                    for inv1, vn in enumerate(num_checked_coord_box):
                        for inv2, v_5 in enumerate(num_checked_coord_box):

                            if abs(midpoint(vn)[1]- dpr) < 50 : #  vn은 평가액라인 속으로 좁힘. 
                        
                                if price_L < vn[0][0] < price_R:       
                                    if re.search("^(\d{1,3}\,)+\d{1,3}$", vn[5]):
                                        building_attr["감정평가액"] =  "{}".format(vn[5])                                                      
                                        #print("감정평가액::", vn[5], building_attr, B_list)

                                if midpoint(vn)[0] < generalinfo_L:
                                    if re.search("\w{1,3}", vn[5]):
                                        building_attr["일련번호_건물"] = "{}".format(vn[5])    
                                        #print("일련번호_건물::", building_attr, B_list)


                                if paper_L < vn[0][0] < (paper_R + estim_L)/2:       
                                    if re.search("^(\d{1,3}\,)*\d{1,3}.?\d+[-]?$", vn[5]):
                                        building_attr["공부_전유면적"] =  "{}".format(vn[5]) 

                                if estim_L < vn[0][0] < (estim_R + price_L)/2:       
                                    if re.search("^(\d{1,3}\,)*\d{1,3}.?\d+[-]?$", vn[5]):
                                        building_attr["사정_전유면적"] =  "{}".format(vn[5]) 

                                        if re.search("^(\d{1,3}\,)*\d{1,3}.?\d+[-]?$", v_5[5]) and estim_L < midpoint(v_5)[0] < price_L:
                                            if v_5[0][1] > vn[0][1] + 20 and dp == da:
                                                building_attr["대지권면적_사정"] = "{}".format(v_5[5]) ## 사정_전유면적 아래에 존재하는 수
                                                #print("대지권면적_사정::", v_5[5])
                                if "landclass" in key_blocks_B:
                                    if num_R < midpoint(vn)[0] < landclass_L:       
                                        if re.search("호$", vn[5]):
                                            building_attr["호"] =  "{}".format(vn[5])  
                                            #print("호::", building_attr, B_list)

                                        if re.search("층$", vn[5]):
                                            building_attr["층"] =  "{}".format(vn[5]) 
                                            #print("층::", building_attr, B_list)
                                elif "builuse" in key_blocks_B:
                                    if num_R < midpoint(vn)[0] < builuse_L:
                                        if re.search("호$", vn[5]):
                                            building_attr["호"] =  "{}".format(vn[5])  
                                            #print("호::", building_attr, B_list)

                                        if re.search("층$", vn[5]):
                                            building_attr["층"] =  "{}".format(vn[5]) 
                                            #print("층::", building_attr, B_list)

                            if inv1 == len(num_checked_coord_box)-1:   ## 밸류항목에 대한 한번 순회로 위 필터에 다 걸리게 되어 있다.       
                                print("한 번 순회 완료")
                                p_breaker = True
                                break

                if p_breaker:
                    building_attr["페이지 ID"] = image_full_path.split('/')[-1].split('.')[0]
                    building_attr_copy = building_attr.copy()
                    B_list.append(building_attr_copy) 
                    
                    building_attr.clear()

        
        if len(B_list)==0:
            
            berr_note = "파일명: {}__ 건물속성이 모아지지 않았습니다::".format(idir)
            with open(r"D:/results/spec_errors.txt", 'a') as f:
                f.write("\n")
                f.write(berr_note)

        print("    B형_건물속성 :: ",B_list, "\n")


    return (spec_general_data, B_list, L_list)

    #except:
        #spec_B_errors.append(image_full_path)

        #new_spec_B_errors = []
        #for nsg in spec_B_errors:
        #    if nsg not in new_spec_B_errors:
        #        new_spec_B_errors.append(nsg)

        #for sne in new_spec_B_errors:
        #    with open(r"D:/results/spec_B_errors.txt", 'a') as s:
        #        s.write("\n")
        #        s.write(str(sne))
