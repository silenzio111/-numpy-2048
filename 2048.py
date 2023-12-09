import numpy as np
import random as rd
import keyboard
import warnings
import os
from time import sleep
warnings.filterwarnings('ignore') # 忽略numpy的警告,如果不加,numpy会警告将来有一天会不支持部分操作,详情请去掉这行代码运行查看


global game_array
game_array = np.zeros([4,4])
fixed_number = [2,4]
random_list = [0,1]


def basic_operate(array):    # 默认向下
    #获取按列分割的数组,并进行迭代
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
        
        # 这里偷懒了,用了比较笨的方法实现数字的相消
        sub = sorted_arr
        a = sub[0] == sub[1]
        b = sub[1] == sub[2]
        c = sub[2] == sub[3]
        d = sub[0] != sub[1] and sub[1] != sub[2] and sub[2] != sub [3]
        # 直接穷举所有情况,并对游戏数组进行修改,正因为这样,才写的这么长     
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
#定义完基本的消去操作,然后进行具体的实现

def down_operate(arr):     #下
        display_array = basic_operate(arr)
        return display_array
    
# 只用旋转数组,处理完再转回来就可以了                                               
def  right_operate(arr):    #右
        array  = np.rot90(arr, -1)
        a = basic_operate(array)
        display_array = np.rot90(a,1)
        return display_array                       
    
def up_operate(arr):        #上
        array  = np.rot90(arr, -2)
        a = basic_operate(array)
        display_array = np.rot90(a,2)
        return display_array
        
def left_operate(arr):       #左
        array  = np.rot90(arr, -3)
        a = basic_operate(array)
        display_array = np.rot90(a,3)
        return display_array
    
# 这个函数名没起好,实际上是初始化数组后向数组添加两个元素                     
def array_operate(n):
    for i in range(n):
        postions_row = rd.randint(0,3)
        postions_column = rd.randint(0,3)
        
        value = rd.choice(fixed_number)
        game_array[postions_row][postions_column] = value
# 如名字
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
        
        v = False    #发送状态码
        return v
          
    except ValueError or IndexError:
        
        v = True
        return v
 
 # 刷新终端
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def update_terminal():
    clear_terminal()
    print("----------------")  # 上边框
    for i, row in enumerate(game_array):
        # 打印每一行的内容
        for j, value in enumerate(row):
            if j < len(row) - 1:
                # 打印数字，除了最后一列
                print(f" {get_colored_char(value)} ", end="")
            else:

                print(f" {get_colored_char(value)}")
    
    print("----------------")    #下边框
    v = from_available_position_generate() #get game conditon
    if v : print("no space warning ! maybe you have died,press q to exit ")

#设置数字的颜色
def get_colored_char(value):
    color = get_color(value)
    if value != 0:
        return f"\033[38;5;{color}m{value:2}\033[0m"
    else:
        return "  "

def get_color(value):
    # 根据不同的数字返回不同的颜色代码
    if value == 2:
        return 214
    elif value == 4:
        return 220
    elif value == 8:
        return 226
    elif value == 16:
        return 202
    elif value == 32:
        return 196
    elif value == 64:
        return 160
    elif value == 128:
        return 126
    elif value == 256:
        return 82
    elif value == 512:
        return 46
    elif value == 1024:
        return 27
    elif value == 2048:
        return 21
    else:
        return 15  # 默认白色

# 主程序    
def main():
    array_operate(2)
    global game_array
    update_terminal()
    condition = True
    while condition:

            if keyboard.is_pressed("down"):
                game_array = down_operate(game_array)
                from_available_position_generate()
                update_terminal()
                sleep(0.15)

            elif keyboard.is_pressed("up"):
                game_array = up_operate(game_array)
                from_available_position_generate()
                update_terminal()
                sleep(0.15)
            elif keyboard.is_pressed("left"):
                game_array = left_operate(game_array)
                from_available_position_generate()
                update_terminal()    
                sleep(0.15)
            elif keyboard.is_pressed("right"):
                game_array = right_operate(game_array)
                from_available_position_generate()
                update_terminal()   
                sleep(0.15)
            elif keyboard.is_pressed("q"):
                print('Good game！')
                condition = False
# 2048启动
main()

