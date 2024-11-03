import subprocess
from ryvencore import Node
from ryvencore.NodePortType import NodeInputType, NodeOutputType

from DES_model import DES_Model


def add_line(self, line):
    self.code_lines.append(line)

def generate_code(self):
    return "\n".join(self.code_lines)

class Load_Model_Node(Node):
    """
    加载现有模型
    """
    title = '加载现有模型'
    version = 'v1.0'
    init_inputs = [
        NodeInputType(label='模型路径', data_type=str),
    ]
    init_outputs = [
        NodeOutputType(label='模型代码', data_type=str),
    ]

    def update_event(self, input_called=-1):
        des_model = DES_Model()
        path = self.input(0).payload
        model = des_model.load_model(path)
        self.set_output_val(0, model)

class example_Operation_Node(Node):
    """
    示例模型操作节点
    """
    title = '示例模型操作节点'
    version = 'v1.0'
    init_inputs = [
        NodeInputType(label='前置操作代码[列表]', data_type=list),
        NodeInputType(label='数量', data_type=int),
        NodeInputType(label='步骤索引', data_type=str),
        NodeInputType(label='涂层用时', data_type=str),
        NodeInputType(label='加热用时', data_type=str),
        NodeInputType(label='滴落用时', data_type=str),
        NodeInputType(label='涂层持续时间', data_type=str),
        NodeInputType(label='模型名称', data_type=str)
    ]
    init_outputs = [
        NodeOutputType(label='操作代码[列表]', data_type=list),
    ]

    def update_event(self, input_called=-1):
        former_code = self.input(0).payload
        g = self.input(1).payload
        i = self.input(2).payload
        Put_glass_coater_time = self.input(3).payload
        Put_glass_heater_time = self.input(4).payload
        Drop_time = self.input(5).payload
        Coating_time = self.input(6).payload
        model_name = self.input(7).payload
        # 生成操作代码
        code = f"DES = {model_name}"+"({"+f" g = {g}, i = {i}, Put_glass_coater_time = {Put_glass_coater_time}, Put_glass_heater_time = {Put_glass_heater_time}, Drop_time = {Drop_time}, Coating_time = {Coating_time}"" })"
        if former_code:
            code_list = former_code + [code]
        else:
            code_list = [code]
        self.set_output_val(0, code_list)

class Simulation_Node(Node):
    """
    DES运行节点
    """
    title = '模型运行节点'
    version = 'v1.0'
    init_inputs = [
        NodeInputType(label='模型代码', data_type=str),
        NodeInputType(label='操作代码[列表]', data_type=list),
        NodeInputType(label="luafaudes路径", data_type=str)
    ]
    def update_event(self, input_called=-1):
        des_model = DES_Model()
        model_code = self.input(0).payload
        operation_code_list = self.input(1).payload
        des_path = self.input(2).payload

        code = ""
        # list to str
        for operation_code in operation_code_list:
            code = code + operation_code + "\n"
        code = "function Simulation()\n"+ code +"end\n"

        des_model.to_lua(code, './output/temp.lua')
        result = subprocess.run([des_path, './output/temp.lua'])
        if result.returncode == 0:
            return result.stdout.decode('utf-8') 
        else:
            raise Exception(result.stderr.decode('utf-8'))
            return
        
def export_nodes():
    return [
        Load_Model_Node,
        example_Operation_Node,
        Simulation_Node
    ]