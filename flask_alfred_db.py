from flask import current_app, _app_ctx_stack

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


Session = sessionmaker(autocommit=False, autoflush=False)


class AlfredDB(object):

    def __init__(self, app=None, session_factory=None):
        if session_factory is None:
            session_factory = Session
        self.session_class = scoped_session(
            session_factory=session_factory,
            scopefunc=_app_ctx_stack.__ident_func__,
        )
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.extensions['alfred-db'] = {
            'engine': self.create_engine(app),
        }

        @app.teardown_appcontext
        def shutdown_session(response):
            self.session_class.remove()
            return response

    def create_engine(self, app):
        database_uri = app.config.get('DATABASE_URI')
        return create_engine(database_uri)

    @property
    def engine(self):
        return current_app.extensions['alfred-db']['engine']

    @property
    def session(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'db_session'):
                ctx.db_session = self.session_class(bind=self.engine)
            return ctx.db_session
