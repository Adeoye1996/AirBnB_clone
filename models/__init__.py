#!/usr/bin/python3
"""Initialize the FileStorage engine for models"""
from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
