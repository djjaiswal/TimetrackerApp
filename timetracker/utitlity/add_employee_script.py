from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
#######################################################################
class Solution(object):
    less_than_20 = ["", "One", "Two", "Three", "Four", "Five", "Six",
    "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen",
    "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen",
    "Nineteen"]

    tens = ["","Ten", "Twenty", "Thirty", "Forty", "Fifty", "Sixty",
    "Seventy", "Eighty", "Ninety"]

    thousands = ["", "Thousand", "Million", "Billion"]

    def helper(self, n):
        if n == 0:
            return ""
        elif n < 20:
            return Solution.less_than_20[n] + " "
        elif n < 100:
            return Solution.tens[n // 10] + " " + self.helper(n % 10)
        else:
            return Solution.less_than_20[n // 100] + " Hundred " + self.helper(n % 100)

    def numberToWords(self, num):
       if num == 0:
          return "Zero"
       ans = ""
       i = 0
       while num > 0:
         if num % 1000 != 0:
            ans = self.helper(num % 1000) + Solution.thousands[i] + " " + ans
            i += 1
            num //= 1000
         return ans.strip()


obj = Solution()


######################################################################
s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.implicitly_wait(12)
url= "http://127.0.0.1:5000/login/"
driver.get(url)
driver.maximize_window()
driver.find_element("id","email").send_keys("jjayshree185@gmail.com")
driver.find_element("id","password").send_keys("India@123")
driver.find_element("id","submit").click()
driver.find_element("css selector","#bs-example-navbar-collapse-1 > ul > li:nth-child(3) > a").click()


def add_user(email, empid, fname, lname, dep, passw, confirmpassw):
    driver.find_element("xpath", "/html/body/div[1]/div/div/div/div/div/div/div/div/div/div[2]/button").click()
    driver.find_element("id","email").send_keys(email)
    driver.find_element("id", "emp_id").send_keys(empid)
    driver.find_element("id", "first_name").send_keys(fname)
    driver.find_element("id", "last_name").send_keys(lname)
    Select(driver.find_element("id","department")).select_by_value(str(dep))
    driver.find_element("id", "password").send_keys(passw)
    driver.find_element("id", "confirm_password").send_keys(confirmpassw)
    driver.find_element("id", "submit").click()

num = 4
for department in range(1,5):
    for count in range(1,10):
        email= f"Emp0{num}@gmail.com"
        empid =f"TT00{num}"
        fname = "Employee"
        lname = obj.numberToWords(num)
        passw = "India@123"
        confirmpassw = "India@123"
        add_user(email,empid,fname,lname,department, passw,confirmpassw)
        num+=1
