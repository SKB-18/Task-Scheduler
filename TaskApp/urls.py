from django.urls import path

from . import views

urlpatterns = [path("home.html", views.home, name="home"),
		     path("index.html", views.index, name="index"),
                     path("AdminLogin.html", views.AdminLogin, name="AdminLogin"),	      
                     path("AdminLoginAction", views.AdminLoginAction, name="AdminLoginAction"),
		     path("UserLogin.html", views.UserLogin, name="UserLogin"),
	             path("UserLoginAction", views.UserLoginAction, name="UserLoginAction"),
		     path("EmployeePage", views.EmployeePage, name="EmployeePage"),
		     path("AddEmployee.html", views.AddEmployee, name="AddEmployee"),
	             path("AddEmployeeAction", views.AddEmployeeAction, name="AddEmployeeAction"),
		     path("UpdateEmployeeDetails", views.UpdateEmployeeDetails, name="UpdateEmployeeDetails"),
		     path("UpdateEmployee", views.UpdateEmployee, name="UpdateEmployee"),
		     path("UpdateEmployeeAction", views.UpdateEmployeeAction, name="UpdateEmployeeAction"),
		     path("Modules", views.Modules, name="Modules"),
		     path("DeactivateAccount", views.DeactivateAccount, name="DeactivateAccount"),
              path('UndoDeactivation', views.UndoDeactivation, name='UndoDeactivation'),
		     path("DeactivateAccountDetails", views.DeactivateAccountDetails, name="DeactivateAccountDetails"),
		     path("ViewEmpHistory.html", views.ViewEmpHistory, name="ViewEmpHistory"),
	             path("ViewEmpHistoryAction", views.ViewEmpHistoryAction, name="ViewEmpHistoryAction"),
		     path("DepartmentPage", views.DepartmentPage, name="DepartmentPage"),
		     path("AddDepartment.html", views.AddDepartment, name="AddDepartment"),	      
                     path("AddDepartmentAction", views.AddDepartmentAction, name="AddDepartmentAction"),
		     path("AssignManager.html", views.AssignManager, name="AssignManager"),	      
                     path("AssignManagerAction", views.AssignManagerAction, name="AssignManagerAction"),
		     path("UpdateDepartment", views.UpdateDepartment, name="UpdateDepartment"),
		     path("UpdateDepartmentDetails", views.UpdateDepartmentDetails, name="UpdateDepartmentDetails"),
		     path("UpdateDepartmentAction", views.UpdateDepartmentAction, name="UpdateDepartmentAction"),
		     path("ProjectsPage", views.ProjectsPage, name="ProjectsPage"),
		     path("CreateProject", views.CreateProject, name="CreateProject"),
		     path("CreateProjectAction", views.CreateProjectAction, name="CreateProjectAction"),
		     path("TrackUpdateStatus", views.TrackUpdateStatus, name="TrackUpdateStatus"),
		     path("TrackUpdateStatusDetails", views.TrackUpdateStatusDetails, name="TrackUpdateStatusDetails"),
		     path("TrackUpdateStatusAction", views.TrackUpdateStatusAction, name="TrackUpdateStatusAction"),

		     path("TaskPage", views.TaskPage, name="TaskPage"),
		     path("CreateTask", views.CreateTask, name="CreateTask"),
		     path("CreateTaskAction", views.CreateTaskAction, name="CreateTaskAction"),
		     path("UpdateTaskStatus", views.UpdateTaskStatus, name="UpdateTaskStatus"),
		     path("UpdateTaskStatusDetails", views.UpdateTaskStatusDetails, name="UpdateTaskStatusDetails"),
		     path("UpdateTaskStatusAction", views.UpdateTaskStatusAction, name="UpdateTaskStatusAction"),

		     path("ResourcePage", views.ResourcePage, name="ResourcePage"),
		     path("ResourceModule", views.ResourceModule, name="ResourceModule"),
		     path("AddResource", views.AddResource, name="AddResource"),
		     path("AddResourceAction", views.AddResourceAction, name="AddResourceAction"),
		     path("UpdateResource", views.UpdateResource, name="UpdateResource"),
		     path("UpdateResourceDetails", views.UpdateResourceDetails, name="UpdateResourceDetails"),
		     path("UpdateResourceAction", views.UpdateResourceAction, name="UpdateResourceAction"),

		     path("SchedulingModule", views.SchedulingModule, name="SchedulingModule"),
		     path("CreateSchedule", views.CreateSchedule, name="CreateSchedule"),
		     path("CreateScheduleAction", views.CreateScheduleAction, name="CreateScheduleAction"),
		     path("ViewSchedule", views.ViewSchedule, name="ViewSchedule"),

		     path("LogtimeEntry", views.LogtimeEntry, name="LogtimeEntry"),
		     path("LogtimeEntryAction", views.LogtimeEntryAction, name="LogtimeEntryAction"),
		     path("DeleteEntry", views.DeleteEntry, name="DeleteEntry"),
		     path("DeleteEntryAction", views.DeleteEntryAction, name="DeleteEntryAction"),

		     path("TimeTrackingModule", views.TimeTrackingModule, name="TimeTrackingModule"),
		     path("TimeTrackingModuleAction", views.TimeTrackingModuleAction, name="TimeTrackingModuleAction"),

		     path("SkillsModule", views.SkillsModule, name="SkillsModule"),
		     path("AddSkills", views.AddSkills, name="AddSkills"),
		     path("AddSkillsAction", views.AddSkillsAction, name="AddSkillsAction"),
		     path("AssignSkills", views.AssignSkills, name="AssignSkills"),
		     path("AssignSkillsAction", views.AssignSkillsAction, name="AssignSkillsAction"),
		     path("UpdateSkills", views.UpdateSkills, name="UpdateSkills"),
		     path("UpdateSkillsDetails", views.UpdateSkillsDetails, name="UpdateSkillsDetails"),
		     path("UpdateSkillsAction", views.UpdateSkillsAction, name="UpdateSkillsAction"),
		     path("UpdateSkillsDetailsAction", views.UpdateSkillsDetailsAction, name="UpdateSkillsDetailsAction"),

		     path("GenerateReport", views.GenerateReport, name="GenerateReport"),

		     path("Register.html", views.Register, name="Register"),	      
                     path("RegisterAction", views.RegisterAction, name="RegisterAction"),
]