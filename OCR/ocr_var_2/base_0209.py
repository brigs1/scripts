
import math, re
from itertools import filterfalse, tee, islice, chain
from statistics import mean
from difflib import SequenceMatcher

def this_and_next(some_iterable):
    this, nexts = tee(some_iterable, 2) # 첫째인수는 이터러블, 두번째는 만들고자하는 복사본 갯수, 한번 사용된 레퍼런스는 더 이상 값을 참조하지 않음
    this = chain(this, nexts)
    nexts = chain(islice(nexts, 1, None), [None])
    return zip(this, nexts)

def string_num_Sort(e):
    ne = e.split('.')[0].split('_')[1]
    return int(ne)

def get_mid_distance(coord1, coord2): #coord = [x, y] 중점좌표 기준
    # mid 좌표계만 해당
    distance = math.dist((coord1[0],coord1[1]), (coord2[0], coord2[1]))
    return distance

def get_mid_angle(coord1, coord2): #coord = [x, y] 중점좌표 기준
    # mid 좌표계만 해당
    x = coord1[0] - coord2[0]
    y = coord2[1] - coord1[1]
    radian = math.atan2(y, x)
    degree = radian * 180 / math.pi    
    return degree

def midpoint(raw_coord): #중점좌표계로 변환
    # raw 좌표계만 해당
    #print(raw_coord)
    mid_x = (raw_coord[0][0]+raw_coord[2][0])/2
    mid_y = (raw_coord[0][1]+raw_coord[2][1])/2
    mid = [mid_x, mid_y, raw_coord[5]]
    return mid


def mid_merge(element1, element2):
    # mid 좌표계만 해당
    mid_merged = [(element1[0]+element2[0])/2, (element1[1]+element2[1])/2, element1[2]+element2[2]]
    return mid_merged

def mid_underbar_merge(element1, element2):
    # mid 좌표계만 해당
    mid_merged = [(element1[0]+element2[0])/2, (element1[1]+element2[1])/2, element1[2]+ "__" + element2[2]]
    return mid_merged


def raw_x_merge(element1, element2):
    # raw 좌표계만 해당
    #if len(element1[5]) > 1 and len(element2[5]) > 1:
    #    raw_x_merged = [element1[0], [element2[1][0], element1[1][1]], [element2[2][0], element1[2][1]], element1[3], element1[4], element1[5] + element2[5]]
    #    return raw_x_merged
    #else:
    raw_x_merged = [element1[0], [element2[1][0], element1[1][1]], [element2[2][0], element1[2][1]], element1[3], element1[4], element1[5] + element2[5]]
    return raw_x_merged

def raw_num_x_merge(element1, element2):
    # raw 좌표계만 해당
    raw_x_merged = [element1[0], [element2[1][0], element1[1][1]], [element2[2][0], element1[2][1]], element1[3], element1[4], element1[5] + element2[5]]
    return raw_x_merged

def raw_y_merge(element1, element2):
    # raw 좌표계만 해당
    if len(element1[5]) > 1 and len(element2[5]) > 1  and re.search("\D+", element1[5]) and re.search("\D+", element2[5]):
        raw_y_merged = [element1[0], element1[1], [element1[1][0], element2[2][1]], [element1[1][0], element2[3][1]], element1[4], element1[5] +"_"+ element2[5]]
        return raw_y_merged
    else:
        raw_y_merged = [element1[0], element1[1], [element1[1][0], element2[2][1]], [element1[1][0], element2[3][1]], element1[4], element1[5] + element2[5]]
        return raw_y_merged
    

def remove_duplicate_list(old_list, new_list):
    new_list = []
    for x in old_list:
        if x not in new_list:
            new_list.append(x)
    return new_list


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


@run_once
def merge_lists(list1, list2):
    sum_list = list1 + list2
    new_list = []
    for el in sum_list:
        if el not in new_list:
            new_list.append(el)
    return new_list


def group_near_coord(source_iter, x, y, result_groups):
    result_groups = []
    for coord in source_iter:
        found_group = False
                        
        for group in result_groups:
            for end_member in group:
                #print("에러발생?" , end_member, coord)
                if abs(end_member[0] - coord[0]) < x and abs(end_member[1] - coord[1]) < y:                    
                    group.append(coord)
                    found_group = True                                    
                    break
                    
                elif found_group:
                    break

        if not found_group:
            result_groups.append([coord])        
    return result_groups


def group_near_coord_raw(source_iter, x, y, result_groups):
    result_groups = []
    for coord in source_iter:
        found_group = False
                        
        for group in result_groups:
            for end_member in group:
                #print("에러발생?" , end_member, coord)
                if abs(end_member[0][0] - coord[0][0]) < x and abs(end_member[0][1] - coord[0][1]) < y:
                    
                    group.append(coord)
                    found_group = True                                    
                    break
                    
                elif found_group:
                    break

        if not found_group:
            result_groups.append([coord])        
    return result_groups


def merge_near_coord(source_iter, result):
    ## 박스모드 >> 그룹별로 합하여 명사구를 완성 : 1차 상하 머징
    result = []

    for group in source_iter:
        group.sort(key=lambda t: t[1])

        #merged_1.append(mean(merged_y))
        #merged_1.append([lambda i,j: i+j, merged_text)

        for_merge_x = []
        for_merge_y =[]
        for_merge_text = []

        for element in group:
            for_merge_x.append(element[0])
            for_merge_y.append(element[1])
            for_merge_text.append(element[2])
        X = int(mean(for_merge_x))
        Y = int(mean(for_merge_y))
        T = ' '.join(for_merge_text)

        result.append([X, Y, T])
        result.sort(key=lambda t : t[1])
            
    return result

def concatanate(list_in_list):
    for this, next in this_and_next(list_in_list):
        if next != None:
            match = SequenceMatcher(None, this[2],next[2]).find_longest_match(0, len(this[2]), len(next[2]))

    return this[2][match.a: match.a + match.size]

def raw_x3_merge(a, b, c):
    x3 = [a[0], c[1], c[2], a[3], a[4], a[5]+ b[5]+c[5]]
    return x3

def split(word):
    return [char for char in word]