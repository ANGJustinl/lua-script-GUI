from ryvencore import Node
from ryvencore.NodePortType import NodeInputType, NodeOutputType

from extra_func import add_custom_code, add_custom_var, add_custom_if_loop, add_custom_for_loop

class Add_Custom_Code_Node(Node):
    title = '自定义代码节点'
    init_inputs = [
        NodeInputType(label='Input Code'),
        NodeInputType(label='Custom Code'),
    ]
    init_outputs = [
        NodeOutputType(label='Merged Code'),
    ]

    def update_event(self, input_called=-1):
        input_code = self.input(0).payload
        code = self.input(1).payload
        merged_code = input_code + code if '\n' in code else input_code + code + '\n'
        self.set_output_val(0, merged_code)

class AddCustomVarNode(Node):
    title = '添加自定义变量'
    init_inputs = [
        NodeInputType(label='Input Code'),
        NodeInputType(label='Variable Name'),
        NodeInputType(label='Variable Value'),
    ]
    init_outputs = [
        NodeOutputType(label='Merged Code'),
    ]

    def update_event(self, input_called=-1):
        input_code = self.input(0).payload
        var_name = self.input(1).payload
        var_value = self.input(2).payload if self.input(2).payload is not None else ''
        merged_code = input_code + f"local {var_name} = {var_value}\n"
        self.set_output_val(0, merged_code)

class AddCustomForLoopNode(Node):
    title = '添加自定义for循环'
    init_inputs = [
        NodeInputType(label='Input Code'),
        NodeInputType(label='Loop Variable'),
        NodeInputType(label='Loop Code'),
    ]
    init_outputs = [
        NodeOutputType(label='Merged Code'),
    ]

    def update_event(self, input_called=-1):
        input_code = self.input(0).payload
        for_var = self.input(1).payload
        loop_code = self.input(2).payload
        merged_code = input_code + f"for {for_var} do\n{loop_code}\nend\n"
        self.set_output_val(0, merged_code)

class AddCustomIfLoopNode(Node):
    title = '添加自定义if语句'
    init_inputs = [
        NodeInputType(label='Input Code'),
        NodeInputType(label='If Condition'),
        NodeInputType(label='If Code'),
    ]
    init_outputs = [
        NodeOutputType(label='Merged Code'),
    ]

    def update_event(self, input_called=-1):

        input_code = self.input(0).payload
        if_condition = self.input(1).payload
        loop_code = self.input(2).payload
        merged_code = input_code + f"if {if_condition} then\n{loop_code}\nend\n"
        self.set_output_val(0, merged_code)

def export_nodes():
    return [
        Add_Custom_Code_Node,
        AddCustomVarNode,
        AddCustomForLoopNode,
        AddCustomIfLoopNode,
    ]