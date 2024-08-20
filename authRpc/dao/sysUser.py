from authRpc.entity.sysUser import SysUser
from authRpc.exc.sysUser import RpcError


class SysUserDao:

    @classmethod
    def queryUserByPhone(cls, session, phone):
        user = session.query(SysUser).filter(SysUser.phone == phone).first()
        return user

    @classmethod
    def createUser(cls, session, username, phone, password, email):
        existedUser = session.query(SysUser).filter(SysUser.phone == phone).first()
        if existedUser:
            raise RpcError(error="手机号已存在")
        try:
            userCreated = SysUser(username=username, phone=phone, password=password, email=email)
            session.add(userCreated)
            session.commit()
            return userCreated
        except Exception as e:
            session.rollback()
            raise RpcError(error=f"创建用户: {username}-{phone} 失败.")

    @classmethod
    def updateUser(cls, session, userId, username=None, phone=None, password=None, email=None):
        userExisted = session.query(SysUser).filter(SysUser.id == userId).first()
        if not userExisted:
            raise RpcError(error="用户不存在")
        updateFields = False
        try:
            if username is not None:
                userExisted.username = username
                updateFields = True
            if phone is not None:
                userExisted.phone = phone
                updateFields = True
            if password is not None:
                userExisted.password = password
                updateFields = True
            if email is not None:
                userExisted.email = email
                updateFields = True
            if not updateFields:
                raise RpcError(error="更新用户信息不能为空")
            session.commit(userExisted)
            return userExisted
        except Exception as e:
            session.rollback()
            raise RpcError(error=f"更新用户: {username}-{phone} 失败.")
