from xenon_runsDB_api.app import app, db, guard
from xenon_runsDB_api.common.user import User

# Add users
with app.app_context():
    db.create_all()
    db.session.add(User(
        username='admin',
        password=guard.encrypt_password('test_admin'),
        roles='admin,production,user'
    ))    
    db.session.add(User(
        username='xenon-admin',
        password=guard.encrypt_password('LZSTINXS'),
        roles='admin,production,user'
    ))
    db.session.add(User(
        username='xenon-prod',
        password=guard.encrypt_password('LZSTINXS_prod'),
        roles='production,user'
    ))
    db.session.add(User(
        username='xenon-user',
        password=guard.encrypt_password('LZSTINXS_user'),
        roles='user'
    ))
    db.session.commit()