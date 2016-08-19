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
        for i in self.test_accounts:
            res = requests.get(self.check_url,
                               auth=(i, self.password),
                               verify=False)
            if res.status_code == 401 and "The system is unable to complete the requested transaction" in res.content:
                return i

    def get_sku(self, number):
        db = MySQLdb.connect(host=self.db_host, user=self.db_username, passwd=self.password, db="sku_db")
        c = db.cursor()
        c.execute("select id from sku_attributes_all;")
        d = c.fetchall()
        skus_list = [i[0] for i in d]
        return random.sample(skus_list, number)

username_line1 = Accounts().get_new_account()
skus_line1 = Accounts().get_sku(1)
username_line2 = Accounts().get_new_account()
skus_line2 = Accounts().get_sku(10)
username_line3 = Accounts().get_new_account()
skus_line3 = Accounts().get_sku(100)
username_line4 = Accounts().get_new_account()
skus_line4 = Accounts().get_sku(1000)
username_line5 = Accounts().get_new_account()
skus_line5 = Accounts().get_sku(10000)
info_str = """

"""

data_path = "/home/liusong/code/Ethel_Performance_Test/Test_Data/test_stress_account_attach.csv"
with open(data_path, "a+") as f:
    f.write()


print username, skus










