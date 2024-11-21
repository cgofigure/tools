
def salary_info(pay=None):
    weekly_hours = 40
    monthly_hours = 160
    yearly_hours = 1920

    if not pay:
        pay = float(input("What is your hourly pay? "))

    weekly_pay = pay * weekly_hours
    monthly_pay = pay * monthly_hours
    yearly_pay = pay * yearly_hours

    print("Weekly : {}".format(weekly_pay))
    print("Monthly : {}".format(monthly_pay))
    print("Yearly : {}".format(yearly_pay))
