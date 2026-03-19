from datetime import datetime , timedelta
print((datetime.now()- (datetime.now() - timedelta(days = 1))).total_seconds())