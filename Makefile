BASE_INST_DIR=/var/lib/openquake/oq-ui-geoserver/

BASE_SRC_DIR=

deploy: install postinst

install:
	test -d $(BASE_INST_DIR) || mkdir -p $(BASE_INST_DIR)
	cp -a geoserver "$(BASE_INST_DIR)"
	chown -R tomcat6.tomcat6 $(BASE_INST_DIR)geoserver

postinst:
	./bin/geoserver-xml-mangler.py install $$(find "$(BASE_INST_DIR)geoserver/data/workspaces/" -type f -name datastore.xml | grep -v "$(BASE_INST_DIR)geoserver/data/workspaces/temp")

template:
	./bin/geoserver-xml-mangler.py template $$(find "$(BASE_SRC_DIR)geoserver/data/workspaces/" -type f -name datastore.xml | grep -v "$(BASE_SRC_DIR)geoserver/data/workspaces/temp")

.PHONY: deploy install postinst template

