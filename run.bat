@echo off
call .venv\scripts\activate

uvicorn main:app --reload