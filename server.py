#! /usr/bin/env python
import os
import cherrypy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

import json
from models import Device
from contextlib import contextmanager
from cherrypy.lib.static import serve_file
from time import time

PATH = os.path.abspath(os.path.dirname(__file__))

db = create_engine("sqlite:///ipMacCrud.db")


@contextmanager
def sessionScope():
    Session = sessionmaker(bind=db)
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        print e
        session.rollback()
    finally:
        session.close()


class Devices(object):
    
    exposed = True

    @staticmethod
    def updateObject(s, device, data):
       
        try: 
            for field, value in data.iteritems():
                setattr(device, field, value)  

            s.add(device)
        except Exception as e:
            print e

    def GET(self):
        data = {'devices': []}

        with sessionScope() as s:
            data['devices'] = [d.toDict() for d in s.query(Device).order_by(Device.name).all()]
            
        return json.dumps(data, indent=4)


    def PUT(self, mac):

        try:
            data = json.loads(cherrypy.request.body.read())
        except ValueError:
            return json.dumps({"error": "Bad json"}, indent=4)

        with sessionScope() as s:
            try:
                device = s.query(Device).filter_by(mac=mac).one()
            except NoResultFound:
                device = Device()

            data['mac'] = mac
            data['ip'] = cherrypy.request.headers['Remote-Addr']
	    if "X-Forwarded-For" in cherrypy.request.headers:
		    data['ip'] = cherrypy.request.headers['X-Forwarded-For']
	
	    data['last_updated'] = time()
            return json.dumps(Devices.updateObject(s, device, data), indent=4)


class Root(object):

	devices = Devices()

root = Root()


conf = {
    'global': {
        'server.socket_port': 8080,
    },
    '/': {
	'tools.proxy.on': True,
    	'tools.staticdir.on': True,
        'tools.staticdir.dir': PATH,
        'tools.staticdir.index': 'index.html',
    },
    '/devices': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
    }
}

cherrypy.quickstart(root, '/', conf)
