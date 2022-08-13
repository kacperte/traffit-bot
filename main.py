from agents.traffit_bot import TraffitBot
from mail_connector import MailAdapter
from messages_parser import CandidateAlert
from dotenv import load_dotenv
from os import getenv

load_dotenv()

mailer = MailAdapter(
    host="poczta23110.e-kei.pl",
    port=465,
    username=getenv("L_MAIL"),
    password=getenv("P_MAIL"),
)

msg = CandidateAlert()

content = TraffitBot().get_info_about_all_active_project()
mailer.send_mail(
    recipient_email="kacperte@gmail.com",
    subject="Status kandydatów",
    content=msg.render(content=content),
)
