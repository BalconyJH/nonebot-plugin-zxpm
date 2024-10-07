from pathlib import Path

from nonebot import get_plugin_config
from nonebot_plugin_localstore import get_data_dir
from pydantic import BaseModel, model_validator

DATA_DIR = get_data_dir("nonebot_plugin_zxpm")


class Config(BaseModel):
    zxpm_data_path: str | None | Path = None
    """数据存储路径"""
    zxpm_db_url: str | None = None
    """DB_URL"""
    zxpm_notice_info_cd: int = 300
    """群/用户权限检测等各种检测提示信息cd，为0时不提醒"""
    zxpm_ban_reply: str = "才不会给你发消息."
    """用户被ban时回复消息，为空时不回复"""
    zxpm_ban_level: int = 5
    """使用ban功能的对应权限"""
    zxpm_switch_level: int = 1
    """群组插件开关管理对应权限"""
    zxpm_admin_default_auth: int = 5
    """群组管理员默认权限"""
    zxpm_font: str = "msyh.ttc"
    """字体"""

    @model_validator(mode="before")
    def check_data_path(cls, values):
        if values.get("zxpm_data_path") is None:
            values["zxpm_data_path"] = DATA_DIR

        if isinstance(values.get("zxpm_data_path"), str):
            values["zxpm_data_path"] = Path(values["zxpm_data_path"])

        return values

    @model_validator(mode="before")
    def check_db_url(cls, values):
        if values.get("zxpm_db_url") is None:
            values["zxpm_db_url"] = f"sqlite:{DATA_DIR / 'db' / 'zxpm.db'}"

        if values.get("zxpm_db_url").startswith("sqlite"):
            db_path = values.get("zxpm_db_url").split(":")[-1]
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)

        return values


ZxpmConfig = get_plugin_config(Config)
