from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from authRpc.entity import BaseModel


class SysUser(BaseModel):
    __tablename__ = "sys_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String(14), comment='账号:手机号码', unique=True)
    username = Column(String(64), comment="用户名")
    password = Column(String(255), nullable=False, comment="密码")
    email = Column(String(255), nullable=True, comment="邮箱")
    create_time = Column(DateTime, nullable=False, default=datetime.utcnow, comment="创建时间")
    update_time = Column(DateTime, nullable=True, onupdate=datetime.utcnow, comment="更新时间")

