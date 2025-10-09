import os, sqlite3, datetime
from flask import Blueprint, request, render_template
from mailer import send_email
gumroad_bp=Blueprint('gumroad', __name__)
DB_PATH=os.path.join('database','users.db')
BASE_URL=os.environ.get('BASE_URL','https://archetype-retreats.onrender.com')
@gumroad_bp.route('/gumroad_webhook', methods=['POST'])
def gumroad_webhook():
    payload=request.form; email=(payload.get('email') or '').strip().lower()
    product=(payload.get('product_name') or '').lower(); buyer_name=(payload.get('full_name') or '').strip()
    ts=datetime.datetime.now().isoformat()
    if not email: return 'Missing email',400
    if 'bundle' in product: ptype='bundle'
    elif 'book' in product: ptype='book'
    else: ptype='preview'
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory=sqlite3.Row
        cur=conn.execute('SELECT * FROM users WHERE lower(email)=? ORDER BY id DESC',(email,)); row=cur.fetchone()
        if row:
            conn.execute('UPDATE users SET purchase_type=?, timestamp=? WHERE id=?',(ptype,ts,row['id'])); pdf_path=row['pdf_path']
        else:
            conn.execute('INSERT INTO users (email,name,purchase_type,timestamp) VALUES (?,?,?,?)',(email,buyer_name or None,ptype,ts)); pdf_path=None
        conn.commit()
    html_body=render_template('thank_you.html', name=buyer_name or (email.split('@')[0].title()), purchase_type=ptype, email=email, base_url=BASE_URL)
    attachments=[]; 
    if ptype in ['preview','bundle'] and pdf_path: attachments.append(pdf_path)
    if ptype in ['book','bundle']: attachments.append('static/pdfs/YourStoryIsYou.pdf')
    send_email(email,'Thank you • Archetype Retreats',html_body,attachments)
    return 'OK',200
