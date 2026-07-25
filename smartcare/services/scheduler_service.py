"""
Background job scheduling (APScheduler). Runs inside the same process as
the Flask app — fine for a single-instance deployment like this one; a
multi-worker production setup would move this to a separate worker process
to avoid the job running once per worker.
"""

import logging

from apscheduler.schedulers.background import BackgroundScheduler

from smartcare.emails.mailer import send_bill_reminder
from smartcare.services.billing_service import get_bills_needing_reminder, mark_reminder_sent

logger = logging.getLogger(__name__)

_scheduler = None


def _send_due_bill_reminders(app):
    """The actual job body. Needs an explicit app context because
    APScheduler runs this outside of any Flask request."""
    with app.app_context():
        bills = get_bills_needing_reminder()
        for bill in bills:
            send_bill_reminder(bill)
            mark_reminder_sent(bill)
        if bills:
            logger.info("Sent %d medicine bill payment reminder(s).", len(bills))


def init_scheduler(app):
    global _scheduler
    if _scheduler is not None:
        return  # already running — never start a second one

    _scheduler = BackgroundScheduler(daemon=True)
    _scheduler.add_job(
        func=lambda: _send_due_bill_reminders(app),
        trigger="interval",
        hours=24,
        id="bill_payment_reminders",
        replace_existing=True,
    )
    _scheduler.start()
    logger.info("Background scheduler started (bill payment reminders every 24h).")