from collections import namedtuple

Recruiter = namedtuple(
    "Recruiter", "ewelina_borowska ewelina_beta patrycja_rosik kacper_trzepiecinski"
)


class EmailPreparer:
    def __init__(self, data: list):
        self.data = data

    def locate_candidates_to_recruiter(self):
        if not self.data:
            raise BaseException("Incorrect data was given - empty dataset.")

        borowska = list()
        beta = list()
        trzepiecinski = list()
        rosik = list()

        for result in self.data:
            if result["Project Owner"] == "Ewelina Borowska":
                borowska.append(result)
            if result["Project Owner"] == "Ewelina Beta":
                beta.append(result)
            if result["Project Owner"] == "Patrycja Rosik":
                rosik.append(result)
            else:
                trzepiecinski.append(result)

        borowska = self.prepar_input_to_mails(borowska)
        beta = self.prepar_input_to_mails(beta)
        trzepiecinski = self.prepar_input_to_mails(trzepiecinski)
        rosik = self.prepar_input_to_mails(rosik)

        return Recruiter(borowska, beta, rosik, trzepiecinski)

    @staticmethod
    def prepar_input_to_mails(recruiter_data):
        prepared_info = list()

        for project in recruiter_data:
            project_info = list()
            project_info.append(project["Client"])
            project_info.append(project["Project"])
            candidates = list()

            for candidate in project["Candidate"]:
                candidates.append([candidate, project["Candidate"][candidate]])
            project_info.append(candidates)
            prepared_info.append(project_info)

        return prepared_info
