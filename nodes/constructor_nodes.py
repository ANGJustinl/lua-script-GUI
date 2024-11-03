from ryvencore import Node
from ryvencore.NodePortType import NodeInputType, NodeOutputType

from DES_model import DES_Model


def add_line(self, line):
    self.code_lines.append(line)

def generate_code(self):
    return "\n".join(self.code_lines)

# 定义事件名称函数
class DES_init_Node(Node):
    """
    初始化LuaFauDES
    """
    title = 'DES 初始化节点'
    version = 'v1.0'
    init_inputs = []
    init_outputs = [
        NodeOutputType(label='初始化代码', data_type=str),
    ]

    def update_event(self, input_called=-1):
        self.code_lines = []
        description = "--\n-- Construct By Script\n--"
        variables_init = "local n, name, index"
        DES_init = "DES=faudes.Generator()\nDes:Clear()"
        tick_init = f"local ev_T = DES:InsEvent(\"tick\")"
        add_line(description)
        add_line(self, variables_init)
        add_line(self, DES_init)
        add_line(self, tick_init)
        code = generate_code(self)
        self.set_output_val(0, code)

class Event_Node(Node):
    '''
    若输入了上一事件代码，则在上一事件代码的基础上添加事件定义代码；
    若没有输入上一事件代码，则直接添加事件定义代码。
    
    :param Former_Event: 上一事件代码
    :param Event_Name: 事件名称
    '''
    title = '事件定义节点'
    version = 'v1.0'
    init_inputs = [
        NodeInputType(label='上一事件代码', data_type=str),
        NodeInputType(label='事件名称', data_type=str),
    ]
    init_outputs = [
        NodeOutputType(label='事件代码', data_type=str),
    ]

    def update_event(self, input_called=-1):
        self.code_lines = []
        Former_Event = self.input(0).payload
        Event_Name = self.input(1).payload
        if Former_Event:
            Event_Out = Former_Event+f"local ev_{Event_Name}_i = DES:InsEvent(string.format('{Event_Name}_\%\d', par_i)(Coati.i))"
        else:
            Event_Out = f"local ev_{Event_Name}_i = DES:InsEvent(string.format('{Event_Name}_\%\d', par_i)(Coati.i))"
        add_line(self, Event_Out)
        code = generate_code(self)
        self.set_output_val(0, code)

class State_Node(Node):
    '''
    若输入了上一状态代码，则在上一状态代码的基础上添加状态定义代码；
    若没有输入上一状态代码，则直接添加状态定义代码。

    :param Former_State: 上一状态代码
    :param State_Name: 状态名称
    :param Init_State: 是否是初始状态
    '''
    title = '状态定义节点'
    version = 'v1.0'
    init_inputs = [
        NodeInputType(label='上一状态代码', data_type=str),
        NodeInputType(label='状态名称', data_type=str),
        NodeInputType(label='是否是初始状态', data_type=bool, default=False),
    ]
    init_outputs = [
        NodeOutputType(label='状态代码', data_type=str),
    ]

    def update_event(self, input_called=-1):
        self.code_lines = []
        Former_State = self.input(0).payload
        State_Name = self.input(1).payload
        if Former_State:
            Event_Out = Former_State+f"local st_{State_Name}i = DES:InsState(string.format(\"y_{State_Name}_%d\", Coati.i))"
        else:
            Event_Out = f"local st_{State_Name}i = DES:InsState(string.format(\"y_{State_Name}_%d\", Coati.i))"
        if self.input(2).value:
            State_Init = f"DES:InsInitState(st_{State_Name})\nDES:InsMarkedState(st_{State_Name})"
            add_line(self, State_Init)
            add_line(self, Event_Out)
            code = generate_code(self)
            self.set_output_val(0, code)
            return
        add_line(self, Event_Out)
        code = generate_code(self)
        self.set_output_val(0, code)

class Create_Index_Node(Node):
    '''
    定义索引状态查找表节点

    :param Former_Index: 上一状态查找表代码
    :param Index_Lookup_Name: 状态查找表名称
    :param Var_Name: 索引变量名称
    :param Index_Number: 索引数字序号
    '''
    title = '定义状态查找表节点'
    version = 'v1.0'
    init_inputs = [
        NodeInputType(label='上一状态查找表代码', data_type=str),
        NodeInputType(label='状态查找表名称', data_type=str),
        NodeInputType(label='索引变量名称', data_type=str),
        NodeInputType(label='索引数字序号', data_type=int, default=1),
    ]
    init_outputs = [
        NodeOutputType(label='状态查找表代码', data_type=str),
    ]

    def update_event(self, input_called=-1):
        self.code_lines = []
        Former_Index = self.input(0).payload
        Index_Lookup_Name = self.input(1).payload
        Var_Name = self.input(2).payload
        Index_Number = self.input(3).payload
        if Former_Index:
            line1 = Former_Index+f"local st_{Index_Lookup_Name}"+" = {}"
            line2 = f"for n = {Index_Number}, Coati.{Index_Lookup_Name} do"
            line3 = f"st_{Index_Lookup_Name}[n] = coat:InsState(string.format(\"{Var_Name}_\%\d\", n))end"
        else:
            line1 = f"local st_{Index_Lookup_Name}"+" = {}"
            line2 = f"for n = {Index_Number}, Coati.{Index_Lookup_Name} do"
            line3 = f"st_{Index_Lookup_Name}[n] = coat:InsState(string.format(\"{Var_Name}_\%\d\", n))end"
        add_line(self, line1)
        add_line(self, line2)
        add_line(self, line3)
        code = generate_code(self)
        self.set_output_val(0, code)

class Set_Transition_Node(Node):
    '''
    设置状态转移节点
    '''
    title = '设置状态转移节点'
    version = 'v1.0'
    init_inputs = [
        NodeInputType(label='var1', data_type=str),
        NodeInputType(label='var2', data_type=str),
        NodeInputType(label='var3', data_type=str),
    ]
    init_outputs = [
        NodeOutputType(label='状态转移代码', data_type=str),
    ]

    def update_event(self, input_called=-1):
        self.code_lines = []
        Var1 = self.input(0).payload
        Var2 = self.input(1).payload
        Var3 = self.input(2).payload
        Event_Out = f"DES:SetTransition({Var1}, {Var2}, {Var3})"
        add_line(self, Event_Out)
        code = generate_code(self)
        self.set_output_val(0, code)

# 定义涂层模型节点
class Model_Node(Node):
    title = '模型构建节点'
    version = 'v1.0'
    init_inputs = [
        NodeInputType(label='模型名称前缀', data_type=str),
        NodeInputType(label='初始化代码', data_type=str),
        NodeInputType(label='事件代码', data_type=str),
        NodeInputType(label='状态代码', data_type=int),
        NodeInputType(label='状态查找表代码', data_type=int),
        NodeInputType(label='其他代码', data_type=int),
    ]
    init_outputs = [
        NodeOutputType(label='输出模型代码', data_type=str),
    ]
    def update_event(self, input_called=-1):
        Model_Name = self.input(0).payload
        DES_Init_Code = self.input(1).payload
        Event_Code = self.input(2).payload
        State_Code = self.input(3).payload
        Index_Code = self.input(4).payload
        Other_Code = self.input(5).payload

        Model_Name = f"DES:Name(string.format(\"{Model_Name}_\%\d\", par_i)(Coati.i))"
        Model_Code = "function Model(Coati)\n"+DES_Init_Code+Event_Code+State_Code+Index_Code+Other_Code+Model_Name+"return DES\nend"
        self.set_output_val(0, Model_Code)

class Construct_Model_Node(Node):
    """
    构造模型节点

    :param Model_Name: 模型名称
    :param DES_Init_Code: 初始化代码
    :param Event_Code: 事件代码
    :param State_Code: 状态代码
    :param Index_Code: 状态查找表代码
    :param Other_Code: 其他代码
    :return: [模型名称, 模型代码]
    """
    title = '模型构建节点'
    version = 'v1.0'
    init_inputs = [
        NodeInputType(label='模型代码', data_type=str),
    ]
    init_outputs = [
        NodeOutputType(label='模型输出', data_type=list),
    ]
    def update_event(self, input_called=-1):
        Model_Name = self.input(0).payload
        DES_Init_Code = self.input(1).payload
        Event_Code = self.input(2).payload
        State_Code = self.input(3).payload
        Index_Code = self.input(4).payload
        Other_Code = self.input(5).payload

        Model_Name = f"DES:Name(string.format(\"{Model_Name}_\%\d\", par_i)(Coati.i))"
        Model_Code = "function Model(Coati)\n"+DES_Init_Code+Event_Code+State_Code+Index_Code+Other_Code+Model_Name+"return DES\nend"
        self.set_output_val(0, [Model_Name, Model_Code])

class Save_Model_Node(Node):
    title = '模型保存节点'
    version = 'v1.0'
    init_inputs = [
        NodeInputType(label='模型输出', data_type=list),
        NodeInputType(label='模型保存路径', data_type=str),
    ]
    def update_event(self, input_called=-1):
        des_model = DES_Model
        Model_Name, Model_Code = self.input(0).payload
        Model_Save_Path = self.input(1).payload
        des_model.save_model(model_name=Model_Name, model_code=Model_Code, file_path=Model_Save_Path)
        self.set_output_val(0, Model_Code)

def export_nodes():
    return [
        DES_init_Node,
        Event_Node,
        Event_Node,
        State_Node,
        Create_Index_Node,
        Set_Transition_Node,
        Construct_Model_Node,
        Save_Model_Node
    ]