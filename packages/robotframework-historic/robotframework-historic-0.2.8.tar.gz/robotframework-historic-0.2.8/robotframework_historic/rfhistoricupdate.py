import mysql.connector
import logging

def rfhistoric_update(opts):
    rfdb = connect_to_mysql_db(opts.host, opts.username, opts.password, "robothistoric")
    # get list of databases
    rfobj = rfdb.cursor()
    rfobj.execute("SELECT Project_Name FROM TB_PROJECT;");
    results_data = rfobj.fetchall()

    for item in results_data:
        use_db(rfobj, str(item[0]))
        try:
            print("INFO: Updating TB_EXECUTION table of DB " + str(item[0]))
            execut_query(rfobj, "ALTER TABLE TB_EXECUTION ADD COLUMN Execution_Skip INT NOT NULL DEFAULT(0);")
            execut_query(rfobj, "ALTER TABLE TB_EXECUTION ADD COLUMN Execution_SSkip INT NOT NULL DEFAULT(0);")
        except Exception as e:
            print(str(e))

        try:
            print("INFO: Updating TB_SUITE table of DB " + str(item[0]))
            execut_query(rfobj, "ALTER TABLE TB_SUITE ADD COLUMN Suite_Skip INT NOT NULL DEFAULT(0);")
        except Exception as e:
            print(str(e))

        try:
            print("INFO: Updating TB_TEST table of DB " + str(item[0]))
            execut_query(rfobj, "ALTER TABLE TB_TEST ADD COLUMN Test_Assigned_To TEXT;")
            execut_query(rfobj, "ALTER TABLE TB_TEST ADD COLUMN Test_ETA TEXT;")
            execut_query(rfobj, "ALTER TABLE TB_TEST ADD COLUMN Test_Review_By TEXT;")
            execut_query(rfobj, "ALTER TABLE TB_TEST ADD COLUMN Test_Issue_Type TEXT;")
            execut_query(rfobj, "ALTER TABLE TB_TEST ADD COLUMN Test_Tag TEXT;")
            execut_query(rfobj, "ALTER TABLE TB_TEST ADD COLUMN Test_Updated DATETIME;")
        except Exception as e:
            print(str(e))

    commit_and_close_db(rfdb)

def connect_to_mysql(host, user, pwd):
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=pwd
        )
        return mydb
    except Exception as e:
        print(e)

def connect_to_mysql_db(host, user, pwd, db):
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=pwd,
            database=db
        )
        return mydb
    except Exception as e:
        print(e)

def use_db(cursor, db_name):
    cursor.execute("USE %s;" % db_name)

def commit_and_close_db(db):
    db.commit()
    db.close()

def execut_query(rfobj, query):
    try:
        rfobj.execute(query)
    except Exception as e:
        print(str(e))