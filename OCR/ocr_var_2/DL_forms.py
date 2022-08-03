from matplotlib.style import available
import torch, re

def DL_specA(image_full_path, num_checked_coord_box):

    
    model = torch.hub.load('ultralytics/yolov5', 'custom', '/media/y/850EVO/tries/once/yolov5/runs/train/exp/weights/last.pt')
    model.conf = 0.05
    # Images
    imgs = [image_full_path]  # batch of images

    # Inference
    results = model(imgs)

    ##### Results ######
    #results.print()
    ## >> Speed: 20.7ms pre-process, 6.2ms inference, 1.3ms NMS per image at shape (1, 3, 672, 480)

    #results.save()  # or .show()
    #results.show()  # or .show()

    #results.xyxy[0]  # img1 predictions (tensor)
    xy = results.pandas().xyxy[0]  # img1 predictions (pandas)
    #print("xy:::::::::::", xy)

    #xy.set_index(['name'], inplace = True) # 생성된 xy라는 데이터프레임, [addr_1, addr_2, floor_ho, price]의 레이블을 인덱스로 변경
    xy_conf = xy.sort_values(by=['name','confidence'], ascending=False).drop_duplicates(subset=['name'], keep='first')
    #print("xy_conf:::::::::::", xy_conf)
    
    DL_specA_Bld_info = []
    
    DL_specA_Bld_attr = {}
    xy_1 = xy_conf.reset_index()
    
    if (xy_1['name']=='addr_1').any():  # DL로 infer된 이미지, 그 결과에 addr_2가 존재한다면.. > 단수와 복수로 나누어야 하겠다.
        #print("addr_1 존재!!!", )
        xy_1.set_index(['name'], inplace = True)       
        addr_1_xmin = xy_1.loc['addr_1', ['xmin']].values[0]
        addr_1_xmax = xy_1.loc['addr_1', ['xmax']].values[0]
        addr_1_ymin = xy_1.loc['addr_1', ['ymin']].values[0]
        addr_1_ymax = xy_1.loc['addr_1', ['ymax']].values[0]
        
        DL_addr = []
        for ncc in num_checked_coord_box:
            if addr_1_xmin < ncc[0][0] and ncc[2][0] < addr_1_xmax:
                if addr_1_ymin < ncc[0][1] and ncc[2][1] < addr_1_ymax:
                    
                    DL_addr.append(ncc[5])
                  

                    if re.search("^[가-힣]+\d*도$", ncc[5]):   
                        DL_specA_Bld_attr["도"] = "{}".format(ncc[5])
                   

                    elif re.search("^[가-힣]+\d*시$", ncc[5]):   
                        DL_specA_Bld_attr["시"] = "{}".format(ncc[5])
                   
                        
                    elif re.search("^[가-힣]+\d*[군구]$", ncc[5]):
                        DL_specA_Bld_attr["군구"] = "{}".format(ncc[5])  
                                           

                    elif re.search("^[가-힣]+\d{1,2}[동가]$|^[가-힣]{,4}동$", ncc[5]):
                        DL_specA_Bld_attr["동"] = "{}".format(ncc[5])
                   

                    elif re.search("^[가-힣]+\d*[면]$", ncc[5]):
                        DL_specA_Bld_attr["면"] = "{}".format(ncc[5])
                   

                    elif re.search("^[가-힣]+\d*[리]$", ncc[5]):
                        DL_specA_Bld_attr["리"] = "{}".format(ncc[5])
          

                    elif re.search("[스텔파트빌라맨션숀택]", ncc[5]):
                        DL_specA_Bld_attr["건물명_1"] = "{}".format(ncc[5])      

                    elif re.search("\d동|제?에이동|제?비동|제?시동|제?씨동", ncc[5]):
                        DL_specA_Bld_attr["건물동"] =  "{}".format(ncc[5])                         


    xy_2 = xy_conf.reset_index() 

    if (xy_2['name']=='addr_2').any():  # DL로 infer된 이미지, 그 결과에 addr_2가 존재한다면.. > 단수와 복수로 나누어야 하겠다.
        #print("addr_2 존재!!!")
        xy_2.set_index(['name'], inplace = True) 
        #print("xy_2", xy_2)
      
        try:
            addr_2_xmin = xy_2.loc['addr_2', ['xmin']].values[0]
            addr_2_xmax = xy_2.loc['addr_2', ['xmax']].values[0]
            addr_2_ymin = xy_2.loc['addr_2', ['ymin']].values[0]
            addr_2_ymax = xy_2.loc['addr_2', ['ymax']].values[0]
        except:
            pass

        DL_addrnum = []
        for ncc in num_checked_coord_box:
            if addr_2_xmin < ncc[0][0] and  ncc[2][0] < addr_2_xmax:
                if addr_2_ymin < ncc[0][1] and  ncc[2][1] < addr_2_ymax:
                    if re.search("\d{,4}\-\d{,2}|^\d{,4}$", ncc[5]):

                        
                        DL_addrnum.append(ncc[5])
                    
                        DL_addrnum_set = set(DL_addrnum)
                        DL_addrn = ", ".join(str(e) for e in DL_addrnum_set)
                        DL_specA_Bld_attr["지번"] = "{}".format(DL_addrn)

                    elif re.search("^[가-힣]+\d*시$", ncc[5]):   
                        DL_specA_Bld_attr["시"] = "{}".format(ncc[5])
                      
                        
                    elif re.search("^[가-힣]+\d*[군구]$", ncc[5]):
                        DL_specA_Bld_attr["군구"] = "{}".format(ncc[5])  
                              

                    elif re.search("^[가-힣]+\d{1,2}[동가]$|^[가-힣]{,4}동$", ncc[5]):
                        DL_specA_Bld_attr["동"] = "{}".format(ncc[5])
                     

                    elif re.search("^[가-힣]+\d*[면]$", ncc[5]):
                        DL_specA_Bld_attr["면"] = "{}".format(ncc[5])
                       

                    elif re.search("^[가-힣]+\d*[리]$", ncc[5]):
                        DL_specA_Bld_attr["리"] = "{}".format(ncc[5])
                        

                    elif re.search("[스텔파트빌라맨션숀택]", ncc[5]):
                        DL_specA_Bld_attr["건물명_1"] = "{}".format(ncc[5])      

                    elif re.search("\d동|제?에이동|제?비동|제?시동|제?씨동", ncc[5]):
                        DL_specA_Bld_attr["건물동"] =  "{}".format(ncc[5])   


    xy_3 = xy_conf.reset_index() 
    if (xy_3['name']=='price').any():

        #print("감정평가액 존재!!!", ncc[5])
        
        xy_3.set_index(['name'], inplace = True) 
        price_xmin = xy_3.loc['price', ['xmin']].values[0]
        price_xmax = xy_3.loc['price', ['xmax']].values[0]
        price_ymin = xy_3.loc['price', ['ymin']].values[0]
        price_ymax = xy_3.loc['price', ['ymax']].values[0]
        #print("프라이스 민맥스", price_xmin, price_ymax)


        for ncc in num_checked_coord_box:
            if price_xmin - 10 < ncc[0][0] and  ncc[2][0] < price_xmax + 10:
                if price_ymin - 10 < ncc[0][1] and  ncc[2][1] < price_ymax + 50:
                    if re.search("^(\d{1,3}\,)+\d{1,3}$", ncc[5]):
                        #print({"감정평가액":ncc[5]})
                        DL_specA_Bld_attr["감정평가액"] = "{}".format(ncc[5])

            if price_xmin - 10 < ncc[0][0] and  ncc[2][0] < price_xmax + 10:
                if price_ymin - 100 < ncc[0][1] and  ncc[2][1] < price_ymax + 100:
                    if re.search("\d동|제?에이동|제?비동|제?시동|제?씨동", ncc[5]):
                        #print({"건물동":ncc[5]})
                        DL_specA_Bld_attr["건물동"] = "{}".format(ncc[5])

            if price_xmin - 10 < ncc[0][0] and  ncc[2][0] < price_xmax + 10:
                if price_ymin - 100 < ncc[0][1] and  ncc[2][1] < price_ymax + 100:
                    if re.search("\d층", ncc[5]):
                        #print({"층":ncc[5]})
                        DL_specA_Bld_attr["층"] = "{}".format(ncc[5])  

            if price_xmin - 10 < ncc[0][0] and  ncc[2][0] < price_xmax + 10:
                if price_ymin - 100 < ncc[0][1] and  ncc[2][1] < price_ymax + 100:
                    if re.search("\d호", ncc[5]):
                        #print({"호":ncc[5]})
                        DL_specA_Bld_attr["호"] = "{}".format(ncc[5])



    DL_specA_Bld_attr["페이지 ID"] = "{}".format(image_full_path.split("/")[-1].split(".")[0])                                  
    # print("DL_specA_Bld_attr", DL_specA_Bld_attr)
    # print("DL_specA를 빠져나감!!!")
    #DL_specA_Bld_info.append(DL_specA_Bld_attr)

    return DL_specA_Bld_attr