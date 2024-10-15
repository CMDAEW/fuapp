from app import db

def init_db():
    db.create_all()

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        init_db()
