from app import create_app
from app.core.method_registry import registry

app = create_app()
with app.app_context():
    registry.discover('app.methods')
    methods = registry.list_all()
    print(f'Total metodos: {len(methods)}')
    for m in methods:
        print(f'  [{m["method_type"]:15}] {m["name"]}')
