import traceback
from api.weekly_reports.models import Weekly_reports
from common.query import raw_select     
from common.responses import success,failure
from flask import Blueprint
from api.project_view.models import Project
from common.utils import upload_to_s3
from common.query import raw_select
from flask import request
from config import db,Config
from flask import Blueprint, request
from api.project_view.models import Project
from common.utils import upload_to_s3
from config import Config

from flask import request  
from config import db
project_value = Blueprint('project',__name__,url_prefix='/api/v1/projects')


'''#refresh_token
@project_value.route('/refreshToken', methods=['GET'])
def refreshToken():
    try:
        refresh_token = request.headers['refreshToken']
        # refresh_token = payload["refresh_token"]
        print(refresh_token)
        try:
            payload = jwt.decode(refresh_token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            return failure('Authentication timeout', 419)
        except jwt.DecodeError:
            print(traceback.print_exc())
            return failure('Unauthorized', 401)
        except jwt.InvalidTokenError:
            print(traceback.print_exc())
            return failure('Unauthorized', 401)
        user_id = payload['identity']
        if user_id.startswith('TEMP'):
            user_query = TempUser.query.filter_by(user_id=user_id)
        else:
            user_query = User.query.filter_by(id=payload['identity'])
        result = query_list_to_dict(user_query)
        if len(result) > 0:
            payload = payload['identity']
            identity = {'identity': payload, "exp": get_auth_exp(config.JWT_TOKEN_TIME_OUT_IN_MINUTES)}
            token = jwt.encode(identity, config.SECRET_KEY, config.JWT_ALGORITHM)
            tk = token.decode("utf-8")

            refres_identity = {'identity': payload, "exp": get_auth_exp(config.JWT_REFRESH_TOKEN_TIME_OUT_IN_MINUTES)}
            refres_token = jwt.encode(refres_identity, config.SECRET_KEY, config.JWT_ALGORITHM)
            refres_tk = refres_token.decode("utf-8")
            token = {'token': str(tk), 'refresh_token':str(refres_tk)}
            return success('success', token)
        else:
            print("hre")
            return failure('Unauthorized', 401)
    except Exception as err:
        print(traceback.print_exc())
        return failure('Unauthorized', 401)




#creating user token
@project_value.route('/createUserToken', methods=['GET'])
def createUserToken():
    try:
        user_id = request.headers["userId"]
        if user_id == "0":
            uuid = uuid1()
            import time
            ts = int(time.time())
            user_id = "TEMP" + str(uuid) + str(ts)
            userData = TempUser()
            userData.user_id = user_id
            add_item(userData)
        token = createToken(user_id)
        if len(token) > 0:
            return success("Success", token)
        else:
            return failure("Generating token failed",200)
    except Exception as err:
        print(traceback.print_exc())
        return failure('Unauthorized', 401)'''


#creating project


@project_value.route('/createproject', methods=['POST'])
def insert_user():
    print("debug")
    try:
        data = request.json
        print(data)
        title =data["projectTitle"]
        tm_fixed_cost = data["projectPaymentCost"]
        start_date = data["projectStartDate"]
        duration = data["projectDuration"]
        overall_completion = data["overallProjectCompletion"]
        logo_url = data["projectLogoUrl"]
        resources = data["resourcesUsed"]
        insert_query = Project(
            title=title,
            tm_fixed_cost=tm_fixed_cost,
            start_date= start_date,
            duration=duration,
            resources=resources,
            logo_url=logo_url,
            overall_completion=overall_completion,
        )
        print(insert_query)
        db.session.add(insert_query)
        db.session.commit()

        return success("success","added successfully")


    except Exception as e:
        print(traceback.print_exc())
        return failure("error",traceback.format_exc())


#get overall project

def get_unit_testing_count(res):

    count = 0
    for value in res:    
        unitpercent = value["is_unit_testing"]
        if unitpercent:
            count+=1     
    unitpercentage = int((count/len(res))*100)
    return unitpercentage
def get_review_count(res):
    count = 0
    for value in res:    
        codepercent = value["is_code_review"]
        if codepercent:
            count+=1

    codepercentage = int((count/len(res))*100)
    return codepercentage

def weekly_delay_count(result):
    count = 0
    for value in result:
        delaypercent = value["delay"]
        if delaypercent:
            count += 1
    delaypercentage = int((count/len(result))*100)
    return delaypercentage

def bugs_count(result):
    num_new_bugs = 0
    num_bugs_fixed = 0
    for value in result:
        new_bugs = value["new_bugs"]
        if new_bugs:
            num_new_bugs += new_bugs
        bug_fixed = value["bug_fixed"]
        if bug_fixed:
            num_bugs_fixed += bug_fixed
        total_bugs = num_new_bugs-num_bugs_fixed
        if not total_bugs > 0:
            total_bugs = 0
    return total_bugs






@project_value.route('/getOverallproject', methods=['GET'])
def listuser():

    try: 
        result_project = db.session.query(Project).all()
        list1 = []
        for value in result_project:

            raw_query = f"""select project.id as project_id,weekly_reports.id,weekly_reports.is_code_review,weekly_reports.is_unit_testing,weekly_reports.delay,weekly_reports.new_bugs,weekly_reports.features_completed,weekly_reports.new_bugs,weekly_reports.bug_fixed
                    from project
                    inner join weekly_reports
                    on project.id = weekly_reports.project_id where project.id ='{value.id}'"""
            res_list = raw_select(raw_query)
            print(res_list)
            if len(res_list)>0:
                print(res_list[0]['project_id'])
                unittest_percentage = get_unit_testing_count(res_list)
                codeReviews_percentage = get_review_count(res_list)
                delay_count = weekly_delay_count(res_list)
                bugs_counts = bugs_count(res_list)
                list1.append({"projectId": value.id, "projectName": value.title,"status" : "Inprogress","featuresCompleted" :res_list[0]["features_completed"],
                "startDate": value.start_date, "stopDate": value.end_date, "duration": value.duration,"logoUrl":value.logo_url,
                "completionPercentage": value.overall_completion,"unitTesting":unittest_percentage,"codeReviews":codeReviews_percentage,"numberOfBugs":bugs_counts,"delay":delay_count,"dependencies":0})
                print(delay_count)
                print(bugs_counts)
                
            else:
                sql_for_project = f"""select * from project where id ='{value.id}'"""
                res_list1 = raw_select(sql_for_project)
                if len(res_list1)>0:
                    for dict_data in res_list1:
                        list1.append({"projectId": value.id, "projectName": value.title,"status" : "Inprogress","featuresCompleted" :0,
                            "numberOfBugs" :0,"startDate": value.start_date, "stopDate": value.end_date, "duration": value.duration,"logoUrl":value.logo_url,
                            "completionPercentage": value.overall_completion,"unitTesting":0,"codeReviews":0,"numberOfBugs":0,"delay":0,"dependencies":0})
                    

        result = {"projectsCompleted" : 34,
                "runningProjects" : 99,
                "pipelineProjects" : 55,
                "supportRequired" : 70,
                "projects":list1}
        return success("success",result)
    except Exception as e:
        print(traceback.format_exc())
        return failure(str(e))


#editing the project

@project_value.route('/editProjects', methods=['POST'])
def editlist():
    try:
        data = request.json
        id = data["projectId"]
        title = data["projectTitle"]
        tm_fixed_cost = data["projectPaymentCost"]
        start_date = data["projectStartDate"]
        duration = data["projectDuration"]
        overall_completion = data["overallProjectCompletion"]
        logo_url = data["projectLogoUrl"]
        resources = data["resourcesUsed"]
        value1 = db.session.query(Project).filter(Project.id == id).first()
        if value1:
            value1.title = title
            value1.tm_fixed_cost = tm_fixed_cost
            value1.start_date = start_date
            value1.duration = duration
            value1.resources = resources
            value1.logo_url = logo_url
            value1.overall_completion = overall_completion
            db.session.commit()
            return success("success","added successfully")

        else:

            return failure("failure",)
    except Exception as e:
        return failure(str(e))



#get the project


# def getunittestingpercentage(res):
#     count = 0  
#     value = db.session.query(Project).filter(Project.id == id).first()

#     if value:
#         unitpercent = value["is_unit_testing"]
#         if unitpercent:
#             count = count + 1
#         else:
#             count = count
#     unitpercentage = int((count/len(res))*100)
#     return unitpercentage
# def getcodereviewpercentage(res):
#     count1 = 0
#     for values in res:
#         if values:
#             codepercent = values["is_code_review"]
#             if codepercent:
#                 count1 = count1 + 1
#             else:
#                 count1 = count1
#     codepercentage = int((count1/len(res))*100)
#     return codepercentage


def project_unit_count(result):

    count = 0
    for value in result:    
        unitpercent = value["is_unit_testing"]
        if unitpercent:
            count+=1     
    unitpercentage = int((count/len(result))*100)
    return unitpercentage
def project_code_review(result):
    count = 0
    for value in result:    
        codepercent = value["is_code_review"]
        if codepercent:
            count+=1

    codepercentage = int((count/len(result))*100)
    return codepercentage




@project_value.route('/getProjectDetail', methods=['GET'])
def displayproject():
    try:
        data = request.json
        id = data["projectId"]
        value = db.session.query(Project).filter(Project.id == id).first()
        dict1 = {}
        raw_query = f"""select project.id,weekly_reports.is_code_review,weekly_reports.is_unit_testing,weekly_reports.delay,weekly_reports.new_bugs,weekly_reports.bug_fixed
                from project
                inner join weekly_reports
                on project.id = weekly_reports.project_id where project.id ='{value.id}'"""
        result = raw_select(raw_query)
        if len(result) > 0:
            code_count = project_code_review(result)
            unittesting_count =  project_code_review(result)
            
        title = value.title
        start_date = value.start_date
        end_date = value.end_date
        logo_url = value.logo_url
        dict1 = {"projectId": id, "dashboardData":{"projectName": title,"logoUrl": logo_url,"status": "INPROGRESS","startDate":start_date,"endDate":end_date,"numberOfBugs":33,"numberOfDependencies":34,"codeReviews":code_count,"unitTesting":unittesting_count,
        "delay":delay_count,"bugs":bugs_counts}}
        return success("Success",dict1)
    except Exception as e:
        print(traceback.format_exc())
        return failure(str(e))



@project_value.route('/upload_image',methods=['POST'])
def upload_image():
    try:
        image_file = request.files['file']
        raw = image_file.read()
        filename = image_file.filename
        is_file_pushed=upload_to_s3(filename,obj=raw)
        if is_file_pushed :
           return success("Success",{'url':f'https://{Config.BUCKET}.s3.{Config.AWS_DEFAULT_REGION}.amazonaws.com/{filename}'}) # 'https://'+bucketname+'.s3.'+region_name+'.amazonaws.com/'+filename)
        return failure("unable to upload")
    except Exception as e:
        print(traceback.format_exc())
        return failure(str(e))









