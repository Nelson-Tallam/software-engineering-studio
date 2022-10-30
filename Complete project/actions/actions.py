# from actions import Event_name
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import smtplib
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email import message
import qrcode
from fpdf import FPDF
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Dict, Text, List, Optional, Any
import mysql.connector
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet ,UserUtteranceReverted , EventType
mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="chatbot"
)
mycursor= mydb.cursor()
class ActionOrganizeDetails(Action):
    
    def name(self) -> Text:
        return "organize_event_form"

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        required_slots=['TIME','GPE','DATE']
        for slot_name in required_slots:
            if(tracker.slots.get(slot_name)) is None:
                # The slots are not yet filled
                return[SlotSet("requested_slot",slot_name)]
                      
            else:
                # All slots are filled
                          
                return[SlotSet("requested_slot",None)]
class GetEventDetails(Action):
    def name(self) ->Text:
        return "all_slot_values"
    def run(self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker, 
        domain: "DomainDict") -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_details_organize_thanks",
                                LOCATION=tracker.get_slot("GPE"),
                                Time=tracker.slots.get("TIME"), 
                                DATE=tracker.get_slot("DATE"),
                                 
                                
                                 )
class AllDatabaseOperations(Action):
    def name(self)->Text:
        return "database_operations"
    def run(self,
            dispatcher: "CollectingDispatcher", 
            tracker: Tracker, 
            domain: "DomainDict") -> List[Dict[Text, Any]]:
        # Event_name=tracker.latest_message['text']
        # Event_name=Event_name.strip('The event is called ')
        Event_name=tracker.get_slot("the_event_name")
        Event_name=Event_name.replace('The event is called ','')
        print(Event_name)
        Time=tracker.get_slot("TIME")
        Location=tracker.get_slot("GPE")
        Dates=tracker.get_slot("DATE")
        type=tracker.get_intent_of_latest_message()
        
        if type=='organize_seminar':
            try:
                sql='INSERT INTO seminars(Name,venue,Date,Time) VALUES("{0}","{1}","{2}","{3}");'.format(Event_name,Location,Dates,Time)
                mycursor.execute(sql)
                mydb.commit()
                dispatcher.utter_message(template="utter_details_organize_thanks",
                                    Event_Name=Event_name,
                                    LOCATION=tracker.get_slot("GPE"),
                                    Time=tracker.slots.get("TIME"), 
                                    DATE=tracker.get_slot("DATE"),
                )
            except mysql.connector.Error as err :
                print("There was an error performing the query 1:" ,err)
        elif type=='organize_business_event' :
            try: 
                    
                sql='INSERT INTO business(Name,venue,Date,Time) VALUES("{0}","{1}","{2}","{3}");'.format(Event_name,Location,Dates,Time)
                mycursor.execute(sql)
                mydb.commit()
                dispatcher.utter_message(template="utter_details_organize_thanks",
                                    Event_Name=Event_name,
                                    LOCATION=tracker.get_slot("GPE"),
                                    Time=tracker.slots.get("TIME"), 
                                    DATE=tracker.get_slot("DATE"),
                )
            except mysql.connector.Error as err :
                print("There was an error performing the query:" ,err)
        elif type=='organize_corporate_event':
            try:
                
                sql='INSERT INTO corporate(Name,venue,Date,Time) VALUES("{0}","{1}","{2}","{3}");'.format(Event_name,Location,Dates,Time)
                mycursor.execute(sql)
                mydb.commit()
                dispatcher.utter_message(template="utter_details_organize_thanks",
                                    Event_Name=Event_name,
                                    LOCATION=tracker.get_slot("GPE"),
                                    Time=tracker.slots.get("TIME"), 
                                    DATE=tracker.get_slot("DATE"),
                ) 
            except mysql.connector.Error as err :
                print("There was an error performing the query:" ,err)
        elif type=='organize_private_event':
            try: 
                sql='INSERT INTO private(Name,venue,Date,Time) VALUES("{0}","{1}","{2}","{3}");'.format(Event_name,Location,Dates,Time)
                mycursor.execute(sql)
                mydb.commit()
                dispatcher.utter_message(template="utter_details_organize_thanks",
                                    Event_Name=Event_name,
                                    LOCATION=tracker.get_slot("GPE"),
                                    Time=tracker.slots.get("TIME"), 
                                    DATE=tracker.get_slot("DATE"),
                ) 
            except mysql.connector.Error as err :
                print("There was an error performing the query:" ,err)
        else:
            try:
                sql='INSERT INTO any_other(Name,venue,Date,Time) VALUES("{0}","{1}","{2}","{3}");'.format(Event_name,Location,Dates,Time)
                mycursor.execute(sql)
                mydb.commit()
                dispatcher.utter_message(template="utter_details_organize_thanks",
                                    Event_Name=Event_name,
                                    LOCATION=tracker.get_slot("GPE"),
                                    Time=tracker.slots.get("TIME"), 
                                    DATE=tracker.get_slot("DATE"),
                )
            except mysql.connector.Error as err :
                print("There was an error performing the query :" ,err)
        
class ActionOrganizeDetails(Action):
    
    def name(self) -> Text:
        return "available_merchandise"

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        information=tracker.get_intent_of_latest_message()            
        if information =='inform_looking_for_tents':
            try:
                text="SELECT * from tents"
                mycursor.execute(text)
                myresult=mycursor.fetchall()
                for row in myresult:
                    Numbers=row[0]
                    Email=row[1]
                    
                    details=("We have an advertiser advertising %d tents.You can contact him  on %s" % (Numbers , Email))
                    response=""" {}.""".format(details)
                    dispatcher.utter_message(response)
                # mydb.close()
            except mysql.connector.Error as err :
                print("There was an Error performing the query:" ,err)
            # mydb.close()
        else:
            try:
                text="SELECT * from chairs"
                mycursor.execute(text)
                myresult=mycursor.fetchall()
                for row in myresult:
                    Numbers=row[0]
                    Email=row[1]
                    
                    details=("We have an advertiser advertising %d chairs.You can contact him  on %s" % (Numbers , Email))
                    response=""" {}.""".format(details)
                    dispatcher.utter_message(response)
            except:
                print("There is an Error doing the query")
class GetDetails(Action):
    def name(self) -> Text:
        return "event_name_form"
    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        required_slots=['the_event_name']
        for slot_name in required_slots:
            if(tracker.slots.get(slot_name)) is None:
                # The slots are not yet filled
                return[SlotSet("requested_slot",slot_name)]
                      
            else:
                # All slots are filled
                          
                return[SlotSet("requested_slot",None)]
class ActionScrap(Action):
    
    def name(self) -> Text:
        return "action_look_for_event"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #get user input from user
        destination=tracker.latest_message['text']
        if 'corporate' in destination:
            search='https://www.eventbrite.com/d/kenya--nairobi/business--events/corporate/'
        elif 'business' in destination:
            search='https://www.eventbrite.com/d/kenya--nairobi/business--events/'
        elif 'private' in destination:
            search='https://www.eventbrite.com/d/kenya/private/' 
        elif 'online' in destination:
            search='https://www.eventbrite.com/d/online/all-events/' 
        elif 'seminars' in destination:
            search='https://www.eventbrite.com/d/kenya--nairobi/seminars/'
        else:
            search='https://www.eventbrite.com/d/kenya--nairobi/top-events/'
        print(f'Looking for {destination}')
        html_text=requests.get(search).text
        soup= BeautifulSoup(html_text,'lxml')
        #print(soup)
        jobs=soup.find_all('div',class_='search-event-card-wrapper')
        with open('jobs.csv','w',newline='',encoding='utf8') as f:
            thewriter= csv.writer(f)
            header=['Name','Link','Location','Time']
            thewriter.writerow(header)
            for job in jobs:
                title=job.find('div',class_='eds-is-hidden-accessible').text
                more_info=job.find('div',class_='eds-event-card-content__primary-content')
                links=more_info.a['href']
                time=job.find('div',class_='eds-event-card-content__sub-title eds-text-color--ui-orange eds-l-pad-bot-1 eds-l-pad-top-2 eds-text-weight--heavy eds-text-bm')
                timing=time.text
                location= job.find('div',class_='card-text--truncated__one').text
                # print(location.text)
                # print(timing)
                jobinfo=[title,links,location,timing]
                thewriter.writerow(jobinfo)
                print(f'''
            The event available is : {title}
            The link is : {links}
            The location is {location}
            The Time is {timing}''')
        df=pd.read_csv('jobs.csv')
        for i,j in df.iterrows():
            dispatcher.utter_message(text=j['Name'] + " \n" + str(j['Link']) + " \n" + str(j['Location']))

        #dispatcher.utter_message(text="Hello World!")
        dispatcher.utter_message(text="We hope that helped 😊")
        

        return []
class GetEventsFromDb(Action):
    def name(self)->Text:
        return "get_event_fromdb"
    def run(self, 
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain:Dict) -> List[EventType]:
        destination=tracker.latest_message['text']
        if destination== 'private':
            try:
                text="SELECT * from private"
                mycursor.execute(text)
                myresult=mycursor.fetchall()
                for row in myresult:
                    Venue=row[0]
                    Time=row[1]
                    Date=row[2]
                    details=("This event will be held in %s on %s at %s" % (Venue , Date ,Time))
                    response="""The details of the event are \n {}.""".format(details)
                    dispatcher.utter_message(response)
            except:
                print("There is an Error doing the query")
            # mydb.close()
        elif destination== 'corporate':
            try:
                text="SELECT * from corporate"
                mycursor.execute(text)
                myresult=mycursor.fetchall()
                for row in myresult:
                    Name=row[0]
                    Venue=row[1]
                    Time=row[2]
                    Date=row[3]
                    details=("This event %s will be held in %s on %s at %s" % (Name ,Venue , Date ,Time))
                    response="""The details of the event are \n {}.""".format(details)
                    dispatcher.utter_message(response)
            except:
                print("There is an Error doing the query")
            # mydb.close()
        elif destination== 'seminar':
            try:
                text="SELECT * from seminars"
                mycursor.execute(text)
                myresult=mycursor.fetchall()
                for row in myresult:
                    Name=row[0]
                    Venue=row[1]
                    Time=row[2]
                    Date=row[3]
                    details=("This event %s will be held in %s on %s at %s" % (Name ,Venue , Date ,Time))
                    response="""The details of the event are \n {}.""".format(details)
                    dispatcher.utter_message(response)
            except mysql.connector.Error as err:
                print("There is an Error doing the query:" ,err)
            # mydb.close()
        elif destination== 'business':
            try:
                text="SELECT * from business"
                mycursor.execute(text)
                myresult=mycursor.fetchall()
                for row in myresult:
                    Name=row[0]
                    Venue=row[1]
                    Time=row[2]
                    Date=row[3]
                    details=("This event %s will be held in %s on %s at %s" % (Name ,Venue , Date ,Time))
                    response="""The details of the event are \n {}.""".format(details)
                    dispatcher.utter_message(response)
            except:
                print("There is an Error doing the query")
                
            # mydb.close()
        elif destination== 'corporate':
            try:
                text="SELECT * from corporate"
                mycursor.execute(text)
                myresult=mycursor.fetchall()
                for row in myresult:
                    Name=row[0]
                    Venue=row[1]
                    Time=row[2]
                    Date=row[3]
                    details=("This event %s will be held in %s on %s at %s" % (Name ,Venue , Date ,Time))
                    response="""The details of the event are \n {}.""".format(details)
                    dispatcher.utter_message(response)
            except:
                print("There is an Error doing the query")
            # mydb.close()
        else:
            try:
                text="SELECT * from any_other"
                mycursor.execute(text)
                myresult=mycursor.fetchall()
                for row in myresult:
                    Name=row[0]
                    Venue=row[1]
                    Time=row[2]
                    Date=row[3]
                    details=("This event %s will be held in %s on %s at %s" % (Name ,Venue , Date ,Time))
                    response="""The details of the event are \n {}.""".format(details)
                    dispatcher.utter_message(response)
            except:
                print("There is an Error doing the query")
class pdfDocument(Action,FPDF):
    
    def name(self) ->Text:
        return "send_mail"
    def run(self, 
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict") -> List[Dict[Text, Any]]:  
        Event_name=tracker.latest_message['text']
        Event_name=Event_name.replace('Send me the ticket for the event called ', '')
        
        Email=tracker.get_slot('email')
        Person_name=tracker.get_slot('PERSON') 
        qr=qrcode.QRCode(
        version=1, #size of the qrcode
        box_size=15,
        border=5
        )  
        data=Event_name +"\n" + Email +"\n"+ Person_name
        qr.add_data(data)
        qr.make(fit=True)
        img=qr.make_image(fill='black',back_color='white')
        try:
            img.save('Event QR Code.png')
        except:
            print("An exception occured")
        pdf=FPDF('P','mm','Letter')
        pdf.add_page()
        pdf.set_font('helvetica','',16)
        pdf.image('Event QR Code.png',10,8,25)
        pdf.ln(20)
        Event_details='This is your ticket for  %s '% (Event_name)
        
        pdf.cell(40,10,Event_details)
        
        try:
            pdf.output('Yourticket.pdf')
        except:
            print("Terrible error")
        server = smtplib.SMTP_SSL("smtp.gmail.com",465)
        server.login("egachomba99@gmail.com","eric@gachomba")
        first_email ="egachomba99@gmail.com"
        second_email=Email
        subject="This is your ticket"
        content="You are receiving your tickets"
        msg= MIMEMultipart()
        msg['From']=first_email
        msg['To']= second_email
        msg['Subject']= subject
        body= MIMEText(content,'plain')
        msg.attach(body)
        filename='Yourticket.pdf'
        with open(filename,'rb') as f:
            attachment= MIMEApplication(f.read(),Name=basename(filename))
            attachment['Content-Disposition']= 'attachment;filename="{}"'.format(basename(filename))
        
        msg.attach(attachment)
        server.send_message(msg,from_addr=first_email,to_addrs=[second_email])
        server.quit()
        dispatcher.utter_message(text='Please Check your email inbox')
ADVERTISING=['chairs','tents','soundsystems']




class ValidateAdvertisingForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_advertising_form"

    def validate_merchandise(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
        )->Dict[Text,Any]:
        """ Validate `merchandise` value"""
        if slot_value.lower() not in ADVERTISING:
            dispatcher.utter_message(text=f"We currently only advertise : soundsystems , tents ,chairs .")
            return {"merchandise": None}
        dispatcher.utter_message(text=f"OK!You want to have advertise {slot_value}")
        return{"merchandise":slot_value}
    
    def validate_numbering(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
        )->Dict[Text,Any]:
        """ Validate `numbering` value"""
        if isinstance(slot_value ,int):
            dispatcher.utter_message(text=f"OK!You are advertising {slot_value}")
            return{"numbering":slot_value}
        else:    
            dispatcher.utter_message(text=f"Please enter a valid number")
            return {"numbering": None}
    
    
class ValidateRestaurantForm(Action):
    def name(self)->Text:
        return "user_details_form"
    def run(self, 
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain:Dict) -> List[EventType]:
        
        required_slots=["merchandise","numbering"]
        
        for slot_name in required_slots:
            if(tracker.slots.get(slot_name)) is None:
                # The slots are not yet filled
                return[SlotSet("requested_slot",slot_name)]
                      
            else:
                # All slots are filled
                          
                return[SlotSet("requested_slot",None)]
class ActionSubmit(Action):
    def name(self) ->Text:
        return "action_submit"
    def run(self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker, 
        domain: "DomainDict") -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_details_thanks",
                                 Merchandise=tracker.slots.get("merchandise"), 
                                 Numbering=tracker.get_slot("numbering"),
                                
                                 )
        
class ValidateEmailForm(Action):
    def name(self)->Text:
        return "user_email_form"
    def run(self, 
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain:Dict) -> List[EventType]:
        
        required_slots=["email"]
        
        for slot_name in required_slots:
            if(tracker.slots.get(slot_name)) is None:
                # The slots are not yet filled
                return[SlotSet("requested_slot",slot_name)]
                      
            else:
                # All slots are filled
                          
                return[SlotSet("requested_slot",None)]       
        

  #                               )
class ActionSubmitEmail(Action):
    def name(self) ->Text:
        return "action_submit_email"
    def run(self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker, 
        domain: "DomainDict") -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_details_email",
                                #  Merchandise=tracker.slots.get("merchandise"), 
                                 Email=tracker.get_slot("email"),
                                
                                 )
           
class ActionGiveDetails(Action):
    def name(self) ->Text:
        return "action_submit_adverts"
    def run(self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker, 
        domain: "DomainDict") -> List[Dict[Text, Any]]:
        Email=tracker.get_slot('email')
        Numbering=tracker.get_slot('numbering')
        merchandise=tracker.get_slot('merchandise')
        if 'tent' in merchandise:
            sql='INSERT INTO tents(Numbers,Email) VALUES("{0}","{1}");'.format(Numbering,Email)
            mycursor.execute(sql)
            mydb.commit()
        else:
            sql='INSERT INTO chairs(Numbers,Email) VALUES("{0}","{1}");'.format(Numbering,Email)
            mycursor.execute(sql)
            mydb.commit()
     
