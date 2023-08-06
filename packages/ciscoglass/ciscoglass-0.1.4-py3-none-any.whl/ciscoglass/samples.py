MAIN_PY = """\
from ciscoglass import GlassApp


class {name}(GlassApp):
    def run(self):
        print("Glass App ran successfully!")


if __name__ == "__main__":
    {name}().run()
"""

DOCKERFILE = """\
FROM python:{major}.{minor}-alpine

# Set workdir
WORKDIR /ciscoglass/apps/{name}

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy code
COPY . .

# Set a default entrypoint
ENTRYPOINT ["python3", "-u", "main.py"]
"""

REQUIREMENTS = """\
ciscoglass=={version}
"""

SPEC = {
    "name": "App Name",
    "desc": "Description",
    "img": "http://image/url",
    "usage": "Long description",
    "config": {
        "repo": "repo_name",
        "namespace": "ciscoglass/",
        "tag": "latest",
        "device_type": "TEST",
        "one_shot": True,
    }
}
