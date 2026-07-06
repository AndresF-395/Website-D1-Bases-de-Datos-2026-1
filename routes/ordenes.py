# CORRECTO
from flask import Blueprint, render_template

bp = Blueprint('ordenes', __name__, url_prefix='/ordenes')

@bp.route('/')
def index():
    return "<h1>Módulo de Órdenes de Compra (En construcción)</h1>"