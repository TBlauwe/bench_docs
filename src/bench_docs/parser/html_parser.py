import os
from enum import Enum

from bs4 import BeautifulSoup

from bench_docs.utility.asserts import assert_file_exists, assert_directory_exists
from bench_docs.utility.bokeh import download_bokeh_scripts


class EmbedClass(Enum):
    Default = "bench_docs"


class HtmlParser:

    def __init__(self, html_file: str, bokeh_version, output_location):
        assert_file_exists(html_file)
        assert_directory_exists(output_location)

        self.html_file = html_file
        with open(html_file, 'r') as f:
            self.html = f.read()
            self.soup = BeautifulSoup(self.html, 'html.parser')

        self.output_location = output_location
        self.insert_bokeh_scripts(bokeh_version)

    def insert_bokeh_scripts(self, version: str):
        filenames = download_bokeh_scripts(version, self.output_location)

        head = self.soup.head

        for filename in filenames:
            script = self.soup.new_tag('script', src=filename)
            head.append(script)

        script = self.soup.new_tag('script')
        script.string = " Bokeh.set_log_level('info')"
        head.append(script)

    def embed_bokeh_components(self, div_id, script, div):
        embed_div = self.soup.find('div', {'class': EmbedClass.Default.value, 'id': div_id})
        script_tag = BeautifulSoup(script, 'html.parser')
        div_tag = BeautifulSoup(div, 'html.parser')
        embed_div.append(script_tag)
        embed_div.append(div_tag)

    def save(self):
        with open(os.path.join(self.output_location, self.html_file), 'w') as f:
            f.write(str(self.soup.prettify()))
