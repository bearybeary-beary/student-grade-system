# 学生成绩管理系统

一个基于 Python Flask 的学生成绩管理系统，支持学生信息管理、课程管理、成绩录入与统计。

## 功能

- 用户登录 / 退出
- 学生信息增删改查
- 课程管理
- 成绩录入、查询、删除
- 成绩统计：平均分、最高分、最低分

## 技术栈

- 后端：Python 3.10 + Flask
- 数据库：SQLite
- 前端：HTML + Bootstrap 5 + Jinja2
- 版本管理：Git

## 项目结构

student_grade_system/
├── app.py
├── init_db.py
├── requirements.txt
├── templates/
└── README.md

## 如何运行

1. 克隆项目

git clone https://github.com/bearybeary-beary/student-grade-system.git
cd student-grade-system

2. 安装依赖

pip install -r requirements.txt

3. 初始化数据库

python init_db.py

4. 启动项目

python app.py

5. 浏览器访问 http://127.0.0.1:5000

默认账号：admin / 123456

## 作者

胡晓芳 - 宁夏大学 计算机科学与技术 硕士