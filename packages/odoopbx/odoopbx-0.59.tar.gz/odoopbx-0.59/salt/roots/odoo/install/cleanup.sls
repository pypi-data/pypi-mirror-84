{%- from "odoo/map.jinja" import odoo with context -%}

odoo-zip-removed:
  file.absent:
    - name: /srv/odoo/src/odoo-{{ odoo.version }}.zip

odoo-dir-removed:
  file.absent:
    - name: /srv/odoo/src/odoo-{{ odoo.version }}
