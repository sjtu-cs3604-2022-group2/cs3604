import click,os
from flask import Flask, render_template, request,g
# from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRFError

# from bluelog.blueprints.blog import blog_bp

from models import Post, Category, Comment
from extensions import bootstrap, db, csrf, ckeditor, mail, moment, toolbar, migrate
# from bluelog.settings import config
from blueprints.user import bp as userbp
from blueprints.posts import bp as postsbp
from setting import config
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///'+ os.path.join(app.root_path, 'data.db'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_shell_context(app)
    register_template_context(app)
    # register_request_handlers(app)
    return app

def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    # login_manager.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db)

def register_blueprints(app):
    app.register_blueprint(userbp,url_prefix='/user')
    # app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(postsbp)


def register_shell_context(app):
    '''
    @app.shell_context_processor 装饰器创建并注册一个shell上下文处理器，shell上下文处理器返回一个字典，包含数据库实例和模型。除了默认导入的app外，Flask也将这些对象导入： 
    '''
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Post=Post, Category=Category, Comment=Comment)


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    # @app.cli.command()
    # @click.option('--username', prompt=True, help='The username used to login.')
    # @click.option('--password', prompt=True, hide_input=True,
    #               confirmation_prompt=True, help='The password used to login.')
    # def init(username, password):
    #     """Building Bluelog, just for you."""

    #     click.echo('Initializing the database...')
    #     db.create_all()

    #     admin = Admin.query.first()
    #     if admin is not None:
    #         click.echo('The administrator already exists, updating...')
    #         admin.username = username
    #         admin.set_password(password)
    #     else:
    #         click.echo('Creating the temporary administrator account...')
    #         admin = Admin(
    #             username=username,
    #             blog_title='Bluelog',
    #             blog_sub_title="No, I'm the real thing.",
    #             name='Admin',
    #             about='Anything about you.'
    #         )
    #         admin.set_password(password)
    #         db.session.add(admin)

    #     category = Category.query.first()
    #     if category is None:
    #         click.echo('Creating the default category...')
    #         category = Category(name='Default')
    #         db.session.add(category)

    #     db.session.commit()
    #     click.echo('Done.')

    @app.cli.command()
    @click.option('--users', default=5, help='Quantity of users, default is 5.')
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500.')
    def forge(users,category, post, comment):
        """Generate fake data."""
        from fakes import fake_user, fake_categories, fake_posts, fake_comments

        db.drop_all()
        db.create_all()

        click.echo('Generating the users...')
        fake_user(users)

        click.echo('Generating %d categories...' % category)
        fake_categories(category)

        click.echo('Generating %d posts...' % post)
        fake_posts(post)

        click.echo('Generating %d comments...' % comment)
        fake_comments(comment)

        # click.echo('Generating links...')
        # fake_links()

        click.echo('Done.')
    

def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400


def register_template_context(app):
    @app.context_processor  ###上下文处理器，渲染的所有模板都会执行这个代码
    def context_processor():
        if hasattr(g, 'user'):
            return {'user': g.user}
        else:
            return {}

if __name__ == '__main__':
    app=create_app('development')
    app.run()