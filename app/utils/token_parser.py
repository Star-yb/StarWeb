from datetime import datetime, timezone
from typing import Dict, Any, Optional

from jose import jwt, JWTError

from app.settings.config import JWT_SECRET_KEY, JWT_ALGORITHM


class TokenParser:
    """Token解析工具类"""

    @staticmethod
    def decode_token(token: str) -> Optional[Dict[str, Any]]:
        """
        解析JWT token
        
        :param token: JWT token字符串
        :return: 解析后的数据字典，如果解析失败返回None
        """
        try:
            # 解码token
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            
            # 获取过期时间
            exp = payload.get("exp")
            if exp:
                exp_datetime = datetime.fromtimestamp(exp, tz=timezone.utc)
                payload["exp"] = exp_datetime.isoformat()
            
            return payload
        except JWTError as e:
            print(f"Token解析失败: {str(e)}")
            return None

    @staticmethod
    def analyze_token(token: str) -> None:
        """
        分析并打印token信息
        
        :param token: JWT token字符串
        """
        print("\n=== Token 分析结果 ===")
        print(f"Token: {token}")
        
        # 解析token
        payload = TokenParser.decode_token(token)
        if payload:
            print("\n解析成功!")
            print("\n载荷数据:")
            for key, value in payload.items():
                print(f"{key}: {value}")
        else:
            print("\n解析失败!")
        print("====================")

