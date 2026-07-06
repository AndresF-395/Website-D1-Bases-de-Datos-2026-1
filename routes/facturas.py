from flask import Blueprint, render_template

bp = Blueprint('facturas', __name__, url_prefix='/facturas')

@bp.route('/')
def index():
    return "<h1>Módulo de Facturas (En construcción)</h1>"