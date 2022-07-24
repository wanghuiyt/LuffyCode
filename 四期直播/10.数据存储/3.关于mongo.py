
"""
MySQL: 数据库(database)->表格(table)->数据(data)
mongodb: 数据库(database)->集合(collection)->文档(document)

mongodb常见操作:
    show dbs：显示所有数据库
    show databases：显示所有数据库
    use xxx：调整数据库
    db：当前数据库
    db.dropDatabase()：删除数据库
    show collections：显示当前数据库中所有的集合(表)
    db.createCollection("", {options})：创建集合， capped：是否卷动，size：大小
    db.collection_name.drop()：删除集合
    db.collection_name.insert()：向集合中添加数据(如果集合不存在，自动创建)
    新版：
        db.collection_name.insertOne({})
        db.collection_name.insertMany([{},{}])
    db.collection_name.isCapped()：判断是否有容量上限(判断该集合是否是固定容量的集合)
    db.collection_name.find()：获取数据信息
    db.collection_name.update({查询条件},{待修改内容},{multi:是否多条数据修改, upsert:true})：更新数据
        新版：
            db.collection_name.updateOne()
            db.collection_name.updateMany()
        db.stu.update({"name":"dylan"},{$set:{title:"alex",hobby:["抽烟","喝酒"]}},{multi:true,upsert:true})
        db.stu.update({name:"dylan"},{title:"alex"})
        $set和没有$set的区别：
            $set只会修改当前给出的字段，其他内容保留
            没有$set只会保留当前给出字段，其他内容删除
        multi：如果为True,必须使用$set，否则报错
    db.collection_name.save({待保存数据})： 保存数据
        db.collection_name.save({_id: "", name:"dylan", age:18})
        如果save的内容中_id如果存在就更新，如果不存在就添加
    db.collection_name.remove({条件},{justOne:true|false})：删除数据
    db.collection_name.deleteOne({条件})：删除数据
    db.collection_name.deleteMany({条件})：删除数据

mongodb常见数据类型:
    Object ID：主键ID
    String：字符串
    Boolean：布尔值
    Integer：数字
    Double：小数
    Arrays：数组
    Object：文档(关联其他对象) {name:xiao ming, age: 18, class:{xxx}}
    Null：空值
    Timestamp：时间戳
    Date：时间日期
"""
