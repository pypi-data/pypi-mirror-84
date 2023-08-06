# required by Sphinx
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective
from sphinx.errors import ExtensionError

# required for file system path building
import os
import pathlib

# required to generalte HTML from jinja templates
from jinja2 import Template

################################################################################
#                             Globals                                          #
#                                                                              #
#  This section includes global functions used by both directives              #
#                                                                              #
#  1. def generate_HTML_from_jinja()                                           #
#     This function will generate HTML from the provided template and config   #
#                                                                              #
#  2. def html_statblock()                                                     #
#     This function is invoked once per directive found during the             #
#     Sphinx core event 'html-page-context'. It replaces the doctree node      #
#     with the proper HTML generated from a jinja.                             #
#                                                                              #
#  3. def validTableType() and validKingdom                                    #
#     These functions validate the value provided for a particular :option:.   #
#                                                                              #
################################################################################

# abs_template_path: a path to an absolute path to a jinja template file
# config: the jinja config dict expected by the template
def generate_HTML_from_jinja(abs_template_path, config):
  # Open jinja template and get file content as String
  jinja2_template_string = open(abs_template_path, 'r').read()

  # Create template object
  template = Template(jinja2_template_string)

  # Render HTML template String
  html_template_string = template.render(config = config)

  # Return HTML to HTML parser
  return html_template_string

# this function is invoked once per place_statblock directive found during the
# Sphinx core event 'html-page-context'
# https://www.sphinx-doc.org/en/1.5/extdev/appapi.html#event-html-page-context 
def html_statblock(self, node):
  # find options for current node
  store_key = node['store_key']
  statblocks = self.document.settings.env.veldus[store_key]
  for statblock in statblocks:
    if statblock['docname'] in node.source:
      options = statblock['options']

  # build jinja template config dict from Sphinx options
  # remove option :table_type: which is for internal use
  stats = {key:val for key, val in options.items() if key != 'table_type'}
  config = {
    'stats': stats 
  }

  # build absolute path to jinja template
  # abs_template_path = os.path.join(os.getcwd(), 'source/_ext/veldus_ext/templates/statblock.html')
  current_dir = pathlib.Path(__file__).parent.absolute()
  abs_template_path = os.path.join(current_dir, 'templates/statblock.html')

  # generate HTML from jinja template
  html = generate_HTML_from_jinja(abs_template_path, config)

  # append HTML
  self.body.append(html)

  raise nodes.SkipNode

# validates values given for option :table_type:
def validTableType(arg):
  validTableTypes = ['place', 'npc']

  return directives.choice(arg, validTableTypes)






















################################################################################
#                           Place StatBlock                                    #
#                                                                              #
#  This section will include all functions and classes required to implement   #
#  the .. place_statblock:: directive. This includes:                          #
#                                                                              #
#  1. class Place_Statblock                                                    #
#     This class requires a run() function that is executed when this          #
#     directive is found in an .rst file. Must return a doctree node.          #
#                                                                              #
#  2. class place_statblock                                                    #
#     This class is used to inherit from existing docutils.nodes and provides  #
#     the directive with a doctree node.                                       #
#                                                                              #
#  3. def handle-env-update()                                                  #
#     Sort the rows into the desired order during this phase.                  #
#                                                                              #
################################################################################

# validates values given for option :kingdom:
def validKingdom(arg):
  validKingdomList = ['belrd', 'dynnt', 'unknown']

  return directives.choice(arg, validKingdomList).capitalize()

class Place_Statblock(Directive):
  has_content = True

  # TODO: write validators for all required, at least
  # dict required by docutils/Sphinx for Directives
  # name is *not* optional
  # these are only split for readability, can be added to option_spec directly if desired
  option_spec = {}

  # a dict of required args
  required_args = {
    'table_type': validTableType,
    'place': directives.unchanged_required,
    'kingdom': validKingdom,
    'province': directives.unchanged_required,
    'type': directives.unchanged_required,
  }

  # can be empty
  optional_args = {
    'population': directives.unchanged,
    'leader': directives.unchanged,
    'store_key': directives.unchanged,
  }

  # add to docutils/Sphinx option dict
  option_spec.update(required_args)
  option_spec.update(optional_args)

  # only validates if the option is present
  # add a function similar to validTableType() to validate the value of the option
  # TODO: the validators provided in the option_spec might be able to handle this, not sure
  def has_required_options(self, docname):

    # list of :options: that are required
    # a ValueError will be raised at build if a required arg is missing
    required_arguments = ['table_type']

    for arg in required_arguments:
      if not self.options.get(arg):
        error_message = 'Missing option :{0}: for Statblock in {1}.rst on lineno: {2}'.format(arg, docname, self.lineno)
        raise ValueError(error_message)

  # run() is required by Sphinx
  def run(self):
    env = self.state.document.settings.env

    # ensure required options are present
    self.has_required_options(docname=env.docname)

    # create doctree node
    table_node = place_statblock()
    store_key = self.options.get('store_key')
    if store_key:
      table_node['store_key'] = store_key
    else:
      docname = self.state.document.settings.env.docname
      error_message = 'Missing option :{0}: for Statblock in {1}.rst on lineno: {2}'.format(store_key, docname, self.lineno)
      raise ExtensionError(message=error_message)

    storage = env.veldus.get(store_key)
    if not storage:
      env.veldus[store_key] = []

    env.veldus[store_key].append({
      'docname': env.docname,
      'options': self.options
    })

    return [table_node]

# this needs to be all-lower, else place_statblockList throws warning that Sphinx can't find the directive
class place_statblock(nodes.Body, nodes.Element):
  pass

# after env is finished updating, put places is desired order for summary table
def handle_env_updated(app, env):
  STORE_KEY = 'veldus_all_npcstats'
  if hasattr(env, STORE_KEY):
    # sort alpha ascend by kingdom then name of place
    stats_sorted = sorted(env.veldus[STORE_KEY], key = lambda i: (i['options']['race'], i['options']['npc']))
    env.veldus[STORE_KEY] = stats_sorted

  all_placeinfos = env.veldus.get('all_placeinfos')
  if all_placeinfos:
    # sort alpha ascend by kingdom then name of place
    a = 'kingdom'
    b = 'province'
    kingdom_sorted = sorted(all_placeinfos, key = lambda i: (i['options'][a], i['options'][b]))
    env.veldus['all_placeinfos'] = kingdom_sorted










# this shit has to be all-lower, else npc_statblockList throws warning that Sphinx can't find the directive
class npc_statblock(nodes.Body, nodes.Element):
  pass

class NPC_Statblock(Directive):

  has_content = True

  # TODO: can this be improved?
  option_spec = {
    'npc': directives.unchanged_required,
    'race': directives.unchanged_required,
    'height': directives.unchanged_required,
    'weight': directives.unchanged_required,
    'eyes': directives.unchanged_required,
    'skin': directives.unchanged_required,
    'hair': directives.unchanged_required,
    'occupation': directives.unchanged_required,
    'motivations': directives.unchanged_required,
    'store_key': directives.unchanged
  }
  
  def run(self):
    env = self.state.document.settings.env

    # create doctree node
    table_node = npc_statblock()

    store_key = self.options.get('store_key')
    if store_key:
      table_node['store_key'] = store_key
    else:
      docname = self.state.document.settings.env.docname
      error_message = 'Missing option :{0}: for Statblock in {1}.rst on lineno: {2}'.format(store_key, docname, self.lineno)
      raise ExtensionError(message=error_message)

    if not hasattr(env, store_key):
      env.veldus_all_npcstats = []
    
    # save info to global variable
    env.veldus_all_npcstats.append({
      'docname': env.docname,
      'options': self.options
    })

    storage = env.veldus.get(store_key)
    if not storage:
    # if not hasattr(env.veldus, STORE_KEY):
      env.veldus[store_key] = []

    env.veldus[store_key].append({
      'docname': env.docname,
      'options': self.options
    })

    return [table_node]


# def html_npc_statblock(self, node):
#   # find options for current node
#   for npc in self.document.settings.env.veldus_all_npcstats:
#     if npc['docname'] in node.source:
#       options = npc['options']

#   # create a statblock_table object
#   statblock_table = Statblock_Table(options)

#   # build html from provided options and append
#   self.body.append(statblock_table.build())

#   raise nodes.SkipNode

# after env is finished updating, put places is desired order for summary table
# def handle_env_updated(app, env):
#   if hasattr(env, 'veldus_all_npcstats'):
#     # sort alpha ascend by kingdom then name of place
#     stats_sorted = sorted(env.veldus[STORE_KEY], key = lambda i: (i['options']['race'], i['options']['npc']))
#     env.veldus[STORE_KEY] = stats_sorted





























################################################################################
#                               Sphinx API                                     #
################################################################################

# this function is required to setup the directive when it is
# encountered in the project's conf.py
def setup(app):
  # Add Place Statblock directive
  # We provide our function to generate the HTML that will replace the node during build
  app.add_node(place_statblock,
               html=(html_statblock, None))
  app.add_directive('place_statblock', Place_Statblock)

  # Add NPC Statblock directive
  app.add_node(npc_statblock,
               html=(html_statblock, None))
              #  html=(html_npc_statblock, None))
  app.add_directive('npc_statblock', NPC_Statblock)

  # Add Place Statblock Summary Table directive
  # We provide our function to generate the HTML that will replace the node during build
  app.add_node(summarytable,
               html=(html_summarytable, None))
  app.add_directive('summarytable', SummaryTable)

  # Connect event handlers
  app.connect('env-updated', handle_env_updated)

  app.connect('env-before-read-docs', handle_env_before_read_docs)

  # TODO: figure out exactly what we are, and could be, returing here
  return {
      'version': '0.1',
      'parallel_read_safe': True,
      'parallel_write_safe': True,
  }

def handle_env_before_read_docs(app, env, docnames):
    # make sure global storage has init
    if not hasattr(env, 'veldus'):
      print('MISSING GLOBAL VAR "veldus" but in HANDLER')
      env.veldus = {}
























################################################################################
#                           Place SummaryTable                                 #
#                                                                              #
#  This section will include all functions and classes required to implement   #
#  the .. summarytable:: directive. This includes:                             #
#                                                                              #
#  1. class SummaryTable                                                       #
#     This class requires a run() function that is executed when this          #
#     directive is found in an .rst file. Consumed in Sphinx.setup().          #
#                                                                              #
#  2. class summarytable                                                       #
#     This class is used to inherit from existing docutils.nodes and replaces  #
#     the directive with a doctree node. Consumed in Sphinx.setup().           #
#                                                                              #
#  3. def html_summarytable()                                                  #
#     This function is invoked once per directive found during the             #
#     Sphinx core event 'html-page-context'. It replaces the doctree node      #
#     with the proper HTML generated from a jinja. Consumed in Sphinx.setup(). #
#                                                                              #
################################################################################

class SummaryTable(Directive):
    option_spec = {
        'table_type': validTableType,
        'headers': directives.unchanged_required,
        'store_key': directives.unchanged_required
    }

    def run(self):
        table_node = summarytable()

        table_type = self.options.get('table_type')
        if table_type:
          table_node['table_type'] = table_type
        else:
          docname = self.state.document.settings.env.docname
          error_message = 'Missing option :table_type: for SummaryTable in {0}.rst on lineno: {1}'.format(docname, self.lineno)
          raise ExtensionError(message=error_message)

        headers = self.options.get('headers')
        if headers:
          table_node['headers'] = headers 
        else:
          docname = self.state.document.settings.env.docname
          error_message = 'Missing option :headers: for SummaryTable in {0}.rst on lineno: {1}'.format(docname, self.lineno)
          raise ExtensionError(message=error_message)

        store_key = self.options.get('store_key')
        if store_key:
          table_node['store_key'] = store_key
        else:
          docname = self.state.document.settings.env.docname
          error_message = 'Missing option :store_key: for SummaryTable in {0}.rst on lineno: {1}'.format(docname, self.lineno)
          raise ExtensionError(message=error_message)

        return [table_node]

class summarytable(nodes.Body, nodes.Element):
  pass

def html_summarytable(self, node):
    # TODO: Verify 'table_type' is present
    # get table_type from options
    table_type = node['table_type']

    # get headers from options
    headers = node['headers']
    headers = ' '.join((table_type, headers)) # prepend table_type to headers -> str
    headers = headers.split() # transform to list

    # get store_key
    storeKey = node['store_key']

    # controls the header row of the table 
    summary_rows = []
    urls = []

    # get all statblocks to use via provided store_key
    statblocks = self.document.settings.env.veldus[storeKey]

    # for each statblock in statblocks...
    for statblock in statblocks:
      # build a url for a backlink
      urls.append(statblock['docname'] + '.html')
      
      row = []
      # for each header of table...
      for header in headers:
        # collect info of current place_statblock
        row.append(statblock['options'].get(header))
      
      summary_rows.append(row)

    # build absolute path to jinja template
    # abs_template_path = os.path.join(os.getcwd(), 'source/_ext/veldus_ext/templates/summary-table.html')
    current_dir = pathlib.Path(__file__).parent.absolute()
    abs_template_path = os.path.join(current_dir, 'templates/summary-table.html')

    # build jinja template config dict from Sphinx options
    config = {
      'headers': headers,
      'summary_rows': summary_rows,
      'urls': urls,
      'table_type': table_type
    }

    # generate HTML from jinja template
    html = generate_HTML_from_jinja(abs_template_path, config)

    # append HTML
    self.body.append(html)

    raise nodes.SkipNode
