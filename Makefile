format:
	@echo "Starting autoflake format"
	autoflake --recursive api apps configuracion
	@echo "Starting isort format..."
	isort api apps configuracion --skip __init__.py
	@echo "Starting black format..."
	black api apps configuracion
	@echo "Starting pylint "
	pylint api apps configuracion

test:
	@echo "Starting tests..."
	python manage.py test

