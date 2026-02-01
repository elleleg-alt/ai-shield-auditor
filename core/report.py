
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors

from .schema import AuditReport

def generate_pdf(audit: AuditReport, pdf_path: str) -> str:
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    margin = 0.75 * inch

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, height - margin, "AI Shield Security Audit Report")
    c.setFont("Helvetica", 10)
    meta = audit.meta()
    c.drawString(margin, height - margin - 16, f"Generated: {meta['generated_at']}  |  Overall Score: {meta['overall_score']}  |  Overall Risk: {meta['overall_risk']}")

    y = height - margin - 40

    # Environment
    env = audit.user_environment
    env_text = f"Platform: {env.platform} | Agent Mode: {env.agent_mode} | Connectors: {', '.join(env.connectors) or 'None'}"
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Environment")
    y -= 14
    c.setFont("Helvetica", 10)
    c.drawString(margin, y, env_text)
    y -= 20

    # Categories
    for cat in audit.audit_categories:
        if y < margin + 120:  # new page buffer
            c.showPage()
            y = height - margin
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.black)
        c.drawString(margin, y, f"{cat.category} — Score: {cat.score} | Risk: {cat.risk_level}")
        y -= 12

        c.setFont("Helvetica-Oblique", 9)
        c.drawString(margin, y, "Key Findings:")
        y -= 12
        c.setFont("Helvetica", 9)
        if not cat.findings:
            c.drawString(margin, y, "• None recorded")
            y -= 12
        else:
            for f in cat.findings[:6]:
                text = f"• ({f.severity}) {f.text}"
                y = draw_wrapped(c, text, margin, y, width - 2*margin, 11)
                if y < margin + 120:
                    c.showPage()
                    y = height - margin

        c.setFont("Helvetica-Oblique", 9)
        c.drawString(margin, y, "Top Recommendations:")
        y -= 12
        c.setFont("Helvetica", 9)
        if not cat.recommendations:
            c.drawString(margin, y, "• None recorded")
            y -= 12
        else:
            for r in cat.recommendations[:6]:
                text = f"• ({r.effort}) {r.text}"
                y = draw_wrapped(c, text, margin, y, width - 2*margin, 11)
                if y < margin + 120:
                    c.showPage()
                    y = height - margin
        y -= 8

    c.showPage()
    c.save()
    return pdf_path

def draw_wrapped(c, text, x, y, max_width, leading):
    from reportlab.pdfbase.pdfmetrics import stringWidth
    words = text.split()
    line = ""
    for w in words:
        test = (line + " " + w).strip()
        if stringWidth(test, "Helvetica", 9) < max_width:
            line = test
        else:
            c.drawString(x, y, line)
            y -= leading
            line = w
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y
