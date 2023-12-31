import numpy as np
import random as rd
import keyboard
import warnings
import os
from time import sleep
warnings.filterwarnings('ignore') # 忽略numpy的警告


global game_array
game_array = np.zeros([4,4])
fixed_number = [2,4]
random_list = [0,1]


def basic_operate(array):    # 默认向下
    #获取按列分割的数组,并进行迭代
    print("----------------------------------------------------------------")
    process_array = np.hsplit(array,4)
    collapse = np.zeros([4,4])
    #print(process_array)    # OK
    for i in [0,1,2,3]:  # i 为列标号
        #进行零元排序,把0都放在左边
        arr = process_array[i]
        # 将非零元素和零元素分别提取并排序
        non_zero_elements = arr[arr != 0].flatten()
        zero_elements = arr[arr == 0].flatten()

        # 合并排序后的非零元素和零元素
        sorted_arr = np.concatenate((zero_elements, non_zero_elements))

        # 将结果重新整形成原始数组的形状
        sorted_arr = sorted_arr.reshape(arr.shape)
        
        
        sub = sorted_arr
        a = sub[0] == sub[1]
        b = sub[1] == sub[2]
        c = sub[2] == sub[3]
        d = sub[0] != sub[1] and sub[1] != sub[2] and sub[2] != sub [3]
             
        if a :
                if a and b and c :  #[2,2,2,2] -> [0,0,4,4]
                    collapse[0][i] = 0
                    collapse[1][i] = 0
                    collapse[2][i] = sub[0] *2
                    collapse[3][i] = sub[2] *2
                    
                elif a and b :      #[2,2,2,4] -> [0,2,4,4]
                    collapse[0][i] = 0
                    collapse[1][i] = sub[0]
                    collapse[2][i] = sub[1] + sub[2]
                    collapse[3][i] = sub[3]
    
                elif a and c :      #[2,2,4,4] -> [0,0,4,8]
                    collapse[0][i] = 0
                    collapse[1][i] = 0
                    collapse[2][i] = sub[0] + sub[1]
                    collapse[3][i] = sub[2] + sub[3]
                    
                else:               #[2,2,4,2] -> [0,4,4,2]
                    collapse[0][i] = 0
                    collapse[1][i] = sub[0] *2
                    collapse[2][i] = sub[2]
                    collapse[3][i] = sub[3]
        if  b :
                
                if b and c :        # [4,2,2,2] -> [0,4,2,4]
                    collapse[0][i] = 0
                    collapse[1][i] = sub[0]
                    collapse[2][i] = sub[1]
                    collapse[3][i] = sub[2] *2
                
                else:               # [4,2,2,4] -> [0,4,4,4]
                    collapse[0][i] = 0
                    collapse[1][i] = sub[0]
                    collapse[2][i] = sub[1] *2
                    collapse[3][i] = sub[3]        
        if c :                      #[2,4,2,2] -> [0,2,4,4]
                collapse[0][i] = 0
                collapse[1][i] = sub[0]
                collapse[2][i] = sub[1]
                collapse[3][i] = sub[2] *2
        
        if d: 
                collapse[0][i] = sub[0]
                collapse[1][i] = sub[1]
                collapse[2][i] = sub[2]
                collapse[3][i] = sub[3] 
        
    display_array = collapse.astype(int)    # 转换为整型数组            # OK
    return display_array
   
def down_operate(arr):
        display_array = basic_operate(arr)
        return display_array
                                               
def  right_operate(arr):
        array  = np.rot90(arr, -1)
        a = basic_operate(array)
        display_array = np.rot90(a,1)
        return display_array                       
    
def up_operate(arr):
        array  = np.rot90(arr, -2)
        a = basic_operate(array)
        display_array = np.rot90(a,2)
        return display_array
        
def left_operate(arr):
        array  = np.rot90(arr, -3)
        a = basic_operate(array)
        display_array = np.rot90(a,3)
        return display_array
                     
def array_operate(n):
    for i in range(n):
        postions_row = rd.randint(0,3)
        postions_column = rd.randint(0,3)
        
        value = rd.choice(fixed_number)
        game_array[postions_row][postions_column] = value

def check_avilable_position():
   
    global avilable_positions_array
    avilable_positions_array = np.zeros([4,4]) 
    avilable_positions_array = np.argwhere(game_array==0)
    
def from_available_position_generate():
    check_avilable_position()
    ##
    global position
    shape = np.shape(avilable_positions_array)
    row_number = shape[0] - 1
    try:
        
        
        position = rd.randint(0,row_number)
        random_position_array = avilable_positions_array[position,:]
        value = rd.choice(fixed_number)
        game_array[random_position_array[0]][random_position_array[1]] = value
        
          
    except ValueError or IndexError:
        print("no space warning ! maybe you have died,press q to exit ")
        
def main():
    array_operate(2)
    global game_array
    print(game_array)
    condition = True
    while condition:

            if keyboard.is_pressed("down"):
                game_array = down_operate(game_array)
                from_available_position_generate()
                print(game_array)
                sleep(0.15)

            elif keyboard.is_pressed("up"):
                game_array = up_operate(game_array)
                from_available_position_generate()
                print(game_array)
                sleep(0.15)
            elif keyboard.is_pressed("left"):
                game_array = left_operate(game_array)
                from_available_position_generate()
                print(game_array)
                sleep(0.15)
            elif keyboard.is_pressed("right"):
                game_array = right_operate(game_array)
                from_available_position_generate()
                print(game_array)
                sleep(0.15)
            elif keyboard.is_pressed("q"):
                print('Good game！')
                condition = False

main()

