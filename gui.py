import streamlit as st
from barfi import st_barfi, Block, barfi_schemas
#from barfinew import st_barfi, Block, barfi_schemas

# Set Streamlit page config
st.set_page_config(page_title="Lua Gui", layout="wide")

# Load & Save schemas
saved_schemas = barfi_schemas()
select_schema = st.selectbox('Select a saved schema:', saved_schemas)


Init_Node = Block(name='1.1初始化节点')
Init_Node.add_output(name='Init_1')
def Init_func(self):
    DES_init = "DES=faudes.Generator()\nDes:Clear()\n"
    self.set_interface(name='Init_1', value=4)
Init_Node.add_compute(Init_func)


Def_Tick_Name_Node = Block(name='2.1定义时间戳')
Def_Tick_Name_Node.add_output(name='EventTick()')
Def_Tick_Name_Node.add_option(name='Tick_Name', type='input', value='输入时间戳名称')
def Def_Tick_Name_func(self):
    tick_name = self.get_option(name='Tick_Name')
    func_out = "function EventTick()\nreturn '{tick_name}'\nend\n".format(tick_name)
    self.set_interface(name='Tick_Name', value=func_out)
Def_Tick_Name_Node.add_compute(Def_Tick_Name_func)


Def_Event_Node = Block(name='2.2定义事件')
Def_Event_Node.add_output(name='Event')
Def_Event_Node.add_option(name='Event_Name', type='input', value='输入事件名称')
#Def_Event_Node.add_option(name='Event_Is_Repeatable', type='checkbox', value=True)
def Def_Event_func(self):
    event_name = str(self.get_option(name='Event_Name'))+"_"
    #if self.get_option(name='Event_Is_Repeatable'):
    #    evnet_out = "function Event{}(par_i)\nreturn string.format('{}\%\d',par_i)\nend".format(event_name)
    #else:
    #    evnet_out = "function Event{}()\nreturn string.format('{}')\nend".format(event_name)
    #evnet_out = "local ev_{} = Faudes:InsEvent(EventPut_glass_in_Coater(Coati.i))".format(event_name)
    evnet_out = f"local ev_{event_name} = coat:InsEvent({event_name}(string.format('{event_name}\%\d',Coati.i)))"
    self.set_interface(name='Event', value=evnet_out)
Def_Event_Node.add_compute(Def_Event_func)


Constructor_Node = Block(name='最终构造脚本节点')
Constructor_Node.add_input(name='Init_1')
Constructor_Node.add_input(name='Tick_Name')
Constructor_Node.add_input(name='Events')
Constructor_Node.add_output(name='Lua_Code')
def Constructor_func(self):
    Before_code = "--\n-- Construct By Script\n--\n-- The below functions define event names in the notation used in our paper\n--"
    Init_1 = self.get_interface(name='Init_1')
    Tick_Name = self.get_interface(name='Tick_Name')
    Lua_code = 114514
    self.set_interface(name='Lua_Code', value=Lua_code)
    st.write(1)
Constructor_Node.add_compute(Constructor_func)

compute_engine = st.checkbox('Activate barfi compute engine', value=True)

#barfi_result = st_barfi(base_blocks={"起始节点": [Init_Node],"定义": [Def_Tick_Name_Node, Def_Event_Node, Def_Event_Variable_Node], "最终节点": Constructor_Node})
barfi_result = st_barfi(base_blocks= {'起始节点': [Init_Node], '定义节点': [Def_Tick_Name_Node, Def_Event_Node], "最终节点": [Constructor_Node]}, load_schema=select_schema, compute_engine=compute_engine)

#st.write(barfi_result)