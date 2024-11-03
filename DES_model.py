import yaml
import uuid
from datetime import datetime
from logger import logger

class DES_Model:
    """
    .desmodel模型类
    用于保存和加载.desmodel模型文件, 并提供模型代码转换为Lua代码的功能。
    """
    def __init__(self):
        self.meta_data = {}
        self.model_code = ""
        self.model_data = {
            'meta_data': self.meta_data,
            'code': self.model_code
        }
        
    def save_model(self, model_name, model_code, file_path="./output_model.desmodel"):
        """
        保存模型到.DESmodel文件

        :param model_name: 模型名称
        :param model_code: 模型代码
        :param file_path: 模型文件路径
        :return: True
        """
        # Add meta data to model
        self.meta_data['name'] = model_name
        self.meta_data['uuid'] = str(uuid.uuid4())
        self.meta_data['build_time'] = datetime.now().isoformat()
        model_data = {
            'meta_data': self.meta_data,
            'code': model_code
        }
        print(model_data)

        # Write to YAML file
        with open(file_path, 'w') as f:
            yaml.dump(model_data, f, encoding="utf-8")
            logger.info(f"Saved model to {file_path}")
            logger.info(f"Model Meta Data: {self.model_data['meta_data']}")

        return True


    def load_model(self, file_path="./output_model.desmodel") -> str:
        """
        从.DESmodel模型文件中加载模型代码

        :param file_path: 模型文件路径
        :return: 模型代码
        """
        try:
            with open(file_path, 'r') as f:
                self.model_data = yaml.safe_load(f)
                logger.info(f"Loaded model from {file_path}")
                logger.info(f"Model Meta Data: {self.model_data['meta_data']}")
                return self.model_data['code']
        except FileNotFoundError:
            logger.error(f"The file {file_path} does not exist.")
            return None
        except yaml.YAMLError as exc:
            logger.error(f"Error parsing YAML file: {exc}")
            return None
        
    def to_lua(self, lua_code, lua_file_path="./output_model.lua"):
        # Write the Lua code to a .lua file
        with open(lua_file_path, 'w') as lua_file:
            lua_file.write(lua_code)