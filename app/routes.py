from flask import render_template, request, redirect, url_for
from app import app
from app.models import Todo
from app import db


@app.route('/')
def index():
	incomplete = Todo.query.filter_by(complete=0).all()
	complete = Todo.query.filter_by(complete=1).all()

	return render_template('index.html', incomplete=incomplete, complete=complete)


@app.route('/add', methods=['POST'])
def add():
	todo = Todo(id=request.form['todoid'], text=request.form['todoitem'], complete=0)
	db.session.add(todo)
	db.session.commit()

	return redirect(url_for('index'))


@app.route('/reset')
def reset():
	todo = db.session.query(Todo).delete()
	db.session.commit()

	return redirect(url_for('index'))


@app.route('/complete/<id>')
def complete(id):

	todo = Todo.query.filter_by(id=int(id)).first()
	todo.complete = 1
	db.session.commit()

	return redirect(url_for('index'))
