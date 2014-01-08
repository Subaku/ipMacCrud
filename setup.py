#! /usr/bin/env python

from sqlalchemy import create_engine
import models

db = create_engine('sqlite:///ipMacCrud.db')
models.Base.metadata.create_all(db)