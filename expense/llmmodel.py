from langchain_community.llms import Ollama
import json
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI




class LLMModel() :
    def __init__(self, username) :
        print("username: ", username)

        self.username = username
        prompt = PromptTemplate.from_template(""""
        Given a transaction sentence containing an expense record, I need assistance in categorizing each expense into its appropriate category and subcategory. Additionally, if there are any mentions of contributions, I require information about who contributed and how much they contributed. Please provide the necessary details in a clear text format.

        Transaction sentence: {expsentence}

        Categories and subcagegories are : [
            Food:

Groceries
Dining Out
Fast Food
Restaurants
Cafes
Takeout
Snacks
Beverages
Alcohol
Desserts
Transportation:

Public Transit
Gasoline
Rideshare
Taxi
Parking
Tolls
Vehicle Maintenance
Car Rental
Housing:

Rent
Mortgage
Utilities
Home Insurance
Property Taxes
Maintenance
Furniture
Appliances
Home Improvement
Utilities:

Electricity
Water
Gas
Internet
Phone
Cable
Healthcare:

Insurance
Doctor Visits
Prescriptions
Dental Care
Vision Care
Medical Supplies
Therapy
Gym Membership
Fitness Classes
Education:

Tuition
Books
School Supplies
Course Fees
Exam Fees
Tutoring
Educational Software
Workshops
Entertainment:

Movies
Concerts
Theater
Museums
Amusement Parks
Zoos
Sports Events
Video Streaming
Music Streaming
Clothing:

Clothes
Shoes
Accessories
Sportswear
Formal Wear
Underwear
Swimwear
Outerwear
Work Uniforms
Personal Care:

Haircuts
Salon Services
Skincare
Makeup
Manicure/Pedicure
Shaving Supplies
Hygiene Products
Grooming Tools
Spa Treatments
Gifts & Donations:

Gifts
Charitable Donations
Donation Drives
Crowdfunding Contributions
Volunteer Expenses
Greeting Cards
Special Occasions
Fundraising Events
Insurance:

Life Insurance
Health Insurance
Auto Insurance
Home Insurance
Renter's Insurance
Travel Insurance
Pet Insurance
Insurance Premiums
Insurance Claims
Taxes:

Income Tax
Property Tax
Sales Tax
Vehicle Tax
Capital Gains Tax
Tax Preparation Fees
Tax Deductions
Tax Refunds
Investments:

Stocks
Bonds
Mutual Funds
ETFs
Real Estate Investments
Retirement Accounts
Brokerage Fees
Investment Advice
Financial Planning Fees
        ]

        Instructions: 
        - Don't provide amount spent by person himself in contribution
        - Provide response in JSON format as {{
            "expenses": [{{
                    "category": {{write category amount here}},
                    "amount": {{write spent amount here}},
                    "subcategory": {{write subcategory amount here}},
                    "description": {{write description amount here}},
                    "transtype": {{Income or Expense}}
                }}]
            ,
            "contributions": [
                {{
                "{{contributor}}": {{contribution}},
            }},
        
            ]
        }}.
        - If a contribution is available, then respond with keys as the person's name and the value as their contribution.
        - If a contribution ratio is not given divide amount into all equally else divide in given ratio.
        """
        )
        


        api_key = ""

        model = ChatOpenAI(api_key = api_key )

        print("Hi 1")
        
        
        # model = Ollama(model="mistral", format="json")

        self.chain = LLMChain(llm=model, prompt=prompt)



    def __call__(self, expsentence) :
        print("expsentence = ", expsentence)
        response = self.chain.run(expsentence=expsentence, username=self.username)
        # print(response)
        # response = """{
        #     "expenses": [
        #     {
        #         "category": "Transportation",
        #         "amount": 1000,
        #         "subcategory": "Traveling",
        #         "description": "Traveling expense",
        #         "transtype": "Expense"
        #     }
        #     ],
        #     "contributions": [
        #     {
        #         "Pratham": 400,
        #         "Aditya": 600
        #     }
        #     ]
        # }"""

        return response
