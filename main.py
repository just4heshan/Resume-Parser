from pdfminer.high_level import extract_text
import spacy, re, json

# Create Entity Ruler and return data from the pdf....
# Some of the entities are showing differ entity labels usual than actual label type
# So we can create patterns to change their labels


class CreateEntity:
    patterns = [
        {'label': 'GPE', 'pattern': 'Oakdale Street'},
        {'label': 'GPE', 'pattern': 'VIC'},
        {'label': 'GPE', 'pattern': 'Broadmeadows'},
        {'label': 'ORG', 'pattern': 'Algorithms'},
        {'label': 'ORG', 'pattern': 'Front End Developer'},
        {'label': 'ORG', 'pattern': 'ETL'},
        {'label': 'ORG', 'pattern': 'CSV'},
        {'label': 'ORG', 'pattern': 'Flask'},
        {'label': 'ORG', 'pattern': 'PostgreSQL'},
        {'label': 'ORG', 'pattern': 'SQLAlchemy '},
        {'label': 'ORG', 'pattern': 'Machine Learning'},
        {'label': 'ORG', 'pattern': 'Python'},
        {'label': 'ORG', 'pattern': 'Django'},
        {'label': 'ORG', 'pattern': 'Java'},
        {'label': 'ORG', 'pattern': 'C++'},
        {'label': 'ORG', 'pattern': 'Tableau'},
        {'label': 'ORG', 'pattern': 'AI'},
        {'label': 'ORG', 'pattern': 'Pytz '},
        {'label': 'ORG', 'pattern': 'Jupyter '},
        {'label': 'ORG', 'pattern': 'Justpy '},
        {'label': 'ORG', 'pattern': 'Docker '},
        {'label': 'ORG', 'pattern': 'Problem '},
    ]

    def __init__(self):
        self.resume_data = extract_text('Heshan_Rathnayake_Resume.pdf')
        self.resume_data.replace('/t', ' ')
        self.nlp_label = spacy.load('en_core_web_sm')
        self.ruler = self.nlp_label.add_pipe('entity_ruler', before='ner')
        self.ruler.add_patterns(self.patterns)
        self.doc = self.nlp_label(self.resume_data)

    def find_name(self):
        self.name_list=[]
        for self.ent in self.doc.ents:
            # print(ent.text, ent.label_)
            if self.ent.label_ == 'PERSON':
                self.name = str(self.ent.text)
                self.name_list.append(self.name)
        return self.name_list

    def find_org(self):
        self.org_list=[]
        for self.ent in self.doc.ents:
            if self.ent.label_ == 'ORG':
                self.org = str(self.ent.text)
                self.org_list.append(self.org)
        return self.org_list


def extract_emails(resume_text):
    EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
    email = re.findall(EMAIL_REG, resume_text)
    return email


def json_file_create(person, email, org):
    data = {
        'name': person[0],
        'email': email[0],
        'skills': org
    }
    json_file = json.dumps(data, indent=4)
    with open('data.json', 'w') as file:
        json.dump(data, file)
    print(json_file)


if __name__ == '__main__':
    entity_data = CreateEntity()
    person_name = entity_data.find_name()
    entity_data.find_org()
    emails = extract_emails(entity_data.resume_data)
    json_file_create(person_name, emails, entity_data.find_org())
