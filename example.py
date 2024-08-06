from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from reactpy import component, hooks, html
from reactpy.backend.fastapi import configure, FastAPI

from drawflow_logger import log
from DrawflowInfo import DrawflowInfo
from Drawflow import Drawflow
from your_component_file import component_map

app = FastAPI()

# mounting the static folder will ensure that files are served with the correct MIME type
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
    name="static",
)

@component
def App():
    initial_drawflow = {
                "1": {
                    "name": "welcome",
                    "data": {},
                    "class": "welcome",
                    "component": "WelcomeComponent",
                    "inputs": [],
                    "outputs": {},
                    "pos_x": 50,
                    "pos_y": 50
                },
                "2": {
                    "name": "slack",
                    "data": {},
                    "class": "slack",
                    "component": "SlackComponent",
                    "inputs": ["input_1"],
                    "outputs": {},
                    "pos_x": 1028,
                    "pos_y": 87
                },
                "3": {
                    "name": "telegram",
                    "data": {"channel": "channel_2"},
                    "class": "telegram",
                    "component": "TelegramComponent",
                    "inputs": ["input_1"],
                    "outputs": {},
                    "pos_x": 1032,
                    "pos_y": 184
                },
                "4": {
                    "name": "email",
                    "data": {},
                    "class": "email",
                    "component": "EmailComponent",
                    "inputs": ["input_1"],
                    "outputs": {},
                    "pos_x": 1033,
                    "pos_y": 439
                },
                "5": {
                    "name": "template",
                    "data": {"template": "Write your template"},
                    "class": "template",
                    "component": "TemplateComponent",
                    "inputs": ["input_1"],
                    "outputs": {
                        "output_1": {}
                    },
                    "pos_x": 607,
                    "pos_y": 304
                },
                "6": {
                    "name": "github",
                    "data": {"name": "https://github.com/jerosoler/Drawflow"},
                    "class": "github",
                    "component": "GithubComponent",
                    "inputs": [],
                    "outputs": {
                        "output_1": {
                            "connections": [{"node": "5", "input": "input_1"}]
                        }
                    },
                    "pos_x": 341,
                    "pos_y": 191
                },
                "7": {
                    "name": "facebook",
                    "data": {},
                    "class": "facebook",
                    "component": "FacebookComponent",
                    "inputs": [],
                    "outputs": {
                        "output_1": {
                            "connections": [
                                {"node": "2", "input": "input_1"},
                                {"node": "3", "input": "input_1"},
                                {"node": "11", "input": "input_1"}
                            ]
                        }
                    },
                    "pos_x": 347,
                    "pos_y": 87
                },
                "11": {
                    "name": "log",
                    "data": {},
                    "class": "log",
                    "component": "LogComponent",
                    "inputs": ["input_1"],
                    "outputs": {},
                    "pos_x": 1031,
                    "pos_y": 363
                },
                "8": {
                    "name": "personalized",
                    "data": {},
                    "class": "personalized",
                    "component": "PersonalizedComponent",
                    "inputs": ["input_1"],
                    "outputs": {
                        "output_1": {
                            "connections": [{"node": "9", "input": "input_1"}]
                        }
                    },
                    "pos_x": 764,
                    "pos_y": 227
                },
                "9": {
                    "name": "dbclick",
                    "data": {"name": "Hello World!!"},
                    "class": "dbclick",
                    "component": "DbClickComponent",
                    "inputs": ["input_1"],
                    "outputs": {
                        "output_1": {
                            "connections": [{"node": "12", "input": "input_1"}]
                        }
                    },
                    "pos_x": 209,
                    "pos_y": 38
                },
                "12": {
                    "name": "multiple",
                    "data": {},
                    "class": "multiple",
                    "component": "MultipleComponent",
                    "inputs": ["input_1", "input_2"],
                    "outputs": {
                        "output_1": {
                            "connections": [{"node": "8", "input": "input_1"}]
                        },
                        "output_2": {
                            "connections": []
                        },
                        "output_3": {
                            "connections": []
                        },
                        "output_4": {
                            "connections": []
                        }
                    },
                    "pos_x": 179,
                    "pos_y": 272
                }
    }
    nodes_data, set_nodes_data = hooks.use_state(DrawflowInfo.from_dict(initial_drawflow))

    log(f'App ➜ 🖼 {initial_drawflow.keys()}')

    return html.div(
        {"style": {"user-select": "none", "-moz-user-select": "none", "-webkit-user-select": "none", "-ms-user-select": "none"}},
        html.link({"rel": "stylesheet", "type": "text/css", "href": app.url_path_for('static', path='drawflow.css')}),
        html.link({"rel": "stylesheet", "type": "text/css", "href": app.url_path_for('static', path='beautiful.css')}),
        html.link({"rel": "stylesheet", "href":"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.13.0/css/all.min.css", "integrity": "sha256-h20CPZ0QyXlBuAw7A+KluUYx/3pK+c7lYEpqLTlxjYQ=", "crossorigin": "anonymous"}),
        html.link({"href": "https://fonts.googleapis.com/css2?family=Roboto&display=swap", "rel": "stylesheet"}),
        Drawflow(nodes_data, set_nodes_data, component_map, _offset=(0, 37))
    )

# run
configure(app, App)
