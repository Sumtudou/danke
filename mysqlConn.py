import pymysql

# 远程授权命令 ，以 允许root用户任意地点使用授权码cws+166为例
# GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'cws+166' WITH GRANT OPTION;
USERNAME = "root"
PASSWD = "123456"  # 如果是远程授权访问的话，此选项不必是相应用户(如 root )的登录密码。此时相当于授权码
ADDR = "localhost"
DATABASE = "python"
TABLE = "user"
# 虽然说 MySQLdb 只支持 Python2 ，但Python3也能用
db = pymysql.connect(ADDR, USERNAME, PASSWD, DATABASE)

cursor = db.cursor()

# 创建user表
# mysql 未来都是用 UTF8MB4 来代替 utf8了 ，但只有 5.5.3 以后的版本才开始支持  select version();
# 主要差异  utf8 支持最大字符长度为3字节   utf8mb4 则支持4字节长度的 UTF-8字符
# 任何不在基本多文本平面的 Unicode字符，都无法使用 Mysql 的 utf8 字符集存储。
# 包括 Emoji 表情(Emoji 是一种特殊的 Unicode 编码，常见于 ios 和 android 手机上)，和很多不常用的汉字，以及任何新增的 Unicode 字符等等
# For More ,please refer to https://www.cnblogs.com/beyang/p/7580814.html

cursor.execute("drop table if exists {}".format(TABLE))

sql = """CREATE TABLE IF NOT EXISTS `{}` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(255) NOT NULL,
      `age` int(11) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB  DEFAULT CHARSET=UTF8MB4 AUTO_INCREMENT=0""".format(
    TABLE
)

# 此处没有用到 rollback
cursor.execute(sql)

# 插入
sql = """INSERT INTO `{}` (`name`, `age`) VALUES
('row1', 1),
('row2', 2),
('row3', 3),
('row4', 4);""".format(
    TABLE
)

try:
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
except:
    # 如果发生错误则回滚
    db.rollback()


# 更新
id = 1
sql = "update user set age=100 where id='%s'" % (id)
try:
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()

# 删除
id = 2
sql = "delete from user where id='%s'" % (id)
try:
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()

# 查询
cursor.execute("select * from user")

results = cursor.fetchall()
# results   # [out] 由元组组成的元组，每个元组里面三个元素，依次是 id name test
for row in results:
    name = row[1]
    age = row[2]
    # print(type(row[1])) #打印变量类型 <class 'str'>
    print("name = {} , age = {}".format(name, age))


