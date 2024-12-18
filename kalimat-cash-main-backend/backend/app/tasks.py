from __future__ import absolute_import, unicode_literals

from project.celery import app

@app.task(bind=True)
def sample(self,param1, param2):
    print (f'received {param1} and {param2} - request: {self.request}')
    return f'received {param1} and {param2} - request: {self.request}'


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))