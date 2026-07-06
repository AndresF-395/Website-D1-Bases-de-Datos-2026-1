from flask import Blueprint, render_template

bp = Blueprint('clientes', __name__, url_prefix='/clientes')

@bp.route('/')
def index():
    return "<h1>Módulo de Clientes (En construcción)</h1>"