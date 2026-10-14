# ---------------------------------------------------------
# Project: Ki Integrated Attendance System - Security Module
# Author: ki
# Copyright (c) 2026 ki. All Rights Reserved.
# ---------------------------------------------------------

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# المفتاح السري المعتمد للمنظومة
SECRET_KEY = "ki_super_secure_attendance_system_secret_key_2026!@#"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8  # صلاحية الجلسة 8 ساعات

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """التحقق من صحة كلمة المرور بالمقارنة مع المرور المشفر مباشرة"""
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'), 
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    """تشفير كلمة المرور مباشرة باستخدام مكتبة bcrypt المتقدمة"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """إنشاء رمز توثيق آمن JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str = Depends(oauth2_scheme)) -> dict:
    """التحقق من صحة الرمز وصلاحية الجلسة للمستخدم"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="فشل المصادقة: الرمز غير صالح أو انتهت صلاحية الجلسة",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return {"username": username, "role": payload.get("role", "professor")}
    except JWTError:
        raise credentials_exception