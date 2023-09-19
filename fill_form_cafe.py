from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from operations import Operations


class CafeForm(Operations):
    def __init__(self, 
                 trade: str,
                 own_premises: str,
                 assumptions: str,
                 content_cover: str | None,
                 stock_cover: str | None,
                 temperature_ctrl_stock: str | None,
                 transit_stock: str | None,
                 building_cover: str | None,
                 employer_liability: bool,
                 electronic_equipment: str | None,
                 alcohol_loss: str | None,



                 atm: str,
                 claim: str,
                 claim_list: list,
                 ):
        self.trade = trade
        self.own_premises = own_premises.capitalize()
        self.assumptions = assumptions.capitalize()
        self.content_cover = content_cover
        self.stock_cover = stock_cover
        self.temperature_ctrl_stock = temperature_ctrl_stock
        self.transit_stock = transit_stock
        self.building_cover = building_cover
        self.employer_liability = employer_liability
        self.electronic_equipment = electronic_equipment
        self.alcohol_loss = alcohol_loss



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

        if self.content_cover:
            self.click_element('//*[@ng-reflect-name="contentsCoverSelection"]')
            self.input_text('//*[@ng-reflect-name="contentsCoverAmount"]', self.content_cover)

        if self.stock_cover:
            self.click_element('//*[@ng-reflect-name="stockCoverSelection"]')
            self.input_text('//*[@id="stockCoverAmount"]', self.stock_cover)

        if self.temperature_ctrl_stock:
            self.click_element('//*[@ng-reflect-name="temperatureControlledCoverSele"]')
            self.input_text('//*[@ng-reflect-name="temperatureControlledCoverAmou"]', self.temperature_ctrl_stock)
        
        if self.transit_stock:
            self.click_element('//*[@ng-reflect-name="stockInTransitSelection"]')
            sleep(0.1)
            self.click_element(f'//*[@ng-reflect-name="stockInTransitCoverAmount{self.transit_stock}"]')
        
        if self.building_cover:
            self.click_element('//*[@ng-reflect-name="buildingCoverSelection"]')
            self.input_text('//*[@id="buildingCoverAmount"]', self.temperature_ctrl_stock)
        
        if self.employer_liability:
            self.click_element('//*[@ng-reflect-name="employersLiabilitySelection"]')

        if self.electronic_equipment:
            self.click_element('//*[@ng-reflect-name="electronicEquipmentCoverSelect"]')
            self.input_text('//*[@id="electronicEquipmentCoverAmount"]', self.electronic_equipment)
        
        if self.alcohol_loss:
            self.click_element('//*[@ng-reflect-name="lossOfAlcoholSelection"]')
            self.click_element(f'//*[@id="lossOfAlcoholCoverAmount{self.alcohol_loss}"]')
            
        
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
        #self.fill_page2()
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

form = CafeForm(
    trade = 'Cafe',
    own_premises = 'yes',
    assumptions = 'yes',
    content_cover = '2000',
    stock_cover = '2000',
    temperature_ctrl_stock = '2000',
    transit_stock = '2500',
    building_cover= '2000',
    employer_liability = True,
    electronic_equipment = '2000',
    alcohol_loss = '2500',
    atm = 'yes',
    claim = 'no',
    claim_list = {},
)
form.fill_form()