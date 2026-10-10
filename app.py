from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = 'dev_secret_key_123'

DATABASE = 'student_grade.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        user = conn.execute(
            'SELECT * FROM users WHERE username=? AND password=?',
            (username, password)
        ).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('登录成功', 'success')
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('已退出登录', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    conn = get_db()
    student_count = conn.execute('SELECT COUNT(*) FROM students').fetchone()[0]
    course_count = conn.execute('SELECT COUNT(*) FROM courses').fetchone()[0]
    grade_count = conn.execute('SELECT COUNT(*) FROM grades').fetchone()[0]
    conn.close()
    return render_template(
        'index.html',
        student_count=student_count,
        course_count=course_count,
        grade_count=grade_count
    )

@app.route('/students')
@login_required
def students():
    conn = get_db()
    students = conn.execute('SELECT * FROM students ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('students.html', students=students)

@app.route('/students/add', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        student_no = request.form['student_no']
        name = request.form['name']
        class_name = request.form['class_name']
        conn = get_db()
        try:
            conn.execute(
                'INSERT INTO students (student_no, name, class_name) VALUES (?, ?, ?)',
                (student_no, name, class_name)
            )
            conn.commit()
            flash('学生添加成功', 'success')
        except sqlite3.IntegrityError:
            flash('学号已存在', 'danger')
        conn.close()
        return redirect(url_for('students'))
    return render_template('student_form.html', student=None)

@app.route('/students/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    conn = get_db()
    student = conn.execute('SELECT * FROM students WHERE id=?', (id,)).fetchone()
    if not student:
        conn.close()
        flash('学生不存在', 'danger')
        return redirect(url_for('students'))

    if request.method == 'POST':
        student_no = request.form['student_no']
        name = request.form['name']
        class_name = request.form['class_name']
        try:
            conn.execute(
                'UPDATE students SET student_no=?, name=?, class_name=? WHERE id=?',
                (student_no, name, class_name, id)
            )
            conn.commit()
            flash('学生信息更新成功', 'success')
        except sqlite3.IntegrityError:
            flash('学号已存在', 'danger')
        conn.close()
        return redirect(url_for('students'))

    conn.close()
    return render_template('student_form.html', student=student)

@app.route('/students/delete/<int:id>')
@login_required
def delete_student(id):
    conn = get_db()
    conn.execute('DELETE FROM grades WHERE student_id=?', (id,))
    conn.execute('DELETE FROM students WHERE id=?', (id,))
    conn.commit()
    conn.close()
    flash('学生已删除', 'info')
    return redirect(url_for('students'))

@app.route('/courses', methods=['GET', 'POST'])
@login_required
def courses():
    conn = get_db()
    if request.method == 'POST':
        course_name = request.form['course_name']
        credit = request.form['credit']
        try:
            conn.execute(
                'INSERT INTO courses (course_name, credit) VALUES (?, ?)',
                (course_name, credit)
            )
            conn.commit()
            flash('课程添加成功', 'success')
        except sqlite3.IntegrityError:
            flash('课程已存在', 'danger')
        conn.close()
        return redirect(url_for('courses'))

    courses = conn.execute('SELECT * FROM courses ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('courses.html', courses=courses)

@app.route('/courses/delete/<int:id>')
@login_required
def delete_course(id):
    conn = get_db()
    conn.execute('DELETE FROM grades WHERE course_id=?', (id,))
    conn.execute('DELETE FROM courses WHERE id=?', (id,))
    conn.commit()
    conn.close()
    flash('课程已删除', 'info')
    return redirect(url_for('courses'))

@app.route('/grades', methods=['GET', 'POST'])
@login_required
def grades():
    conn = get_db()
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        score = request.form['score']
        conn.execute(
            'INSERT INTO grades (student_id, course_id, score) VALUES (?, ?, ?)',
            (student_id, course_id, score)
        )
        conn.commit()
        flash('成绩录入成功', 'success')
        conn.close()
        return redirect(url_for('grades'))

    grades = conn.execute('''
        SELECT g.id, s.student_no, s.name, c.course_name, g.score
        FROM grades g
        JOIN students s ON g.student_id = s.id
        JOIN courses c ON g.course_id = c.id
        ORDER BY g.id DESC
    ''').fetchall()

    students = conn.execute('SELECT * FROM students').fetchall()
    courses = conn.execute('SELECT * FROM courses').fetchall()
    conn.close()
    return render_template('grades.html', grades=grades, students=students, courses=courses)

@app.route('/grades/delete/<int:id>')
@login_required
def delete_grade(id):
    conn = get_db()
    conn.execute('DELETE FROM grades WHERE id=?', (id,))
    conn.commit()
    conn.close()
    flash('成绩记录已删除', 'info')
    return redirect(url_for('grades'))

@app.route('/stats')
@login_required
def stats():
    conn = get_db()
    all_stats = conn.execute('''
        SELECT s.student_no, s.name, c.course_name, g.score
        FROM grades g
        JOIN students s ON g.student_id = s.id
        JOIN courses c ON g.course_id = c.id
        ORDER BY s.student_no, c.course_name
    ''').fetchall()

    avg_stats = conn.execute('''
        SELECT c.course_name,
               AVG(g.score) as avg_score,
               MAX(g.score) as max_score,
               MIN(g.score) as min_score,
               COUNT(*) as count
        FROM grades g
        JOIN courses c ON g.course_id = c.id
        GROUP BY c.id
    ''').fetchall()
    conn.close()
    return render_template('stats.html', stats=all_stats, avg_stats=avg_stats)

if __name__ == '__main__':
    app.run(debug=True)