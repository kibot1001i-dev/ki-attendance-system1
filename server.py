# ---------------------------------------------------------
# Project: Ki Integrated Attendance System Backend (Secured & Audited)
# Author: ki
# Copyright (c) 2026 ki. All Rights Reserved.
# ---------------------------------------------------------

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime
from security import verify_access_token, create_access_token, get_password_hash, verify_password

app = FastAPI(
    title="Ki Secured Attendance API with Audit Logs",
    version="2.2.0",
    description="Advanced Secured Backend Engine protected by ki security protocols & audit trailing"
)

# تفعيل سياسة المشاركة الآمنة CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # يمكن تخصيصها بنطاق الكلية حصراً لاحقاً
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AttendanceUpdateRequest(BaseModel):
    student_code: str
    subject: str
    lecture_type: str
    week_index: int
    status_value: int # 1 for present, 0 for absent

# قاعدة بيانات وهمية للمشرفين/الأساتذة (تُربط بجدول MySQL لاحقاً)
fake_users_db = {
    "admin_ki": {
        "username": "admin_ki",
        "hashed_password": get_password_hash("ki_secure_2026"), # كلمة مرور مشفرة
        "role": "super_admin"
    }
}

# تخزين مؤقت لسجلات التدقيق والأنشطة (Audit Logs DB)
audit_logs_db: List[Dict[str, Any]] = []

@app.post("/api/v1/auth/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """مسار تسجيل الدخول للحصول على تصريح الوصول الآمن JWT"""
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="اسم المستخدم أو كلمة المرور غير صحيحة",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"], "role": user["role"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
def read_root():
    return {
        "system": "Ki Integrated Attendance System",
        "developer": "ki",
        "security_status": "Active & Encrypted (JWT + Bcrypt + Audit Trails)",
        "copyright": "© 2026 ki. All Rights Reserved."
    }

@app.post("/api/v1/attendance/update")
def update_attendance(data: AttendanceUpdateRequest, current_user: dict = Depends(verify_access_token)):
    """مسار محمي بالكامل: يتطلب توثيق صالح مع تسجيل النشاط (Audit Log)"""
    if data.week_index < 0 or data.week_index > 7:
        raise HTTPException(status_code=400, detail="رقم الأسبوع غير صحيح")
    if data.status_value not in [0, 1]:
        raise HTTPException(status_code=400, detail="قيمة الحضور يجب أن تكون 1 أو 0")
    
    # تسجيل النشاط وتوثيقه في سجل التدقيق (Audit Trail)
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "username": current_user["username"],
        "role": current_user["role"],
        "student_code": data.student_code,
        "subject": data.subject,
        "lecture_type": data.lecture_type,
        "week_index": data.week_index,
        "status_value": data.status_value
    }
    audit_logs_db.append(log_entry)
    
    return {
        "success": True,
        "message": f"تم التعديل وتسجيل النشاط بنجاح بواسطة المشرف المعتمد: {current_user['username']}",
        "audit_trail": log_entry,
        "data": data.dict()
    }

@app.get("/api/v1/attendance/audit-logs")
def get_audit_logs(current_user: dict = Depends(verify_access_token)):
    """مسار محمي لاستعراض سجلات التدقيق والنشاطات لزيادة الشفافية والرقابة"""
    return {
        "success": True,
        "total_logs": len(audit_logs_db),
        "logs": audit_logs_db
    }