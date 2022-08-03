from coord import *
import re
#from body_base_table import *


def top_gun_for_addr(idir, image_full_path, new_coord_box, new_coord_line, up_limit, down_limit):
    body_Bld_attr = {}
    addr = []
    group_dict = {}

    for vg in new_coord_box:
        if up_limit < vg[0][1] < down_limit:
     
            if re.search("^[가-힣]+\d*도$", vg[5]):   
                addr.append(vg)
                #body_Bld_attr["도"] = "{}".format(vg[5])

            elif re.search("^[가-힣]+\d*시$", vg[5]):  
                addr.append(vg) 
                #body_Bld_attr["시"] = "{}".format(vg[5])
                
            elif re.search("^[가-힣]+\d*[군구]$", vg[5]):
                addr.append(vg)
                #body_Bld_attr["군구"] = "{}".format(vg[5])                        

            elif re.search("^[가-힣]+\d{1,2}[동]$|^[가-힣]{,4}동$", vg[5]):
                addr.append(vg)
                #body_Bld_attr["동"] = "{}".format(vg[5])

            elif re.search("^[가-힣]+\d*[면]$", vg[5]):
                addr.append(vg)
                #body_Bld_attr["면"] = "{}".format(vg[5])

            elif re.search("^[가-힣]+\d*[리]$", vg[5]):
                addr.append(vg)
                #body_Bld_attr["리"] = "{}".format(vg[5])  

            elif re.search("^\d{,4}\-\d{,2}$|^\d{,4}$", vg[5]):   #지번::: [가-힣]{3,20}|\d+[동]$
                addr.append(vg)
                #body_Bld_attr["지번"] = "{}".format(vg[5])

            elif re.search("\d동", vg[5]):  
                group_dict["건물동"] = "{}".format(vg[5])

            elif re.search("\d층", vg[5]):  
                group_dict["층"] = "{}".format(vg[5])

            elif re.search("\d호", vg[5]):  
                group_dict["호"] = "{}".format(vg[5])



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
            
            for vg in group:
                #print("바디::여기 건물동/층호/ 정보있나 좀 봐", vg)
                
                if re.search("^[가-힣]+\d*도$", vg[5]):                       
                    group_dict["도"] = "{}".format(vg[5])
                    #print("group_dict", group_dict)

                elif re.search("^[가-힣]+\d*시$", vg[5]):                       
                    group_dict["시"] = "{}".format(vg[5])
                    #print("group_dict", group_dict)
                    
                elif re.search("^[가-힣]+\d*[군구]$", vg[5]):                    
                    group_dict["군구"] = "{}".format(vg[5]) 
                    #print("group_dict", group_dict)                       

                elif re.search("^[가-힣]+\d{1,2}[동]$|^[가-힣]{,4}동$", vg[5]):                    
                    group_dict["동"] = "{}".format(vg[5])
                    #print("group_dict", group_dict)

                elif re.search("^[가-힣]+\d*[면]$", vg[5]):                    
                    group_dict["면"] = "{}".format(vg[5])
                    #print("group_dict", group_dict)

                elif re.search("^[가-힣]+\d*[리]$", vg[5]):                    
                    group_dict["리"] = "{}".format(vg[5])
                    #print("group_dict", group_dict)  

                elif re.search("\d{,4}\-\d{,2}|^\d{2,4}$", vg[5]):   #[가-힣]{3,20}|\d+[동]$                    
                    group_dict["지번"] = "{}".format(vg[5])
                    #print("group_dict", group_dict)

                elif re.search("\d동", vg[5]):  
                    group_dict["건물동"] = "{}".format(vg[5])

                elif re.search("\d층", vg[5]):  
                    group_dict["층"] = "{}".format(vg[5])

                elif re.search("\d호", vg[5]):  
                    group_dict["호"] = "{}".format(vg[5])
                    #print("group_dict", group_dict)



            if "건물동" in group_dict and "지번" in group_dict: # 이상한 것들이 많으나, 해당 키와 같이 제대로 잡힌경우:
                body_Bld_attr["페이지 ID"] = image_full_path.split('/')[-1].split('.')[0]
                body_Bld_attr.update(group_dict)
                
                #print("body_Bld_attr", body_Bld_attr)
                return body_Bld_attr


def treat_body(idir, image_full_path, new_coord_line, new_coord_box):
    body_errors = []
    body_Bld_info = []
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

                    body_Bld_attr = top_gun_for_addr(idir, image_full_path, new_coord_box, new_coord_line, up_limit, down_limit)
                    
                    # if len(body_Bld_attr) == 0:
                    #     print("body_Bld_attr 출력사항 없음")
                        
                    #     #continue

                    # else:
                    print("대상물건표를 발견해서, 넣으려고 합니다 body_Bld_attr", body_Bld_attr)
                    body_Bld_info.append(body_Bld_attr)
                        
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
                    body_Bld_attr = top_gun_for_addr(idir, image_full_path, new_coord_box, new_coord_line, up_limit, down_limit)
                    


                    # if len(body_Bld_attr) == 0:
                    #     print("body_Bld_attr 항목이 발견되지 않음")
                    #     #continue
                    # else:
                    print("body_Bld_attr", body_Bld_attr)
                    body_Bld_info.append(body_Bld_attr)

                #elif re.search("^([\(])?([0-9가나다라마바사아자차ㄱㄴㄷIVXivx]*)([-\)\.\,])\s?(비교|인근|유사).+(거래\s?사례$)", up[2]): # 거래사례표 처리
                #    treat_deal_case_table()
                #elif re.search("^([\(])?([0-9가나다라마바사아자차ㄱㄴㄷIVXivx]*)([-\)\.\,])\s?(가치|개별)?.+(요인\s?비교치?)", up[2]): # 개별요인비교표 처리
                #    treat_factor_comparison_table()
                #pass
    print("\n", "."*30, "본문표(=body_table) 처리 끝", "."*30, "\n")     
    
    return body_Bld_info