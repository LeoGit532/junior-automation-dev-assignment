import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv


def send_report_email(report_path, summary):
    load_dotenv()

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    email_from = os.getenv("EMAIL_FROM")
    email_to = os.getenv("EMAIL_TO")

    if not all([smtp_host, smtp_user, smtp_password, email_from, email_to]):
        print("Envio de e-mail ignorado: variáveis SMTP não configuradas.")
        return False

    report_path = Path(report_path)

    msg = EmailMessage()
    msg["Subject"] = "Relatório de Faturamento Hospitalar"
    msg["From"] = email_from
    msg["To"] = email_to

    html_body = f"""
    <html>
        <body>
            <h2>Relatório de Faturamento</h2>
            <p>O pipeline foi executado com sucesso.</p>

            <ul>
                <li><strong>PDFs processados:</strong> {summary.get("total", 0)}</li>
                <li><strong>PDFs renomeados:</strong> {summary.get("renomeados", 0)}</li>
                <li><strong>PDFs para revisão manual:</strong> {summary.get("revisao_manual", 0)}</li>
            </ul>

            <p>O relatório consolidado segue em anexo.</p>
        </body>
    </html>
    """

    msg.set_content("Relatório de faturamento gerado. Consulte o anexo.")
    msg.add_alternative(html_body, subtype="html")

    with open(report_path, "rb") as file:
        msg.add_attachment(
            file.read(),
            maintype="application",
            subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=report_path.name
        )

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)

    print("E-mail enviado com sucesso.")
    return True