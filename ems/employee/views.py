import csv

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum

from .models import Employee


# ================= LOGIN =================
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")


# ================= LOGOUT =================
def logout_user(request):
    logout(request)
    return redirect("login")


# ================= HOME (Employee History) + SEARCH + DEPARTMENT FILTER =================
@login_required(login_url="/login/")
def home(request):
    employees = Employee.objects.all().order_by("-id")

    dept = request.GET.get("dept", "").strip()
    if dept:
        employees = employees.filter(department__iexact=dept)

    return render(request, "home.html", {
        "employees": employees,
        "dept": dept,
    })


# ================= ADD EMPLOYEE =================
@login_required(login_url="/login/")
def add_employee(request):
    if request.method == "POST":
        Employee.objects.create(
            name=request.POST.get("name", "").strip(),
            email=request.POST.get("email", "").strip(),
            department=request.POST.get("department", "").strip(),
            salary=request.POST.get("salary", 0),
        )
        return redirect("home")

    return render(request, "add_employee.html")


# ================= UPDATE EMPLOYEE =================
@login_required(login_url="/login/")
def update_employee(request, id):
    emp = Employee.objects.get(id=id)

    if request.method == "POST":
        emp.name = request.POST.get("name", "").strip()
        emp.email = request.POST.get("email", "").strip()
        emp.department = request.POST.get("department", "").strip()
        emp.salary = request.POST.get("salary", 0)
        emp.save()
        return redirect("home")

    return render(request, "update_employee.html", {"emp": emp})


# ================= DELETE EMPLOYEE =================
@login_required(login_url="/login/")
def delete_employee(request, id):
    Employee.objects.get(id=id).delete()
    return redirect("home")


# ================= MESSAGES PAGE =================
@login_required(login_url="/login/")
def messages_page(request):
    # Demo data (you can later create Message model)
    messages = [
        {"title": "Welcome!", "text": "You successfully logged in.", "time": "Today"},
        {"title": "Reminder", "text": "Update employee records regularly.", "time": "This week"},
    ]
    return render(request, "messages.html", {"messages": messages})


# ================= EMPLOYEE SETTINGS PAGE =================
@login_required(login_url="/login/")
def employee_settings(request):
    # Departments summary from DB
    departments = (
        Employee.objects.values("department")
        .annotate(total=Count("id"))
        .order_by("-total")
    )
    return render(request, "employee_settings.html", {"departments": departments})


# ================= EMPLOYEE RECALL PAGE =================
@login_required(login_url="/login/")
def employee_recall(request):
    # Show recent 10 employees
    recent_employees = Employee.objects.all().order_by("-id")[:10]
    return render(request, "employee_recall.html", {"recent_employees": recent_employees})


# ================= REPORTS PAGE =================
@login_required(login_url="/login/")
def reports_page(request):
    total_employees = Employee.objects.count()
    total_salary = Employee.objects.aggregate(total=Sum("salary"))["total"] or 0

    dept_report = (
        Employee.objects.values("department")
        .annotate(total=Count("id"), salary_sum=Sum("salary"))
        .order_by("-total")
    )

    return render(request, "reports.html", {
        "total_employees": total_employees,
        "total_salary": total_salary,
        "dept_report": dept_report,
    })


# ================= EXPORT CSV =================
@login_required(login_url="/login/")
def export_employees_csv(request):
    # Export respects current filters (q, dept)
    employees = Employee.objects.all().order_by("-id")

    q = request.GET.get("q", "").strip()
    if q:
        employees = employees.filter(name__icontains=q)

    dept = request.GET.get("dept", "").strip()
    if dept:
        employees = employees.filter(department__iexact=dept)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="employees.csv"'

    writer = csv.writer(response)
    writer.writerow(["Name", "Email", "Department", "Salary"])

    for emp in employees:
        writer.writerow([emp.name, emp.email, emp.department, emp.salary])

    return response
