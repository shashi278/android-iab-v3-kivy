from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout
from kivy.effects.dampedscroll import DampedScrollEffect

from kivymd.app import MDApp
from kivymd.uix.behaviors.elevation import RectangularElevationBehavior
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.label import MDLabel
import kivymd
from kivy.clock import Clock
from kivy.logger import Logger

from jnius import autoclass, cast
from android.runnable import run_on_ui_thread
from android import python_act as PythonActivity

from iabwrapper import BillingProcessor

Toast= autoclass('android.widget.Toast')
String = autoclass('java.lang.String')
CharSequence= autoclass('java.lang.CharSequence')
Activity = autoclass('android.app.Activity')

LayoutParams= autoclass('android.view.WindowManager$LayoutParams')
AndroidColor= autoclass('android.graphics.Color')
Configuration = autoclass('android.content.res.Configuration')

PROD_ONETIME  = "onetime"
PROD_CONSUME  = "consumable"
PROD_MONTHLY_1= "one_month"
PROD_ANNUAL_1 = "one_year"

products = [ PROD_ONETIME, PROD_CONSUME]
subscriptions = [ PROD_MONTHLY_1, PROD_ANNUAL_1]

LICENSE_KEY = ""

context= PythonActivity.mActivity

@run_on_ui_thread
def show_toast(text):
    text= cast(CharSequence, String(text))
    t= Toast.makeText(context, text, Toast.LENGTH_SHORT)
    t.show()

@run_on_ui_thread
def set_statusbar_color(color):
    window= context.getWindow()
    window.addFlags(LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
    window.setStatusBarColor(AndroidColor.parseColor(color))

kv="""
#:import get_color_from_hex kivy.utils.get_color_from_hex

RootClass:

    HomeScreen:

    PurchaseScreen:

<HomeScreen>:
    name: "homescreen"

    BoxLayout:
        orientation:"vertical"

        MDToolbar:
            title: "Billing App"
            elevation:10
            opposite_colos: True
            left_action_items: [['menu', lambda x: None]]
            right_action_items: [['cart-arrow-right', lambda x: app.go_forwards("purchasescreen")]]

        AnchorLayout:
            MDLabel:
                font_style: "H2"
                text: "Demo app for in-app billing in Kivy. v1.3.7"
                halign: "center"
                theme_text_color: "Custom"
                text_color: [.1,.1,.1,.3] if app.theme_cls.theme_style=="Light" else [.9, .9, .9,.3]

<PurchaseScreen>:
    name: "purchasescreen"
    BoxLayout:
        orientation:"vertical"

        MDToolbar:
            title: "Purchase Screen"
            elevation:9
            opposite_colos: True
            left_action_items: [['arrow-left', lambda x: app.go_backwards()]]
            right_action_items: [['information-outline', lambda x: None]]
        
        BoxLayout:
            ScrollView:
                bar_width:0
                do_scroll_x: False
                #scroll_y:0

                BoxLayout:
                    spacing: dp(8)
                    padding: dp(5)
                    size_hint_y: None
                    height: self.minimum_height
                    orientation: "vertical"

                    ProductCategoryLayout:
                        category_text: "Consumable"
                        
                        ProductLayout:
                            heading_text: "Gas (Play Billing Codelab)"
                            price_text: "10"
                            source: "buy.png"
                            description_text: "Buy gasoline to ride!"
                            product_id: "consumable"
                    
                    ProductCategoryLayout:
                        category_text: "One-time payment"
                        
                        ProductLayout:
                            heading_text: "Gas (Play Billing Codelab)"
                            price_text: "10"
                            source: "buy.png"
                            description_text: "Buy gasoline to ride!"
                            product_id: "onetime"
                            

                    ProductCategoryLayout:
                        category_text: "Monthly-Subscriptions"

                        ProductLayout:
                            heading_text: "Gas (Play Billing Codelab)"
                            price_text: "10"
                            source: "buy.png"
                            description_text: "Buy gasoline to ride!"
                            product_id: "one_month"
                        
                        ProductLayout:
                            heading_text: "Upgrade your car (Play Billing Codelab)"
                            price_text: "15"
                            source: "buy.png"
                            description_text: "Buy a premium outfit for your car!"
                            product_id: "one_month"
                        
                        ProductLayout:
                            heading_text: "Month in gold status (Play Billing Codelab)"
                            price_text: "$0.99"
                            source: "buy.png"
                            description_text: "Enjoy a gold status for a month!"
                            product_id: "one_month"
                    
                        
                    ProductCategoryLayout:
                        category_text: "Annual-Subscriptions"

                        ProductLayout:
                            heading_text: "Gas (Play Billing Codelab)"
                            price_text: "$0.99"
                            source: "buy.png"
                            description_text: "Buy gasoline to ride!"
                            product_id: "one_year"
                        
                        ProductLayout:
                            heading_text: "Year in gold status (Play Billing Codelab)"
                            price_text: "20"
                            source: "buy.png"
                            description_text: "Enjoy a gold status for a year!"
                            product_id: "one_year"


<ProductCategoryLayout@BoxLayout>:
    size_hint_y: None
    height: self.minimum_height
    category_text:""

    orientation: "vertical"
    spacing: 2

    #category area
    Category:
        text_: root.category_text

<Category>:
    canvas:
        Color:
            rgba: [1,1,1,1] if app.theme_cls.theme_style == "Light" else [0,0,0,1]
        Rectangle:
            pos: self.pos
            size: self.size
    text_: ""
    size_hint_y: None
    height: dp(30)
    Widget:
        size_hint_x: None
        width: dp(20)
    MDLabel:
        text: root.text_
        font_size: sp(15) 

<ProductLayout>:
    heading_text: ""
    price_text: ""
    source: ""
    description_text: ""

    product_id: ""

    canvas:
        Color:
            rgba: [1,1,1,1] if app.theme_cls.theme_style == "Light" else [0,0,0,1]
        Rectangle:
            pos: self.pos
            size: self.size

    size_hint_y: None
    height: dp(200)
    orientation: "vertical"

    #heading area
    BoxLayout:
        size_hint_y: 0.3
        
        #text heading
        BoxLayout:
            Widget:
                size_hint_x: None
                width: dp(20)
            MDLabel:
                text: root.heading_text
                bold: True

        #price text
        BoxLayout:
            size_hint_x:.3
            MDLabel:
                text: root.price_text
                bold: True
                halign: "right"
                # theme_text_color: "Custom"
                # text_color: [0,0,,1] if app.theme_cls.theme_style == "Light" else [1, 1, 1,.4]
        Widget:
            size_hint_x: None
            width: dp(20)
    
    #details area
    BoxLayout:
        size_hint_y: 0.3
        Widget:
            size_hint_x: None
            width: dp(20)

        #image area
        AnchorLayout:
            size_hint_x: None
            width: self.height
            BoxLayout:
                canvas:
                    Color:
                        rgba: 1,1,1,1
                    Ellipse:
                        size: self.size
                        pos: self.pos
                        source: root.source
        Widget:
            size_hint_x: None
            width: dp(10)

        #description text
        BoxLayout:
            #size_hint_x: 1
            MDLabel:
                text: root.description_text
                font_size: sp(15)
    
    #Button Area
    BoxLayout:
        size_hint_y: 0.4
        Widget:

        AnchorLayout:
            anchor_x: "right"
            MDRaisedButton:
                elevation_normal: 5
                text: "BUY"
                on_release:
                    #print(app)
                    app.open_payment_layout(root.product_id)
        
        Widget:
            size_hint_x: None
            width: dp(20)

<ListItemWithLabel>:
    on_release: app.initiate_purchase(self.method_name)
    recent: False
    source: ""
    method_name: ""
    right_label_text: "Recent" if self.recent else ""

    ImageLeftWidget:
        source: root.source
    
    RightLabel:
        text: root.right_label_text
        theme_text_color: "Custom"
        text_color: [0,0,0,.4] if app.theme_cls.theme_style == "Light" else [1, 1, 1,.4]
        font_size: sp(12)

<PaymentMethodLayout>:
    orientation: "vertical"
    size_hint_y: None
    height: "200dp"

    BoxLayout:
        size_hint_y: None
        height: dp(40)

        Widget:
            size_hint_x: None
            width: dp(20)
        MDLabel:
            text: "Select Payment Method"
            font_size: sp(14)
            bold: True
            theme_text_color: "Custom"
            text_color: [0,0,0,.5] if app.theme_cls.theme_style == "Light" else [1, 1, 1,.5]


    ScrollView:

        MDGridLayout:
            cols: 1
            adaptive_height: True

            ListItemWithLabel:
                source: "buy.png"
                text: "Google Play"
                method_name: "gplay"
                recent: True

            ListItemWithLabel:
                source: "buy.png"
                text: "BTC"
                method_name: "btc"
            
            ListItemWithLabel:
                source: "buy.png"
                text: "Some Other Method"
                method_name: "som"
            
            ListItemWithLabel:
                source: "buy.png"
                text: "One more method"
                method_name: "omm"
"""

class Category(BoxLayout, RectangularElevationBehavior):
    elevation_normal= .01

class ProductLayout(BoxLayout, RectangularElevationBehavior):
    elevation_normal= .01

class PaymentMethodLayout(BoxLayout):
    pass

class ListItemWithLabel(OneLineAvatarIconListItem):
    pass

class RightLabel(IRightBodyTouch, MDLabel):
    pass

class RootClass(ScreenManager):
    pass

class HomeScreen(Screen):
    pass

class PurchaseScreen(Screen):
    pass

class DemoApp(MDApp):
    screen_traversed= ["homescreen", ]

    def __init__(self, *args):
        self.root= RootClass()
        Window.bind(on_keyboard=self.back_btn)
        super().__init__(*args)
    
    def back_btn(self, window, key, *args):
        if key == 27:
            if len(self.screen_traversed)==1:
                return False
            self.go_backwards()
            return True
    
    def go_forwards(self, scrn):
        self.screen_traversed.append(scrn)
        self.root.transition= SlideTransition(direction="left")
        self.root.current= scrn
    
    def go_backwards(self):
        self.screen_traversed.pop()
        self.root.transition= SlideTransition(direction="right")
        self.root.current= self.screen_traversed[-1]
    
    def open_payment_layout(self, sku):
        if self.bp.is_purchased(sku):
            show_toast("Already Purchased")
            pi = self.bp.get_purchase_info(sku)
            details = {
                "responseData": pi.responseData,
                "signature": pi.signature,
                "purchaseData":{
                    "orderId": pi.purchaseData.orderId,
                    "productId": pi.purchaseData.productId,
                    "purchaseTime": pi.purchaseData.purchaseTime,
                    "purchaseToken": pi.purchaseData.purchaseToken,
                    "purchaseState": pi.purchaseData.purchaseState,
                    "autoRenewing": pi.purchaseData.autoRenewing,
                }
            }
            Logger.info(f"get_purchase_info: {details}")
            self.bp.consume_purchase_async(sku)
            return
        elif self.bp.is_subscribed(sku):
            show_toast("Already Subscribed")
            pi = self.bp.get_subscription_purchase_info(sku)
            details = {
                "responseData": pi.responseData,
                "signature": pi.signature,
                "purchaseData":{
                    "orderId": pi.purchaseData.orderId,
                    "productId": pi.purchaseData.productId,
                    "purchaseTime": pi.purchaseData.purchaseTime,
                    "purchaseToken": pi.purchaseData.purchaseToken,
                    "purchaseState": pi.purchaseData.purchaseState,
                    "autoRenewing": pi.purchaseData.autoRenewing,
                }
            }
            Logger.info(f"get_subscription_purchase_info: {details}")
            return
        pml= PaymentMethodLayout()
        self.product_id= sku
        self.custom_sheet= MDCustomBottomSheet(screen= pml)
        self.custom_sheet.open()
    
    def initiate_purchase(self, method_name):
        
        if method_name== "gplay":
            if self.product_id in products:
                # Get Details about a product
                self.bp.get_purchase_listing_async(self.product_id, self.purchase_details_received)
                self.bp.purchase_product(self.product_id)
            elif self.product_id in subscriptions:
                # Get Details about a subscription
                self.bp.get_subscription_listing_async(self.product_id, self.purchase_details_received)
                self.bp.subscribe_product(self.product_id)
            
        else:
            show_toast("Payment method not implemented")
    
    def on_start(self):
        primary_clr= self.theme_cls.primary_color
        hex_color= '#%02x%02x%02x' % (int(primary_clr[0]*200), int(primary_clr[1]*200), int(primary_clr[2]*200))
        set_statusbar_color(hex_color)

        Logger.info(f"is_initialized: {self.bp.is_initialized()}")
        Logger.info(f"is_iab_service_available: {self.bp.is_iab_service_available()}")
        Logger.info(f"is_subscription_update_supported: {self.bp.is_subscription_update_supported()}")

        # self.bp.load_owned_purchases_async()

        owned_products= self.bp.list_owned_products()
        owned_subscriptions= self.bp.list_owned_subscriptions()

        for product in owned_products:
            Logger.info(f"Product: {product}")

        for subscription in owned_subscriptions:
            Logger.info(f"Subscription: {subscription}")

    def build(self):
        self.bp = BillingProcessor(LICENSE_KEY, self.product_purchased, self.billing_error, onBillingInitializedMethod= self.billing_initialized)
        				
        return Builder.load_string(kv)
    
    def product_purchased(self, product_id, purchase_info):
        show_toast("Product purchased")
        self.custom_sheet.dismiss()
    
    def billing_error(self, error_code, error_message):
        show_toast("Billing error")
    
    def billing_initialized(self):
        show_toast("Billing initialized")
    
    def purchase_details_received(self, product_info):
        if product_info.size() != 0:
            product_info = product_info[0]
            details= {
                "productId": product_info.productId,
                "title": product_info.title,
                "description": product_info.description,
                "isSubscription": product_info.isSubscription,
                "currency": product_info.currency,
                "priceValue": product_info.priceValue,
                "priceText": product_info.priceText,
            }
            Logger.info(details)
            show_toast(f"Purchase details received {details}")
        else:
            show_toast("No purchase details received")
    

if __name__ == "__main__":
    DemoApp().run()
