from barfi import st_barfi, Block

Init_Node = Block(name='初始化节点')
Init_Node.add_output(name='Init_1')
def Init_func(self):
    self.set_interface(name='Init_1', value=4)
Init_Node.add_compute(Init_func)

Def_Tick_Name_Node = Block(name='定义时间戳')
Def_Tick_Name_Node.add_output(name='EventTick()')
Def_Tick_Name_Node.add_option(name='Tick_Name', type='input', value='输入时间戳名称')
def Def_Tick_Name_func(self):
    tick_name = self.get_option(name='Tick_Name')
    func_out = "function EventTick()\nreturn '{tick_name}'\nend\n".format(tick_name)
    self.set_interface(name='Tick_Name', value=func_out)
Def_Tick_Name_Node.add_compute(Def_Tick_Name_func)

Def_Event_Node = Block(name='定义事件')
Def_Event_Node.add_output(name='Event')
Def_Event_Node.add_option(name='Event_Name', type='input', value='输入事件名称')
Def_Event_Node.add_option(name='Event_Is_Repeatable', type='checkbox', value='输入事件名称')
#Def_Event_Node.add_option(name='Event_Name', type='input', value='输入事件名称')
def Def_Tick_Name_func(self):
    tick_name = self.get_option(name='Tick_Name')
    evnet_out = "function EventTick()\nreturn '{tick_name}'\nend".format(tick_name)
    self.set_interface(name='Tick_Name', value=evnet_out)
Def_Event_Node.add_compute(Def_Tick_Name_func)

Constructor_Node = Block(name='最终构造函数节点')
Constructor_Node.add_input(name='Init_1')
def Constructor_func(self):
    Before_code = "--\n-- Construct By Script\n--\n-- The below functions define event names in the notation used in our paper\n--"
    Init_1 = self.get_interface(name='Init_1')
    self.set_interface(name='Init_1', value=4)
Constructor_Node.add_compute(Constructor_func)

st_barfi(base_blocks=[Init_Node, Def_Tick_Name_Node, Constructor_Node])