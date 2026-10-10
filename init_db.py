import sqlite3

conn = sqlite3.connect('student_grade.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)''')

c.execute('''CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_no TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    class_name TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT UNIQUE NOT NULL,
    credit REAL
)''')

c.execute('''CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    score REAL,
    FOREIGN KEY(student_id) REFERENCES students(id),
    FOREIGN KEY(course_id) REFERENCES courses(id)
)''')

try:
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', '123456'))
except sqlite3.IntegrityError:
    pass

try:
    c.execute("INSERT INTO students (student_no, name, class_name) VALUES (?, ?, ?)", ('2024001', '张三', '计算机1班'))
    c.execute("INSERT INTO students (student_no, name, class_name) VALUES (?, ?, ?)", ('2024002', '李四', '计算机2班'))
    c.execute("INSERT INTO courses (course_name, credit) VALUES (?, ?)", ('数据结构', 4.0))
    c.execute("INSERT INTO courses (course_name, credit) VALUES (?, ?)", ('计算机网络', 3.0))
except sqlite3.IntegrityError:
    pass

conn.commit()
conn.close()
print('数据库初始化完成，默认账号 admin / 123456')