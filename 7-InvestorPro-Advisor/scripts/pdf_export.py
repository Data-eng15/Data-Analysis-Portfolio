from fpdf import FPDF

class InvestmentPDF(FPDF):
    def __init__(self, title="Investment Summary"):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.set_title(title)
        self.set_font("Arial", size=12)
        self.cell(200, 10, txt=title, ln=True, align='C')
        self.ln(10)

    def add_section(self, heading):
        self.set_font("Arial", 'B', size=12)
        self.cell(200, 10, txt=heading, ln=True)
        self.set_font("Arial", size=12)

    def add_key_value(self, key, value):
        self.cell(200, 8, txt=f"{key}: {value}", ln=True)

    def add_spacer(self, height=5):
        self.ln(height)

    def export(self):
        return self.output(dest='S').encode('latin1')