import urllib.request


def download_bokeh_scripts(version, location):
    urls = [
        f"https://cdn.bokeh.org/bokeh/release/bokeh-{version}.min.js",
        f"https://cdn.bokeh.org/bokeh/release/bokeh-widgets-{version}.min.js",
        f"https://cdn.bokeh.org/bokeh/release/bokeh-tables-{version}.min.js"
    ]

    filenames = []

    for url in urls:
        filename = url.split("/")[-1]
        filenames.append(filename)
        filepath = f"{location}/{filename}"
        urllib.request.urlretrieve(url, filepath)

    return filenames
