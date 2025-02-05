from impl.hebece.src.api import *
from impl.hebece.src.parser import *
from impl.hebece.src.utils import *
from impl.hebece.src.signer import *

if __name__ == '__main__':
    today = datetime.today().strftime('%d-%m-%y')
    start_date, end_date = get_current_week()
    
    token = APILogin(login = input("login: "),password = input("password: "))
    if not token:
        print("You entered wrong login, password or VULCAN asked for captcha. Verify your login and password and try to log into eduVULCAN from your browser.")
        input("Press Enter to exit...")
        exit()
    
    tenant = get_tenant_from_jwt(token)
    
    content, dinfoJWT = JWTLogin(token, debug=True)
    
    content, dinfoHEBE = HEBELogin(tenant, debug=True)

    Name, SecondName, Surname, Class, PupilID, SchoolID, ConstituentID, UnitID, PeriodID = getUserInfo(tenant)

    content, dinfoLUCK = getLuckyNumber(tenant=tenant, schoolid=SchoolID, pupilid=PupilID, constituentid=ConstituentID, debug=True)

    content, dinfoGRADE = getGrades(tenant=tenant, schoolid=SchoolID, pupilid=PupilID, unitid=UnitID, periodid=PeriodID, debug=True)

    content, dinfoTIME = getTimetable(tenant=tenant, schoolid=SchoolID, pupilid=PupilID, start_date=start_date, end_date=end_date, debug=True)

    content, dinfoEXAM = getExams(tenant=tenant, schoolid=SchoolID, pupilid=PupilID, start_date=start_date, end_date=end_date, debug=True)
    
    print(f"\nJWT Status: {dinfoJWT[0]} {dinfoJWT[1]}")
    print(f"HEBE Status: {dinfoHEBE[0]} {dinfoHEBE[1]}")
    print(f"Lucky Number Status: {dinfoLUCK[0]} {dinfoLUCK[1]}")
    print(f"Grades Status: {dinfoGRADE[0]} {dinfoGRADE[1]}")
    print(f"Timetable Status: {dinfoTIME[0]} {dinfoTIME[1]}")
    print(f"Exams Status: {dinfoEXAM[0]} {dinfoEXAM[1]}")