from flask import Blueprint, render_template

bp = Blueprint('proveedores', __name__, url_prefix='/proveedores')

@bp.route('/')
def index():
    return "<h1>Módulo de Proveedores (En construcción)</h1>"