from flask import render_template
from google.cloud import storage
from pathlib import PurePath

client = storage.Client()


def rewrite_index():
    client.bucket("www.wowless.dev").blob("index.html").upload_from_string(
        render_template(
            "index.html",
            extracts=[
                PurePath(blob.name).stem
                for blob in client.list_blobs(
                    "wowless.dev", prefix="extracts/"
                )
                if "wow" not in blob.name
            ],
            gscrapes=[
                PurePath(blob.name).stem
                for blob in client.list_blobs(
                    "wowless.dev", prefix="gscrapes/"
                )
            ],
        ),
        content_type="text/html",
    )


def genindex(event, _context):
    n = event["name"]
    if n.startswith("extracts/") or n.startswith("gscrapes/"):
        rewrite_index()


if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)
    with app.app_context():
        rewrite_index()
