def add_custom_code(input_code, code):
    """
    添加自定义代码

    :param input_code: 前置代码
    :param code: 自定义代码
    :return: 合并后的代码
    """
    # check if code has /n at the end, if not add it
    if code.find("\n") != -1:
        return input_code+code
    else:
        return input_code+code+"\n"

def add_custom_var(input_code, var_name, var_value):
    """
    添加自定义变量

    :param input_code: 前置代码
    :param var_name: 变量名
    :param var_value: 变量值
    :return: 合并后的代码
    """
    if var_value == None:
        return input_code+f"local {var_name} = {var_value}\n"
    else:
        return input_code+f"local {var_name}\n"

def add_custom_for_loop(input_code, for_var, loop_code):
    """
    添加自定义for循环  

    for {for_var} do
		{loop_code}
	end
    
    :param input_code: 前置代码
    :param for_var: 循环变量
    :param loop_code: 循环代码
    :return: 合并后的代码
    """
    return input_code+f"for {for_var} do\n{loop_code}\nend\n"

def add_custom_if_loop(input_code, if_condition, loop_code):
    """
    添加自定义if语句  

    :param input_code: 前置代码
    :param if_condition: if条件
    :param loop_code: if代码
    :return: 合并后的代码
    """
    """
    if {if_condition} then
        {loop_code}
    end
    """
    return input_code+f"if {if_condition} then\n{loop_code}\nend\n"
