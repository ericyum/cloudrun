from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 데이터베이스 대신 사용할 인메모리 리스트
todos = []
todo_id_counter = 1

@app.route('/')
def index():
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_task():
    global todo_id_counter
    task_content = request.form.get('task')
    if task_content:
        todos.append({'id': todo_id_counter, 'task': task_content, 'done': False})
        todo_id_counter += 1
    return redirect(url_for('index'))

@app.route('/complete/<int:todo_id>')
def complete_task(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todo['done'] = not todo['done']
            break
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete_task(todo_id):
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    return redirect(url_for('index'))

@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit_task(todo_id):
    todo_to_edit = None
    for todo in todos:
        if todo['id'] == todo_id:
            todo_to_edit = todo
            break

    if todo_to_edit is None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        new_task_content = request.form.get('task')
        if new_task_content:
            todo_to_edit['task'] = new_task_content
        return redirect(url_for('index'))
    else:
        return render_template('edit.html', todo=todo_to_edit)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
