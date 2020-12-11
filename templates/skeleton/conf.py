project = 'FIXME: Use project name params'
copyright = '2020, FIXME: Use author name params'
author = 'FIXME: Use author name params'
release = 'FIXME: get release info from git environment'
extensions = [
    'sphinxcontrib.needs',
]
templates_path = ['_templates']
exclude_patterns = [
    '_build', 'Thumbs.db',
    '.DS_Store', '.venv'
]
html_theme = 'alabaster'
html_static_path = ['_static']
#
# Needs config
needs_types = [
    dict(directive="objective", title="Objective", prefix="OBJ_", color="#BFD8D2", style="node"),
    dict(directive="goal", title="Goal", prefix="GL_", color="#FEDCD2", style="node"),
    dict(directive="epic", title="Epic", prefix="EPIC_", color="#DF744A", style="node"),
    dict(directive="ticket", title="Ticket", prefix="TCKT_", color="#DCB239", style="node"),
]
