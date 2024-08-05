from typing import Dict, Any

from reactpy import component, html, event, hooks

from NodeInfo import NodeInfo

@component
def WelcomeComponent(data: NodeInfo, set_data: Any):
    return html.div({
        "class_name": "drawflow_content_node"
    }, [
        html.div({"class_name": "title-box"}, "Welcome!!"),
        html.div({"class_name": "box"}, [
            html.p("Simple flow demo based on ", html.b("Jero Soler"), "'s beautiful ", html.a({"href": "https://github.com/jerosoler/Drawflow", "target": "_blank"}, "Drawflow"), "."),
            html.br(),
            html.br(),
            html.p("Run with the command: ", html.b("uvicorn example:app --reload"))
        ])
    ])

@component
def DbClickComponent(data: NodeInfo, set_data: Any):
    return html.div({
        "class_name": "drawflow_content_node"
    }, [
        html.div({"class_name": "title-box"}, html.i({"class_name": "fas fa-mouse"}), " Db Click"),
        html.div({"class_name": "box dbclickbox", "ondblclick": lambda event: showpopup(event)}, [
            "Db Click here",
            html.div({"class_name": "modal", "style": {"display": "none"}}, [
                html.div({"class_name": "modal-content"}, [
                    html.span({"class_name": "close", "onclick": lambda event: closemodal(event)}, "&times;"),
                    html.p("Change your variable {name}!"),
                    html.input({"type": "text", "df-name": ""})
                ])
            ])
        ])
    ])

@component
def PersonalizedComponent(data: NodeInfo, set_data: Any):
    return html.div({
        "class_name": "drawflow_content_node"
    }, "Personalized")

@component
def MultipleComponent(data: NodeInfo, set_data: Any):
    return html.div({
        "class_name": "drawflow_content_node"
    }, [
        html.div({"class_name": "box"}, "Multiple!")
    ])

@component
def TemplateComponent(data: NodeInfo, set_data: Any):
    node_info, _ = hooks.use_state(data)
    
    @event(prevent_default=True, stop_propagation=False)
    def on_textarea_change(event):
        new_text = event["target"]["value"]
        updated_data = node_info.copy()
        updated_data.data["template"] = new_text
        set_data(updated_data)
    
    return html.div({
        "class_name": "drawflow_content_node"
    }, [
        html.div({"class_name": "title-box"}, html.i({"class_name": "fas fa-code"}), " Template"),
        html.div({"class_name": "box"}, [
            html.p("Ger Vars"),
            html.textarea({
                "df-template": "",
                "value": node_info.data.get("template", ""),
                "onChange": on_textarea_change
            }),
            html.p("Output template with vars")
        ])
    ])

@component
def EmailComponent(data: NodeInfo, set_data: Any):
    return html.div({
        "class_name": "drawflow_content_node"
    }, [
        html.div({"class_name": "title-box"}, html.i({"class_name": "fas fa-at"}), " Send Email")
    ])

@component
def GoogleComponent(data: NodeInfo, set_data: Any):
    return html.div({
        "class_name": "drawflow_content_node"
    }, [
        html.div({"class_name": "title-box"}, html.i({"class_name": "fab fa-google-drive"}), " Google Drive save")
    ])

@component
def LogComponent(data: NodeInfo, set_data: Any):
    return html.div({
        "class_name": "drawflow_content_node"
    }, [
        html.div({"class_name": "title-box"}, html.i({"class_name": "fas fa-file-signature"}), " Save log file")
    ])

@component
def AWSComponent(data: NodeInfo, set_data: Any):
    return html.div({
        "class_name": "drawflow_content_node"
    }, [
        html.div({"class_name": "title-box"}, html.i({"class_name": "fab fa-aws"}), " Aws Save"),
        html.div({"class_name": "box"}, [
            html.p("Save in aws"),
            html.input({"type": "text", "df-db-dbname": "", "placeholder": "DB name"}),
            html.br(), html.br(),
            html.input({"type": "text", "df-db-key": "", "placeholder": "DB key"}),
            html.p("Output Log")
        ])
    ])

@component
def TelegramComponent(data: NodeInfo, set_data: Any):
    node_info, _ = hooks.use_state(data)
    
    @event(prevent_default=True, stop_propagation=False)
    def on_channel_change(event):
        new_channel = event["target"]["value"]
        updated_data = node_info.copy()
        updated_data.data["channel"] = new_channel
        set_data(updated_data)

    return html.div({
        "class_name": "drawflow_content_node"
    }, [
        html.div({"class_name": "title-box"}, html.i({"class_name": "fab fa-telegram-plane"}), " Telegram bot"),
        html.div({"class_name": "box"}, [
            html.p("Send to telegram"),
            html.p("select channel"),
            html.select({
                "df-channel": "",
                "value": node_info.data.get("channel", ""),
                "onChange": on_channel_change
            }, [
                html.option({"value": "channel_1"}, "Channel 1"),
                html.option({"value": "channel_2"}, "Channel 2"),
                html.option({"value": "channel_3"}, "Channel 3"),
                html.option({"value": "channel_4"}, "Channel 4")
            ])
        ])
    ])

@component
def GithubComponent(data: NodeInfo, set_data: Any):
    node_info, _ = hooks.use_state(data)
    
    @event(prevent_default=True, stop_propagation=False)
    def on_input_change(event):
        new_url = event["target"]["value"]
        updated_data = node_info.copy()
        updated_data.data["url"] = new_url
        set_data(updated_data)

    return html.div({
        "class_name": "drawflow_content_node"
    }, [
        html.div({"class_name": "title-box"}, html.i({"class_name": "fab fa-github"}), " Github Stars"),
        html.div({"class_name": "box"}, [
            html.p("Enter repository url"),
            html.input({
                "type": "text",
                "df-name": "",
                "value": node_info.data.get("url", ""),
                "onChange": on_input_change
            })
        ])
    ])

@component
def SlackComponent(data: NodeInfo, set_data: Any):
    return html.div({
        "class_name": "drawflow_content_node"
    }, [
        html.div({"class_name": "title-box"}, html.i({"class_name": "fab fa-slack"}), " Slack chat message")
    ])

@component
def FacebookComponent(data: NodeInfo, set_data: Any):
    return html.div({
        "class_name": "drawflow_content_node"
    }, [
        html.div({"class_name": "title-box"}, html.i({"class_name": "fab fa-facebook"}), " Facebook Message")
    ])


# Map component names to actual components
component_map = {
    "WelcomeComponent": WelcomeComponent,
    "SlackComponent": SlackComponent,
    "FacebookComponent": FacebookComponent,
    "GithubComponent": GithubComponent,
    "TelegramComponent": TelegramComponent,
    "AWSComponent": AWSComponent,
    "LogComponent": LogComponent,
    "GoogleComponent": GoogleComponent,
    "EmailComponent": EmailComponent,
    "TemplateComponent": TemplateComponent,
    "MultipleComponent": MultipleComponent,
    "PersonalizedComponent": PersonalizedComponent,
    "DbClickComponent": DbClickComponent,
    # Add more components if needed...
}