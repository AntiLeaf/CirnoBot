from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""

    priority = 114514 # 没必要先处理
    repeat_times = 5