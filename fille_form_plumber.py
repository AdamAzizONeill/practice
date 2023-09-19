from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from operations import Operations


class PlumberForm(Operations):
    def __init__(self, 
                 trade: str,
                 own_premises: str,
                 assumptions: str,
                 employers_liability: bool,
                 business_equipment: str | None,
                 atm: str,
                 claim: str,
                 claim_list: list,
                 ):
        self.trade = trade
        self.claim = claim
        self.assumptions = assumptions.capitalize()
        self.employers_liability = employers_liability
        self.business_equipment = business_equipment
        self.own_premises = own_premises.capitalize()
        self.atm = atm.capitalize()
        self.claim = claim.capitalize()
        self.claim_list = claim_list


    def fill_page1(self):
        self.input_text('//*[@id="tradeCodeText"]', self.trade)
        sleep(0.1)

        dropdown_options = self.driver.find_elements(By.CLASS_NAME, 'mat-option-text')
        self.select_from_dropdown(self.trade, dropdown_options)
        self.click_element(f'//*[@id="fixedBusinessPremises{self.own_premises}"]')
        self.click_element(f'//*[@id="coverAssumptions{self.assumptions}-button"]')
        if self.employers_liability:
            self.click_element(f'//*[@ng-reflect-name="employersLiabilitySelection"]')
        sleep(0.2)
        if self.business_equipment:
            self.click_element('//*[@ng-reflect-name="toolsStockEquipmentSelection"]')
            self.driver.execute_script("window.scrollBy(0,300);")
            sleep(0.3)
            self.click_element(f'//*[@ng-reflect-name="toolStockCoverAmount{self.business_equipment}"]')
        self.click_element('//*[@id="continueButton"]')


    def fill_claim(self):
        for i, claim in enumerate(self.claim_list):
            self.click_element(f'//*[@id="{claim["type"]}Ind"]')

            if claim['type'] != 'professionalIndemnity':
                self.input_text(f'//*[@ng-reflect-name="claimDateMonth{i}"]', claim['month'])
                self.input_text(f'//*[@ng-reflect-name="claimDateYear{i}"]', claim['year'])
                dropdown_bar = self.driver.find_element(By.XPATH, f'//*[@ng-reflect-name="claimType{i}"]')
                dropdown_bar.click()
                dropdown_list = dropdown_bar.find_elements(By.XPATH, './child::*')   
                self.select_from_dropdown(claim['main_cause'], dropdown_list)
                self.input_text(f'//*[@ng-reflect-name="claimAmount{i}"]', claim['amount_of_loss'])
                self.input_text(f'//*[@ng-reflect-name="claimPostcode{i}"]', claim['postcode'])
                
            else:
                self.input_text(f'//*[@ng-reflect-name="claimDateMonth{i}"]', claim['month'])
                self.input_text(f'//*[@ng-reflect-name="claimDateYear{i}"]', claim['year'])
                self.input_text(f'//*[@ng-reflect-name="claimDescription{i}"]', claim['details'])
                self.input_text(f'//*[@ng-reflect-name="claimAmount{i}"]', claim['amount_of_loss'])



    def fill_page2(self):
        self.click_element(f'//*[@ng-reflect-name="displayInd{self.atm}"]')
        self.click_element(f'//*[@ng-reflect-name="claimsRequired{self.claim}"]')
        if len(claim_list) > 0:
            sleep(0.2)
            self.fill_claim()


    def fill_form(self):
        self.setup()
        self.fill_page1()
        sleep(0.4)
        self.fill_page2()
        sleep(1000)

#for claim type property and liability have fields (type, month, year, main_cause, amount_of_loss, postcode) and for claim type professionalIndemnity have fields (month, year, details, amount_of_loss)
#for now due to the error will assume that there is only one claim
claim_list = [
#    {
#        'type': 'property', #either property, liability, professionalIndemnity
#        'month': '01', #mm
#        'year': '2020', #yyyy              needs to be in the last five years
#        'main_cause': 'Falling Trees', #select from the dropdown, put exacltly as shown
#        'amount_of_loss': '1000',
#        'postcode': 'PO168UT'
#    },
    {
        'type': 'professionalIndemnity',
        'month': '01', #mm
        'year': '2020', #yyyy              needs to be in the last five years
        'details': 'broke a leg',
        'amount_of_loss': '2000',

    },
]

claims = PlumberForm('Plumber', 'no', 'yes', True, '2500', 'yes', 'yes', claim_list)
claims.fill_form()