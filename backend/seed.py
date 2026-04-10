from backend.database import SessionLocal, engine, Base
from backend import models

Base.metadata.create_all(bind=engine)
db = SessionLocal()

if not db.query(models.Branch).first():
    branch = models.Branch(branch_id="1", branch_name="Main Branch - Kochi")
    user = models.Employee(
        emp_id="1001", name="Admin User", password="password123", 
        designation="Manager", branch_code="1", phone="9988776655"
    )
    db.add(branch)
    db.add(user)
    db.commit()
db.close()
print("Database Initialized for KivyMD 2.0!")
