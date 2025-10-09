from fpdf import FPDF
import os
def create_pdf(archetype, data):
    os.makedirs('static', exist_ok=True)
    from datetime import datetime
    safe_email = (data.get('email') or 'user').replace('@','_').replace('/','_')
    filename = f"static/{safe_email}_{archetype}.pdf"
    pdf = FPDF(); pdf.set_auto_page_break(True, margin=15); pdf.add_page()
    pdf.set_font('Helvetica','B',16); pdf.multi_cell(0,10, f"InnerCube Archetype Report: {archetype.title()}"); pdf.ln(5)
    pdf.set_font('Helvetica','',12)
    pdf.multi_cell(0,8, f"Cube: {data.get('cube','')}\nLadder: {data.get('ladder','')}\nHorse: {data.get('horse','')}\nWeather: {data.get('weather','')}\nFlowers: {data.get('flowers','')}")
    for _ in range(2): pdf.add_page(); pdf.set_font('Helvetica','',12); pdf.multi_cell(0,8, f"Further insights for {archetype.title()}...")
    pdf.output(filename); return filename
