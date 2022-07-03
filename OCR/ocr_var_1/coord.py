
from SynapOCR import *
from base_0209 import *

API_KEY = "SNOCR-36f14f097af546af86ab05c525ef82f5"
API_ENDPOINT = "http://10.0.0.37:62975"
ocrEngine = SynapOCR(API_ENDPOINT, API_KEY)


def engine(image_full_path):
    global ret_line
                ###### OCR 엔진구동 #####
    ret_line = ocrEngine.post_ocr(image=open(image_full_path,'rb'),type="upload", boxes_type="line", textout=True, extract_table=False, recog_form=False)
    
global new_coord_line, new_coord_box

def coord(image_full_path):
    """
    ############ 이미지 >> box mode, line mode 좌표계 생성 ####################
    """
    global raw_coord_line, mid_coord_line, new_coord_box, mid_coord_box, new_coord_line
    raw_coord_line = ret_line['result']['line_boxes'] 

    ###### OCR 모드 1 : line #####
    new_coord_line = []
    for xo in raw_coord_line:
        # OCR raw 결과물의 소수점아래 숫자 줄이기(이 모드에만 해당)
        #each_line = [[int(xo[0][0]),int(xo[0][1])],[int(xo[1][0]),int(xo[1][1])],[int(xo[2][0]),int(xo[2][1])],[int(xo[3][0]),int(xo[3][1])],xo[4], xo[5]]
        each_line = [[int(xo[0][0]),int(xo[0][1])],[int(xo[1][0]),int(xo[1][1])],[int(xo[2][0]),int(xo[2][1])],[int(xo[3][0]),int(xo[3][1])],xo[4], xo[5]]
        new_coord_line.append(each_line)
        new_coord_line.sort(key=lambda t: t[0][1])

    #print("라인_소수점 정리::::", new_coord_line, "\n") 

    ###### OCR 모드 1 >> midpoint 좌표계로 변환 #####
    mid_coord_line = []
    for ncl in new_coord_line:
        mid_coord_line.append(midpoint(ncl))
    #print("중점_라인::::", mid_coord_line, "\n")   


    ##### OCR 모드 2 : box (띄어쓴 글자뭉치 인식) #####
    ret_box = ocrEngine.post_ocr(image=open(image_full_path,'rb'),type="upload", boxes_type="block", textout=True, extract_table=False, recog_form=False)
    raw_coord_box = ret_box['result']['block_boxes']            
    #print("개별박스 수정전::::", raw_coord_box, "\n")

    new_coord_box = []
    for xo in raw_coord_box:
        # OCR raw 결과물의 소수점아래 숫자 줄이기(이 모드에만 해당)
        #each_line = [[int(xo[0][0]),int(xo[0][1])],[int(xo[1][0]),int(xo[1][1])],[int(xo[2][0]),int(xo[2][1])],[int(xo[3][0]),int(xo[3][1])],xo[4], xo[5]]
        each_line = [[int(xo[0][0]),int(xo[0][1])],[int(xo[1][0]),int(xo[1][1])],[int(xo[2][0]),int(xo[2][1])],[int(xo[3][0]),int(xo[3][1])],xo[4], xo[5]]
        new_coord_box.append(each_line)
        new_coord_box.sort(key=lambda t: t[0][1])

    ###### OCR 모드 2 >> midpoint 좌표계로 변환 #####
    mid_coord_box = []
    for nb in raw_coord_box:
        mid_coord_box.append(midpoint(nb))
    #print("중점_박스::::", mid_coord_box, "\n") 

    ##### OCR 모드 3 : raw (낱글자) ##### 2022. 2월 중순 이후 문의하여 업데이트 가능여부 확인할 것
    #ret_raw = ocrEngine.post_ocr(image=open(image_full_path,'rb'),type="upload", boxes_type="raw", textout=True, extract_table=False, recog_form=False)
    #print("로우모드:::", ret_raw)
    #raw_coord_raw = ret_box['result']['block_boxes']            
    #print("개별박스 수정전::::", raw_coord_box, "\n")
    
    return new_coord_line, new_coord_box
