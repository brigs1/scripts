from coord import *
import re
from body_base_table import *



def treat_body(idir, image_full_path, new_coord_line, new_coord_box):
    body_errors = []
    body_general_data = []
    try:

        print("\n", "."*30, "본문표(=body_table) 처리 시작", "."*30, "\n")

        ### 소제목 라인들 리스트 구축  ###

        title_line = []
        breaker = False
        delete_from_mcl = []
        for me in new_coord_line:
            ### 현페이지에서 소제목 형식을 갖는 라인 탐색
            ### 제목번호와 제목이 따로 떨어져 있는 버그를 찾아 붙여주기

            if re.search("^([\(])?([0-9가나다라마바사아자차ㄱㄴㄷIVXivx]*)([-\)\.\,])$",  me[5]) and not re.search("[)\]]?\s?감\s?정\s?평\s?가\s?명?\s?세?\s?표?$", me[5]) and me[0][1] < 400: # 페이지 상단부에서 찾기:

                for rest_me in new_coord_line: 
                    if 175 < get_mid_angle(me, rest_me) <= 180 or -180 < get_mid_angle(me, rest_me) <= -175:
                        if get_mid_distance(me, rest_me) <= 800:                               

                            delete_from_mcl.append(me)
                            delete_from_mcl.append(rest_me)
                            mid_coord_line.append(mid_merge(me, rest_me))
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
                        body_general_attr = treat_base_table(idir, image_full_path, new_coord_box, new_coord_line, up_limit, down_limit)
                        
                        if len(body_general_attr) == 0:
                            print("body_general_attr 출력사항 없음")
                            
                            #continue

                        else:
                            #print("", body_general_attr)
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
                        body_general_attr = treat_base_table(idir, image_full_path, new_coord_box, new_coord_line, up_limit, down_limit)
                        


                        if len(body_general_attr) == 0:
                            print("body_general_attr 항목이 발견되지 않음")
                            #continue
                        else:
                            print("body_general_attr", body_general_attr)
                            body_general_data.append(body_general_attr)

                    #elif re.search("^([\(])?([0-9가나다라마바사아자차ㄱㄴㄷIVXivx]*)([-\)\.\,])\s?(비교|인근|유사).+(거래\s?사례$)", up[2]): # 거래사례표 처리
                    #    treat_deal_case_table()
                    #elif re.search("^([\(])?([0-9가나다라마바사아자차ㄱㄴㄷIVXivx]*)([-\)\.\,])\s?(가치|개별)?.+(요인\s?비교치?)", up[2]): # 개별요인비교표 처리
                    #    treat_factor_comparison_table()
                    #pass
        print("\n", "."*30, "본문표(=body_table) 처리 끝", "."*30, "\n")     
        
        return body_general_data

    except:
        body_errors.append(image_full_path)

        new_body_errors = []
        for nsg in body_errors:
            if nsg not in new_body_errors:
                new_body_errors.append(nsg)

        for sne in new_body_errors:
            with open(r"D:/results/body_errors.txt", 'a') as s:
                s.write("\n")
                s.write(str(sne))











































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

    #                elif re.search("\w{1,8}동$", can_val[5]):
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



