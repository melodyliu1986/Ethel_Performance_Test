__author__ = 'liusong'

"""
Random fetch $num skus.
"""

import MySQLdb

import requests
import random


class Accounts:
    """
    Return a new account in stage candlepin, which is used to test the account_new function.
    """
    def __init__(self):
        self.check_url = "https://subscription.rhsm.stage.redhat.com/subscription/products/MCT2888"
        self.test_accounts = ["stress_account_attach_{0}".format(i) for i in range(1000)]
        self.password = "redhat"
        # DB info.
        self.db_host = "account-manager-stage.app.eng.rdu2.redhat.com"
        self.db_username = "account_tool"

    def get_new_account(self):
        while 1:
            account = random.sample(self.test_accounts, 1)[0]
            res = requests.get(self.check_url, auth=(account, self.password), verify=False)
            print "#"*20
            print res.status_code
            print res.content, type(res.content)
            if res.status_code == 401 and "Invalid username or password" in res.content:
                return account

    def get_sku(self, number):
        db = MySQLdb.connect(host=self.db_host, user=self.db_username, passwd=self.password, db="sku_db")
        c = db.cursor()
        c.execute("select id from sku_attributes_all;")
        d = c.fetchall()
        skus_list = [i[0] for i in d]
        return random.sample(skus_list, number)


# Get different account for different line.
def get_different_account(account1):
    different_code = 0
    while 1:
        account2 = Accounts().get_new_account()
        if account2 == account1:
            Accounts().get_new_account(account1)
        else:
            different_code = 1
        if different_code == 1:
            return account2


username_line1 = Accounts().get_new_account()
skus_line1 = Accounts().get_sku(1)
username_line2 = get_different_account(username_line1)
skus_line2 = Accounts().get_sku(10)
username_line3 = get_different_account(username_line2)
skus_line3 = Accounts().get_sku(100)
username_line4 = get_different_account(username_line3)
skus_line4 = Accounts().get_sku(1000)
username_line5 = get_different_account(username_line4)
skus_line5 = Accounts().get_sku(10000)

info_str = """{0},,{1}
{2},,{3}
{4},,{5}
{6},,{7}
{8},,{9}
""".format(username_line1, skus_line1, username_line2, skus_line2, username_line3, skus_line3, username_line4, skus_line4, username_line5, skus_line5)
info_str = info_str.replace("\'", "\"")

data_path = "/home/workspace/Ethel_performance_test2/test_stress_account_attach.csv"
with open(data_path, "a+") as f:
    f.write(info_str)











