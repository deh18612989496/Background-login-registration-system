from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from back.models import User, Article, ArticleType, db
from utils.functions import is_login

back_blue = Blueprint('back', __name__)


@back_blue.route('/index/')
@is_login
def index():
    return render_template('back/index.html')


@back_blue.route('/register/', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('back/register.html')
    if request.method == 'POST':
        #获取数据
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if username and password and password2:
            user = User.query.filter(User.username == username).first()
            if user:
                error = '该账号已经注册，请更换账号！'
                return render_template('back/register.html', error=error)
            else:
                if password == password2:
                    user = User()
                    user.username = username
                    user.password = generate_password_hash(password)
                    user.save()
                    return redirect(url_for('back.login'))
                else:
                    error = '密码错误两次密码不一致！'
                    return render_template('back/register.html', error=error)
        else:
            error = '亲，请填写完整的信息！'
            return render_template('back/register.html', error=error)


@back_blue.route('/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('back/login.html')
    if request.method == 'POST':
        #获取数据
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            user = User.query.filter(User.username == username).first()
            if not user:
                error = '该账号不存在请注册！'
                return render_template('back/login.html', error=error)
            if not check_password_hash(user.password, password):
                error = '密码错误！'
                return render_template('back/login.html', error=error)
            #账号密码都正确
            session['user_id'] = user.id
            return redirect(url_for('back.index'))


        else:
            error = '请填写完整的登录信息！'
            return render_template('back/login.html', error=error)


@back_blue.route('/logout/', methods = ['GET'])
@is_login
def logout():
    del session['user_id']
    return redirect(url_for('back.login'))

@back_blue.route('/a_type/', methods = ['GET', 'POST'])
def a_type():
    if request.method == 'GET':
        types = ArticleType.query.all()
        return render_template('back/category_list.html', types=types)

@back_blue.route('/add_type/', methods = ['POST', 'GET'])
def add_type():
    if request.method == 'GET':
        return render_template('back/category_add.html')
    if request.method == 'POST':
        atype = request.form.get('atype')
        if atype:
            #保存分类信息
            art_type = ArticleType()
            art_type.t_name = atype
            db.session.add(art_type)
            db.session.commit()
            return redirect(url_for('back.a_type'))

        else:
            error = '请填写分类信息！'
            return render_template('back/category_add.html', error=error)

@back_blue.route('/del_type/<int:id>', methods = ['GET'])
def del_type(id):
    #删除分类
    atype = ArticleType.query.get(id)
    db.session.delete(atype)
    db.session.commit()
    return redirect(url_for('back.a_type'))

@back_blue.route('/article_list/',methods=['GET'])
def article_list():
    articles = Article.query.all()
    return render_template('back/article_list.html', articles=articles)

@back_blue.route('/article_add/', methods = ['POST', 'GET'])
def article_add():
    if request.method == 'GET':
        types = ArticleType.query.all()
        return render_template('back/article_detail.html', types = types)
    if request.method == 'POST':
        title = request.form.get('name')
        desc = request.form.get('desc')
        category = request.form.get('category')
        content = request.form.get('content')
        if title and desc and category and content:
            #保存
            art = Article()
            art.title = title
            art.desc = desc
            art.content = content
            art.type = category
            db.session.add(art)
            db.session.commit()
            return redirect(url_for('back.article_list'))
            pass
        else:
            error = '请填写完整的信息！'
            return render_template('back/article_detail.html', error = error)