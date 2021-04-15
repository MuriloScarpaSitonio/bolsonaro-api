.PHONY: db-populate setup-dev create-venv django-pipeline django react all

DJANGO_DIR := django
REACT_DIR := react

db-populate: 
	$(MAKE) -C $(DJANGO_DIR) db-populate

create-venv: 
	$(MAKE) -C $(DJANGO_DIR) create-venv

django-test:
	$(MAKE) -C $(DJANGO_DIR) test


django-code-convention:
	$(MAKE) -C $(DJANGO_DIR) code-convention


django-security-checker:
	$(MAKE) -C $(DJANGO_DIR) security-checker


django-typing-checker:
	$(MAKE) -C $(DJANGO_DIR) typing-checker


django-pipeline: django-test django-code-convention django-security-checker django-typing-checker


django-run:
	$(MAKE) -C $(DJANGO_DIR) run


django-collectstatic:
	$(MAKE) -C $(DJANGO_DIR) collectstatic


django-setup-dev:
	$(MAKE) -C $(DJANGO_DIR) setup-dev


react-install:
	$(MAKE) -C $(REACT_DIR) install


react-build:
	$(MAKE) -C $(REACT_DIR) build


react-run:
	$(MAKE) -C $(REACT_DIR) run


django:
	$(MAKE) -C $(DJANGO_DIR) all

react:
	$(MAKE) -C $(REACT_DIR) all
