from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from datetime import datetime, timezone, timedelta
import json
from . import models
from .models import Report

# ------------------- AUTH -------------------
def authenticate_user(db: Session, emp_id: str, password: str):
    """Verifies employee credentials."""
    return db.query(models.Employee).filter(
        models.Employee.emp_id == emp_id,
        models.Employee.password == password
    ).first()

# 
def get_all_branches(db: Session):
    return db.query(models.Branch).all()
#  EMPLOYEES -------------------
def get_employee_by_branch(db: Session, branch_code: str):
    """Retrieves all employees for a specific branch."""
    return db.query(models.Employee).filter(models.Employee.branch_code == branch_code).all()

# ------------------- MESSAGES -------------------
def create_message(db: Session, emp_id: str, content: str):
    """Creates a new message with current UTC timestamp."""
    msg = models.Message(
        sender_id=emp_id,
        content=content,
        timestamp = datetime.now(timezone.utc)
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_messages(db: Session):
    """Retrieves all messages with sender details joined."""
    # We join Message -> Employee -> Branch to get all info in one go
    return db.query(models.Message).options(
        joinedload(models.Message.sender).joinedload(models.Employee.branch)
    ).order_by(models.Message.timestamp.asc()).all()



def get_recent_messages(db: Session):
    """Retrieves messages with joined Employee and Branch data."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=12)
    return db.query(models.Message).options(
        joinedload(models.Message.sender).joinedload(models.Employee.branch)
    ).filter(models.Message.timestamp >= cutoff).all()

# ------------------- REPORTS -------------------
def create_report(db: Session, emp_id: str, description: str):
    report = Report(emp_id=emp_id, description=description, timestamp=datetime.now(timezone.utc))
    db.add(report)
    try:
        db.commit()
        db.refresh(report)
        return report
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to create report: constraint violation.")

def get_reports(db: Session, emp_id: str):
    """Retrieves all reports for a specific employee."""
    return db.query(models.Report).filter(models.Report.emp_id == emp_id).order_by(models.Report.timestamp.desc()).all()

# crud.py
def get_all_reports(db: Session):
    """Retrieves all reports submitted by all employees."""
    return db.query(models.Report).order_by(models.Report.timestamp.desc()).all()

def resolve_report(db: Session, report_id: int, ho_id: str):
    report = db.query(models.Report).filter(models.Report.report_id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    report.status = "completed"
    report.resolved_by = ho_id
    report.resolved_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(report)
    return report

def cancel_report(db: Session, report_id: int, emp_id: str):
    report = db.query(models.Report).filter(
        models.Report.report_id == report_id,
        models.Report.emp_id == emp_id,
        models.Report.status == "pending"
    ).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found or cannot be cancelled")
    report.status = "cancelled"
    db.commit()
    db.refresh(report)
    return report

# ------------------- SMA DATA -------------------
def get_branch_sma_data(db: Session, branch_code: str):
    return db.query(models.BranchSMAData).filter(models.BranchSMAData.branch_code == branch_code).first()

def get_collection_snapshot(db: Session, branch_code: str, category: str):
    row = get_branch_sma_data(db, branch_code)
    if not row:
        return {
            "previous_day": {"number": 0, "amount": 0},
            "today": {"number": 0, "amount": 0},
            "total_month": {"number": 0, "amount": 0},
        }

    return {
        "previous_day": {
            "number": getattr(row, f"{category}_number_previous", 0) or 0,
            "amount": getattr(row, f"{category}_amount_previous", 0) or 0,
        },
        "today": {
            "number": getattr(row, f"{category}_number_collected", 0) or 0,
            "amount": getattr(row, f"{category}_amount_collected", 0) or 0,
        },
        "total_month": {
            "number": getattr(row, f"{category}_numbertotal_collected", 0) or 0,
            "amount": getattr(row, f"{category}_amounttotal_collected", 0) or 0,
        },
    }

def migrate_yesterday_to_previous(db: Session, branch_code: str):
    """Manually migrate yesterday's data to previous day fields for all categories"""
    row = get_branch_sma_data(db, branch_code)
    if not row:
        return False
    
    today = datetime.now(timezone.utc).date()
    yesterday = today - timedelta(days=1)
    
    categories = ["sma0", "sma1", "sma2", "npa1", "npa2", "d1", "d2", "d3"]
    
    for category in categories:
        last_updated = getattr(row, f"{category}_last_updated", None)
        if last_updated:
            last_updated_date = last_updated.date()
            
            # If last update was yesterday, move data to previous day
            if last_updated_date == yesterday:
                current_number = getattr(row, f"{category}_number_collected", 0) or 0
                current_amount = getattr(row, f"{category}_amount_collected", 0) or 0
                
                setattr(row, f"{category}_number_previous", current_number)
                setattr(row, f"{category}_amount_previous", current_amount)
                
                # Reset today's data
                setattr(row, f"{category}_number_collected", 0)
                setattr(row, f"{category}_amount_collected", 0)
    
    db.commit()
    db.refresh(row)
    return True

def save_daily_collection(db: Session, branch_code: str, category: str, collection_number: int, collection_amount: int):
    row = get_branch_sma_data(db, branch_code)
    if not row:
        raise HTTPException(status_code=404, detail="Branch SMA data not found")

    today = datetime.now(timezone.utc).date()
    opening_number = getattr(row, f"{category}_number", 0) or 0
    opening_amount = getattr(row, f"{category}_outstanding", 0) or 0
    current_number = getattr(row, f"{category}_number_collected", 0) or 0
    current_amount = getattr(row, f"{category}_amount_collected", 0) or 0
    total_number = getattr(row, f"{category}_numbertotal_collected", 0) or 0
    total_amount = getattr(row, f"{category}_amounttotal_collected", 0) or 0
    last_updated = getattr(row, f"{category}_last_updated", None)
    last_updated_date = last_updated.date() if last_updated else None

    # Check if we're on a new day
    if last_updated_date and last_updated_date < today:
        # Move yesterday's data to previous_day fields
        setattr(row, f"{category}_number_previous", current_number)
        setattr(row, f"{category}_amount_previous", current_amount)
        # Reset today's data for new day
        total_number = collection_number
        total_amount = collection_amount
    elif last_updated_date == today:
        # Same day, update totals
        total_number += collection_number - current_number
        total_amount += collection_amount - current_amount
    else:
        # First time entering data for this category
        total_number = collection_number
        total_amount = collection_amount

    setattr(row, f"{category}_number_collected", collection_number)
    setattr(row, f"{category}_amount_collected", collection_amount)
    setattr(row, f"{category}_numbertotal_collected", total_number)
    setattr(row, f"{category}_amounttotal_collected", total_amount)
    setattr(row, f"{category}_number_balance", opening_number - total_number)
    setattr(row, f"{category}_amount_balance", opening_amount - total_amount)
    setattr(row, f"{category}_last_updated", datetime.now(timezone.utc))
    db.commit()
    db.refresh(row)
    return row

# ------------------- DOCUMENTS -------------------
def save_document(db: Session, emp_id: str, filename: str, filepath: str, reason: str):
    """Saves document record and lets the database assign the primary key."""
    doc = models.Document(
        emp_id=emp_id,
        filename=filename,
        filepath=filepath,
        reason=reason,   # <-- store reason
        uploaded_at = datetime.now(timezone.utc)
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def get_documents(db: Session, emp_id: str):
    """Retrieves all documents for a specific employee."""
    return db.query(models.Document).filter(models.Document.emp_id == emp_id).all()


def get_circular_documents(db: Session):
    return (
        db.query(models.Document)
        .options(joinedload(models.Document.employee))
        .filter(models.Document.reason == "Circular from HO")
        .order_by(models.Document.uploaded_at.desc())
        .all()
    )
# ------------------- URGENT -------------------
def create_urgent_message(db: Session, emp_id: str, content: str):
    """Creates an urgent broadcast message with a sender."""
    urgent = models.UrgentMessage(sender_id=emp_id, content=content, timestamp=datetime.now(timezone.utc))
    db.add(urgent)
    db.commit()
    db.refresh(urgent)
    return urgent

# Change this line in crud.py
def get_urgent_messages(db: Session):
    """Retrieves urgent messages from the last 12 hours, newest first."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=12)
    return db.query(models.UrgentMessage).options(joinedload(models.UrgentMessage.sender)).filter(
        models.UrgentMessage.timestamp >= cutoff
    ).order_by(models.UrgentMessage.timestamp.desc()).all()

# ------------------- SECURITY -------------------
def update_password(db: Session, emp_id: str, new_password: str):
    """Updates the password for a specific employee."""
    user = db.query(models.Employee).filter(models.Employee.emp_id == emp_id).first()
    if user:
        user.password = new_password
        db.commit()
        db.refresh(user)
    return user

# ------------------- PROFILE -------------------
def update_profile(db: Session, emp_id: str, name: str, designation: str, phone: str, branch_code: str, avatar: str = None):
    user = db.query(models.Employee).filter(models.Employee.emp_id == emp_id).first()
    if user:
        user.name = name
        user.designation = designation
        user.phone = phone
        user.branch_code = branch_code  # Update branch relationship[cite: 5]
        if avatar:
            user.avatar = avatar
        db.commit()
        db.refresh(user)
    return user


def create_loan_action(db: Session, emp_id: str, payload: dict):
    loan_number = (payload.get("loan_number") or "").strip()
    if not loan_number:
        raise HTTPException(status_code=400, detail="Loan number is required")

    existing = db.query(models.LoanAction).filter(models.LoanAction.loan_number == loan_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Loan number already exists")

    record = models.LoanAction(
        loan_number=loan_number,
        action1=(payload.get("action1") or "").strip() or None,
        action1_date=(payload.get("action1_date") or "").strip() or None,
        action2=(payload.get("action2") or "").strip() or None,
        action2_date=(payload.get("action2_date") or "").strip() or None,
        action3=(payload.get("action3") or "").strip() or None,
        action3_date=(payload.get("action3_date") or "").strip() or None,
        action4=(payload.get("action4") or "").strip() or None,
        action4_date=(payload.get("action4_date") or "").strip() or None,
        action5=(payload.get("action5") or "").strip() or None,
        action5_date=(payload.get("action5_date") or "").strip() or None,
        created_by=emp_id,
        updated_at=datetime.now(timezone.utc),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_loan_action(db: Session, loan_number: str):
    return db.query(models.LoanAction).filter(models.LoanAction.loan_number == loan_number).first()


def update_loan_action(db: Session, loan_number: str, payload: dict):
    record = get_loan_action(db, loan_number)
    if not record:
        raise HTTPException(status_code=404, detail="Loan number not found")

    today_str = datetime.now().strftime("%d-%m-%Y")
    for idx in range(1, 6):
        action_key = f"action{idx}"
        date_key = f"{action_key}_date"
        if action_key in payload:
            value = (payload.get(action_key) or "").strip()
            previous_value = getattr(record, action_key) or ""
            setattr(record, action_key, value or None)
            if value != previous_value:
                setattr(record, date_key, today_str if value else None)

    record.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(record)
    return record


def delete_loan_action(db: Session, loan_number: str):
    record = get_loan_action(db, loan_number)
    if not record:
        raise HTTPException(status_code=404, detail="Loan number not found")
    db.delete(record)
    db.commit()


def create_consolidation_link(db: Session, emp_id: str, heading: str, link_url: str):
    record = models.ConsolidationLink(
        heading=heading.strip(),
        link_url=link_url.strip(),
        created_by=emp_id,
        created_at=datetime.now(timezone.utc),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_consolidation_links(db: Session):
    return (
        db.query(models.ConsolidationLink)
        .order_by(models.ConsolidationLink.created_at.desc(), models.ConsolidationLink.id.desc())
        .all()
    )


def create_finacle_help_entry(db: Session, emp_id: str, section_title: str, menu_code: str, description: str):
    record = models.FinacleHelpEntry(
        section_title=section_title.strip(),
        menu_code=menu_code.strip(),
        description=(description or "").strip(),
        created_by=emp_id,
        created_at=datetime.now(timezone.utc),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_finacle_help_entries(db: Session):
    return (
        db.query(models.FinacleHelpEntry)
        .order_by(
            models.FinacleHelpEntry.section_title.asc(),
            models.FinacleHelpEntry.created_at.asc(),
            models.FinacleHelpEntry.id.asc(),
        )
        .all()
    )
