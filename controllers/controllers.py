from flask import request, session, render_template, flash, redirect, url_for
from main import app
from applications.models import *
from datetime import datetime
import plotly.express as px
import plotly.utils
import json
from collections import Counter, defaultdict


@app.route('/update_user', methods=['POST'])
def update_user():
    user_id = request.form.get('user_id')
    user = User.query.get(user_id)
    user.name = request.form.get('name')
    user.email = request.form.get('email')
    user.dob = request.form.get('dob')
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form.get('user_id')
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))