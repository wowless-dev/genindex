from flask import render_template
from google.cloud import storage

products = [
    "wow",
    "wowt",
    "wow_classic",
    "wow_classic_era",
    "wow_classic_era_ptr",
    "wow_classic_ptr",
]

client = storage.Client()


def rendered_index():
    def fun(p):
        v = (
            client.bucket("wowless.dev")
            .blob(f"extracts/{p}.txt")
            .download_as_text()
            .strip()
        )
        has_gscrape = (
            client.bucket("wowless.dev").blob(f"gscrapes/{v}.lua").exists()
        )
        return {
            "name": p,
            "version": v,
            "has_gscrape": has_gscrape,
        }

    return render_template("index.html", products=map(fun, products))


def genindex(event, _context):
    n = event["name"]
    if n.startswith("extracts/") or n.startswith("gscrapes/"):
        client.bucket("www.wowless.dev").blob("index.html").upload_from_string(
            rendered_index(), content_type="text/html"
        )


if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)
    with app.app_context():
        print(rendered_index())
