import sqlite3;

conn = sqlite3.connect('server.sqlite3')
c = conn.cursor()


class Serverdatabase():
    @staticmethod
    def upload(id, fname, title, abstract, desc, email, path, time, id1):
        conn = sqlite3.connect('server.sqlite3')
        c1 = conn.cursor()
        c1.execute('insert or ignore into Publish'
                   '(id, fname, title, abstract, desc, email, path, time) '
                   'values (?,?,?,?,?,?,?,?)', (id, fname, title, abstract, desc, email, path, time))
        conn.commit()
        c1.close()
        c2 = conn.cursor()
        c2.execute('insert into Article_Catalogue(article_id, catalogue_id) values (?,?)', (id, id1))
        conn.commit()
        c2.close()
        conn.close()

    @staticmethod
    def showInfo():
        conn = sqlite3.connect('server.sqlite3')
        c = conn.cursor()
        sql = 'select * from Publish'
        c.execute(sql)
        data = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        print(data)
        print(str(data))
        return data

    @staticmethod
    def article(id):
        conn = sqlite3.connect('server.sqlite3')
        c = conn.cursor()
        sql = 'select * from Article where id = \'' + id + '\' order by time desc'
        c.execute(sql)
        data = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        return data

    @staticmethod
    def article1(id):
        conn = sqlite3.connect('server.sqlite3')
        c = conn.cursor()
        sql = 'select * from Publish where id = \'' + id + '\''
        c.execute(sql)
        data = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        return data

    @staticmethod
    def insert_comment(id,comment,email,time):
        conn = sqlite3.connect('server.sqlite3')
        c = conn.cursor()
        c.execute('insert or ignore into Article(id, comment,email,time) values (?,?,?,?)', (id, comment, email,time))
        conn.commit()
        c.close()
        conn.close()





    @staticmethod
    def setCata(catalogue, desc):
        conn = sqlite3.connect('server.sqlite3')
        c = conn.cursor()
        sql = 'select * from Catalogue where subject like \'%'+ catalogue + '%\''
        c.execute(sql)
        data = c.fetchall()
        if data == []:
            c.execute('insert into Catalogue(catalogue, desc) VALUES (?,?)', (catalogue, desc))
            conn.commit()
            c.close()
            conn.close()
            return True
        else:
            return False

    @staticmethod
    def getCata():
        conn = sqlite3.connect('server.sqlite3')
        c = conn.cursor()
        sql = 'select * from Catalogue'
        c.execute(sql)
        data = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        return data


    @staticmethod
    def getArticle(id):
        conn = sqlite3.connect('server.sqlite3')
        c = conn.cursor()
        c.execute("select * from Publish where id in "
                  "(select article_id from Article_Catalogue where catalogue_id = '%s') order by time desc" %id)
        data = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        return data

    @staticmethod
    def search_articles(id, content):
        conn = sqlite3.connect('server.sqlite3')
        c = conn.cursor()
        sql = 'select article_id from Article_Catalogue where catalogue_id =\''+id+'\''
        c.execute(sql)
        data = c.fetchall()
        info = len(data)
        rows = []
        for i in range(info):
            sql = 'select * from Publish where (title like\'%'+ content +'%\' or abstract like \'%'+content+'%\' or desc like\'%'+content+'%\' or email like\'%'+content+'%\' or time like \'%' +content+'%\') and id = \''+data[i][0]+'\''
            # sql = 'select * from Publish where id = \''+data[i][0]+'\''
            print(data[i][0])
            c.execute(sql)
            # data = c.fetchone()
            # rows[i] = c.fetchone()
            rows.append(c.fetchone())
        conn.commit()
        c.close()
        conn.close()
        info1 = len(rows)
        datas = []
        for i in range(info1):
            if rows[i] is None:
                pass
            else:
                datas.append(rows[i])
            # print(rows[i])
        print(datas)
        return datas

    @staticmethod
    def search(search):
        conn = sqlite3.connect('server.sqlite3')
        c = conn.cursor()
        sql = 'select * from Publish where title like\'%'+ search +'%\' or abstract like \'%'+search+'%\' or desc like\'%'+search+'%\' or email like\'%'+search+'%\' or time like \'%' +search+'%\''
        c.execute(sql)
        data = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        return data
    @staticmethod
    def search_comment(search):
        conn = sqlite3.connect('server.sqlite3')
        c = conn.cursor()
        sql = 'select * from main.Article where comment like\'%'+ search +'%\''
        c.execute(sql)
        data = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        return data

        #     print(data[i][0])
        # print(data)

    @staticmethod
    def get_article_catalogue_info(id):
        conn = sqlite3.connect('server.sqlite3')
        c = conn.cursor()
        c.execute("select * from Catalogue where id in "
                  "(select catalogue_id from Article_Catalogue where article_id = '%s')" %id)
        data = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        return data


    @staticmethod
    def set_count(id, ip):
        conn = sqlite3.connect('server.sqlite3')
        c = conn.cursor()
        sql = 'select * from Browse where id = \''+id+'\' and ip = \'' + ip + '\''
        c.execute(sql)
        data = c.fetchall()
        if data == []:
            c.execute('Insert into Browse(id, count, ip) values (?,?,?)',(id, 1, ip))
            conn.commit()
            c.close()
            conn.close()
        else:
            # sql = 'update Browse set count = count + 1 where id =\'' + id + '\''
            # c.execute(sql)
            conn.commit()
            c.close()
            conn.close()



    @staticmethod
    def get_count(id):
        conn = sqlite3.connect('server.sqlite3')
        c = conn.cursor()
        sql = 'select * from Browse where id = \''+id+'\''
        c.execute(sql)
        data = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        return data


    @staticmethod
    def increase_count(id):
        conn = sqlite3.connect('server.sqlite3')
        c = conn.cursor()
        sql = 'Update Like set count = count+1 where article_id = \''+id+'\''
        c.execute(sql)
        conn.commit()
        c.close()
        conn.close()

    @staticmethod
    def decrease_count(id):
        conn = sqlite3.connect('server.sqlite3')
        c = conn.cursor()
        sql = 'select * from Like where article_id = \''+id+'\''
        c.execute(sql)
        data = c.fetchall()
        if data==[]:
            c.execute("insert into Like(article_id, count) values(?,?)", (id, '1'))
        else:
            sql = 'Update Like set count = count -1 where article_id=\'' + id + '\''
            c.execute(sql)

        conn.commit()
        c.close()
        conn.close()

    @staticmethod
    def insert_words(word):
        conn = sqlite3.connect('server.sqlite3')
        c = conn.cursor()
        c.execute("insert or ignore into Inappropriate(words) values (?)", (word,))
        conn.commit()
        c.close()
        conn.close()
    @staticmethod
    def check_words(word):
        conn = sqlite3.connect('server.sqlite3')
        c = conn.cursor()
        sql = 'select * from Inappropriate where words = \'' + word + '\''
        c.execute(sql)
        data = c.fetchall()
        if data == []:
            return True
        else:
            return False
    @staticmethod
    def record_ip(ip):
        conn = sqlite3.connect('server.sqlite3')
        c = conn.cursor()
        sql = 'select * from IP where ip = \'' + ip + '\''
        c.execute(sql)
        data = c.fetchall()
        if data == []:
            c.execute("INSERT into IP(ip) values (?)", (ip,))
            conn.commit()
            c.close()
            conn.close()
        else:
            c.close()
            conn.close()

    @staticmethod
    def insert_subject( catalogue, desc, subject):
        conn = sqlite3.connect('server.sqlite3')
        c = conn.cursor()
        c.execute('insert or ignore into main.Catalogue(catalogue, desc, subject) values (?,?,?)', (catalogue, desc, subject))
        conn.commit()
        c.close()
        conn.close()

    @staticmethod
    def get_author(email):
        conn = sqlite3.connect('server.sqlite3')
        c = conn.cursor()
        sql = 'select * from main.Publish where email = \''+email+'\''
        c.execute(sql)
        data = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        return data
    @staticmethod
    def get_author1(email):
        conn = sqlite3.connect('server.sqlite3')
        c = conn.cursor()
        sql = 'select * from main.Article where email = \''+email+'\''
        c.execute(sql)
        data = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        return data


if __name__ == '__main__':

    # Serverdatabase.upload('10', 'PS', 'PS', '10000', '', ',', '', '')
    # Serverdatabase.setCata('physics', 'physicsphysics')
    # Serverdatabase.upload('1222','2','2','2','2','2','2','2','222')
    # Serverdatabase.search_articles('1')
    Serverdatabase.search_articles('1','111')
    Serverdatabase.insert_words('fuck')
    Serverdatabase.insert_words('bitch')
    Serverdatabase.insert_words('md')
    Serverdatabase.insert_words('nmsl')
    Serverdatabase.insert_words('idiot')

    Serverdatabase.insert_words('shit')
    Serverdatabase.insert_words('freak')
    Serverdatabase.insert_words('foolish')
    Serverdatabase.insert_words('liar')
    Serverdatabase.insert_words('stupid')

    Serverdatabase.insert_words('silly')
    Serverdatabase.insert_words('jerk')
    Serverdatabase.insert_words('prat')
    Serverdatabase.insert_words('insane')
    Serverdatabase.insert_words('rubbish')
    Serverdatabase.insert_words('nonsense')

    Serverdatabase.search('kiko')








