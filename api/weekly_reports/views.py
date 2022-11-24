import traceback
import json
from flask import Blueprint, jsonify,request
from api.weekly_reports.models import Other_weekly_reports_data, Weekly_reports
from flask import Blueprint, request
from flask import request
from common.query import raw_select 
from config import db
from datetime import date
from common.responses import failure, success
weekly_reports = Blueprint('projects',__name__,url_prefix='/api/v1/reports')

todays_date = date.today()


# create a API for Weekly reports creation 

@weekly_reports.route('/addWeeklyReport', methods=['POST'])
def create_reports():

    try:
            if request.method == 'POST':
                data = request.json
                t_m_and_fixed_cost  =data['TMfixedCost']
                project_id = data['projectId']
                resources  = data['resourceInfo']
                weekly_completion = data['weeklyCompletion']
                no_storeis = data['numberOfStories']
                features_completed = data['featuresCompleted']
                new_bugs = data['newBugs']
                bug_fixed = data['bugsFixed']
                is_code_review = data['codeReview']
                load_code_review = json.loads(is_code_review)
                is_unit_testing = data['unitTesting']
                load_unit_testing = json.loads(is_unit_testing)
                is_weekly_communication = data['weeklyCommunication']
                load_weekly_communication =json.loads(is_weekly_communication)
                delay = data['delay']
                dependencies = data["dependencies"]
                riskMitigation = data["riskMitigation"]
                risks = data["risks"];
                supportRequired = data["supportRequired"]
                new_record = Weekly_reports(t_m_and_fixed_cost = t_m_and_fixed_cost, resources = resources,
                is_weekly_communication = load_weekly_communication,weekly_completion = weekly_completion,
                no_storeis = no_storeis,features_completed = features_completed,new_bugs = new_bugs,bug_fixed = bug_fixed,
                is_code_review = load_code_review , is_unit_testing = load_unit_testing ,delay = delay,project_id = project_id)
                print(resources)
                db.session.add(new_record)
                db.session.commit()
                new_reports = Other_weekly_reports_data(risk = risks,dependencies = dependencies,risk_mitigation = riskMitigation,support_required = supportRequired,weekly_report_id =new_record.id)
                db.session.add(new_reports)
                db.session.commit()
            return {"content":"Added successfully","error":0,"message":"success"}
    except Exception as e:
            print(traceback.format_exc())
            return failure(str(e))


# Get API for Get a inserted weeekly record

@weekly_reports.route('/getWeeklyReport', methods=['GET','POST'])
def test():
    try:
        data = request.json
        id = data["ProjectId"]
        week = data["Week"]
        month = data["Month"]
        if week == 1:
            x_range = f'{todays_date.year}-{month}-1'
            y_range = f'{todays_date.year}-{month}-8'
        if week == 2:
            x_range = f'{todays_date.year}-{month}-8'
            y_range = f'{todays_date.year}-{month}-15'
        if week == 3:
            x_range = f'{todays_date.year}-{month}-15'
            y_range = f'{todays_date.year}-{month}-22'
        if week == 4:
            x_range = f'{todays_date.year}-{month}-22'
            y_range = f'{todays_date.year}-{month}-31'
        week_sql = f'''select *
                        from weekly_reports
                        where created_at >= '{x_range}' and created_at<= '{y_range}' and project_id = '{id}'
                        order by created_at desc limit 1;'''
        weekly_list = raw_select(week_sql)
        dict2={}
        list2 = [] 
        dict1={}
        list1 = []       
        for weekly in weekly_list:
            id = weekly['id']
            t_m_fixedcost = weekly['t_m_and_fixed_cost']
            resources = weekly["resources"]
            weekly_completion = weekly["weekly_completion"]
            no_storeis = weekly["no_storeis"]
            features_completed = weekly["features_completed"]
            new_bugs = weekly["new_bugs"]
            bug_fixed = weekly["bug_fixed"]
            is_code_review = weekly["is_code_review"]
            is_unit_testing = weekly["is_unit_testing"]
            is_weekly_communication = weekly["is_weekly_communication"]
            delay = weekly["delay"]
            project_id = weekly["project_id"]
            dict2 = {"weeklyReportId":id,"TMfixedCost":t_m_fixedcost,"resourceInfo":json.loads(resources),"weeklyCompletion":weekly_completion,"numberOfStories":no_storeis,"ProjectId":project_id,
            "featuresCompleted":features_completed,"newBugs":new_bugs,"bugsFixed":bug_fixed,"codeReview":bool(is_code_review),"unitTesting":bool(is_unit_testing),"weeklyCommunication":bool(is_weekly_communication),"delay":delay}
            list2.append(dict2)
            raw_query = f""" select * from other_weekly_reports_data 
                    where weekly_report_id = '{dict2['weeklyReportId']}'"""
            result = raw_select(raw_query)
            
            for val in result:
                dependencies =val['dependencies']
                risk = val['risk']
                risk_mitigation = val['risk_mitigation']
                support_required = val['support_required']
                dict1 = {"dependencies":dependencies,"risk":risk,"support_required":support_required,"risk_mitigation":risk_mitigation}
                list1.append(dict1)
        reports = {"weeklyDetail":list2,"others":list1,"Month":month,"Week":week} 
        return success("Sucess",reports)
    except Exception as e:
        print(traceback.format_exc())
        return failure(str(e))

# Edit API for Edit a inserted weeekly record

@weekly_reports.route('/editWeeklyReport', methods=['PUT'])
def edit_report():
    try:
        data = request.json
        id = data["Id"]
        t_m_and_fixed_cost = data["T&M-fixedCost"]
        resources = data["resourceInfo"]
        weekly_completion = data["weeklyCompletion"]
        no_storeis = data["numberOfStories"]
        features_completed = data["featuresCompleted"]
        new_bugs = data["newBugs"]
        bug_fixed = data["bugsFixed"]
        is_code_review = data["codeReview"]
        is_unit_testing = data["unitTesting"]
        is_weekly_communication = data["weeklyCommunication"]
        delay = data["delay"]

        values = db.session.query(Weekly_reports).filter(Weekly_reports.id == id).first()
        if values :
            values.t_m_and_fixed_cost = t_m_and_fixed_cost
            values.resources = resources
            values.weekly_completion = weekly_completion
            values.no_storeis = no_storeis
            values.features_completed = features_completed
            values.new_bugs = new_bugs
            values.bug_fixed = bug_fixed
            values.is_code_review = is_code_review
            values.is_unit_testing = is_unit_testing
            values.is_weekly_communication = is_weekly_communication
            values.delay = delay
            db.session.commit()
            # return success("success","Update Reports")
            return {"content":"Added successfully","error":0,"message":"success"}
    except Exception as e:
        print(traceback.format_exc())
        return failure(str(e))       




