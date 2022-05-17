# # This files contains your custom actions which can be used to run
# # custom Python code.
# #
# # See this guide on how to implement these action:
# # https://rasa.com/docs/rasa/custom-actions


# # This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
# #
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher


# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         # listDrinks = []
#         # listDrinks.append(tracker.get_slot("drinks"))
#         # listBakery = []
#         # listBakery.append(tracker.get_slot("bakery"))
#         # listnumber = []
#         # listnumber.append(tracker.get_slot("drinks"))
#         # for x in listBakery:

#         dispatcher.utter_message(text="You want,"+)

#         return []
import json
from pathlib import Path
from typing import Any, Text, Dict, List


from rasa_sdk import Action, FormValidationAction, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict 

global nameDrink


# class ActionDrinksOrder(Action):

#     def name(self) -> Text:
#         return "action_drinks_order"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         nameDrink = ""
#         for blob in tracker.latest_message['entities']:
#             print(tracker.latest_message)
#             if blob['entity'] == 'drinks':
#                 nameDrink = blob['value']
#                 # dispatcher.utter_message(
#                 #     text="You have order: {}.".format(name))
#         return []


# orders list which contain all customer orders 
orders={"drinks":{"small":{},"medium":{},"large":{}},"bakery":{}}

#Has all items in menu and with prices 
menu={
    "drinks":{
        #small size price
        "small":{
            "black coffee":10,
            "latte":15,
            "iced latte":15,
            "iced coffee":14,
            "cappuccino":12
         }
         ,
         #medium size price
         "medium":{
            "black coffee":15,
            "latte":20,
            "iced latte":20,
            "iced coffee":19,
            "cappuccino":17
         }
         ,
         #large size price
         "large":{
            "black coffee":20,
            "latte":25,
            "iced latte":25,
            "iced coffee":24,
            "cappuccino":22
         }
    }
    ,
    "bakery":{
        #cookie  price
        "cookie": 10
         ,
         #croissant  price
         "croissant":15
         ,
         #begal  price
         "begal":20
         ,
         #donut  price
         "donut":5
    }

}

# add order method
def order_add(category,item,amount,size):
    global orders
    if amount==0:
        amount=1
    # drink case
    if category =="drinks":
        #check in the size lits
        if(size=="small"):
            if item in orders["drinks"]["small"].keys():
                # if it is already there grab it and add new amount to it 
                previous_amount=orders["drinks"]["small"][item]
                amount+=previous_amount
                orders["drinks"]["small"][item]=amount
            else:
                #First time ordered 
                orders["drinks"]["small"][item]=amount
        elif(size=="medium"):
            if item in orders["drinks"]["medium"].keys():
                # if it is already there grab it and add new amount to it 
                previous_amount=orders["drinks"]["medium"][item]
                amount+=previous_amount
                orders["drinks"]["medium"][item]=amount
            else:
                #First time ordered 
                orders["drinks"]["medium"][item]=amount        
        elif(size=="large"):
            if item in orders["drinks"]["large"].keys():
                # if it is already there grab it and add new amount to it 
                previous_amount=orders["drinks"]["large"][item]
                amount+=previous_amount
                orders["drinks"]["large"][item]=amount
            else:
                #First time ordered 
                orders["drinks"]["large"][item]=amount 

    ## for bakery items 
    if category =="bakery":
        #check if it is there 
        if item in orders["bakery"].keys():
             # if it is already there grab it and add new amount to it 
            previous_amount=orders["bakery"][item]
            amount+=previous_amount
            orders["bakery"][item]=amount
        else:
            #First time ordered 
            orders["bakery"][item]=amount

# remove order method 
def order_remove(category,item,amount,size):
    global orders
    if amount==0:
        return None
        # drink case
    else:
            if category =="drinks":
                #check in the size lits
                if(size=="small"):
                    if item in orders["drinks"]["small"].keys():
                        # if it is already there grab it and add new amount to it 
                        previous_amount=orders["drinks"]["small"][item]
                        previous_amount-=amount
                        if (previous_amount<=0):
                            #if it is set to be zero or - negative number remove it 
                            orders['drinks']['small'].pop(item)
                        else:
                            orders["drinks"]["small"][item]=previous_amount

                elif(size=="medium"):
                    if item in orders["drinks"]["medium"].keys():
                        # if it is already there grab it and add new amount to it 
                        previous_amount=orders["drinks"]["medium"][item]
                        previous_amount-=amount
                        if (previous_amount<=0):
                            #if it is set to be zero or - negative number remove it 
                            orders['drinks']['medium'].pop(item)
                        else:
                            orders["drinks"]["medium"][item]=previous_amount        
                elif(size=="large"):
                    if item in orders["drinks"]["large"].keys():
                        # if it is already there grab it and add new amount to it 
                        previous_amount=orders["drinks"]["large"][item]
                        previous_amount-=amount
                        if (previous_amount<=0):
                            #if it is set to be zero or - negative number remove it 
                            orders['drinks']['large'].pop(item)
                        else:
                            orders["drinks"]["large"][item]=previous_amount
            ## for bakery items 
            if category =="bakery":
                #check if it is there 
                if item in orders["bakery"].keys():
                    # if it is already there grab it and add new amount to it 
                    previous_amount=orders["bakery"][item]
                    previous_amount-=amount
                    if (previous_amount<=0):
                        orders['drinks'].pop(item)       
                    else:
                        orders["bakery"][item]=previous_amount
                # else:
                #     #First time ordered 
                #     orders["bakery"][item]=amount

#calculate bill 
def calculate_bill():
    global orders
    bill_list=[]
    cost=0
    for category in orders.keys():
        if category=="drinks":
            for size,items in orders["drinks"].items():
                for item,value in items.items():
                    #seeing item price in menu 
                    for category_menu in menu.keys():
                        if category_menu=="drinks":
                            for size_menu,items_menu in menu["drinks"].items():
                              if (size_menu==size):
                                for item_menu,value_menu in items_menu.items():
                                  if(item_menu==item):
                                    description=str(item)+" # "+str(value)+" price per item: "+str(value_menu)+" total with  "+str(((value*value_menu)))
                                    #adding it to the main bill
                                    bill_list.append(description)
                                    #adding over all cost
                                    cost+=((value*value_menu))
                                
                                    
        else:
            for item,value in orders["bakery"].items():
              for item_menu,value_menu in menu["bakery"].items():
                              if(item_menu==item):
                                    description=str(item)+" # "+str(value)+" price per item: "+str(value_menu)+" total with  "+str(((value*value_menu)))
                                    #adding it to the main bill
                                    bill_list.append(description)
                                    #adding over all cost
                                    cost+=((value*value_menu))
    #return the bill to be
    cost=cost+(cost*0.15)
    bill="Thanks for buying\nYour have ordered the following\n"
    for record in  bill_list:
      bill+= record+"\n"

    
    bill+="***** Your total bill with tax amount is (" +str(cost) +" SAR) *****"                          
    return bill
 
                                    
# used to convert words to number (five --> 5) in order to calculate
from word2number import w2n       
#adding 
# add bakery order
class ActionBakeryOrder(Action):

    def name(self) -> Text:
        return "action_bakery_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            item=tracker.get_slot('bakery')
            number_str=tracker.get_slot('number')
            number_str=str(number_str)
            number=w2n.word_to_num(number_str)
            order_add("bakery",item,number,0)
            
           
            dispatcher.utter_message(
                    text="You have order: {} of {}.".format(number,item))
            
            return [SlotSet("bakery",None),
            SlotSet("number","one")]

#add drinks order 
class ActionDrinksOrder(Action):

    def name(self) -> Text:
        return "action_drinks_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            item=tracker.get_slot('drinks')
            number_str=tracker.get_slot('number')
            number_str=str(number_str)
            number=w2n.word_to_num(number_str)
            size=tracker.get_slot('size')
            order_add("drinks",item,number,size)
            
           
            dispatcher.utter_message(
                    text="You have order: {} # {} of size {}.".format(item,number,size))
                          
            return [SlotSet("drinks",None),
            SlotSet("number","one"),
            SlotSet("size",None) ]



# removing orders

#bakery remove
class ActionBakeryRemoveOrder(Action):

    def name(self) -> Text:
        return "action_bakery_remove"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            item=tracker.get_slot('bakery')
            number_str=tracker.get_slot('number')
            number_str=str(number_str)
            number=w2n.word_to_num(number_str)
            order_remove("bakery",item,number,0)
            
           
            dispatcher.utter_message(
                    text="You have removed: {} of {}.".format(number,item))
            
            return [SlotSet("bakery",None),
            SlotSet("number","one")]

#drinks remove
class ActionDrinksRemoveOrder(Action):

    def name(self) -> Text:
        return "action_drinks_remove"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            item=tracker.get_slot('drinks')
            number_str=tracker.get_slot('number')
            number_str=str(number_str)
            number=w2n.word_to_num(number_str)
            size=tracker.get_slot('size')
            order_remove("drinks",item,number,size)
            
           
            dispatcher.utter_message(
                    text="You have removed: {} # {} of size {}.".format(item,number,size))
                          
            return [SlotSet("drinks",None),
            SlotSet("number","one"),
            SlotSet("size",None) ]

#remove all orders 
class ActionRemoveAllOrder(Action):

    def name(self) -> Text:
        return "action_remove_all"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            resetOrders()           
            dispatcher.utter_message(
                    text="You have removed all orders .")
                          
            return [SlotSet("drinks",None),
            SlotSet("number","one"),
            SlotSet("size",None) ]

#restOrders
def resetOrders():
    global orders
    orders = {"drinks":{"small":{},"medium":{},"large":{}},"bakery":{}}

#checkout 
class ActionCheckOut(Action):

    def name(self) -> Text:
        return "action_checkout"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            bill =calculate_bill()
            dispatcher.utter_message(
                    text="{}".format(bill))
            #SlotSet("bill",bill)
            return []



import random
#print suggestions 
class ActionSuggestions(Action):

    def name(self) -> Text:
        return "action_suggestion"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            drinks_list=['black coffee','latte','iced latte','iced coffee','cappuccino']
            bakery_list=['cookie','croissant','begal','donut']
            suggested=random.choice(bakery_list)+" with "+ random.choice(drinks_list)
            dispatcher.utter_message(
                    text="You can have {}".format(suggested))
            #SlotSet("bill",bill)
            return []


#print menu list 
class ActionMenuList(Action):

    def name(self) -> Text:
        return "action_display_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            menu_list=[]
            menu_list.append("\nDrinks\n")
            for size,items in menu['drinks'].items():
                menu_list.append("\n"+str(size )+"\n")
                for item, price in items.items():
                    menu_item=str(size)+" "+str(item)+" price: "+str(price)+" SAR"
                    menu_list.append(menu_item)


                    
            menu_list.append("\nBakery\n")
            for item,price in menu['bakery'].items():
                    menu_item=str(item)+" price: "+str(price)+" SAR"
                    menu_list.append(menu_item)

            menu_items=""
            for record in menu_list:
                menu_items+= record+"\n"
            dispatcher.utter_message(
                    text="The Menu of the coffee shop \n {}".format(menu_items))
            #SlotSet("bill",bill)
            return []


ALLOWED_Drinks_SIZES = ["small", "medium", "large", "s", "m", "l"]
ALLOWED_Drinks_TYPES = ["black coffee", "latte", "iced latte", "iced coffee", "cappuccino"]
#validate drinks add
class ValidateSimpleDrinksForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_drinks_form"

    def validate_size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `size` value."""

        if tracker.get_slot('size') not in ALLOWED_Drinks_SIZES:
            #dispatcher.utter_message(text=f"We only accept pizza sizes: Small/Medium/Large .")
            return {"size": None} # we did not validate the value user gave us 
        #dispatcher.utter_message(text=f"OK! You want to have a {slot_value} drink.")
        return {"size": slot_value}

    def validate_drinks(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `drinks` value."""

        if tracker.get_slot('drinks') not in ALLOWED_Drinks_TYPES:
            #dispatcher.utter_message(text="Hello form other world ")
            return {"drinks": None}
        #dispatcher.utter_message(text=f"OK! You want to have a {slot_value} .")
        return {"drinks": slot_value}


#validate drinks remove 
class ValidateSimpleDrinksRemoveForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_drinks_remove_form"

    def validate_size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `size` value."""

        if tracker.get_slot('size') not in ALLOWED_Drinks_SIZES:
            dispatcher.utter_message(text=f"Size allocation probelm")
            return {"size": None} # we did not validate the value user gave us 
        #dispatcher.utter_message(text=f"OK! You want to have a {slot_value} drink.")
        return {"size": slot_value}

    def validate_drinks(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `drinks` value."""

        if tracker.get_slot('drinks') not in ALLOWED_Drinks_TYPES:
            dispatcher.utter_message(text=f"Drinks allocation probelm")
            return {"drinks": None}
        #dispatcher.utter_message(text=f"OK! You want to have a {slot_value} .")
        return {"drinks": slot_value}




ALLOWED_Bakery_TYPES = ["donut", "begal", "croissant", "cookie"]
#validate bakery add
class ValidateSimpleBakeryForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_bakery_form"
    def validate_bakery(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `bakery` value."""

        if tracker.get_slot('bakery') not in ALLOWED_Bakery_TYPES:
            #dispatcher.utter_message(text=f"I don't recognize that pizza. We serve {'/'.join(ALLOWED_Bakery_TYPES)}.")
            return {"bakery": None}
        #dispatcher.utter_message(text=f"OK! You want to have a {slot_value} .")
        return {"bakery": slot_value}


#validate bakery remove
class ValidateSimpleBakeryRemoveForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_bakery_remove_form"
    def validate_bakery(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `bakery` value."""

        if tracker.get_slot('bakery') not in ALLOWED_Bakery_TYPES:
            #dispatcher.utter_message(text=f"I don't recognize that pizza. We serve {'/'.join(ALLOWED_Bakery_TYPES)}.")
            return {"bakery": None}
        #dispatcher.utter_message(text=f"OK! You want to have a {slot_value} .")
        return {"bakery": slot_value}























# class ActionActionSize(Action):

#     def name(self) -> Text:
#         return "action_size"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         for blob in tracker.latest_message['entities']:
#             print(tracker.latest_message)
#             if blob['entity'] == 'size':
#                 name = blob['value']
#                 dispatcher.utter_message(
#                     text="The size of your order is: {}: {}.".format(name, nameDrink))
#         return []


# class MyKnowledgeBaseAction(ActionQueryKnowledgeBase):
#     def __init__(self):
#         knowledge_base = InMemoryKnowledgeBase("data/pokemondb.json")
#         super().__init__(knowledge_base)
