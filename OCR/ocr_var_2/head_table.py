from coord import *
import re, os


def head_table(idir, image_file, image_full_path, new_coord_line, new_coord_box): 
    target_js = r"D:/results/var_2/"
    #print("\n", " "*30, "::: 감정평가표 분석시작 :::", "\n\n")
 
    head_errors = []
    head_data = []
    head_attr = {}
    

    #try:
       
            
    ## 숫자 이산가족 바로잡기 :: 박스로 인식한 경우, 화폐단위, 날짜가 쉼표, 마침표를 기점으로 쪼개지는 현상 바로잡기 ## 삭제>> bachup_OCR/최초의 통합본.py 참고
        
    #######  기본항목 리딩  #######
    for base_key in new_coord_line:
        if re.search("\w+감정원$|\w법인$|\w법인(주)$|\w사무소$", base_key[5]):
            head_attr["법인명"] = base_val[5]
            print("법인명 : {}".format(base_val[5]))

        for base_val in new_coord_line:
            
            if re.search("목\s?적$", base_key[5]):                    
                if re.search("경\s?매|담\s?보|거\s?래|매\s?매|공\s?매|일\s?반", base_val[5]) and 175 < get_mid_angle(midpoint(base_key), midpoint(base_val)) <= 180 or -180 < get_mid_angle(midpoint(base_key), midpoint(base_val)) < -175:
                        
                    head_attr["평가목적"] = base_val[5]
                    print("평가목적 : {}".format(base_val[5]))                

            elif re.search("시\s?점$|기\s?준\s?시\s?점$", base_key[5]):                    
                if re.search("[20]\d{2}[.,]\s?\d{1,2}[.,]\s?\d{1,2}[.,]?", base_val[5]) and 80 < get_mid_angle(midpoint(base_key), midpoint(base_val)) < 100:
                    head_attr["기준시점"] = base_val[5]
                    print("기준시점 : {}".format(base_val[5]))
    
    # with open(target_js + os.path.splitext(image_file)[0]+".json", 'w', encoding="UTF-8") as ht: #"
    #     ht.write(str(head_attr))



    head_attr["페이지 ID"] = image_full_path.split('/')[-1].split('.')[0]
    head_data.append(head_attr)

    
    return head_data


    # except:
        
        
    #     head_errors.append(image_full_path)

    #     nhead_errors = []
    #     for ng in head_errors:
    #         if ng not in nhead_errors:
    #             nhead_errors.append(ng)

    #     for nhe in nhead_errors:
    #         with open(r"D:/results/var_2/head_errors.txt", 'a') as h:
    #             h.write("\n")
    #             h.write(str(nhe))

    
            
