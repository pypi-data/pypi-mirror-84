def copy_from_clipboard():
    import pandas as pd
    import time
    try:
        # print('开始读取粘贴板')
        local_time = time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime(time.time()))
        df = pd.read_clipboard()
        df.to_excel(r"C:\Users\smadmin\Desktop\%s.xlsx"%str(local_time),index=False)
        print('成功生成xlsx文件,路径是:C:\\Users\\smadmin\\Desktop')
    except Exception as e:
        print(e)

def apply_sum(init_data, sum_name, col_list):
    init_data[sum_name] = 0
    for col in col_list:
        init_data[sum_name] += init_data[col]
    return init_data

def transform_muti_columns(init_data):
    init_data.columns = [str(i[0]) if i[1] == '' else str(i[1]) for i in init_data.columns.values.tolist()]
    return init_data