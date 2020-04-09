from app import create_production_app, db
from app.models.api_access import Access

app = create_production_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'access': Access}


if __name__ == '__main__':
    app.run()
