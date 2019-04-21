
import os
from flask import Flask, render_template, send_from_directory, request, jsonify, url_for, redirect, abort
import time
import datetime
import uuid
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
from flask import session
from flask import request


from publish import Serverdatabase

app = Flask(__name__)
app.config['SECRET_KEY']='123456'
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024


#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'


@app.route('/Publish')
def Publish():
    return render_template('Publish.html')


@app.route('/editor', methods=['GET', 'POST'])
def editor():
    #如果是post方法就返回tinymce生成html代码，否则渲染editor.html
    if request.method=='POST':
        return request.form['content']
    return render_template('editor.html')


UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # 设置文件上传的目标文件夹
basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径
ALLOWED_EXTENSIONS = set(['pdf', 'jpg', 'xlxs', 'doc', 'docx', 'txt', 'ppt', 'pptx', 'xls'])  # 允许上传的文件后缀


# 判断文件是否合法
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#下载文件
@app.route("/download/<filename>")
def download(filename):
    dirpath = os.path.join(app.root_path, 'static/upload')  # 这里是下在目录，从工程的根目录写起，比如你要下载static/js里面的js文件，这里就要写“static/js”
    return send_from_directory(dirpath, filename, as_attachment=True)  # as_attachment=True 一定要写，不然会变成打开，而不是下载

@app.route('/publish1')
def publish1():
    info = Serverdatabase.showInfo()
    return render_template('publish1.html', info = info)


@app.route('/add', methods=['GET', 'POST'], strict_slashes=False)
def add():
    if request.method == 'GET':
        return render_template('fail.html')
    else:
        catalogue = request.form['catalogue']
        desc = request.form['desc']
        if catalogue == ''or desc == '':
            return "False, the input cannot be empty."
        else:
            if Serverdatabase.check_words(catalogue) and Serverdatabase.check_words(desc):
                if Serverdatabase.setCata(catalogue, desc):
                    return redirect(url_for('catalogue'))

                else:
                    return "False, There are the same subjects, please re-input."
            else:
                return "False, Please re-input, you maybe input " \
                       "inappropriate words include fuck, bitch, md, nmsl, idiot, shit, " \
                       "freak, foolish, liar, stupid, silly, jerk, prat, insane, rubbish, nonsense."


@app.route('/donate')
def donate():
    return render_template("donate.html")

@app.route('/')
def catalogue():
    info = Serverdatabase.getCata()
    return render_template('index.html',info=info)

@app.route('/forum/<id>')
def forum(id):
    info = Serverdatabase.getArticle(id)
    tool = Tool()

    return render_template('publish1.html', info=info, id=id, tool=tool)


@app.route('/forum/search/<id>', methods=['Get', 'POST'])
def search(id):
    if request.method=='Get':
        return render_template('publish1.html', id=id)
    else:
        search_content = request.form['search_content']
        if search_content =='':
            return "False, please input the information what you want to search."
        else:
            if Serverdatabase.check_words(search_content):
                info = Serverdatabase.search_articles(id, search_content)
                tool = Tool()
                return render_template('publish1.html', id=id, info=info, tool=tool)
            else:
                return "False, Please re-input, you maybe input " \
                       "inappropriate words include fuck, bitch, md, nmsl, idiot, shit, " \
                       "freak, foolish, liar, stupid, silly, jerk, prat, insane, rubbish, nonsense."

@app.route('/search', methods=['Get', 'POST'])
def search1():
    if request.method=='Get':
        return render_template('index.html')
    else:
        search_content = request.form['search_content']
        if search_content =='':
            return "False, please input the information what you want to search."
        else:
            if Serverdatabase.check_words(search_content):
                info = Serverdatabase.search(search_content)
                info1 = Serverdatabase.search_comment(search_content)
                tool = Tool()
                return render_template('result.html', info=info,info1=info1, tool=tool)
            else:
                return "False, Please re-input, you maybe input " \
                       "inappropriate words include fuck, bitch, md, nmsl, idiot, shit, " \
                       "freak, foolish, liar, stupid, silly, jerk, prat, insane, rubbish, nonsense."



@app.route('/publish/<id>')
def publish(id):
    return render_template('Home1.html', id1=id)


@app.route('/upload/<id>', methods=['POST', 'GET'], strict_slashes=False)
def api_upload(id):
    if request.method == 'GET':
        return render_template('Home1.html')
        app.logger.debug('get')
    else:
        title = request.form['title']
        desc = request.form['content']
        email = request.form['email']
        abstract = request.form['abstract']
        vcode = request.form['vcode']
        id1 = str(uuid.uuid4())
        print(id)
        if desc == '':
            return "false, please input the highlight."
        else:
            if Serverdatabase.check_words(title) and Serverdatabase.check_words(abstract) and Serverdatabase.check_words(desc) and Serverdatabase.check_words(vcode) and Serverdatabase.check_words(email):

                if session['captcha'] == vcode:
                    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])  # 拼接成合法文件夹地址
                    if not os.path.exists(file_dir):
                        os.makedirs(file_dir)  # 文件夹不存在就创建
                    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
                    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
                        fname = f.filename
                        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
                        path = str(os.path.join(file_dir, fname))
                        time = datetime.datetime.now()
                        time = str(time)
                        time = time[0:16]
                        print(os.path.join(file_dir, fname))
                        if ext == 'pdf':
                            f.save(os.path.join(file_dir, fname))
                            if not check_session(100):
                                return "False, you have upload it in a short period."
                            Serverdatabase.upload(id1, fname, title, abstract, desc, email, path, time, id)
                            return redirect(url_for('forum', id=id))
                        else:
                            return "False. Please upload PDF file."

                else:
                    return "Failed. Please enter the correct verification code "
            else:
                return "False, Please re-input, you maybe input " \
                       "inappropriate words include fuck, bitch, md, nmsl, idiot, shit, " \
                       "freak, foolish, liar, stupid, silly, jerk, prat, insane, rubbish, nonsense."




@app.route('/<id>')
def title(id):
    info = Serverdatabase.article(id)
    info1 = Serverdatabase.article1(id)
    info2 = Serverdatabase.get_article_catalogue_info(id)
    info3 = Serverdatabase.get_count(id)
    tool = Tool()

    return render_template('article.html', info=info, info1=info1, info2=info2, id=id, info3=info3,tool=tool)
#加密操作
class Tool:
    def jiami(self, email):
        email3 = email
        count1 = len(email)
        email = email[0:email.rfind('@', 0)]
        count = len(email)
        email1 = email[0:int(count / 3)]
        email2 = email[int(count / 3):count]
        email2 = email2.replace(email2, "***")
        email4 = email3[count:count1]
        email5 = email1 + email2 + email4
        return email5

@app.route('/comment/<id>',methods=['POST', 'GET'])
def comment(id):
    if request.method=='GET':
        return render_template('article.html')
    else:
        if not check_session(20):
            return "False, you have commented it in a short period."
        comment = request.form['comment']
        email = request.form['email']
        vcode = request.form['vcode']
        if Serverdatabase.check_words(comment) and Serverdatabase.check_words(email) and Serverdatabase.check_words(
                vcode):
            if session['captcha'] == vcode:
                time = datetime.datetime.now()
                time = str(time)
                time = time[0:16]
                Serverdatabase.insert_comment(id, comment, email, time)
                info = Serverdatabase.article(id)
                info1 = Serverdatabase.article1(id)
                info2 = Serverdatabase.get_article_catalogue_info(id)
                info3 = Serverdatabase.get_count(id)
                tool = Tool()
                return render_template('article.html', info=info, info1=info1, info2=info2, id=id, info3=info3,
                                       tool=tool)
            else:
                return "Failed. Please enter the correct verification code "
        else:
            return "False, Please re-input, you maybe input " \
                   "inappropriate words include fuck, bitch, md, nmsl, idiot, shit, " \
                   "freak, foolish, liar, stupid, silly, jerk, prat, insane, rubbish, nonsense."


@app.after_request
def after_request(response):
    if request.path.startswith('/'):
        id = request.path[request.path.rfind('/', 0)+1:]
        print(id)
        ip = request.remote_addr
        print(ip)
        Serverdatabase.set_count(id, ip)
    return response

@app.before_request
def before_request():
    if request.path.startswith('/publish/'):
        verify = Verify()
        verify.show()


@app.before_request
def beforeRequest():
    ip = request.remote_addr
    Serverdatabase.record_ip(ip)


@app.errorhandler(413)
def request_error(e):
    return render_template('413.html'), 413

# using session to limit repeat request
def check_session(limit=5):
    t1 = 0
    if session.get('timestamp') is not None:
        t1 = session.get('timestamp')
    delta = time.time() - t1
    session['timestamp'] = time.time()
    if (delta > limit):
        return True
    return False

@app.route('/author/<email>')
def author(email):
    info = Serverdatabase.get_author(email)
    info1 = Serverdatabase.get_author1(email)
    tool = Tool()
    return render_template('author.html', info = info, info1 = info1, tool = tool)


@app.route('/like/<id>', methods=['POST'])
def like(id):
    color = request.form['color']
    if color == "#ff0000":
        Serverdatabase.increase_count(id)
    else:
        Serverdatabase.decrease_count(id)

#生成验证码操作
class Verify:
    # 生成随机字母
    def rndChar(self):
        return chr(random.randint(65, 90))
    # 随机生成数字和字母
    def getrand(num, many):  # num 位数   many 个数
        for x in range(many):  # 验证码一共的位数
            s = ""
            for y in range(num):
                n = random.randint(1, 2)  # n=1 或者 n=2, n=1生成数字 n=2 生成字母
                if n == 1:
                    numb = random.randint(0, 9)
                    s += str(numb)
                else:
                    nn = random.randint(1, 2)
                    cc = random.randint(1, 26)
                    if nn == 1:
                        numb = chr(64 + cc)
                        s += numb
                    else:
                        numb = chr(96 + cc)
                        s += numb
            return s

    # 随机的颜色
    def rndColor(self):
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

    def rndColor1(self):
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

    def show(self):
        width = 60 * 4  # 生成四个随机字母
        height = 60

        image = Image.new('RGB', (width, height), (255, 255, 255))

        # 创建Font对象: 选择文字字体和大小
        font = ImageFont.truetype("Arial.ttf", 36)
        # 创建Draw对象:
        draw = ImageDraw.Draw(image)

        # 填充每个像素
        for x in range(width):
            for y in range(height):
                draw.point((x, y), fill=Verify.rndColor1(self))

        # 输出文字:
        captcha = ''
        for t in range(4):
            captcha += Verify.getrand(1, 4)
            draw.text((60 * t + 10, 10), captcha[t], font=font, fill=Verify.rndColor(self))
        session['captcha'] = captcha
        image.save('static/vcode/vcode.jpg', 'jpeg')

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80)

