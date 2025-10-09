import os, sqlite3, datetime
from apscheduler.schedulers.background import BackgroundScheduler
from flask import render_template
from mailer import send_email
def send_followups(db_path):
    now=datetime.datetime.utcnow()
    with sqlite3.connect(db_path) as conn:
        conn.row_factory=sqlite3.Row
        rows=conn.execute('SELECT * FROM users').fetchall()
        for r in rows:
            ptype=(r['purchase_type'] or '').lower()
            try: ts=datetime.datetime.fromisoformat((r['timestamp'] or '').split('.')[0])
            except Exception: continue
            days=(now-ts).days; email=r['email']
            if (ptype in ['', 'preview', None]) and (days>=2) and (not r['followed_up1']):
                html=render_template('followup1.html'); send_email(email,'Your Archetype Still Speaks',html,None)
                conn.execute('UPDATE users SET followed_up1=1 WHERE id=?',(r['id'],)); conn.commit()
            if (ptype in ['', 'preview', None]) and (days>=5) and (not r['followed_up2']):
                html=render_template('followup2.html'); send_email(email,'Your Story Is You',html,None)
                conn.execute('UPDATE users SET followed_up2=1 WHERE id=?',(r['id'],)); conn.commit()
def start_scheduler(db_path):
    sched=BackgroundScheduler(daemon=True); sched.add_job(send_followups,'cron',hour=9,minute=0,args=[db_path],id='daily_followups',replace_existing=True); sched.start()
