import os

if __name__ == '__main__':

    # 数据源目录
    path = 'outfile/community-1000'

    sqlstr_del ='';
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            ofile = os.path.join(dirpath, file)
            print(ofile)
            if(file[-4:]=='.sql'):
                print(ofile)
                os.system('mysql -hlocalhost -uroot -p123 -D eapp < ' + ofile)

                # 生成del脚本
                tab=file[:file.rfind('_')]
                tab=tab[:tab.rfind('_')]
                sqlstr_del = sqlstr_del + 'delete from ' + tab + " where substring(created_time,1,4) in ('2015','2016','2017','2018');\n"

    # 写文件
    with open('del_data.sql','w') as file:
        file.write(sqlstr_del)



