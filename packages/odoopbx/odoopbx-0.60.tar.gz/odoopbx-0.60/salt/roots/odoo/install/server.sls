{%- from "odoo/map.jinja" import odoo with context -%}

{% set version_short = odoo.version.split('.')[0] %}

virtualenv-init:
  virtualenv.managed:
    - name: /srv/odoo/venv/odoo{{ version_short }}
    - python: python3

pip-upgraded:
  cmd.run:
    - name: /srv/odoo/venv/odoo{{ version_short }}/bin/pip3 install --upgrade pip
    - reload_modules: true
    - require:
      - virtualenv-init

odoo-group:
  group.present:
    - name: odoo

odoo-user:
  user.present:
    - name: odoo
    - groups: [odoo]

odoo-src-dir:
  file.directory:
    - name: /srv/odoo/src/
    - makedirs: True

odoo-filestore-dir:
  file.directory:
    - name: /srv/odoo/data/filestore
    - makedirs: True
    - user: odoo
    - group: root
    - dir_mode: 750

odoo-data-addons-dir:
  file.directory:
    - name: /srv/odoo/data/addons/{{ odoo.version }}
    - makedirs: True
    - user: root
    - group: odoo
    - dir_mode: 750

odoo-addons-dir:
  file.directory:
    - name: /srv/odoo/addons/{{ odoo.version }}
    - makedirs: True
    - user: root
    - group: odoo
    - dir_mode: 750

odoo-etc-dir:
  file.directory:
    - name: /etc/odoo
    - group: odoo
    - dir_mode: 750

odoo-downloaded:
  file.managed:
    - name: /srv/odoo/src/odoo-{{ odoo.version }}.zip
    - source: https://github.com/odoo/odoo/archive/{{ odoo.version }}.zip
    - skip_verify: True    

odoo-extracted:
  archive.extracted:
    - source: /srv/odoo/src/odoo-{{ odoo.version }}.zip
    - name: /srv/odoo/src/

odoo-addons-copied:
  cmd.run:
    - name: cp -r /srv/odoo/src/odoo-{{ odoo.version }}/addons/* /srv/odoo/data/addons/{{ odoo.version }}
    - require:
      - odoo-extracted

odoo-installed:
  pip.installed:
    - name: /srv/odoo/src/odoo-{{ odoo.version }}
    - bin_env: /srv/odoo/venv/odoo{{ version_short }}
    - require:
        - virtualenv-init
        - odoo-extracted
    - unless:
        - /srv/odoo/venv/odoo{{ version_short }}/bin/pip3 freeze | grep odoo

werkzeug-fixed:
  pip.installed:
    - name: werkzeug == 0.16.1
    - bin_env: /srv/odoo/venv/odoo{{ version_short }}
    - require:
      - virtualenv-init

odoo-configs:
  file.managed:
    - names:
      - /etc/odoo/odoo{{ version_short }}.conf:
        - source: salt://odoo/templates/odoo.conf
        - group: {{ odoo.user }}
        - mode: 640
      - /etc/systemd/system/odoo{{ version_short }}.service:
        - source: salt://odoo/templates/odoo.service
    - user: root
    - mode: 644
    - template: jinja
    - context: {{ odoo }}
    - backup: minion

{% if grains.virtual == 'container' %}
odoo-postgresql:
  cmd.run:
    - name: pg_ctlcluster {{ odoo.pg_ver }} main start
    - runas: postgres
    - unless:
      - pidof postgres
    - require:
      - odoo-installed
    - require_in:
      - postgres_user: odoo-dbuser
{% else %}
odoo-service-stop:
  service.dead:
    - name: odoo{{ version_short }}
    - require:
      - file: odoo-configs
{% endif %}

odoo-dbuser:
  postgres_user.present:
    - name: {{ odoo.user }}
    - createdb: True
    - encrypted: True
    - db_user: postgres
    - require:
      - odoo-installed

odoo-init:
  cmd.run:
    - name: /srv/odoo/venv/odoo{{ version_short }}/bin/odoo -d {{ odoo.dbname }} -c /etc/odoo/odoo{{ version_short }}.conf --no-http --stop-after-init  -i base
    - runas: {{ odoo.user }}
    - shell: /bin/bash
    - unless: echo "env['res.users']" | /srv/odoo/venv/odoo{{ version_short }}/bin/odoo shell -c /etc/odoo/odoo{{ version_short }}.conf --no-http
    - require:
      - odoo-dbuser
