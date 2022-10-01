import jinja2


class Message:
    def __init__(self):
        template_loader = jinja2.FileSystemLoader(searchpath="./")
        self.template_env = jinja2.Environment(loader=template_loader)
        self.template = self.template_env.get_template(self.TEMPLATE_FILE)

    def render(self, **kwargs):
        return self.template.render(**kwargs)


class CandidateAlert(Message):
    TEMPLATE_FILE = "./templates/candidate_alert.html"


class TestsAlert(Message):
    TEMPLATE_FILE = "./templates/tests_alert.html"
