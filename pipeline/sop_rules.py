from datetime import datetime, timedelta
import pandas as pd
# ----------------------------
# SOP RULES
# ----------------------------
def get_next_action(overdue_days):
    if overdue_days <= 7:
        return "Call Customer"
    elif overdue_days <= 15:
        return "Send Reminder"
    else:
        return "Escalate to Legal"


# ----------------------------
# SLA DEADLINES
# ----------------------------
def get_sla_deadline(overdue_days, assigned_date):
    assigned_date = pd.to_datetime(assigned_date)

    if overdue_days <= 7:
        return assigned_date + timedelta(days=2)
    elif overdue_days <= 15:
        return assigned_date + timedelta(days=3)
    else:
        return assigned_date + timedelta(days=1)


# ----------------------------
# SLA BREACH CHECK
# ----------------------------
def check_sla_breach(sla_deadline):
    return datetime.now() > sla_deadline
from datetime import datetime, timedelta
import pandas as pd
# ----------------------------
# SOP RULES
# ----------------------------
def get_next_action(overdue_days):
    if overdue_days <= 7:
        return "Call Customer"
    elif overdue_days <= 15:
        return "Send Reminder"
    else:
        return "Escalate to Legal"


# ----------------------------
# SLA DEADLINES
# ----------------------------
def get_sla_deadline(overdue_days, assigned_date):
    assigned_date = pd.to_datetime(assigned_date)

    if overdue_days <= 7:
        return assigned_date + timedelta(days=2)
    elif overdue_days <= 15:
        return assigned_date + timedelta(days=3)
    else:
        return assigned_date + timedelta(days=1)


# ----------------------------
# SLA BREACH CHECK
# ----------------------------
def check_sla_breach(sla_deadline):
    return datetime.now() > sla_deadline
