from flask import render_template, request, redirect, url_for
from app import app
from app.models import Todo
from app import db


exist = 0

@app.route('/')
def index():
	global exist
	incomplete = Todo.query.filter_by(complete=0).all()
	complete = Todo.query.filter_by(complete=1).all()

	return render_template('home.html', incomplete=incomplete, complete=complete, exist=exist)


@app.route('/add', methods=['POST'])
def add():
	global exist

	todo = Todo(id=request.form['todoid'], text=request.form['todoitem'], complete=0)
	try:
		db.session.add(todo)
		db.session.commit()
		exist = 0
	except:
		exist = 1

	return redirect(url_for('index'))


@app.route('/reset')
def reset():
	global exist
	exist = 0
	
	todo = db.session.query(Todo).delete()
	db.session.commit()

	return redirect(url_for('index'))


@app.route('/complete/<id>')
def complete(id):
	global exist
	exist = 0
	
	todo = Todo.query.filter_by(id=int(id)).first()
	todo.complete = 1
	db.session.commit()

	return redirect(url_for('index'))


@app.route('/clear_completed')
def clear_completed():
	global exist
	exist = 0
	
	todo = db.session.query(Todo).filter_by(complete=1).delete()
	db.session.commit()

	return redirect(url_for('index'))