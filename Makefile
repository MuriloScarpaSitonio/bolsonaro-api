.PHONY: db-populate setup-dev create-venv django-pipeline django react all

DJANGO_DIR := django
REACT_DIR := react
AWS_LAMDA_DIR := aws_lambda

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


aws-lambda-setup-dev:
	$(MAKE) -C $(AWS_LAMDA_DIR) setup-dev


aws-lambda-test:
	$(MAKE) -C $(AWS_LAMDA_DIR) test


aws-lambda-code-convention:
	$(MAKE) -C $(AWS_LAMDA_DIR) code-convention


aws-lambda-security-checker:
	$(MAKE) -C $(AWS_LAMDA_DIR) security-checker


aws-lambda-typing-checker:
	$(MAKE) -C $(AWS_LAMDA_DIR) typing-checker


aws-lambda-pipeline: aws-lambda-test aws-lambda-code-convention aws-lambda-security-checker aws-lambda-typing-checker
