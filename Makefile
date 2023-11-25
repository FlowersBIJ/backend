all: remove build run

rerun: stop remove build run

run-d: remove build run-detached

build:
	@docker compose build

run:
	@docker compose up --remove-orphans

run-detached:
	@docker compose up -d --remove-orphans

remove:
	@docker compose down
	@docker compose rm

stop:
	@docker compose down

# E203 - whitespace before ':' - конфликтует с black
# E501 - line too long - конфликтует с black (не игнорирует комменты)
# W503 - line break before binary operator - конфликтует с black
# F401 - imported but unused - неактуально для __init__ и main.py файлов
# PIE803 - prefer-logging-interpolation - lazy % форматирования в логах (смысла нет)
# PIE786 - Use precise exception handlers - коде однозначную ошибку сложно поределить
# DUO104, DUO110 - не использовать eval и compile
flake:
	poetry run flake8 \
		--per-file-ignores="__init__.py:F401" \
		--ignore E203,E501,W503,PIE803,PIE786,DUO104,DUO110 \
		src main.py tests

format:
	@echo "Форматирование"
	poetry run isort .
	poetry run black .

