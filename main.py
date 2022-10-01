from agents.traffit_bot import TraffitBot
from mail_adapter.mail_connector import MailAdapter
from mail_adapter.messages_parser import CandidateAlert, CandidateAlertEmpty
from mail_adapter.emial_preparer import EmailPreparer
import os


if __name__ == "__main__":
    info = TraffitBot(
        login=os.environ.get("LOGIN"),
        password=os.environ.get("PASSWORD")
    ).get_info_about_all_active_project()

    prepared_info = EmailPreparer(data=info).assign_candidates_to_recruiter()
    msg = CandidateAlert()
    msg_empty = CandidateAlertEmpty()
    mailer = MailAdapter(
        host="poczta23110.e-kei.pl",
        port=465,
        username=os.getenv("L_MAIL"),
        password=os.getenv("P_MAIL"),
    )

    # Trzepiecinski
    k_trzepiecinski_info = prepared_info.kacper_trzepiecinski
    if len(k_trzepiecinski_info) > 0:
        mailer.send_mail(
            recipient_email="kacper.trzepiecinski@hsswork.pl",
            subject="Status kandydatów",
            content=msg.render(name="Kacper", content=k_trzepiecinski_info)
        )
    else:
        mailer.send_mail(
            recipient_email="kacper.trzepiecinski@hsswork.pl",
            subject="Status kandydatów",
            content=msg_empty.render(name="Kacper", content=k_trzepiecinski_info))

    # Borowska
    e_borowska_info = prepared_info.ewelina_borowska
    if len(e_borowska_info) > 0:
        mailer.send_mail(
            recipient_email="ewelina.borowska@hsswork.pl",
            subject="Status kandydatów",
            content=msg.render(name="Ewelina", content=e_borowska_info),
        )
    else:
        mailer.send_mail(
            recipient_email="ewelina.borowska@hsswork.pl",
            subject="Status kandydatów",
            content=msg_empty.render(name="Ewelina", content=e_borowska_info),
        )

    # Beta
    e_beta_info = prepared_info.ewelina_beta
    if len(e_beta_info) > 0:
        mailer.send_mail(
                recipient_email="ewelina.beta@hsswork.pl",
                subject="Status kandydatów",
                content=msg.render(name="Ewelina", content=e_beta_info),
            )
    else:
        mailer.send_mail(
            recipient_email="ewelina.beta@hsswork.pl",
            subject="Status kandydatów",
            content=msg_empty.render(name="Ewelina", content=e_beta_info),
        )

    # Rosik
    p_rosik_info = prepared_info.patrycja_rosik
    if len(p_rosik_info) > 0:
        mailer.send_mail(
            recipient_email="patrycja.rosik@hsswork.pl",
            subject="Status kandydatów",
            content=msg.render(name="Patrycja", content=p_rosik_info),
        )
    else:
        mailer.send_mail(
            recipient_email="patrycja.rosik@hsswork.pl",
            subject="Status kandydatów",
            content=msg_empty.render(name="Patrycja", content=p_rosik_info),
        )

