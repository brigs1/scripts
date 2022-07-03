from coord import *
import re, os


class HeadTable():
    def __init__(self, idir, image_file, image_full_path, new_coord_line, new_coord_box):

        self.idir=idir
        self.image_file=image_file
        self.image_full_path=image_full_path
        self.new_coord_line=new_coord_line
        self.new_coord_box=new_coord_box

        self.head_errors = []
        self.head_data = []
        self.head_attr = {"평가목적":None, "기준시점":None}

    def head_table(self): 

        target_js = r"D:/results/forDL/jsons/"
        print("\n", " "*30, "::: 감정평가표 분석시작 :::", "\n\n")

        #try:      
                
            ## 숫자 이산가족 바로잡기 :: 박스로 인식한 경우, 화폐단위, 날짜가 쉼표, 마침표를 기점으로 쪼개지는 현상 바로잡기 ## 삭제>> bachup_OCR/최초의 통합본.py 참고
                
            #######  기본항목 리딩  #######
        for base_key in self.new_coord_line:
            for base_val in self.new_coord_line:
                
                if re.search("목\s?적$", base_key[5]):                    
                    if re.search("경\s?매|담\s?보|거\s?래|매\s?매|공\s?매|일\s?반", base_val[5]) and 175 < get_mid_angle(midpoint(base_key), midpoint(base_val)) <= 180 or -180 < get_mid_angle(midpoint(base_key), midpoint(base_val)) < -175:
                        print("평가목적발견!!!", base_val[5])    
                        self.head_attr["평가목적"] = base_val[5]
                        
                        print(self.head_attr)                

                elif re.search("시\s?점$|기\s?준\s?시\s?점$", base_key[5]):                    
                    if re.search("[20]\d{2}[.,]\s?\d{1,2}[.,]\s?\d{1,2}[.,]?", base_val[5]) and 80 < get_mid_angle(midpoint(base_key), midpoint(base_val)) < 100:
                        self.head_attr["기준시점"]=base_val[5]
                        print(self.head_attr)
        
        with open(target_js + os.path.splitext(self.image_file)[0]+".json", 'w', encoding="UTF-8") as ht: #"
            ht.write(str(self.head_attr))



        self.head_attr["평가서 ID"] = self.idir
        self.head_data.append(self.head_attr)

        
        return self.head_data


        # except:
            
        #     self.head_errors.append(self.image_full_path)

        #     nhead_errors = []
        #     for ng in self.head_errors:
        #         if ng not in nhead_errors:
        #             nhead_errors.append(ng)

        #     for nhe in nhead_errors:
        #         with open(r"D:/results/parsed/head_errors.txt", 'a') as h:
        #             h.write("\n")
        #             h.write(str(nhe))

        
                
