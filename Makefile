.PHONY: all rebuild

all: app/translations/*/LC_MESSAGES/messages.mo

rebuild:
	$(MAKE) --always-make

app/translations/%/LC_MESSAGES/messages.mo: app/translations/%/LC_MESSAGES/messages.po
	pybabel compile -i $< -o $@ -l $(shell grep Language: $< | cut -c 12-13)

app/translations/%/LC_MESSAGES/messages.po: messages.pot
	pybabel update -i messages.pot -o $@ -w 160 -l $(shell grep Language: $@ | cut -c 12-13)

messages.pot: app/*.py
	pybabel extract -F babel.cfg --no-location -w 160 -o messages.pot .

new-locale:
	@echo "run pybabel init -i messages.pot -d app/translations -l CODE"
