from sanxuat.models import *

from .models import Gan


class Employee(object):

    def __init__(self, ID, name, level, conveyor, device):
        self.ID = ID
        self.name = name
        self.level = level
        self.conveyor = conveyor
        self.device = device
        self.total_time_working = 0
        self.stage_ids = []

    def get_name(self):
        return self.name

    def add_time_working(self, time_working):
        self.total_time_working += time_working

    def add_stage_id(self, stage_id):
        self.stage_ids.append(stage_id)


class Stage(object):

    def __init__(self, ID, name, level, device, time_complete):
        self.ID = ID
        self.name = name
        self.level = level
        self.device = device
        self.time_complete = time_complete

    def get_name(self):
        return self.name


class Manage(object):

    def __init__(self):
        self.list_employee = []
        self.list_stage = []

    def add_employee(self, emp: Employee):
        self.list_employee.append(emp)

    def get_list_employees(self):
        return self.list_employee

    def sort_list_employee_by_level(self):
        for i in range(len(self.list_employee)):
            for j in range(i, len(self.list_employee)):
                if j != 0:
                    if self.list_employee[j].level is None or self.list_employee[j-1].level > self.list_employee[j].level:
                        self.list_employee[j], self.list_employee[j-1] = self.list_employee[j-1], self.list_employee[j]

    def add_stage(self, stage: Stage):
        self.list_stage.append(stage)

    def get_list_stages(self):
        return self.list_stage

    def remove_employee_assigned(self, emp: Employee):
        self.list_employee.remove(emp)


class AssignTask(object):

    def __init__(self):
        self.total_time = 0
        self.takt_time = 0
        self.manage = Manage()

    def get_conveyor(self, conveyor):
        self.conveyor = conveyor

    def get_conveyor_object(self):
        self.conveyor_object = Chuyen.objects.get(TenChuyen=self.conveyor)

    def add_emps_to_manage(self, emps):
        for emp in emps:
            if emp.BacTho is None:
                level = None
            else:
                level = emp.BacTho.dongia
            self.manage.add_employee(Employee(
                emp.id, 
                emp.TenNhanVien, 
                level, 
                emp.TenChuyen.TenChuyen,
                emp.MayUT1
            ))

    def get_emps(self, exclude_id_emps=None):
        if exclude_id_emps is None:
            self.emps = self.conveyor_object.nhanvien_set.all()
            self.add_emps_to_manage(self.emps)
        else:
            self.emps = self.conveyor_object.nhanvien_set.exclude(id__in=exclude_id_emps)
            self.add_emps_to_manage(self.emps)

    def count_emp_in_conveyor(self):
        self.total_emp = self.conveyor_object.nhanvien_set.count()
        return self.total_emp

    def print_list_employees(self):
        for emp in self.manage.get_list_employees():
            print(emp.get_name())

    def print_list_stages(self):
        for stage in self.manage.get_list_stages():
            print(stage.get_name())

    def get_id_instance(self, id):
        self.id_instance = id

    def get_stages(self):
        self.stages = CongDoan.objects.filter(gancongdoan__id=self.id_instance)
        self.add_stage_to_manage(self.stages)
        
    def add_stage_to_manage(self, stages):
        for stage in stages:
            if stage.BacTho is None:
                level = None
            else:
                level = stage.BacTho.dongia
            self.manage.add_stage(Stage(
                stage.id, 
                stage.TenCongDoan, 
                level,
                stage.ThietBi,
                stage.ThoiGianHoanThanh
            ))

    def get_total_time(self):
        for stage in self.stages:
            self.total_time += stage.ThoiGianHoanThanh
        return self.total_time

    def get_takl_time(self):
        self.takt_time = self.total_time / self.total_emp
        return self.takt_time # thoi gian trung binh cua 1 nv

    def get_tolerance(self, tolerance): # sai so cho phep
        self.tolerance = tolerance

    def get_amount_a_day(self):
        return 8*60*60/self.takt_time

    def get_products_amount(self):
        return

    def divide_task(self):
        for stage in self.manage.get_list_stages():
            a = self.takt_time
            b = self.tolerance
            c = stage.time_complete
            if stage.time_complete > self.takt_time + self.tolerance:
                pass
            elif self.takt_time - self.tolerance <= stage.time_complete <= self.takt_time + self.tolerance:
                for emp in self.manage.get_list_employees():
                    if emp.device == stage.device:
                        try:
                            # if emp.level >= stage.level:
                                gan = Gan.objects.filter(GanCongDoan__id=self.id_instance, CongDoan__id=stage.ID)
                                if gan.count() == 1:
                                    emp.add_time_working(stage.time_complete)
                                    gan.update(TongThoiGianCuaNhanVien = emp.total_time_working)
                                    gan[0].NhanVien.add(emp.ID)
                                    # print(emp.total_time_working)
                                    self.manage.remove_employee_assigned(emp)
                                    break
                        except Exception as e:
                            print(e)
            else:
                for emp in self.manage.get_list_employees():
                    if emp.device == stage.device:
                        try:
                            # if emp.level >= stage.level:
                                if emp.total_time_working >= self.takt_time - self.tolerance:
                                    emp.add_time_working(stage.time_complete)
                                    emp.add_stage_id(stage.ID)
                                    for stage_id in emp.stage_ids:
                                        gan = Gan.objects.filter(GanCongDoan__id=self.id_instance, CongDoan__id=stage_id)
                                        if gan.count() == 1:
                                            gan[0].NhanVien.add(emp.ID)
                                            gan.update(TongThoiGianCuaNhanVien=emp.total_time_working)
                                    # print(emp.total_time_working)
                                    self.manage.remove_employee_assigned(emp)
                                break
                        except Exception as e:
                            print(e)

