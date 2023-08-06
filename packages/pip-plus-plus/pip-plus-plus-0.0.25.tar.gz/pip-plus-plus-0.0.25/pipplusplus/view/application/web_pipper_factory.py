import _thread
import json
import os
import pathlib

from flask import render_template, url_for, request, make_response

from utils.thread_safe_dict import ThreadSafeDict
from utils.url_msg_parser import UrlMessageListParser
from view.application.flask_piper import FlaskPipper


class WebPipperFactory(object):
    @classmethod
    def get_pipper(cls, **kwargs):
        pass


def command_runner(run_command, data, req_method):
    print("Starting command")
    FlaskPipperFactory.REQUESTS[data["id"]] = ThreadSafeDict()
    page, msg = run_command(data, req_type=req_method)
    if not msg:
        msg = "None"

    print("Finishing command")
    FlaskPipperFactory.REQUESTS[data["id"]]["page"] = page
    FlaskPipperFactory.REQUESTS[data["id"]]["msg"] = msg
    FlaskPipperFactory.REQUESTS[data["id"]]["status"] = "Done"


def get_template_path():
    package_path = os.path.realpath(os.path.join(__file__, "..", "..", ".."))
    temp_path = os.path.join(package_path, "templates")
    return temp_path


class FlaskPipperFactory(WebPipperFactory):
    REQUESTS = ThreadSafeDict()

    @classmethod
    def get_pipper(cls, **kwargs):
        app = FlaskPipper("Pipper", template_folder=get_template_path())

        @app.route("/")
        def main_page():
            return render_template("home.html")

        @app.route("/status", methods=['GET'])
        def get_stat():
            id = request.args["id"]
            req = cls.REQUESTS[id]
            if "page" in req and "list" == req["page"]:
                req = {
                    "page": "list",
                    "msg": id,
                    "status": "Done"
                }
            response = make_response()
            response.data = str(req).replace("'", "\"")
            return response

        @app.route("/about")
        def about():
            return render_template("about.html")

        @app.route("/submit", methods=['GET', 'POST'])
        def submit_request():
            data = json.loads(request.data)
            cls.REQUESTS[data["id"]] = ThreadSafeDict()
            cls.REQUESTS[data["id"]]["status"] = "Processed"

            _thread.start_new_thread(command_runner, (app.run_command, data, request.method))

            response = make_response()
            response.data = str(cls.REQUESTS[data["id"]]).replace("'", "\"")
            return response

        @app.route("/success")
        @app.route("/success/<msg>")
        def success_page(msg=""):
            return render_template("success.html", msg=msg)

        @app.route("/failure")
        @app.route("/failure/<msg>")
        def failure(msg=""):
            return render_template("failure.html", msg=msg)

        @app.route("/list/<proc_id>")
        def list_packages(proc_id):
            msg = UrlMessageListParser.parse(cls.REQUESTS[proc_id]["msg"])
            return render_template("list.html", msg=msg)

        @app.route("/waiting")
        def waiting_page():
            proc_id = request.args["id"]
            return render_template("waiting.html", msg=proc_id)

        with app.test_request_context():
            cls.set_static()

        return app

    @classmethod
    def set_static(cls):
        proj_dir = pathlib.Path(__file__).parent.parent.parent
        static_path = proj_dir / "static"

        for static_file in static_path.iterdir():
            url_for("static", filename=static_file.name)
