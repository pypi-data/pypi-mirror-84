from docutils import nodes
from docutils.parsers.rst import Directive

from sphinx.util.docutils import SphinxDirective

class HelloWorld(SphinxDirective):
    def run(self):
        image_node = nodes.paragraph(text='Hello, Veldus!')
        return [image_node]


def setup(app):
    app.add_directive("helloworld", HelloWorld)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }