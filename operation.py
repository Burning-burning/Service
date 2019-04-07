import sqlite3

conn = sqlite3.connect('server.sqlite3')
cursor = conn.cursor()
print('Do you want to operate the article or comment?')
i = input('Please input what you want to change, article or comment:')
if i == 'article':
    print('What do you want to operate article? hide or remove?')
    j = input('Please input your operation like hide, remove, recovery:')
    if j == 'hide':
        id = input('Please input you want to hide the article\'s id:')
        sql = 'select * from main.Publish where id=\''+id+'\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows == []:
            print('Not exist!')
        else:
            row = rows[0]
            sql = 'insert into hidden_publish(id, fname, title, abstract, desc, email, path, time) VALUES (?,?,?,?,?,?,?,?)'
            cursor.execute(sql, (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
            cursor.execute('delete from main.Publish where id=\''+id+'\'')
            print('Hide the article which id is '+id+' success!')
    elif j == 'remove':
        id = input('Please input you want to remove the article\'s id:')
        sql = 'select * from main.Publish where id=\'' + id + '\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        sql = 'select * from hidden_publish where id=\'' + id + '\''
        cursor.execute(sql)
        rows1 = cursor.fetchall()
        if rows == [] and rows1 == []:
            print('Not exist!')
        else:
            cursor.execute('delete from main.Publish where id=\'' + id + '\'')
            cursor.execute('delete from hidden_publish where id=\'' + id + '\'')
            print('Remove the article which id is ' + id + ' success!')
    elif j =='recovery':
        id = input('Please input you want to recovery the article\'s id:')
        sql = 'select * from hidden_publish where id=\'' + id + '\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows == []:
            print('Not exist!')
        else:
            row = rows[0]
            sql = 'insert into main.Publish(id, fname, title, abstract, desc, email, path, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
            cursor.execute(sql,(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
            cursor.execute('delete from hidden_publish where id=\'' + id + '\'')
            print('Recovery the article which id is ' + id + ' success!')
    else:
        print('Wrong instructions!')

elif i == 'comment':
    print('What do you want to manage with comments? hide , remove or recovery?')
    j = input('Please input the operation what you want to do? hide, remove, recovery')
    if j == 'hide':
        id = input('Please input you want to hide the comment\'s id:')
        sql = 'select * from main.Article where comment_id=\'' + id + '\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows == []:
            print('Not exist!')
        else:
            row = rows[0]
            sql = 'insert into hidden_article(id, thumb, comment, email, time, comment_id) values (?,?,?,?,?,?)'
            cursor.execute(sql, (row[0], row[1], row[2], row[3], row[4], row[5]))
            cursor.execute('delete from main.Article where comment_id=\'' + id + '\'')
            print('Hide the comment which id is' + id + ' success!')
    elif j == 'remove':
        id = input('Please input you want to remove the comment\'s id:')
        sql = 'select * from main.Article where comment_id=\'' + id + '\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        sql = 'select * from hidden_article where comment_id=\'' + id + '\''
        cursor.execute(sql)
        rows1 = cursor.fetchall()
        if rows == [] and rows1 == []:
            print('Not exist!')
        else:
            cursor.execute('delete from main.Article where comment_id=\'' + id + '\'')
            cursor.execute('delete from hidden_article where comment_id=\'' + id + '\'')
            print('Remove the comment which id is' + id + ' success!')
    elif j == 'recovery':
        id = input('Please input you want to recovery the comment\'s id:')
        sql = 'select * from hidden_article where comment_id=\'' + id + '\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows == []:
            print('Not exist!')
        else:
            row = rows[0]
            sql = 'insert into main.Article(id, thumb, comment, email, time, comment_id) values (?,?,?,?,?,?)'
            cursor.execute(sql, (row[0], row[1], row[2], row[3], row[4], row[5]))
            cursor.execute('delete from hidden_article where comment_id=\'' + id + '\'')
            print('Recovery the comment which id is' + id + ' success!')
    else:
        print('Wrong instructions!')
else:
    print('Wrong instructions,please re-star!')
conn.commit()
cursor.close()
conn.close()





