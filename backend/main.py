from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import Response, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import models, crud
import shutil
import os
from fastapi.staticfiles import StaticFiles
from .models import Employee, UrgentSeen
from pydantic import BaseModel
from sqlalchemy import text
from xml.sax.saxutils import escape
from functools import lru_cache

SMA_CATEGORIES = ("sma0", "sma1", "sma2", "npa1", "npa2", "d1", "d2", "d3")
FINACLE_HELP_SEED = [
    ("Transactions", "HCASHDEP", "cash deposit and cross-currency cash deposit."),
    ("Transactions", "HCASHWD", "cash payment and cross-currency payment."),
    ("Transactions", "HXFER", "transfer transaction for bank-induced or customer-induced transfer."),
    ("Transactions", "HTM", "supports cash deposit, payment and transfer transactions."),
    ("Transactions", "HCRT", "reversal of transaction."),
    ("Transactions", "HTI", "transaction inquiry."),
    ("Transactions", "HFTI", "financial transaction inquiry."),
    ("Transactions", "HFTR", "transaction report generation."),
    ("Transactions", "GTID", "transaction ID report."),
    ("Customer Information File", "CRM Application", "CIF Retail > New Entity > Customer SQDE."),
    ("Customer Information File", "Corporate CIF", "use for corporate customer creation."),
    ("Signature Verification System", "SVS Application", "used for signature verification."),
    ("General Ledger", "HRRCDM", "create GL code."),
    ("General Ledger", "HGLSHM", "create GL sub head code."),
    ("General Ledger", "HGLSHR", "replicate GL sub head code."),
    ("General Ledger", "HGSPM", "link GL sub head code to savings product."),
    ("General Ledger", "HOAACSB", "open savings account."),
    ("General Ledger", "HIOGLT", "inquire general ledger transactions."),
    ("Customer Accounts", "HOAACSB / HOAACVSB / HOAACMSB", "open, verify and modify savings account."),
    ("Customer Accounts", "HALM", "lien maintenance."),
    ("Customer Accounts", "HICHB", "cheque book issue."),
    ("Customer Accounts", "HAFSM", "freeze account."),
    ("Customer Accounts", "HACM", "account modification."),
    ("Customer Accounts", "HGCHRG", "collect and reverse charges."),
    ("Customer Accounts", "HINTTM", "change interest rate."),
    ("Customer Accounts", "HACCBALI", "account balance inquiry."),
    ("Customer Accounts", "HCHBI", "cheque book inquiry."),
    ("Customer Accounts", "HACLI", "account ledger inquiry."),
    ("Customer Accounts", "HJHOLDER", "joint account holder inquiry."),
    ("Inventory Management", "HIMAUM", "authoriser management setup."),
    ("Inventory Management", "HIMC", "inventory movement between locations."),
    ("Inventory Management", "HISAI", "inventory split and inquiry."),
    ("Inventory Management", "HIMAI", "inventory merge."),
    ("Inventory Management", "HIIA", "inventory inquiry."),
    ("Inventory Management", "HIMR", "inventory movement report."),
    ("Inventory Management", "HISR", "inventory status report."),
    ("Remittance And Charges", "HPORDM", "maintain payment order and RTGS generation."),
    ("Remittance And Charges", "HIRM", "inward remittance maintenance."),
    ("Remittance And Charges", "HICHBA", "cheque book issue under event-based charges."),
    ("Remittance And Charges", "HGCHRG", "balance confirmation certificate and charge collection."),
    ("Rate Maintenance", "HRRCDM", "create reference code."),
    ("Rate Maintenance", "HMNTRTM", "rate code maintenance."),
    ("Rate Maintenance", "HMNTRTSQ", "rate code sequence maintenance."),
    ("Rate Maintenance", "HCNCM", "country currency maintenance."),
    ("Rate Maintenance", "HMNTRTLH", "home currency rate list."),
    ("Rate Maintenance", "HRTHQRY", "rate history inquiry."),
    ("Rate Maintenance", "HPRRTL", "print rate list."),
    ("Rate Maintenance", "HCLERPM", "customer concession in rate."),
    ("Interest", "HICTM", "interest table code maintenance."),
    ("Interest", "HBIVSM", "base interest version slab maintenance."),
    ("Interest", "HINTTM", "change account interest rate."),
    ("Interest", "HAITINQ", "interest details inquiry."),
    ("Interest", "HACBOOK", "interest booking."),
    ("Interest", "HACINT", "interest application."),
    ("Interest", "HIARM", "interest adjustment maintenance."),
    ("Interest", "HAINTRPT", "interest calculation as on date."),
    ("Interest", "HCUIR", "report on interest paid and collected."),
    ("Interest", "HINTADV", "generate interest charged advice."),
    ("Term Deposits", "HOAACTD / HOAACVTD", "open and verify term deposit."),
    ("Term Deposits", "HDRP", "print term deposit receipt."),
    ("Term Deposits", "HACMTD", "modify term deposit."),
    ("Term Deposits", "HCAACTD / HCAACVTD", "close and verify closure."),
    ("Term Deposits", "HDTREN", "renew term deposit."),
    ("Term Deposits", "HACTID", "term deposit inquiry."),
    ("Term Deposits", "HCUTD / HCUTDMAT / HRELACI", "customer and maturity inquiry."),
    ("Term Deposits", "HFDOCD / HGDET / HMDD / HSDD / HRDD", "deposit reports."),
    ("Top Up Deposits", "HOAACTU / HOAACVTU / HOAACMTU", "open, verify and modify top up deposit."),
    ("Top Up Deposits", "HACMFTU", "account maintenance for top up deposit."),
    ("Top Up Deposits", "HTUTM", "deposit transaction maintenance."),
    ("Top Up Deposits", "HCAACTD / HCAACVTD", "closure and verification."),
    ("Top Up Deposits", "HTDREN", "renewal of top up deposit."),
    ("Top Up Deposits", "HTUINST", "installment inquiry."),
    ("Top Up Deposits", "HACITD / HCUTD / HCUTDMAT / HRELACI", "top up deposit inquiries."),
    ("Top Up Deposits", "HPSP", "generate account statement."),
    ("Tax Related Menus", "HRFTDS", "TDS refund."),
    ("Tax Related Menus", "RMWTAX", "remit withholding tax."),
    ("Tax Related Menus", "HRMTDS", "remittance report."),
    ("Tax Related Menus", "RFWTAX", "refund withholding tax."),
    ("Tax Related Menus", "HTDSIP", "tax details inquiry and print."),
    ("Tax Related Menus", "HTDSPROJ", "tax projection inquiry."),
    ("Payment Systems RTGS", "HPORDM", "generate RTGS messages."),
    ("Payment Systems RTGS", "HRISP", "inward messages under suspense processing."),
    ("Payment Systems RTGS", "HSMI", "inquiry on inward and outward RTGS messages."),
    ("Payment Systems RTGS", "HPOMR", "payment order monitoring reports."),
    ("Payment Systems SWIFT", "HPORDM", "transfer of payment."),
    ("Payment Systems SWIFT", "HSMI", "inquiry on payment system messages."),
    ("Payment Systems SWIFT", "HSMM", "modify SWIFT messages."),
    ("Payment Systems SWIFT", "HSMV", "verify modified or created messages."),
    ("Payment Systems SWIFT", "HSMG", "generate SWIFT messages."),
    ("Payment Systems SWIFT", "HSAG", "generate SWIFT advice."),
    ("Payment Systems SWIFT", "HUPLPMSG", "inward message upload."),
    ("Payment Systems SWIFT", "HPSTTUM", "outward message upload."),
    ("Payment Systems SWIFT", "HPOMR", "payment order monitoring reports."),
    ("Overdraft Accounts", "HOAACOD / HOAACVOD", "open and verify overdraft account."),
    ("Overdraft Accounts", "HACM", "modify overdraft account."),
    ("Overdraft Accounts", "HACLHM", "increase or decrease sanction limit."),
    ("Loan Accounts", "HOAACLA / HOAACMLA / HOAACVLA", "open, modify and verify loan account."),
    ("Loan Accounts", "HLADISB", "loan disbursement."),
    ("Loan Accounts", "HLADGEN", "demand generation."),
    ("Loan Accounts", "HLASPAY", "scheduled payment."),
    ("Loan Accounts", "HLADSP", "demand satisfaction and recovery."),
    ("Loan Accounts", "HLAUPAY", "unscheduled payment."),
    ("Loan Accounts", "HLARA", "loan rescheduling or amendment."),
    ("Loan Accounts", "HLINTTM", "maintain loan interest table."),
    ("Loan Accounts", "HLAFACR / HLAWFEE", "collect, refund or waive loan fees."),
    ("Loan Accounts", "HPAYOFF", "loan payoff inquiry."),
    ("Loan Accounts", "HACLI / HLACLI / HLFEEI / HLPAYH / HLPREPH / HLRPSI / HDOCTR / HLAGI / HLNGI / HCCI / HLAPSP", "loan inquiries and reports."),
    ("Commercial Loans And Savings Home Loan", "HOAACCL / HOAACVCL / HACMCL", "commercial loan opening, verification and modification."),
    ("Commercial Loans And Savings Home Loan", "HCLDSM / HCLDRDN", "drawdown schedule maintenance and drawdown."),
    ("Commercial Loans And Savings Home Loan", "HLADGEN / HLAFACR / HLASPAY / HCLACLI / HPAYOFF / HCLSPAY", "commercial loan operations."),
    ("Commercial Loans And Savings Home Loan", "HOAACLA / HLADISB / HALDGEN / HPR", "savings home loan related menus."),
    ("Limit Nodes", "HLNM", "create limit node."),
    ("Limit Nodes", "HLNI / HLNDI", "limit node inquiry."),
    ("Limit Nodes", "HLLI", "limit liability inquiry."),
    ("Limit Nodes", "HLTL", "limit tree lookup."),
    ("Limit Nodes", "HLNHIR", "limit node history inquiry."),
    ("Collaterals", "HACCBALI", "overdraft balance inquiry."),
    ("Collaterals", "HCLM", "collateral lodgment."),
    ("Collaterals", "HSCLM", "link collateral to overdraft account."),
    ("Collaterals", "HCLL", "collateral linkage lookup."),
    ("Collaterals", "HCOLINI", "customer collateral details."),
    ("Collaterals", "HCLMRPTS", "collateral module reports."),
    ("Asset Classification", "HSASCL", "system asset classification and upgrade or downgrade."),
    ("Asset Classification", "HMEAC", "user classification change."),
    ("Asset Classification", "HASSET", "asset classification inquiry."),
    ("Asset Classification", "HLAOPI", "loan overdue position inquiry."),
    ("Asset Classification", "HPR", "asset classification report."),
    ("Asset Classification", "HASPROV / HAPR", "provisioning menus."),
    ("Asset Classification", "HCOLA / HRACO", "charge off, write back and recovery after charge off."),
    ("Asset Classification", "HACS / HCPI", "customer account and provisioning inquiry."),
    ("Loan Litigation", "HLLDM", "capture loan litigation details."),
    ("Forward Contracts And Bank Guarantees", "MNTFWC", "booking, extension, verification, modification and cancellation of forward contracts."),
    ("Forward Contracts And Bank Guarantees", "IFWCH / IFWC / FWCRMND", "forward contract history, inquiry and reminders."),
    ("Forward Contracts And Bank Guarantees", "OGM", "bank guarantee operations."),
    ("Forward Contracts And Bank Guarantees", "HBNKGI", "bank guarantee inquiry."),
    ("Documentary Credit And Trade Finance", "ODCM / IDCM / DCQRY", "documentary credit maintenance and inquiry."),
    ("Documentary Credit And Trade Finance", "MPOD / OAACPS / OAACVPS / MPT / HPLR / GOPCR / GIPR / HPCARPT", "packing credit menus."),
    ("Documentary Credit And Trade Finance", "MEOB", "export bills."),
    ("Documentary Credit And Trade Finance", "MIIB", "import bills."),
    ("Documentary Credit And Trade Finance", "MBCO / IPBCD", "buyers credit operations and inquiry."),
    ("Referral And DSA", "HEXCDM", "exception code maintenance."),
    ("Referral And DSA", "HRINBX / HREFINQA / HREFINQI / HREFRPT", "referral processing and reports."),
    ("Referral And DSA", "HDSAMM", "DSA master maintenance."),
    ("Referral And DSA", "HDSACOMM / HDSASUB / HDSAIP / HHIGHTRA", "DSA commission, subvention and inquiries."),
    ("Builder Master, Factoring And Hire Purchase", "HPJMM / HSTGM / HVALM / HBLMM", "builder master and project maintenance."),
    ("Builder Master, Factoring And Hire Purchase", "MFA / MID / MIDS / MFRT / HSCFM / MFF / MIIBAC / PIR / GFAR / GIIR / GIIRBAI / BJSTM", "factoring menus."),
    ("Builder Master, Factoring And Hire Purchase", "MSAC / MDMD / HOAACLA / HLADGEN / HPAYOFF / HLADISB", "hire purchase related menus."),
]

def _excel_cell(value):
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f'<Cell><Data ss:Type="Number">{value}</Data></Cell>'
    text_value = "" if value is None else escape(str(value))
    return f'<Cell><Data ss:Type="String">{text_value}</Data></Cell>'

def _excel_row(values):
    return "<Row>" + "".join(_excel_cell(value) for value in values) + "</Row>"

def _build_branch_report_xls(branch_name: str, branch_code: str, as_on_date: str, report_rows: list[tuple]):
    rows_xml = [
        _excel_row(["Kerala Bank Branch SMA/NPA Report"]),
        _excel_row(["Branch Code", branch_code]),
        _excel_row(["Branch Name", branch_name]),
        _excel_row(["As On Date", as_on_date]),
        _excel_row([]),
        _excel_row([
            "Category",
            "Opening Number",
            "Opening Amount",
            "Previous Day Number",
            "Previous Day Amount",
            "Today Number",
            "Today Amount",
            "Total Number",
            "Total Amount",
            "Balance Number",
            "Balance Amount",
        ]),
    ]
    rows_xml.extend(_excel_row(row) for row in report_rows)

    workbook = f"""<?xml version="1.0"?>
<?mso-application progid="Excel.Sheet"?>
<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:o="urn:schemas-microsoft-com:office:office"
 xmlns:x="urn:schemas-microsoft-com:office:excel"
 xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet">
 <Worksheet ss:Name="Branch Report">
  <Table>
   {''.join(rows_xml)}
  </Table>
 </Worksheet>
</Workbook>"""
    return workbook.encode("utf-8")
def _ensure_urgent_sender_column():
    # SQLite: create_all doesn't add columns to existing tables.
    with engine.connect() as conn:
        cols = conn.execute(text("PRAGMA table_info(urgent_messages)")).fetchall()
        col_names = {row[1] for row in cols}  # (cid, name, type, notnull, dflt_value, pk)
        if "sender_id" not in col_names:
            conn.execute(text("ALTER TABLE urgent_messages ADD COLUMN sender_id VARCHAR"))
            conn.commit()

def _ensure_report_columns():
    with engine.connect() as conn:
        cols = conn.execute(text("PRAGMA table_info(reports)")).fetchall()
        col_names = {row[1] for row in cols}
        if "status" not in col_names:
            conn.execute(text("ALTER TABLE reports ADD COLUMN status VARCHAR DEFAULT 'pending'"))
        if "resolved_by" not in col_names:
            conn.execute(text("ALTER TABLE reports ADD COLUMN resolved_by VARCHAR"))
        if "resolved_at" not in col_names:
            conn.execute(text("ALTER TABLE reports ADD COLUMN resolved_at DATETIME"))
        conn.commit()

def _ensure_branch_sma_schema():
    with engine.connect() as conn:
        tables = {
            row[0]
            for row in conn.execute(
                text("SELECT name FROM sqlite_master WHERE type='table'")
            ).fetchall()
        }
        if "branch_sma_data" not in tables:
            return

        cols = conn.execute(text("PRAGMA table_info(branch_sma_data)")).fetchall()
        col_names = {row[1] for row in cols}

        expected_columns = {
            "branch_code",
            "as_on_date",
        }
        for category in SMA_CATEGORIES:
            expected_columns.update(
                {
                    f"{category}_number",
                    f"{category}_outstanding",
                    f"{category}_number_collected",
                    f"{category}_amount_collected",
                    f"{category}_numbertotal_collected",
                    f"{category}_amounttotal_collected",
                    f"{category}_number_balance",
                    f"{category}_amount_balance",
                    f"{category}_number_previous",
                    f"{category}_amount_previous",
                    f"{category}_last_updated",
                }
            )

        def _blank_row(branch_code, as_on_date=None):
            row = {"branch_code": branch_code, "as_on_date": as_on_date}
            for category in SMA_CATEGORIES:
                row[f"{category}_number"] = 0
                row[f"{category}_outstanding"] = 0
                row[f"{category}_number_collected"] = 0
                row[f"{category}_amount_collected"] = 0
                row[f"{category}_numbertotal_collected"] = 0
                row[f"{category}_amounttotal_collected"] = 0
                row[f"{category}_number_balance"] = 0
                row[f"{category}_amount_balance"] = 0
                row[f"{category}_number_previous"] = 0
                row[f"{category}_amount_previous"] = 0
                row[f"{category}_last_updated"] = None
            return row

        needs_rebuild = "category" in col_names or not expected_columns.issubset(col_names)
        if needs_rebuild:
            migrated_rows = {}

            if "category" in col_names:
                old_rows = conn.execute(
                    text(
                        """
                        SELECT branch_code, category, opening_number, outstanding_amount, as_of_date
                        FROM branch_sma_data
                        ORDER BY branch_code, category
                        """
                    )
                ).fetchall()
                for branch_code, category, opening_number, outstanding_amount, as_of_date in old_rows:
                    row = migrated_rows.setdefault(branch_code, _blank_row(branch_code, as_of_date))
                    if category in SMA_CATEGORIES:
                        row[f"{category}_number"] = opening_number or 0
                        row[f"{category}_outstanding"] = outstanding_amount or 0
                        row[f"{category}_number_balance"] = opening_number or 0
                        row[f"{category}_amount_balance"] = outstanding_amount or 0
                        if as_of_date:
                            row["as_on_date"] = as_of_date
            else:
                existing_rows = conn.execute(text("SELECT * FROM branch_sma_data")).mappings().all()
                for existing in existing_rows:
                    branch_code = existing["branch_code"]
                    row = _blank_row(branch_code, existing.get("as_on_date"))
                    for category in SMA_CATEGORIES:
                        opening_number = existing.get(f"{category}_number", 0) or 0
                        opening_amount = existing.get(f"{category}_outstanding", 0) or 0
                        row[f"{category}_number"] = opening_number
                        row[f"{category}_outstanding"] = opening_amount
                        row[f"{category}_number_collected"] = existing.get(f"{category}_number_collected", 0) or 0
                        row[f"{category}_amount_collected"] = existing.get(f"{category}_amount_collected", 0) or 0
                        row[f"{category}_numbertotal_collected"] = existing.get(f"{category}_numbertotal_collected", 0) or 0
                        row[f"{category}_amounttotal_collected"] = existing.get(f"{category}_amounttotal_collected", 0) or 0
                        row[f"{category}_number_previous"] = existing.get(f"{category}_number_previous", 0) or 0
                        row[f"{category}_amount_previous"] = existing.get(f"{category}_amount_previous", 0) or 0
                        row[f"{category}_last_updated"] = existing.get(f"{category}_last_updated")
                        row[f"{category}_number_balance"] = existing.get(f"{category}_number_balance")
                        row[f"{category}_amount_balance"] = existing.get(f"{category}_amount_balance")
                        if row[f"{category}_number_balance"] is None:
                            row[f"{category}_number_balance"] = opening_number - row[f"{category}_numbertotal_collected"]
                        if row[f"{category}_amount_balance"] is None:
                            row[f"{category}_amount_balance"] = opening_amount - row[f"{category}_amounttotal_collected"]
                    migrated_rows[branch_code] = row

            conn.execute(text("ALTER TABLE branch_sma_data RENAME TO branch_sma_data_old"))

            create_sql = """
                CREATE TABLE branch_sma_data (
                    branch_code VARCHAR NOT NULL PRIMARY KEY,
                    sma0_number INTEGER,
                    sma0_outstanding INTEGER,
                    sma1_number INTEGER,
                    sma1_outstanding INTEGER,
                    sma2_number INTEGER,
                    sma2_outstanding INTEGER,
                    npa1_number INTEGER,
                    npa1_outstanding INTEGER,
                    npa2_number INTEGER,
                    npa2_outstanding INTEGER,
                    d1_number INTEGER,
                    d1_outstanding INTEGER,
                    d2_number INTEGER,
                    d2_outstanding INTEGER,
                    d3_number INTEGER,
                    d3_outstanding INTEGER,
                    as_on_date DATETIME,
                    sma0_number_collected INTEGER,
                    sma0_amount_collected INTEGER,
                    sma1_number_collected INTEGER,
                    sma1_amount_collected INTEGER,
                    sma2_number_collected INTEGER,
                    sma2_amount_collected INTEGER,
                    npa1_number_collected INTEGER,
                    npa1_amount_collected INTEGER,
                    npa2_number_collected INTEGER,
                    npa2_amount_collected INTEGER,
                    d1_number_collected INTEGER,
                    d1_amount_collected INTEGER,
                    d2_number_collected INTEGER,
                    d2_amount_collected INTEGER,
                    d3_number_collected INTEGER,
                    d3_amount_collected INTEGER,
                    sma0_numbertotal_collected INTEGER,
                    sma0_amounttotal_collected INTEGER,
                    sma1_numbertotal_collected INTEGER,
                    sma1_amounttotal_collected INTEGER,
                    sma2_numbertotal_collected INTEGER,
                    sma2_amounttotal_collected INTEGER,
                    npa1_numbertotal_collected INTEGER,
                    npa1_amounttotal_collected INTEGER,
                    npa2_numbertotal_collected INTEGER,
                    npa2_amounttotal_collected INTEGER,
                    d1_numbertotal_collected INTEGER,
                    d1_amounttotal_collected INTEGER,
                    d2_numbertotal_collected INTEGER,
                    d2_amounttotal_collected INTEGER,
                    d3_numbertotal_collected INTEGER,
                    d3_amounttotal_collected INTEGER,
                    sma0_number_balance INTEGER,
                    sma0_amount_balance INTEGER,
                    sma1_number_balance INTEGER,
                    sma1_amount_balance INTEGER,
                    sma2_number_balance INTEGER,
                    sma2_amount_balance INTEGER,
                    npa1_number_balance INTEGER,
                    npa1_amount_balance INTEGER,
                    npa2_number_balance INTEGER,
                    npa2_amount_balance INTEGER,
                    d1_number_balance INTEGER,
                    d1_amount_balance INTEGER,
                    d2_number_balance INTEGER,
                    d2_amount_balance INTEGER,
                    d3_number_balance INTEGER,
                    d3_amount_balance INTEGER,
                    sma0_number_previous INTEGER,
                    sma0_amount_previous INTEGER,
                    sma1_number_previous INTEGER,
                    sma1_amount_previous INTEGER,
                    sma2_number_previous INTEGER,
                    sma2_amount_previous INTEGER,
                    npa1_number_previous INTEGER,
                    npa1_amount_previous INTEGER,
                    npa2_number_previous INTEGER,
                    npa2_amount_previous INTEGER,
                    d1_number_previous INTEGER,
                    d1_amount_previous INTEGER,
                    d2_number_previous INTEGER,
                    d2_amount_previous INTEGER,
                    d3_number_previous INTEGER,
                    d3_amount_previous INTEGER,
                    sma0_last_updated DATETIME,
                    sma1_last_updated DATETIME,
                    sma2_last_updated DATETIME,
                    npa1_last_updated DATETIME,
                    npa2_last_updated DATETIME,
                    d1_last_updated DATETIME,
                    d2_last_updated DATETIME,
                    d3_last_updated DATETIME,
                    FOREIGN KEY(branch_code) REFERENCES branches (branch_id)
                )
            """
            conn.execute(text(create_sql))

            insert_columns = [
                "branch_code",
                "sma0_number", "sma0_outstanding",
                "sma1_number", "sma1_outstanding",
                "sma2_number", "sma2_outstanding",
                "npa1_number", "npa1_outstanding",
                "npa2_number", "npa2_outstanding",
                "d1_number", "d1_outstanding",
                "d2_number", "d2_outstanding",
                "d3_number", "d3_outstanding",
                "as_on_date",
                "sma0_number_collected", "sma0_amount_collected",
                "sma1_number_collected", "sma1_amount_collected",
                "sma2_number_collected", "sma2_amount_collected",
                "npa1_number_collected", "npa1_amount_collected",
                "npa2_number_collected", "npa2_amount_collected",
                "d1_number_collected", "d1_amount_collected",
                "d2_number_collected", "d2_amount_collected",
                "d3_number_collected", "d3_amount_collected",
                "sma0_numbertotal_collected", "sma0_amounttotal_collected",
                "sma1_numbertotal_collected", "sma1_amounttotal_collected",
                "sma2_numbertotal_collected", "sma2_amounttotal_collected",
                "npa1_numbertotal_collected", "npa1_amounttotal_collected",
                "npa2_numbertotal_collected", "npa2_amounttotal_collected",
                "d1_numbertotal_collected", "d1_amounttotal_collected",
                "d2_numbertotal_collected", "d2_amounttotal_collected",
                "d3_numbertotal_collected", "d3_amounttotal_collected",
                "sma0_number_balance", "sma0_amount_balance",
                "sma1_number_balance", "sma1_amount_balance",
                "sma2_number_balance", "sma2_amount_balance",
                "npa1_number_balance", "npa1_amount_balance",
                "npa2_number_balance", "npa2_amount_balance",
                "d1_number_balance", "d1_amount_balance",
                "d2_number_balance", "d2_amount_balance",
                "d3_number_balance", "d3_amount_balance",
                "sma0_number_previous", "sma0_amount_previous",
                "sma1_number_previous", "sma1_amount_previous",
                "sma2_number_previous", "sma2_amount_previous",
                "npa1_number_previous", "npa1_amount_previous",
                "npa2_number_previous", "npa2_amount_previous",
                "d1_number_previous", "d1_amount_previous",
                "d2_number_previous", "d2_amount_previous",
                "d3_number_previous", "d3_amount_previous",
                "sma0_last_updated", "sma1_last_updated", "sma2_last_updated",
                "npa1_last_updated", "npa2_last_updated",
                "d1_last_updated", "d2_last_updated", "d3_last_updated",
            ]
            insert_sql = text(
                f"""
                INSERT INTO branch_sma_data ({", ".join(insert_columns)})
                VALUES ({", ".join(f":{column}" for column in insert_columns)})
                """
            )
            for row in migrated_rows.values():
                conn.execute(insert_sql, row)

            conn.execute(text("DROP TABLE branch_sma_data_old"))
            conn.commit()

        # Ensure every branch from `branches` has one row in the new wide table.
        branch_rows = conn.execute(
            text("SELECT branch_id FROM branches ORDER BY branch_id")
        ).fetchall()
        existing_branch_codes = {
            row[0]
            for row in conn.execute(
                text("SELECT branch_code FROM branch_sma_data")
            ).fetchall()
        }

        for (branch_code,) in branch_rows:
            if branch_code in existing_branch_codes:
                continue
            values = {"branch_code": branch_code}
            for category in SMA_CATEGORIES:
                values[f"{category}_number"] = 0
                values[f"{category}_outstanding"] = 0
                values[f"{category}_number_collected"] = 0
                values[f"{category}_amount_collected"] = 0
                values[f"{category}_numbertotal_collected"] = 0
                values[f"{category}_amounttotal_collected"] = 0
                values[f"{category}_number_balance"] = 0
                values[f"{category}_amount_balance"] = 0
                values[f"{category}_number_previous"] = 0
                values[f"{category}_amount_previous"] = 0
                values[f"{category}_last_updated"] = None

            conn.execute(
                text(
                    """
                    INSERT INTO branch_sma_data (
                        branch_code,
                        sma0_number, sma0_outstanding, sma1_number, sma1_outstanding,
                        sma2_number, sma2_outstanding, npa1_number, npa1_outstanding,
                        npa2_number, npa2_outstanding, d1_number, d1_outstanding,
                        d2_number, d2_outstanding, d3_number, d3_outstanding,
                        as_on_date,
                        sma0_number_collected, sma0_amount_collected,
                        sma1_number_collected, sma1_amount_collected,
                        sma2_number_collected, sma2_amount_collected,
                        npa1_number_collected, npa1_amount_collected,
                        npa2_number_collected, npa2_amount_collected,
                        d1_number_collected, d1_amount_collected,
                        d2_number_collected, d2_amount_collected,
                        d3_number_collected, d3_amount_collected,
                        sma0_numbertotal_collected, sma0_amounttotal_collected,
                        sma1_numbertotal_collected, sma1_amounttotal_collected,
                        sma2_numbertotal_collected, sma2_amounttotal_collected,
                        npa1_numbertotal_collected, npa1_amounttotal_collected,
                        npa2_numbertotal_collected, npa2_amounttotal_collected,
                        d1_numbertotal_collected, d1_amounttotal_collected,
                        d2_numbertotal_collected, d2_amounttotal_collected,
                        d3_numbertotal_collected, d3_amounttotal_collected,
                        sma0_number_balance, sma0_amount_balance,
                        sma1_number_balance, sma1_amount_balance,
                        sma2_number_balance, sma2_amount_balance,
                        npa1_number_balance, npa1_amount_balance,
                        npa2_number_balance, npa2_amount_balance,
                        d1_number_balance, d1_amount_balance,
                        d2_number_balance, d2_amount_balance,
                        d3_number_balance, d3_amount_balance,
                        sma0_number_previous, sma0_amount_previous,
                        sma1_number_previous, sma1_amount_previous,
                        sma2_number_previous, sma2_amount_previous,
                        npa1_number_previous, npa1_amount_previous,
                        npa2_number_previous, npa2_amount_previous,
                        d1_number_previous, d1_amount_previous,
                        d2_number_previous, d2_amount_previous,
                        d3_number_previous, d3_amount_previous,
                        sma0_last_updated, sma1_last_updated, sma2_last_updated,
                        npa1_last_updated, npa2_last_updated,
                        d1_last_updated, d2_last_updated, d3_last_updated
                    ) VALUES (
                        :branch_code,
                        :sma0_number, :sma0_outstanding, :sma1_number, :sma1_outstanding,
                        :sma2_number, :sma2_outstanding, :npa1_number, :npa1_outstanding,
                        :npa2_number, :npa2_outstanding, :d1_number, :d1_outstanding,
                        :d2_number, :d2_outstanding, :d3_number, :d3_outstanding,
                        CURRENT_TIMESTAMP,
                        :sma0_number_collected, :sma0_amount_collected,
                        :sma1_number_collected, :sma1_amount_collected,
                        :sma2_number_collected, :sma2_amount_collected,
                        :npa1_number_collected, :npa1_amount_collected,
                        :npa2_number_collected, :npa2_amount_collected,
                        :d1_number_collected, :d1_amount_collected,
                        :d2_number_collected, :d2_amount_collected,
                        :d3_number_collected, :d3_amount_collected,
                        :sma0_numbertotal_collected, :sma0_amounttotal_collected,
                        :sma1_numbertotal_collected, :sma1_amounttotal_collected,
                        :sma2_numbertotal_collected, :sma2_amounttotal_collected,
                        :npa1_numbertotal_collected, :npa1_amounttotal_collected,
                        :npa2_numbertotal_collected, :npa2_amounttotal_collected,
                        :d1_numbertotal_collected, :d1_amounttotal_collected,
                        :d2_numbertotal_collected, :d2_amounttotal_collected,
                        :d3_numbertotal_collected, :d3_amounttotal_collected,
                        :sma0_number_balance, :sma0_amount_balance,
                        :sma1_number_balance, :sma1_amount_balance,
                        :sma2_number_balance, :sma2_amount_balance,
                        :npa1_number_balance, :npa1_amount_balance,
                        :npa2_number_balance, :npa2_amount_balance,
                        :d1_number_balance, :d1_amount_balance,
                        :d2_number_balance, :d2_amount_balance,
                        :d3_number_balance, :d3_amount_balance,
                        :sma0_number_previous, :sma0_amount_previous,
                        :sma1_number_previous, :sma1_amount_previous,
                        :sma2_number_previous, :sma2_amount_previous,
                        :npa1_number_previous, :npa1_amount_previous,
                        :npa2_number_previous, :npa2_amount_previous,
                        :d1_number_previous, :d1_amount_previous,
                        :d2_number_previous, :d2_amount_previous,
                        :d3_number_previous, :d3_amount_previous,
                        :sma0_last_updated, :sma1_last_updated, :sma2_last_updated,
                        :npa1_last_updated, :npa2_last_updated,
                        :d1_last_updated, :d2_last_updated, :d3_last_updated
                    )
                    """
                ),
                values,
            )
        conn.commit()

        if "daily_collections" in tables:
            conn.execute(text("DROP TABLE daily_collections"))
            conn.commit()


def _ensure_loan_actions_schema():
    with engine.connect() as conn:
        tables = {
            row[0]
            for row in conn.execute(
                text("SELECT name FROM sqlite_master WHERE type='table'")
            ).fetchall()
        }
        if "loan_actions" not in tables:
            return

        cols = conn.execute(text("PRAGMA table_info(loan_actions)")).fetchall()
        col_names = {row[1] for row in cols}
        expected = {
            "loan_number",
            "action1", "action1_date",
            "action2", "action2_date",
            "action3", "action3_date",
            "action4", "action4_date",
            "action5", "action5_date",
            "created_by",
            "updated_at",
        }
        if expected.issubset(col_names):
            return

        conn.execute(text("ALTER TABLE loan_actions RENAME TO loan_actions_old"))
        conn.execute(text("""
            CREATE TABLE loan_actions (
                loan_number VARCHAR NOT NULL PRIMARY KEY,
                action1 VARCHAR,
                action1_date VARCHAR,
                action2 VARCHAR,
                action2_date VARCHAR,
                action3 VARCHAR,
                action3_date VARCHAR,
                action4 VARCHAR,
                action4_date VARCHAR,
                action5 VARCHAR,
                action5_date VARCHAR,
                created_by VARCHAR,
                updated_at DATETIME
            )
        """))
        conn.execute(text("""
            INSERT INTO loan_actions (
                loan_number, action1, action1_date, action2, action2_date,
                action3, action3_date, action4, action4_date,
                action5, action5_date, created_by, updated_at
            )
            SELECT
                loan_number,
                action1, action1_date, action2, action2_date,
                action3, action3_date, action4, action4_date,
                action5, action5_date, created_by, updated_at
            FROM loan_actions_old
        """))
        conn.execute(text("DROP TABLE loan_actions_old"))
        conn.commit()

def _ensure_finacle_help_seed():
    with engine.begin() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM finacle_help_entries")).scalar() or 0
        if count:
            return
        for idx, (section_title, menu_code, description) in enumerate(FINACLE_HELP_SEED, start=1):
            conn.execute(
                text("""
                    INSERT INTO finacle_help_entries (section_title, menu_code, description, created_by, created_at)
                    VALUES (:section_title, :menu_code, :description, :created_by, CURRENT_TIMESTAMP)
                """),
                {
                    "section_title": section_title,
                    "menu_code": menu_code,
                    "description": description,
                    "created_by": None,
                },
            )

# 2. Create database tables
models.Base.metadata.create_all(bind=engine)
_ensure_urgent_sender_column()
_ensure_report_columns()
_ensure_branch_sma_schema()
_ensure_loan_actions_schema()
_ensure_finacle_help_seed()

# 1. Create the FastAPI instance FIRST
app = FastAPI(title="Kerala Bank Backend API")

@app.get("/health")
def health_check():
    """Health check endpoint for Render"""
    return {"status": "healthy", "message": "Kerala Bank API is running"}

@app.post("/create-tables")
def create_tables():
    """Manually create all database tables"""
    try:
        from .database import engine
        from . import models
        
        # Create all tables
        models.Base.metadata.create_all(bind=engine)
        
        # Run additional table creation functions
        _ensure_urgent_sender_column()
        _ensure_report_columns()
        _ensure_branch_sma_schema()
        _ensure_loan_actions_schema()
        _ensure_finacle_help_seed()
        
        return {"status": "success", "message": "All tables created successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.on_event("startup")
async def startup_event():
    """Create tables on application startup"""
    try:
        from .database import engine
        from . import models
        
        # Create all tables
        models.Base.metadata.create_all(bind=engine)
        
        # Run additional table creation functions
        _ensure_urgent_sender_column()
        _ensure_report_columns()
        _ensure_branch_sma_schema()
        _ensure_loan_actions_schema()
        _ensure_finacle_help_seed()
        
        print("Tables created successfully on startup")
    except Exception as e:
        print(f"Error creating tables on startup: {e}")

@app.get("/check-tables")
def check_tables():
    """Check if tables exist in database"""
    try:
        from .database import SessionLocal
        from sqlalchemy import text
        
        db = SessionLocal()
        
        # Check if tables exist
        result = db.execute(text("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """))
        
        tables = [row[0] for row in result]
        db.close()
        
        return {
            "status": "success",
            "tables": tables,
            "count": len(tables)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "tables": []
        }



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
AVATARS_DIR = os.path.join(STATIC_DIR, "avatars")

# Create the folders if they don't exist
if not os.path.exists(AVATARS_DIR):
    os.makedirs(AVATARS_DIR, exist_ok=True)

# Mount using the absolute path
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------- ROUTES -------------------

# Login
@app.get("/login")
def login(emp_id: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.Employee).filter(models.Employee.emp_id == emp_id).first()
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {
        "emp_id": user.emp_id,
        "name": user.name,
        "avatar": user.avatar,
        "phone": user.phone,
        "designation": user.designation,
        "branch": user.branch.branch_name if user.branch else "General",
        "branch_code": user.branch_code
    }

# Employees by branch
@app.get("/employees/{branch_code}")
def get_employees(branch_code: str, db: Session = Depends(get_db)):
    employees = crud.get_employee_by_branch(db, branch_code)
    return [
        {
            "emp_id": emp.emp_id,
            "name": emp.name,
            "designation": emp.designation,
            "branch_code": emp.branch_code,
            "phone": emp.phone,
            "avatar": emp.avatar,
        }
        for emp in employees
    ]

# Messages
@app.post("/messages")
def send_message(emp_id: str, content: str, db: Session = Depends(get_db)):
    message = crud.create_message(db, emp_id, content)
    return {
        "chat_id": message.id,
        "sender_id": message.sender_id,
        "content": message.content,
        "timestamp": message.timestamp
    }

@app.get("/messages")
def get_all_messages(db: Session = Depends(get_db)):
    # This calls the crud function we updated with joinedload
    messages = crud.get_recent_messages(db)
    return [
        {
            "content": m.content,
            "sender_id": m.sender_id,
            "sender_name": m.sender.name if m.sender else "Unknown",
            "branch_name": m.sender.branch.branch_name if m.sender and m.sender.branch else "General",
            "timestamp": str(m.timestamp)
        } for m in messages
    ]
# Reports
@app.post("/reports")
def submit_report(emp_id: str, description: str, db: Session = Depends(get_db)):
    report = crud.create_report(db, emp_id, description)
    return {
        "status": "submitted",
        "id": report.report_id,       # <--- Change this from report.id to report.report_id
        "daily_id": getattr(report, 'daily_id', None), 
        "emp_id": report.emp_id,
        "description": report.description,
        "timestamp": str(report.timestamp)
    }

def _serialize_report(report):
    return {
        "report_id": report.report_id,
        "emp_id": report.emp_id,
        "description": report.description,
        "status": report.status,
        "resolved_by": report.resolved_by,
        "resolved_at": str(report.resolved_at) if report.resolved_at else None,
        "timestamp": str(report.timestamp) if report.timestamp else None,
    }

@app.get("/reports/all")
def get_all_reports(db: Session = Depends(get_db)):
    try:
        reports = crud.get_all_reports(db)
        print(f"DEBUG: get_all_reports called, found {len(reports)} reports")
        if reports:
            print(f"DEBUG: First report: {reports[0].report_id} - {reports[0].description}")
        return {"count": len(reports), "reports": [_serialize_report(r) for r in reports]}
    except Exception as e:
        print(f"ERROR in get_all_reports: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e), "traceback": traceback.format_exc()}

@app.get("/reports/{emp_id}")
def get_reports(emp_id: str, db: Session = Depends(get_db)):
    reports = crud.get_reports(db, emp_id)
    return [_serialize_report(r) for r in reports]

@app.post("/reports/{report_id}/resolve")
def resolve_report(report_id: int, ho_id: str, db: Session = Depends(get_db)):
    report = crud.resolve_report(db, report_id, ho_id)
    return {
        "status": report.status,
        "report_id": report.report_id,
        "emp_id": report.emp_id,
        "description": report.description,
        "resolved_by": report.resolved_by,
        "resolved_at": str(report.resolved_at) if report.resolved_at else None,
    }

@app.post("/reports/{report_id}/cancel")
def cancel_report(report_id: int, emp_id: str, db: Session = Depends(get_db)):
    report = crud.cancel_report(db, report_id, emp_id)
    return {
        "status": report.status,
        "report_id": report.report_id,
        "emp_id": report.emp_id,
        "description": report.description,
    }

# Documents

@app.post("/upload-doc")
def upload_doc(
    emp_id: str = Form(...),
    reason: str = Form(...),   # <-- new field
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    allowed_ext = [".txt", ".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"]
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in allowed_ext:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    os.makedirs("uploads", exist_ok=True)
    safe_name = os.path.basename(file.filename)
    filepath = os.path.join("uploads", safe_name)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    document = crud.save_document(db, emp_id, file.filename, filepath, reason)
    return {
        "status": "uploaded",
        "doc_id": document.doc_id,
        "emp_id": document.emp_id,
        "filename": document.filename,
        "filepath": document.filepath,
        "reason": document.reason,
        "uploaded_at": document.uploaded_at
    }


@app.get("/documents/{emp_id}")
def get_documents(emp_id: str, db: Session = Depends(get_db)):
    return crud.get_documents(db, emp_id)


@app.post("/upload-circular")
def upload_circular(
    emp_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.Employee).filter(models.Employee.emp_id == emp_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if str(user.branch_code).strip() != "109000":
        raise HTTPException(status_code=403, detail="Only head office can send circulars")

    allowed_ext = [".txt", ".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"]
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_ext:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    os.makedirs("uploads", exist_ok=True)
    safe_name = os.path.basename(file.filename)
    filepath = os.path.join("uploads", safe_name)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    document = crud.save_document(db, emp_id, file.filename, filepath, "Circular from HO")
    return {
        "status": "uploaded",
        "doc_id": document.doc_id,
        "filename": document.filename,
        "filepath": document.filepath,
        "reason": document.reason,
        "uploaded_at": str(document.uploaded_at),
    }


@app.get("/circulars")
def get_circulars(db: Session = Depends(get_db)):
    documents = crud.get_circular_documents(db)
    return [
        {
            "doc_id": doc.doc_id,
            "filename": doc.filename,
            "filepath": doc.filepath,
            "reason": doc.reason,
            "uploaded_at": str(doc.uploaded_at) if doc.uploaded_at else None,
            "emp_id": doc.emp_id,
            "sender_name": doc.employee.name if doc.employee else "Unknown",
        }
        for doc in documents
    ]


@app.get("/circulars/download/{doc_id}")
def download_circular(doc_id: int, db: Session = Depends(get_db)):
    document = db.query(models.Document).filter(
        models.Document.doc_id == doc_id,
        models.Document.reason == "Circular from HO"
    ).first()
    if not document:
        raise HTTPException(status_code=404, detail="Circular not found")
    if not os.path.exists(document.filepath):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=document.filepath, filename=document.filename)


# Urgent Messages
@app.post("/urgent")
def create_urgent(emp_id: str, content: str, db: Session = Depends(get_db)):
    try:
        urgent = crud.create_urgent_message(db, emp_id=emp_id, content=content)
        return {
            "id": urgent.id,
            "content": urgent.content,
            "timestamp": str(urgent.timestamp),
            "sender": {
                "emp_id": urgent.sender.emp_id if urgent.sender else urgent.sender_id,
                "name": urgent.sender.name if urgent.sender else None,
            },
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/urgent")
def get_urgent(db: Session = Depends(get_db)):
    msgs = crud.get_urgent_messages(db)
    return [
        {
            "id": m.id,
            "content": m.content,
            "timestamp": str(m.timestamp),
            "sender": {
                "emp_id": m.sender.emp_id if m.sender else m.sender_id,
                "name": m.sender.name if m.sender else None,
            },
        }
        for m in msgs
    ]

# Update Password
@app.post("/update-password")
def update_password(emp_id: str, new_pwd: str, db: Session = Depends(get_db)):
    user = crud.update_password(db, emp_id, new_pwd)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success"}

# Update Profile
@app.post("/update-profile")
def update_profile(emp_id: str, name: str, designation: str, phone: str, branch_code: str, db: Session = Depends(get_db)):
    user = crud.update_profile(db, emp_id, name, designation, phone, branch_code)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success", "branch_code": user.branch_code}
    db.commit()
    return {"message": "Success"}

@app.post("/upload-avatar")
def upload_avatar(emp_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="Only PNG/JPG files are allowed")

    user = db.query(models.Employee).filter(models.Employee.emp_id == emp_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    ext = os.path.splitext(file.filename)[1].lower()
    safe_filename = f"{emp_id}{ext}"
    avatar_path = os.path.join(AVATARS_DIR, safe_filename)
    with open(avatar_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    user.avatar = f"static/avatars/{safe_filename}"
    db.commit()
    db.refresh(user)
    return {"status": "success", "avatar": user.avatar}


def _serialize_loan_action(record):
    if not record:
        return None
    return {
        "loan_number": record.loan_number,
        "action1": record.action1 or "",
        "action1_date": record.action1_date or "",
        "action2": record.action2 or "",
        "action2_date": record.action2_date or "",
        "action3": record.action3 or "",
        "action3_date": record.action3_date or "",
        "action4": record.action4 or "",
        "action4_date": record.action4_date or "",
        "action5": record.action5 or "",
        "action5_date": record.action5_date or "",
        "created_by": record.created_by,
        "updated_at": str(record.updated_at) if record.updated_at else None,
    }


def _serialize_consolidation_link(record):
    if not record:
        return None
    return {
        "id": record.id,
        "heading": record.heading or "",
        "link_url": record.link_url or "",
        "created_by": record.created_by or "",
        "created_by_name": record.creator.name if getattr(record, "creator", None) else "",
        "created_at": str(record.created_at) if record.created_at else None,
    }


def _serialize_finacle_help_entry(record):
    if not record:
        return None
    return {
        "section_title": record.section_title,
        "menu_code": record.menu_code,
        "description": record.description or "",
    }


@app.post("/loan-actions")
def create_loan_action(data: dict, db: Session = Depends(get_db)):
    emp_id = (data.get("emp_id") or "").strip()
    record = crud.create_loan_action(db, emp_id, data)
    return {"status": "created", "record": _serialize_loan_action(record)}


@app.get("/loan-actions/{loan_number}")
def get_loan_action(loan_number: str, db: Session = Depends(get_db)):
    record = crud.get_loan_action(db, loan_number)
    if not record:
        raise HTTPException(status_code=404, detail="Loan number not found")
    return _serialize_loan_action(record)


@app.put("/loan-actions/{loan_number}")
def update_loan_action(loan_number: str, data: dict, db: Session = Depends(get_db)):
    record = crud.update_loan_action(db, loan_number, data)
    return {"status": "updated", "record": _serialize_loan_action(record)}


@app.delete("/loan-actions/{loan_number}")
def delete_loan_action(loan_number: str, db: Session = Depends(get_db)):
    crud.delete_loan_action(db, loan_number)
    return {"status": "deleted", "loan_number": loan_number}


@app.post("/consolidation-links")
def create_consolidation_link(data: dict, db: Session = Depends(get_db)):
    emp_id = (data.get("emp_id") or "").strip()
    heading = (data.get("heading") or "").strip()
    link_url = (data.get("link_url") or "").strip()
    user = db.query(models.Employee).filter(models.Employee.emp_id == emp_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if str(user.branch_code).strip() != "109000":
        raise HTTPException(status_code=403, detail="Only 109000 users can add consolidation links")
    if not heading:
        raise HTTPException(status_code=400, detail="Heading is required")
    if not link_url:
        raise HTTPException(status_code=400, detail="Link is required")
    if not (link_url.startswith("http://") or link_url.startswith("https://")):
        raise HTTPException(status_code=400, detail="Please enter a valid link")
    record = crud.create_consolidation_link(db, emp_id, heading, link_url)
    return {"status": "created", "record": _serialize_consolidation_link(record)}


@app.get("/consolidation-links")
def get_consolidation_links(db: Session = Depends(get_db)):
    records = crud.get_consolidation_links(db)
    return [_serialize_consolidation_link(record) for record in records]


@app.post("/finacle-help")
def create_finacle_help_entry(data: dict, db: Session = Depends(get_db)):
    emp_id = (data.get("emp_id") or "").strip()
    section_title = (data.get("section_title") or "").strip()
    menu_code = (data.get("menu_code") or "").strip()
    description = (data.get("description") or "").strip()
    user = db.query(models.Employee).filter(models.Employee.emp_id == emp_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if str(user.branch_code).strip() != "109000":
        raise HTTPException(status_code=403, detail="Only 109000 users can add Finacle Help entries")
    if not section_title:
        raise HTTPException(status_code=400, detail="Subheading is required")
    if not menu_code:
        raise HTTPException(status_code=400, detail="Menu code is required")
    record = crud.create_finacle_help_entry(db, emp_id, section_title, menu_code, description)
    # Clear cache to ensure fresh data on next request
    get_finacle_help_entries.cache_clear()
    return {"status": "created", "record": _serialize_finacle_help_entry(record)}


@app.get("/finacle-help")
@lru_cache(maxsize=128)
def get_finacle_help_entries(db: Session = Depends(get_db)):
    records = crud.get_finacle_help_entries(db)
    return [_serialize_finacle_help_entry(record) for record in records]

@app.get("/branches")
@lru_cache(maxsize=64)
def read_branches(db: Session = Depends(get_db)):
    branches = crud.get_all_branches(db)
    return [
        {"branch_id": branch.branch_id, "branch_name": branch.branch_name}
        for branch in branches
    ]

@app.get("/branch-report/{emp_id}")
def download_branch_report(emp_id: str, db: Session = Depends(get_db)):
    user = db.query(models.Employee).filter(models.Employee.emp_id == emp_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    branch_code = user.branch_code
    branch_name = user.branch.branch_name if user.branch else branch_code
    data = crud.get_branch_sma_data(db, branch_code)
    if not data:
        raise HTTPException(status_code=404, detail="Branch report data not found")

    as_on_date = data.as_on_date.strftime("%d-%m-%Y") if data.as_on_date else ""
    rows = []
    for category in SMA_CATEGORIES:
        rows.append(
            (
                category.upper(),
                getattr(data, f"{category}_number", 0) or 0,
                getattr(data, f"{category}_outstanding", 0) or 0,
                getattr(data, f"{category}_number_previous", 0) or 0,
                getattr(data, f"{category}_amount_previous", 0) or 0,
                getattr(data, f"{category}_number_collected", 0) or 0,
                getattr(data, f"{category}_amount_collected", 0) or 0,
                getattr(data, f"{category}_numbertotal_collected", 0) or 0,
                getattr(data, f"{category}_amounttotal_collected", 0) or 0,
                getattr(data, f"{category}_number_balance", 0) or 0,
                getattr(data, f"{category}_amount_balance", 0) or 0,
            )
        )

    content = _build_branch_report_xls(branch_name, branch_code, as_on_date, rows)
    filename = f"branch_report_{branch_code}.xls"
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return Response(content=content, media_type="application/vnd.ms-excel", headers=headers)

# SMA Data
from datetime import datetime, timedelta

@app.get("/sma-data/{branch_code}")
def get_sma_data(branch_code: str, db: Session = Depends(get_db)):
    data = crud.get_branch_sma_data(db, branch_code)
    if not data:
        return {}

    as_on_date = data.as_on_date.strftime("%d-%m-%Y") if data.as_on_date else ""
    result = {}
    for category in ("sma0", "sma1", "sma2", "npa1", "npa2", "d1", "d2", "d3"):
        result[category] = {
            "opening_number": getattr(data, f"{category}_number", 0) or 0,
            "outstanding_amount": getattr(data, f"{category}_outstanding", 0) or 0,
            "as_of_date": as_on_date,
        }
    return result

@app.get("/collections/{branch_code}/{category}")
def get_collections(branch_code: str, category: str, db: Session = Depends(get_db)):
    return crud.get_collection_snapshot(db, branch_code, category)

@app.post("/save-collection")
def save_collection(data: dict, db: Session = Depends(get_db)):
    crud.save_daily_collection(db, data["branch_code"], data["category"], data["number"], data["amount"])
    snapshot = crud.get_collection_snapshot(db, data["branch_code"], data["category"])
    return snapshot

@app.post("/migrate-yesterday-data")
def migrate_yesterday_data(branch_code: str, db: Session = Depends(get_db)):
    """Manually migrate yesterday's data to previous day fields"""
    success = crud.migrate_yesterday_to_previous(db, branch_code)
    if success:
        return {"status": "success", "message": "Yesterday's data migrated to previous day"}
    else:
        return {"status": "error", "message": "Branch data not found"}

@app.post("/urgent/seen")
def mark_seen(emp_id: str, urgent_id: int, db: Session = Depends(get_db)):
    existing = db.query(UrgentSeen).filter(
        UrgentSeen.emp_id == emp_id,
        UrgentSeen.urgent_id == urgent_id,
    ).first()
    if existing:
        return {"status": "already_seen", "emp_id": emp_id, "urgent_id": urgent_id}

    seen = UrgentSeen(emp_id=emp_id, urgent_id=urgent_id)
    db.add(seen)
    db.commit()
    return {"status": "seen", "emp_id": emp_id, "urgent_id": urgent_id}

@app.get("/urgent/report/{urgent_id}")
def get_seen_report(urgent_id: int, db: Session = Depends(get_db)):
    seen_records = db.query(UrgentSeen).filter(UrgentSeen.urgent_id == urgent_id).all()
    return [
        {
            "emp_id": s.emp_id,
            "name": s.employee.name,
            "branch": s.employee.branch.branch_name,
            "seen_at": str(s.seen_at)
        }
        for s in seen_records
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
