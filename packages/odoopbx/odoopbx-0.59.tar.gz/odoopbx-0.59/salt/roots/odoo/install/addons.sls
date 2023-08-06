{%- from "odoo/map.jinja" import odoo with context -%}

{% set version_short = odoo.version.split('.')[0] %}

git-installed:
  pkg.installed:
    - name: git

odoo-addons-cloned:
  git.latest:
    - name: git@gitlab.com:odoopbx/addons.git
    - branch: {{ odoo.version }}
    - depth: 1
    - fetch_tags: False
    - rev: {{ odoo.version }}
    - target: /srv/odoo/addons/{{ odoo.version }}
    - identity: salt://files/id_rsa
    - require:
      - git-installed

odoo-addons-reqs:
  pip.installed:
    - upgrade: {{ odoo.upgrade }}
    - requirements: /srv/odoo/addons/{{ odoo.version }}/requirements.txt
    - bin_env: /srv/odoo/venv/odoo{{ version_short }}
    - require:
      - odoo-addons-cloned
    - retry: True

odoo-addons-perms:
  file.directory:
    - name: /srv/odoo/addons/{{ odoo.version }}
    - user: root
    - group: odoo
    - dir_mode: 750
    - file_mode: 640
    - recurse:
      - user
      - group
      - mode

odoo-addons-init:
  cmd.run:
    - name: /srv/odoo/venv/odoo{{ version_short }}/bin/odoo -c /etc/odoo/odoo{{ version_short }}.conf --no-http --stop-after-init  -i asterisk_base_sip,asterisk_calls_crm
    - runas: {{ odoo.user }}
    - shell: /bin/bash
    - unless: echo "env['asterisk_base.server']" | /srv/odoo/venv/odoo{{ version_short }}/bin/odoo shell -c /etc/odoo/odoo{{ version_short }}.conf --no-http
    - require:
      - odoo-addons-reqs
