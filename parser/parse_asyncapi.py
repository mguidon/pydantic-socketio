import argparse
import pprint
import tempfile
from pathlib import Path
from subprocess import PIPE, Popen

import yaml

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(message)s")

class AsyncApiParser:
    def __init__(self, spec_file: Path, template_file: Path, model_file: Path):
        self.spec_file = spec_file
        self.template_file = template_file
        self.model_file = model_file
        self.spec_data = ""
        self.template_data = ""

    def read_yaml(self, filename: Path) -> str:
        with open(filename, 'r') as stream:
            try:
                data = yaml.safe_load(stream)
                return data
            except yaml.YAMLError as exc:
                print(exc)

    def write_yaml(self, filename: Path, data: dict) -> str:
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
        with tempfile.NamedTemporaryFile() as fp:
            tmp_file = Path(fp.name)
            self.write_yaml(tmp_file, self.template_data)

            # datamodel-codegen --input tt.yml --output models.py
            p = Popen(['datamodel-codegen', '--input', tmp_file, "--output", self.model_file], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, err = p.communicate()
            rc = p.returncode
            if rc:
                logger.error(err.decode("utf-8"))



def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec_file", help="asyncapi spec file")
    parser.add_argument("--template_file", help="openapi template file")
    parser.add_argument("--model_file", help="pydantic models")
    
    return parser

def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)
    if None in [args.spec_file, args.template_file, args.model_file]:
        parser.error("--spec_file and --template_file are  required")

    spec_file = Path(args.spec_file)
    template_file = Path(args.template_file)
    model_file = Path(args.model_file)
    parser = AsyncApiParser(spec_file, template_file, model_file)
    parser.parse_schemas()



if __name__ == '__main__':
    main()
