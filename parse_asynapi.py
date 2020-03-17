import pprint

import yaml

class AsyncApiParser:
    def __init__(self, spec_file: str, template_file: str):
        self.spec_file = spec_file
        self.template_file = template_file
        self.spec_data = ""
        self.template_data = ""

    def read_yaml(self, filename: str) -> str:
        with open(filename, 'r') as stream:
            try:
                data = yaml.safe_load(stream)
                return data
            except yaml.YAMLError as exc:
                print(exc)

    def write_yaml(self, filename: str, data: dict) -> str:
        with open(filename, 'w') as stream:
            try:
                yaml.dump(data, stream)
            except yaml.YAMLError as exc:
                print(exc)

    def read_spec(self):
        self.spec_data = self.read_yaml(self.spec_file)

    def read_template(self):
        self.template_data = self.read_yaml(self.template_file)

    def parse_schemas(self):
        if not self.spec_data:
            self.read_spec()
        if not self.template_data:
            self.read_template()

        schemas = self.spec_data["components"]["schemas"]
        self.template_data["components"]["schemas"] = schemas
        self.write_yaml("specs/tt.yml", self.template_data)


parser = AsyncApiParser("specs/async-api.yml", "specs/template.yml")
parser.parse_schemas()
