from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
import os
import pymysql
from datetime import datetime
from django.db import transaction
global uname

def GenerateReport(request):
    if request.method == 'GET':
        columns = ['Employee ID', 'First Name', 'Last Name', 'Email', 'Phone', 'Hire Date', 
                   'Position', 'Salary', 'Department', 'Project Name', 'Task Name', 
                   'Task Status']
        output = '<table border=1 align=center><tr>'
        for column in columns:
            output += f'<th><font size="3" color="black">{column}</font></th>'
        output += '</tr>'
        
        con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', 
                              database='task', charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("""
                SELECT 
                    e.employeeID,
                    e.firstName,
                    e.lastName,
                    e.email,
                    e.phone,
                    e.hireDate,
                    e.position,
                    e.salary,
                    d.departmentName,
                    p.projectName,
                    t.taskName,
                    t.status AS taskStatus
                FROM 
                    Employee e
                LEFT JOIN Department d ON e.departmentID = d.departmentID
                LEFT JOIN Works w ON e.employeeID = w.employeeID
                LEFT JOIN Project p ON w.projectID = p.projectID
                LEFT JOIN Task t ON e.employeeID = t.assignedTo
                ORDER BY 
                    e.employeeID, p.projectName, t.taskName;
            """)
            rows = cur.fetchall()
            for row in rows:
                output += '<tr>'
                for cell in row:
                    output += f'<td><font size=3 color=black>{str(cell)}</font></td>'
                output += '</tr>'
        output += "</table><br/><br/><br/><br/>"
        context = {'data': output}
        return render(request, 'Modules.html', context)




def UpdateSkillsDetailsAction(request):
    if request.method == 'POST':
        skill_id = request.POST.get('t1', False)
        level = request.POST.get('t2', False)
        current_date = str(datetime.now().date())
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "update employeeskills set proficiencyLevel='"+level+"', dateAcquired='"+current_date+"' where employeeSkillID='"+skill_id+"'"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        status = "skill successfully updated"
        context= {'data': status}
        return render(request, 'SkillsModule.html', context)

def UpdateSkillsDetails(request):
    if request.method == 'GET':
        global username
        skill_id = request.GET['rid']
        output = '<tr><td><font size="3" color="black">Employee&nbsp;Skill&nbsp;ID</td><td><input type="text" name="t1" size="15" value="'+skill_id+'" readonly/></td></tr>'
        context= {'data1':output}        
        return render(request,'UpdateSkillsDetails.html', context)

def UpdateSkillsAction(request):
    if request.method == 'POST':
        skill = request.POST.get('t1', False)
        columns = ['Employee Skill ID', 'Skill ID', 'Employee ID', 'Proficiency Level', 'Acquired Date', 'Update Skills']
        output = '<table border=1 align=center><tr>'
        for i in range(len(columns)):
            output+='<th><font size="3" color="black">'+columns[i]+'</font></th>'
        output+='</th></tr>'
        skill_id = ""
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select skillID FROM skill where skillName='"+skill+"'")
            rows = cur.fetchall()
            for row in rows:
                skill_id = str(row[0])
                break
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM employeeskills where skillID='"+skill_id+"'")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size=3 color=black>'+str(row[0])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[1])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[2])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[3])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[4])+'</font></td>'
                output+='<td><a href=\'UpdateSkillsDetails?rid='+str(row[0])+'\'><font size=3 color=red>Click Here to Update Level</font></a></td></tr>'
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'SkillsModule.html', context)

def UpdateSkills(request):
    if request.method == 'GET':
        output = '<tr><td><font size="3" color="black">Task&nbsp;ID</td><td><select name="t1">'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select skillName FROM skill")
            rows = cur.fetchall()
            for row in rows:
                output += '<option value="'+str(row[0])+'">'+str(row[0])+'</option>'
        output += '</select></td></tr>'        
        context= {'data1': output}
        return render(request, 'UpdateSkills.html', context)

def AssignSkillsAction(request):
    if request.method == 'POST':
        skill = request.POST.get('t1', False)
        emp = request.POST.get('t2', False)
        proficiency = request.POST.get('t3', False)
        current_date = str(datetime.now().date())
        skill_id = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select max(employeeSkillID) FROM employeeskills")
            rows = cur.fetchall()
            for row in rows:
                skill_id = row[0]
                break
        if skill_id is not None:
            skill_id += 1
        else:
            skill_id = 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO employeeskills VALUES('"+str(skill_id)+"','"+skill+"','"+emp+"','"+proficiency+"','"+current_date+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            status = "Employee skills successfully assigned"
        context= {'data': status}
        return render(request, 'SkillsModule.html', context)

def AssignSkills(request):
    if request.method == 'GET':
        output = '<tr><td><font size="3" color="black">Skill&nbsp;ID</td><td><select name="t1">'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select skillID FROM skill")
            rows = cur.fetchall()
            for row in rows:
                output += '<option value="'+str(row[0])+'">'+str(row[0])+'</option>'
        output += '</select></td></tr>'        
        output += '<tr><td><font size="3" color="black">Employee&nbsp;ID</td><td><select name="t2">'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select employeeID FROM Employee")
            rows = cur.fetchall()
            for row in rows:
                output += '<option value="'+str(row[0])+'">'+str(row[0])+'</option>'
        output += '</select></td></tr>'
        context= {'data1': output}
        return render(request, 'AssignSkills.html', context) 

def AddSkillsAction(request):
    if request.method == 'POST':
        skills = request.POST.get('t1', False)
        desc = request.POST.get('t2', False)
        category = request.POST.get('t3', False)
        emp = request.POST.get('t4', False)
        skill_id = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select max(skillID) FROM skill")
            rows = cur.fetchall()
            for row in rows:
                skill_id = row[0]
                break
        if skill_id is not None:
            skill_id += 1
        else:
            skill_id = 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO skill VALUES('"+str(skill_id)+"','"+skills+"','"+desc+"','"+category+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            status = "New Skills created with ID = "+str(skill_id)
        context= {'data': status}
        return render(request, 'AddSkills.html', context)

def AddSkills(request):
    if request.method == 'GET':
        return render(request, 'AddSkills.html', {}) 

def SkillsModule(request):
    if request.method == 'GET':
        return render(request, 'SkillsModule.html', {})  

#lskills entry====================================

def TimeTrackingModuleAction(request):
    if request.method == 'POST':
        global username
        eid = request.POST.get('t1', False)
        columns = ['Entry ID', 'Entry Date', 'Hours Worked', 'Description', 'Task ID', 'Employee ID']
        output = '<table border=1 align=center><tr>'
        for i in range(len(columns)):
            output+='<th><font size="3" color="black">'+columns[i]+'</font></th>'
        output+='</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM timeentry where employeeID='"+eid+"'")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size=3 color=black>'+str(row[0])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[1])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[2])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[3])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[4])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[5])+'</font></td></tr>'
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'ResourcePage.html', context)


def TimeTrackingModule(request):
    if request.method == 'GET':
        output = '<tr><td><font size="3" color="black">Employee&nbsp;ID</td><td><select name="t1">'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select employeeID FROM Employee")
            rows = cur.fetchall()
            for row in rows:
                output += '<option value="'+str(row[0])+'">'+str(row[0])+'</option>'
        output += '</select></td></tr>'
        context= {'data1': output}
        return render(request, 'TimeTrackingModule.html', context)  

def DeleteEntryAction(request):
    if request.method == 'GET':
        entry = request.GET['rid']
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "delete from timeentry where entryID='"+entry+"'"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        status = "Entry successfully Deleted with ID = "+entry
        context= {'data': status}
        return render(request, 'UserScreen.html', context)

def DeleteEntry(request):
    if request.method == 'GET':
        global uname
        columns = ['Entry ID', 'Entry Date', 'Hours Worked', 'Description', 'Task ID', 'Employee ID', 'Delete Entry']
        output = '<table border=1 align=center><tr>'
        for i in range(len(columns)):
            output+='<th><font size="3" color="black">'+columns[i]+'</font></th>'
        output+='</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM timeentry where employeeID='"+uname+"'")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size=3 color=black>'+str(row[0])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[1])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[2])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[3])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[4])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[5])+'</font></td>'
                output+='<td><a href=\'DeleteEntryAction?rid='+str(row[0])+'\'><font size=3 color=red>Click Here to Delete Entry</font></a></td></tr>'
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'UserScreen.html', context)

def LogtimeEntryAction(request):
    if request.method == 'POST':
        hours = request.POST.get('t1', False)
        desc = request.POST.get('t2', False)
        task = request.POST.get('t3', False)
        emp = request.POST.get('t4', False)
        current_date = str(datetime.now().date())
        entry_id = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select max(entryID) FROM timeentry")
            rows = cur.fetchall()
            for row in rows:
                entry_id = row[0]
                break
        if entry_id is not None:
            entry_id += 1
        else:
            entry_id = 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO timeentry VALUES('"+str(entry_id)+"','"+current_date+"','"+hours+"','"+desc+"','"+task+"','"+emp+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            status = "New Worked Entry created with ID = "+str(entry_id)
        context= {'data': status}
        return render(request, 'UserScreen.html', context)

def LogtimeEntry(request):
    if request.method == 'GET':
        output = '<tr><td><font size="3" color="black">Task&nbsp;ID</td><td><select name="t3">'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select taskID FROM task")
            rows = cur.fetchall()
            for row in rows:
                output += '<option value="'+str(row[0])+'">'+str(row[0])+'</option>'
        output += '</select></td></tr>'        
        output += '<tr><td><font size="3" color="black">Employee&nbsp;ID</td><td><select name="t4">'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select employeeID FROM Employee")
            rows = cur.fetchall()
            for row in rows:
                output += '<option value="'+str(row[0])+'">'+str(row[0])+'</option>'
        output += '</select></td></tr>'
        context= {'data1': output}
        return render(request, 'LogtimeEntry.html', context)  

#logtime entry====================================

def ViewSchedule(request):
    if request.method == 'GET':
        global username
        columns = ['Schedule ID', 'Schedule Date', 'Start Time', 'End Time', 'Schedule Type', 'Employee ID']
        output = '<table border=1 align=center><tr>'
        for i in range(len(columns)):
            output+='<th><font size="3" color="black">'+columns[i]+'</font></th>'
        output+='</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM schedule")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size=3 color=black>'+str(row[0])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[1])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[2])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[3])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[4])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[5])+'</font></td></tr>'
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'SchedulingModule.html', context)

def CreateScheduleAction(request):
    if request.method == 'POST':
        schedule_date = request.POST.get('t1', False)
        start_time = request.POST.get('t2', False)
        end_time = request.POST.get('t3', False)
        schedule_type = request.POST.get('t4', False)
        empId = request.POST.get('t5', False)
        schedule_date = datetime.strptime(schedule_date, "%d-%m-%Y")
        schedule_date = str(schedule_date)
        schedule_date = schedule_date.split(" ")
        schedule_date = schedule_date[0]
        start_time = start_time.strip().split(" ")
        start_time = start_time[1]
        end_time = end_time.strip().split(" ")
        end_time = end_time[1]        
        schedule_id = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select max(scheduleID) FROM schedule")
            rows = cur.fetchall()
            for row in rows:
                schedule_id = row[0]
                break
        if schedule_id is not None:
            schedule_id += 1
        else:
            schedule_id = 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO schedule VALUES('"+str(schedule_id)+"','"+schedule_date+"','"+start_time+"','"+end_time+"','"+schedule_type+"','"+empId+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            status = "New Schedule created with ID = "+str(schedule_id)
        context= {'data': status}
        return render(request, 'SchedulingModule.html', context)

def CreateSchedule(request):
    if request.method == 'GET':
        output = '<tr><td><font size="3" color="black">Employee&nbsp;ID</td><td><select name="t5">'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select employeeID FROM Employee")
            rows = cur.fetchall()
            for row in rows:
                output += '<option value="'+str(row[0])+'">'+str(row[0])+'</option>'
        output += '</select></td></tr>'        
        context= {'data1': output}
        return render(request, 'CreateSchedule.html', context)

def SchedulingModule(request):
    if request.method == 'GET':
        return render(request, 'SchedulingModule.html', {})

#=====================================================schedule page

def UpdateResourceAction(request):
    if request.method == 'POST':
        pid = request.POST.get('t1', False)
        status = request.POST.get('t2', False)
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "update resource set assignedTaskID='"+status+"' where resourceID='"+pid+"'"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        status = "Resource successfully Assigned as "+status
        context= {'data': status}
        return render(request, 'ResourceModule.html', context)

def UpdateResourceDetails(request):
    if request.method == 'GET':
        global username
        pid = request.GET['rid']
        output = '<tr><td><font size="3" color="black">Resource&nbsp;ID</td><td><input type="text" name="t1" size="15" value="'+pid+'" readonly/></td></tr>'
        output += '<tr><td><font size="3" color="black">Assigned&nbsp;Task&nbsp;ID</td><td><input type="text" name="t2" size="15"/></td></tr>' 
        context= {'data1':output}        
        return render(request,'UpdateResourceDetails.html', context)

def UpdateResource(request):
    if request.method == 'GET':
        global username
        columns = ['Resource ID', 'Resource Name', 'Resource Type', 'Cost', 'Assigned Task ID', 'Quantity', 'Update Status']
        output = '<table border=1 align=center><tr>'
        for i in range(len(columns)):
            output+='<th><font size="3" color="black">'+columns[i]+'</font></th>'
        output+='</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM resource")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size=3 color=black>'+str(row[0])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[1])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[2])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[3])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[4])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[5])+'</font></td>'
                output+='<td><a href=\'UpdateResourceDetails?rid='+str(row[0])+'\'><font size=3 color=red>Click Here to Update Status</font></a></td></tr>'
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'ResourceModule.html', context)

def AddResourceAction(request):
    if request.method == 'POST':
        resource_name = request.POST.get('t1', False)
        resource_type = request.POST.get('t2', False)
        cost = request.POST.get('t3', False)
        task = request.POST.get('t4', False)
        quantity = request.POST.get('t5', False)
        resource_id = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select max(resourceID) FROM resource")
            rows = cur.fetchall()
            for row in rows:
                resource_id = row[0]
                break
        if resource_id is not None:
            resource_id += 1
        else:
            resource_id = 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO resource VALUES('"+str(resource_id)+"','"+resource_name+"','"+resource_type+"','"+cost+"','"+task+"','"+quantity+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            status = "New resource created with ID = "+str(resource_id)
        context= {'data': status}
        return render(request, 'ResourceModule.html', context)

def AddResource(request):
    if request.method == 'GET':
        output = '<tr><td><font size="3" color="black">Project&nbsp;ID</td><td><select name="t4">'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select taskID FROM task")
            rows = cur.fetchall()
            for row in rows:
                output += '<option value="'+str(row[0])+'">'+str(row[0])+'</option>'
        output += '</select></td></tr>'        
        context= {'data1': output}
        return render(request, 'AddResource.html', context)

def ResourceModule(request):
    if request.method == 'GET':
        return render(request, 'ResourceModule.html', {})

def ResourcePage(request):
    if request.method == 'GET':
        return render(request, 'ResourcePage.html', {})

#=====================================================resource page
def UpdateTaskStatusAction(request):
    if request.method == 'POST':
        pid = request.POST.get('t1', False)
        status = request.POST.get('t2', False)
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "update task set status='"+status+"' where taskID='"+pid+"'"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        status = "Task status successfully updated"
        context= {'data': status}
        return render(request, 'TaskPage.html', context)

def UpdateTaskStatusDetails(request):
    if request.method == 'GET':
        global username
        pid = request.GET['pid']
        output = '<tr><td><font size="3" color="black">Task&nbsp;ID</td><td><input type="text" name="t1" size="15" value="'+pid+'" readonly/></td></tr>'
        output += '<tr><td><font size="3" color="black">Update&nbsp;Status</td><td><input type="text" name="t2" size="65"/></td></tr>' 
        context= {'data1':output}        
        return render(request,'UpdateTaskStatusDetails.html', context)

def UpdateTaskStatus(request):
    if request.method == 'GET':
        global username
        columns = ['Task ID', 'Project ID', 'Task Name', 'Description', 'Assigned To', 'Status', 'Priority', 'Estimated Hours', 'Start Date', 'Due Date',
                   'ETA', 'Update Status']
        output = '<table border=1 align=center><tr>'
        for i in range(len(columns)):
            output+='<th><font size="3" color="black">'+columns[i]+'</font></th>'
        output+='</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM task")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size=3 color=black>'+str(row[0])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[1])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[2])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[3])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[4])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[5])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[6])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[7])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[8])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[9])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[10])+'</font></td>'
                output+='<td><a href=\'TrackUpdateStatusDetails?pid='+str(row[0])+'\'><font size=3 color=red>Click Here to Update Status</font></a></td></tr>'
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'TaskPage.html', context)

def CreateTaskAction(request):
    if request.method == 'POST':
        tname = request.POST.get('t1', False)
        desc = request.POST.get('t2', False)
        project_id = request.POST.get('t3', False)
        assigned_to = request.POST.get('t4', False)
        status = request.POST.get('t5', False)
        priority = request.POST.get('t6', False)
        hours = request.POST.get('t7', False)
        start_date = request.POST.get('t8', False)
        end_date = request.POST.get('t9', False)
        eta = request.POST.get('t10', False)

        eta = datetime.strptime(eta, "%d-%m-%Y")
        eta = str(eta)
        eta = eta.split(" ")
        eta = eta[0]
        
        start_date = datetime.strptime(start_date, "%d-%m-%Y")
        start_date = str(start_date)
        start_date = start_date.split(" ")
        start_date = start_date[0]
        end_date = datetime.strptime(end_date, "%d-%m-%Y")
        end_date = str(end_date)
        end_date = end_date.split(" ")
        end_date = end_date[0]
        task_id = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select max(taskID) FROM task")
            rows = cur.fetchall()
            for row in rows:
                task_id = row[0]
                break
        if task_id is not None:
            task_id += 1
        else:
            task_id = 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO task VALUES('"+str(task_id)+"','"+project_id+"','"+tname+"','"+desc+"','"+assigned_to+"','"+status+"','"+priority+"','"+hours+"','"+start_date+"','"+end_date+"','"+eta+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            status = "Task created with ID = "+str(task_id)
        context= {'data': status}
        return render(request, 'TaskPage.html', context)

def CreateTask(request):
    if request.method == 'GET':
        output = '<tr><td><font size="3" color="black">Project&nbsp;ID</td><td><select name="t3">'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select projectID FROM project")
            rows = cur.fetchall()
            for row in rows:
                output += '<option value="'+str(row[0])+'">'+str(row[0])+'</option>'
        output += '</select></td></tr>'        
        output += '<tr><td><font size="3" color="black">Assigned&nbsp;To</td><td><select name="t4">'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select employeeID FROM Employee")
            rows = cur.fetchall()
            for row in rows:
                output += '<option value="'+str(row[0])+'">'+str(row[0])+'</option>'
        output += '</select></td></tr>'
        context= {'data1': output}
        return render(request, 'CreateTask.html', context)         

def TaskPage(request):
    if request.method == 'GET':
        return render(request, 'TaskPage.html', {})    


#===============================================project code

def TrackUpdateStatusAction(request):
    if request.method == 'POST':
        pid = request.POST.get('t1', False)
        status = request.POST.get('t2', False)
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "update Project set status='"+status+"' where projectID='"+pid+"'"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        status = "Project status successfully updated"
        context= {'data': status}
        return render(request, 'ProjectsPage.html', context)

def TrackUpdateStatusDetails(request):
    if request.method == 'GET':
        global username
        pid = request.GET['pid']
        output = '<tr><td><font size="3" color="black">Project&nbsp;ID</td><td><input type="text" name="t1" size="15" value="'+pid+'" readonly/></td></tr>'
        output += '<tr><td><font size="3" color="black">Update&nbsp;Status</td><td><input type="text" name="t2" size="65"/></td></tr>' 
        context= {'data1':output}        
        return render(request,'TrackUpdateStatusDetails.html', context)

def TrackUpdateStatus(request):
    if request.method == 'GET':
        global username
        columns = ['Project ID', 'Project Name', 'Description', 'Start Date', 'End Date', 'Status', 'Budget', 'Project Manager', 'Update Status']
        output = '<table border=1 align=center><tr>'
        for i in range(len(columns)):
            output+='<th><font size="3" color="black">'+columns[i]+'</font></th>'
        output+='</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM Project")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size=3 color=black>'+str(row[0])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[1])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[2])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[3])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[4])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[5])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[6])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[7])+'</font></td>'
                output+='<td><a href=\'TrackUpdateStatusDetails?pid='+str(row[0])+'\'><font size=3 color=red>Click Here to Update Status</font></a></td></tr>'
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'ProjectsPage.html', context)

def CreateProjectAction(request):
    if request.method == 'POST':
        pname = request.POST.get('t1', False)
        desc = request.POST.get('t2', False)
        start_date = request.POST.get('t3', False)
        end_date = request.POST.get('t4', False)
        budget = request.POST.get('t5', False)
        manager = request.POST.get('t6', False)
        start_date = datetime.strptime(start_date, "%d-%m-%Y")
        start_date = str(start_date)
        start_date = start_date.split(" ")
        start_date = start_date[0]
        end_date = datetime.strptime(end_date, "%d-%m-%Y")
        end_date = str(end_date)
        end_date = end_date.split(" ")
        end_date = end_date[0]
        project_id = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select max(projectID) FROM Project")
            rows = cur.fetchall()
            for row in rows:
                project_id = row[0]
                break
        if project_id is not None:
            project_id += 1
        else:
            project_id = 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO Project VALUES('"+str(project_id)+"','"+pname+"','"+desc+"','"+start_date+"','"+end_date+"','Working','"+budget+"','"+manager+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            status = "New Project details added with ID = "+str(project_id)
        context= {'data': status}
        return render(request, 'ProjectsPage.html', context)

def CreateProject(request):
    if request.method == 'GET':
        output = '<tr><td><font size="3" color="black">Employee&nbsp;ID</td><td><select name="t6">'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select employeeID FROM Employee")
            rows = cur.fetchall()
            for row in rows:
                output += '<option value="'+str(row[0])+'">'+str(row[0])+'</option>'
        output += '</select></td></tr>'
        context= {'data1': output}
        return render(request, 'CreateProject.html', context)         

def ProjectsPage(request):
    if request.method == 'GET':
        return render(request, 'ProjectsPage.html', {})    


#===============================================department code

def UpdateDepartmentAction(request):
    if request.method == 'POST':
        did = request.POST.get('t1', False)
        name = request.POST.get('t2', False)
        location = request.POST.get('t3', False)
        manager = request.POST.get('t4', False)
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "update department set departmentName='"+name+"', location='"+location+"', managerID='"+manager+"' where departmentID='"+did+"'"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        status = "Department details successfully updated"
        context= {'data': status}
        return render(request, 'DepartmentPage.html', context)

def UpdateDepartmentDetails(request):
    if request.method == 'GET':
        global username
        name = ""
        location = ""
        manager = ""
        did = request.GET['did']
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM department where departmentID='"+did+"'")
            rows = cur.fetchall()
            for row in rows:
                did = str(row[0])
                name = str(row[1])
                location = str(row[2])
                manager = str(row[3])                
                break          
        output = '<tr><td><font size="3" color="black">Department&nbsp;ID</td><td><input type="text" name="t1" size="15" value="'+did+'" readonly/></td></tr>'
        output += '<tr><td><font size="3" color="black">Department&nbsp;Name</td><td><input type="text" name="t2" size="15" value="'+name+'"/></td></tr>' 
        output += '<tr><td><font size="3" color="black">Location</td><td><input type="text" name="t3" size="15" value="'+location+'"/></td></tr>'
        output += '<tr><td><font size="3" color="black">Manager</td><td><input type="text" name="t4" size="20" value="'+manager+'"/></td></tr>'
        context= {'data1':output}        
        return render(request,'UpdateDepartmentDetails.html', context)

def UpdateDepartment(request):
    if request.method == 'GET':
        global username
        columns = ['Department ID', 'Department Name', 'Location', 'Manager ID', 'Update Department']
        output = '<table border=1 align=center><tr>'
        for i in range(len(columns)):
            output+='<th><font size="3" color="black">'+columns[i]+'</font></th>'
        output+='</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM department")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size=3 color=black>'+str(row[0])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[1])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[2])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[3])+'</font></td>'
                output+='<td><a href=\'UpdateDepartmentDetails?did='+str(row[0])+'\'><font size=3 color=red>Click Here to Edit</font></a></td></tr>'
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'DepartmentPage.html', context)

def AssignManagerAction(request):
    if request.method == 'POST':
        eid = request.POST.get('t1', False)
        did = request.POST.get('t2', False)
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "update department set managerID='"+eid+"' where departmentID='"+did+"'"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            status = 'Manager successfully assigned to department '+did
        context= {'data': status}
        return render(request, 'DepartmentPage.html', context)

def AssignManager(request):
    if request.method == 'GET':
        output = '<tr><td><font size="3" color="black">Employee&nbsp;ID</td><td><select name="t1">'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select employeeID FROM Employee")
            rows = cur.fetchall()
            for row in rows:
                output += '<option value="'+str(row[0])+'">'+str(row[0])+'</option>'
        output += '</select></td></tr>'

        output += '<tr><td><font size="3" color="black">Department&nbsp;ID</td><td><select name="t2">'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select departmentID FROM department")
            rows = cur.fetchall()
            for row in rows:
                output += '<option value="'+str(row[0])+'">'+str(row[0])+'</option>'
        output += '</select></td></tr>'        
        context= {'data1': output}
        return render(request, 'AssignManager.html', context) 

def AddDepartmentAction(request):
    if request.method == 'POST':
        dept_name = request.POST.get('t1', False)
        loc_name = request.POST.get('t2', False)
        manager_id = request.POST.get('t3', False)
        dept_id = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select max(departmentID) FROM department")
            rows = cur.fetchall()
            for row in rows:
                dept_id = row[0]
                break
        if dept_id is not None:
            dept_id += 1
        else:
            dept_id = 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO department VALUES('"+str(dept_id)+"','"+dept_name+"','"+loc_name+"','"+manager_id+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            status = "Department details added with ID = "+str(dept_id)
        context= {'data': status}
        return render(request, 'AddDepartment.html', context)

def AddDepartment(request):
    if request.method == 'GET':
        return render(request, 'AddDepartment.html', {})

def DepartmentPage(request):
    if request.method == 'GET':
        return render(request, 'DepartmentPage.html', {})    


#===============================================department code

def ViewEmpHistoryAction(request):
    if request.method == 'POST':
        global username
        eid = request.POST.get('t1', False)
        columns = ['Employee ID', 'First Name', 'Last Name', 'Email', 'Phone', 'HireDate', 'Department ID', 'Position', 'Salary', 'Password']
        output = '<table border=1 align=center><tr>'
        for i in range(len(columns)):
            output+='<th><font size="3" color="black">'+columns[i]+'</font></th>'
        output+='</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from Employee e where e.employeeID = '"+eid+"'")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size=3 color=black>'+str(row[0])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[1])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[2])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[3])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[4])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[5])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[6])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[7])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[8])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[9])+'</font></td></tr>'
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'EmployeePage.html', context) 

def ViewEmpHistory(request):
    if request.method == 'GET':
        output = '<tr><td><font size="3" color="black">Employee&nbsp;ID</td><td><select name="t1">'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select employeeID FROM Employee")
            rows = cur.fetchall()
            for row in rows:
                output += '<option value="'+str(row[0])+'">'+str(row[0])+'</option>'
        output += '</select></td></tr>'
        context= {'data1': output}
        return render(request, 'ViewEmpHistory.html', context) 
from django.db import transaction

def DeactivateAccountDetails(request):
    if request.method == 'GET':
        eid = request.GET['eid']
        deactivated_employee = None
        status = ''
        
        db_connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='root',
            database='task',
            charset='utf8'
        )
        db_cursor = db_connection.cursor()
        
        try:
            # Store employee details before deletion
            db_cursor.execute("SELECT * FROM Employee WHERE employeeID = %s", (eid,))
            deactivated_employee = db_cursor.fetchone()
            
            with transaction.atomic():
                db_cursor.execute("SET FOREIGN_KEY_CHECKS=0")
                delete_sql_query = "DELETE FROM Employee WHERE employeeID = %s"
                db_cursor.execute(delete_sql_query, (eid,))
                db_cursor.execute("SET FOREIGN_KEY_CHECKS=1")
                db_connection.commit()
                status = 'Employee details successfully deactivated'
        except Exception as e:
            status = f'Error deactivating employee: {e}'
        finally:
            db_cursor.close()
            db_connection.close()
            
        context = {
            'data': status,
            'deactivated_employee': deactivated_employee,
            'show_undo': True
        }
        return render(request, 'EmployeePage.html', context)

from datetime import datetime
from django.db import transaction

@transaction.atomic
def UndoDeactivation(request):
    if request.method == 'POST':
        status = ''
        db_connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='root',
            database='task',
            charset='utf8'
        )
        db_cursor = db_connection.cursor()
        
        try:
            # Convert the date from "Month DD, YYYY" to "YYYY-MM-DD"
            hire_date_str = request.POST['hire_date']
            hire_date = datetime.strptime(hire_date_str, '%B %d, %Y').strftime('%Y-%m-%d')
            
            insert_sql_query = """
            INSERT INTO Employee (employeeID, FirstName, LastName, Email, Phone, HireDate)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            db_cursor.execute("SET FOREIGN_KEY_CHECKS=0")
            db_cursor.execute(insert_sql_query, (
                request.POST['eid'],
                request.POST['first_name'],
                request.POST['last_name'],
                request.POST['email'],
                request.POST['phone_no'],
                hire_date
            ))
            db_cursor.execute("SET FOREIGN_KEY_CHECKS=1")
            db_connection.commit()
            status = 'Employee account restored successfully'
            
        except Exception as e:
            db_connection.rollback()
            status = f'Error restoring employee account: {e}'
        finally:
            db_cursor.close()
            db_connection.close()
            
        context = {'data': status}
        return render(request, 'EmployeePage.html', context)

  

def DeactivateAccount(request):
    if request.method == 'GET':
        global username
        columns = ['Employee ID', 'First Name', 'Last Name', 'Email', 'Phone No', 'Hire Date', 'Deactivate Account']
        output = '<table border=1 align=center><tr>'
        for i in range(len(columns)):
            output+='<th><font size="3" color="black">'+columns[i]+'</font></th>'
        output+='</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM Employee")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size=3 color=black>'+str(row[0])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[1])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[2])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[3])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[4])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[5])+'</font></td>'                
                output+='<td><a href=\'DeactivateAccountDetails?eid='+str(row[0])+'\'><font size=3 color=red>Click Here to Deactivate</font></a></td></tr>'
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'EmployeePage.html', context) 

def UpdateEmployeeAction(request):
    if request.method == 'POST':
        eid = request.POST.get('t1', False)
        phone = request.POST.get('t2', False)
        dept = request.POST.get('t3', False)
        position = request.POST.get('t4', False)
        salary = request.POST.get('t5', False)
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "update Employee set phone='"+phone+"', departmentID='"+dept+"', position='"+position+"', salary='"+salary+"' where employeeID='"+eid+"'"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        status = "Employee details successfully updated"
        context= {'data': status}
        return render(request, 'EmployeePage.html', context)

def UpdateEmployeeDetails(request):
    if request.method == 'GET':
        global username
        phone = ""
        dept = ""
        position = ""
        salary = ""
        eid = request.GET['eid']
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select phone, departmentID, position, salary FROM Employee where employeeID='"+eid+"'")
            rows = cur.fetchall()
            for row in rows:
                phone = str(row[0])
                dept = str(row[1])
                position = str(row[2])
                salary = str(row[3])                
                break          
        output = '<tr><td><font size="3" color="black">Employee&nbsp;ID</td><td><input type="text" name="t1" size="15" value="'+eid+'" readonly/></td></tr>'
        output += '<tr><td><font size="3" color="black">Phone&nbsp;No</td><td><input type="text" name="t2" size="15" value="'+phone+'"/></td></tr>' 
        output += '<tr><td><font size="3" color="black">Department&nbsp;ID</td><td><input type="text" name="t3" size="15" value="'+dept+'"/></td></tr>'
        output += '<tr><td><font size="3" color="black">Position</td><td><input type="text" name="t4" size="20" value="'+position+'"/></td></tr>'
        output += '<tr><td><font size="3" color="black">Salary</td><td><input type="text" name="t5" size="15" value="'+salary+'"/></td></tr>'
        context= {'data1':output}        
        return render(request,'UpdateEmployeeDetails.html', context)

def UpdateEmployee(request):
    if request.method == 'GET':
        global username
        columns = ['Employee ID', 'First Name', 'Last Name', 'Email', 'Phone No', 'Hire Date', 'Department ID', 'Position', 'Salary', 'Password', 'Update Employee']
        output = '<table border=1 align=center><tr>'
        for i in range(len(columns)):
            output+='<th><font size="3" color="black">'+columns[i]+'</font></th>'
        output+='</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM Employee")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size=3 color=black>'+str(row[0])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[1])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[2])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[3])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[4])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[5])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[6])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[7])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[8])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[9])+'</font></td>'
                output+='<td><a href=\'UpdateEmployeeDetails?eid='+str(row[0])+'\'><font size=3 color=red>Click Here to Edit</font></a></td></tr>'
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'EmployeePage.html', context) 

def AddEmployeeAction(request):
    if request.method == 'POST':
        fname = request.POST.get('t1', False)
        lname = request.POST.get('t2', False)
        email = request.POST.get('t3', False)
        phone = request.POST.get('t4', False)
        hiredate = request.POST.get('t5', False)
        dept = request.POST.get('t6', False)
        position = request.POST.get('t7', False)
        salary = request.POST.get('t8', False)
        report_to = request.POST.get('t9', False)
        password = request.POST.get('t10', False)
        #hiredate = datetime.strptime(hiredate, "%d-%m-%Y")
        #hiredate = str(hiredate)
        #hiredate = hiredate.split(" ")
        #hiredate = hiredate[0]
        emp_id = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select max(employeeID) FROM Employee")
            rows = cur.fetchall()
            for row in rows:
                emp_id = row[0]
                break
        if emp_id is not None:
            emp_id += 1
        else:
            emp_id = 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO Employee VALUES('"+str(emp_id)+"','"+fname+"','"+lname+"','"+email+"','"+phone+"','"+hiredate+"','"+dept+"','"+position+"','"+salary+"','"+password+"','"+report_to+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            status = "Employee details added with ID = "+str(emp_id)
        context= {'data': status}
        return render(request, 'EmployeePage.html', context)

def AddEmployee(request):
    if request.method == 'GET':
        output = '<tr><td><font size="3" color="black">Department&nbsp;ID</td><td><select name="t6">'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select departmentID FROM Department")
            rows = cur.fetchall()
            for row in rows:
                output += '<option value="'+str(row[0])+'">'+str(row[0])+'</option>'
        output += '</select></td></tr>'
        context= {'data1': output}
        return render(request, 'AddEmployee.html', context)

def RegisterAction(request):
    if request.method == 'POST':
        fname = request.POST.get('t1', False)
        lname = request.POST.get('t2', False)
        email = request.POST.get('t3', False)
        phone = request.POST.get('t4', False)
        hiredate = request.POST.get('t5', False)
        dept = request.POST.get('t6', False)
        position = request.POST.get('t7', False)
        salary = request.POST.get('t8', False)
        report_to = request.POST.get('t9', False)
        password = request.POST.get('t10', False)
        #hiredate = datetime.strptime(hiredate, "%d-%m-%Y")
        #hiredate = str(hiredate)
        #hiredate = hiredate.split(" ")
        #hiredate = hiredate[0]
        emp_id = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select max(employeeID) FROM Employee")
            rows = cur.fetchall()
            for row in rows:
                emp_id = row[0]
                break
        if emp_id is not None:
            emp_id += 1
        else:
            emp_id = 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO Employee VALUES('"+str(emp_id)+"','"+fname+"','"+lname+"','"+email+"','"+phone+"','"+hiredate+"','"+dept+"','"+position+"','"+salary+"','"+password+"','"+report_to+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            status = "Employee details added with ID = "+str(emp_id)
        context= {'data': status}
        return render(request, 'home.html', context)
    

def Register(request):
    if request.method == 'GET':
        output = '<tr><td><font size="3" color="black">Department&nbsp;ID</td><td><select name="t6">'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select departmentID FROM Department")
            rows = cur.fetchall()
            for row in rows:
                output += '<option value="'+str(row[0])+'">'+str(row[0])+'</option>'
        output += '</select></td></tr>'
        context= {'data1': output}
        return render(request, 'Register.html', context)    

def EmployeePage(request):
    if request.method == 'GET':
        return render(request, 'EmployeePage.html', {})     

def Modules(request):
    if request.method == 'GET':
        return render(request, 'Modules.html', {})   

def index(request):
    if request.method == 'GET':
        return render(request, 'index.html', {})    

def AdminLoginAction(request):
    if request.method == 'POST':
        global uname
        index = 0
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if username == 'admin' and password == 'admin':
            index = 1
            context= {'data':'welcome '+username}
            return render(request, 'Modules.html', context)
        else:
            con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
            with con:    
                cur = con.cursor()
                cur.execute("select email, password, employeeID FROM Employee")
                rows = cur.fetchall()
                for row in rows:
                    if row[0] == username and row[1] == password:
                        uname = str(row[2])
                        index = 1
                        break
            if index == 1:
                context= {'data':'welcome '+username}
                return render(request, 'UserScreen.html', context)
            else:
                context= {'data':'login failed'}
                return render(request, 'home.html', context)
            

def AdminLogin(request):
    if request.method == 'GET':
        return render(request, 'AdminLogin.html', {})

def UserLogin(request):
    if request.method == 'GET':
        return render(request, 'UserLogin.html', {})

def home(request):
    if request.method == 'GET':
        return render(request, 'home.html', {})    

def UserLoginAction(request):
    if request.method == 'POST':
        global uname
        username = request.POST.get('t1', False)
        index = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'task',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select employeeID FROM Employee")
            rows = cur.fetchall()
            for row in rows:
                if str(row[0]) == username:
                    uname = username
                    index = 1
                    break		
        if index == 1:
            context= {'data':'welcome '+username}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'UserLogin.html', context)


        
