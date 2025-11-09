import os, sqlite3, datetime
from flask import Flask, render_template, request, send_file, redirect, url_for, session, Response
from dotenv import load_dotenv
from archetype_logic import determine_archetype
from pdf_generator import create_pdf
from gumroad_webhook import gumroad_bp
from scheduler import start_scheduler
load_dotenv()
app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/static",
    template_folder="templates"
)
# Redirect "www." URLs to root domain for HTTPS consistency
from flask import redirect, request

@app.before_request
def redirect_www():
    url = request.url
    if url.startswith("http://www.") or url.startswith("https://www."):
        return redirect(url.replace("://www.", "://", 1), code=301)
# redeploy trigger for static css visibility
# Optional: prevent CSS caching during testing
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Explicit static route (helps on Render)
@app.route('/static/<path:filename>')
def static_files(filename):
    from flask import send_from_directory
    return send_from_directory('static', filename)
app.secret_key=os.environ.get('SECRET_KEY','please_change_me')
ADMIN_USER='angelo'; ADMIN_PASS=os.environ.get('ADMIN_PASS','retreat2025')
DB_PATH=os.path.join('database','users.db')
def init_db():
    os.makedirs('database', exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT, name TEXT,
            cube TEXT, ladder TEXT, horse TEXT, weather TEXT, flowers TEXT,
            archetype TEXT, purchase_type TEXT, pdf_path TEXT, timestamp TEXT,
            followed_up1 INTEGER DEFAULT 0, followed_up2 INTEGER DEFAULT 0
        )''')
init_db(); start_scheduler(DB_PATH)
@app.route('/')
def home(): return render_template('index.html')
@app.route('/test')
def test_form(): return render_template('innercube.html')
@app.route('/submit', methods=['POST'])
def submit():
    email=request.form.get('email','').strip().lower()
    data={k: request.form.get(k,'') for k in ['cube','ladder','horse','weather','flowers']}
    data['email']=email
    archetype=determine_archetype(data)
    pdf_path=create_pdf(archetype,data)
    ts=datetime.datetime.now().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''INSERT INTO users (email,cube,ladder,horse,weather,flowers,archetype,purchase_type,pdf_path,timestamp)
                        VALUES (?,?,?,?,?,?,?,?,?,?)''',(email,data['cube'],data['ladder'],data['horse'],data['weather'],data['flowers'],archetype,'preview',pdf_path,ts))
    return render_template('result.html', archetype=archetype, pdf_path=pdf_path, email=email)
@app.route('/innercube')
def innercube():
    return render_template('innercube.html')
@app.route('/purchase')
def purchase(): return render_template('purchase.html')
@app.route('/download/<path:filename>')
def download(filename): return send_file(filename, as_attachment=True)
@app.route('/my_downloads')
def my_downloads():
    email=request.args.get('email','').strip().lower()
    if not email: return 'Please provide your email, e.g. /my_downloads?email=you@example.com'
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory=sqlite3.Row
        row=conn.execute('SELECT * FROM users WHERE lower(email)=? ORDER BY id DESC',(email,)).fetchone()
    if not row: return f'No record found for {email}. Make sure you used the same email as your Gumroad purchase.'
    purchase_type=row['purchase_type']; pdf_path=row['pdf_path']
    downloads=[]
    if purchase_type in ['preview','bundle']: downloads.append({'label':'3-Page Archetype Report','path':pdf_path})
    if purchase_type in ['book','bundle']: downloads.append({'label':'Your Story Is You (Full Book)','path':'static/pdfs/YourStoryIsYou.pdf'})
    return render_template('downloads.html', email=email, purchase_type=purchase_type, downloads=downloads)
@app.route('/reserve', methods=['POST'])
def reserve():
    name=request.form.get('name',''); email=request.form.get('email','').strip().lower(); archetype=request.form.get('archetype',''); ts=datetime.datetime.now().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('INSERT INTO users (email,name,archetype,purchase_type,timestamp) VALUES (?,?,?,?,?)',(email,name,archetype,'retreat_interest',ts))
    return render_template('thank_you.html', name=name)
@app.route('/admin', methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        if request.form.get('user')=='angelo' and request.form.get('password')==ADMIN_PASS:
            session['admin']=True; return redirect('/dashboard')
        return render_template('admin_login.html', error='Invalid credentials')
    return render_template('admin_login.html')
@app.route('/dashboard')
def dashboard():
    if not session.get('admin'): return redirect('/admin')
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory=sqlite3.Row
        users=conn.execute('SELECT * FROM users ORDER BY timestamp DESC').fetchall()
    return render_template('dashboard.html', users=users)
@app.route('/export_csv')
def export_csv():
    if not session.get('admin'): return redirect('/admin')
    def generate():
        with sqlite3.connect(DB_PATH) as conn:
            cur=conn.execute('SELECT * FROM users'); yield ','.join([d[0] for d in cur.description])+'\n'
            for row in cur: yield ','.join([str(v) for v in row])+'\n'
    from flask import Response
    return Response(generate(), mimetype='text/csv', headers={'Content-Disposition':'attachment; filename=innercube_users.csv'})
@app.route('/logout')
def logout(): session.clear(); return redirect('/')
@app.route('/robots.txt')
def robots_txt(): return app.send_static_file('robots.txt')
@app.route('/retreats')
def retreats():
    return render_template('retreats.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

@app.route("/innercube_thankyou")
def innercube_thankyou():
    return render_template("innercube_thankyou.html")
    
 @app.route('/retreats')
def retreats():
    return render_template('retreats.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/innercube')
def innercube():
    return render_template('innercube.html')   
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
