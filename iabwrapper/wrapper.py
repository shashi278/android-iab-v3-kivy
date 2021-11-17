from jnius import PythonJavaClass, autoclass, java_method, JavaClass, MetaJavaClass, JavaMethod, JavaStaticMethod
from kivy.logger import Logger
from iabwrapper import lib_name

PythonActivity = autoclass("org.kivy.android.PythonActivity")

PurchaseInfo = autoclass("com.anjlab.android.iab.v3.PurchaseInfo")
SkuDetails = autoclass("com.anjlab.android.iab.v3.SkuDetails")

context = PythonActivity.mActivity

class PythonBillingHandler(PythonJavaClass):
    __javainterfaces__ = ["com/anjlab/android/iab/v3/BillingProcessor$IBillingHandler"]
    __javacontext__ = "app"

    def __init__(
        self,
        onProductPurchasedMethod,
        onBillingErrorMethod,
        onPurchaseHistoryRestoredMethod=None,
        onBillingInitializedMethod=None,
    ):
        self.onBillingInitializedMethod = onBillingInitializedMethod
        self.onProductPurchasedMethod = onProductPurchasedMethod
        self.onBillingErrorMethod = onBillingErrorMethod
        self.onPurchaseHistoryRestoredMethod = onPurchaseHistoryRestoredMethod
        super(PythonBillingHandler, self).__init__()

    @java_method("()V")
    def onBillingInitialized(self):
        Logger.info(f"{lib_name}: onBillingInitialized")
        if self.onBillingInitializedMethod:
            self.onBillingInitializedMethod()

    @java_method("(Ljava/lang/String;Lcom/anjlab/android/iab/v3/PurchaseInfo;)V")
    def onProductPurchased(self, productId, purchaseInfo):
        Logger.info(f"{lib_name}: onProductPurchased: " + productId)
        self.onProductPurchasedMethod(productId, purchaseInfo)
    
    @java_method("(ILjava/lang/Throwable;)V")
    def onBillingError(self, errorCode, error):
        Logger.info(f"{lib_name}: onBillingError: {errorCode} {error.message}")
        self.onBillingErrorMethod(errorCode, error)

    @java_method("()V")
    def onPurchaseHistoryRestored(self):
        Logger.info(f"{lib_name}: onPurchaseHistoryRestored")
        if self.onPurchaseHistoryRestoredMethod:
            self.onPurchaseHistoryRestoredMethod()


class PythonIPurchasesResponseListener(PythonJavaClass):
    __javainterfaces__ = [
        "com/anjlab/android/iab/v3/BillingProcessor$IPurchasesResponseListener"
    ]
    __javacontext__ = "app"

    def __init__(self, onPurchasesSuccessMethod=None, onPurchasesErrorMethod=None):
        self.onPurchasesSuccessMethod = onPurchasesSuccessMethod
        self.onPurchasesErrorMethod = onPurchasesErrorMethod
        super(PythonIPurchasesResponseListener, self).__init__()

    @java_method("()V")
    def onPurchasesSuccess(self):
        Logger.info(f"{lib_name}: onPurchasesSuccess")
        if self.onPurchasesSuccessMethod:
            self.onPurchasesSuccessMethod()

    @java_method("()V")
    def onPurchasesError(self):
        Logger.info(f"{lib_name}: onPurchasesError")
        if self.onPurchasesErrorMethod:
            self.onPurchasesErrorMethod()


class PythonISkuDetailsResponseListener(PythonJavaClass):
    __javainterfaces__ = [
        "com/anjlab/android/iab/v3/BillingProcessor$ISkuDetailsResponseListener"
    ]
    __javacontext__ = "app"

    def __init__(self, onSkuDetailsSuccessMethod=None, onSkuDetailsErrorMethod=None):
        self.onSkuDetailsSuccessMethod = onSkuDetailsSuccessMethod
        self.onSkuDetailsErrorMethod = onSkuDetailsErrorMethod
        super(PythonISkuDetailsResponseListener, self).__init__()

    @java_method("(Ljava/util/List;)V")
    def onSkuDetailsResponse(self, products):
        Logger.info(f"{lib_name}: onSkuDetailsResponse")
        if self.onSkuDetailsSuccessMethod:
            self.onSkuDetailsSuccessMethod(products)

    @java_method("(Ljava/lang/String;)V")
    def onSkuDetailsError(self, error):
        Logger.info(f"{lib_name}: onSkuDetailsError")
        if self.onSkuDetailsErrorMethod:
            self.onSkuDetailsErrorMethod(error)


class BillingProcessor(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = 'com/anjlab/android/iab/v3/BillingProcessor'
    __javaconstructor__ = [(
        '(Landroid/content/Context;Ljava/lang/String;Lcom/anjlab/android/iab/v3/BillingProcessor$IBillingHandler;)V',
        False
    )
    ]

    initialize = JavaMethod('()V')
    purchase = JavaMethod('(Landroid/app/Activity;Ljava/lang/String;)Z')
    consumePurchaseAsync = JavaMethod('(Ljava/lang/String;Lcom/anjlab/android/iab/v3/BillingProcessor$IPurchasesResponseListener;)V')
    getPurchaseListingDetailsAsync = JavaMethod('(Ljava/lang/String;Lcom/anjlab/android/iab/v3/BillingProcessor$ISkuDetailsResponseListener;)V')
    subscribe = JavaMethod('(Landroid/app/Activity;Ljava/lang/String;)Z')
    loadOwnedPurchasesFromGoogleAsync = JavaMethod('(Lcom/anjlab/android/iab/v3/BillingProcessor$IPurchasesResponseListener;)V')
    getSubscriptionListingDetailsAsync = JavaMethod('(Ljava/lang/String;Lcom/anjlab/android/iab/v3/BillingProcessor$ISkuDetailsResponseListener;)V')
    release = JavaMethod('()V')
    isInitialized = JavaMethod('()Z')
    isPurchased = JavaMethod('(Ljava/lang/String;)Z')
    isSubscribed = JavaMethod('(Ljava/lang/String;)Z')
    isSubscriptionUpdateSupported = JavaMethod('()Z')
    isIabServiceAvailable = JavaStaticMethod('(Landroid/content/Context;)Z')
    listOwnedProducts = JavaMethod('()Ljava/util/List;')
    listOwnedSubscriptions = JavaMethod('()Ljava/util/List;')
    isConnected = JavaMethod('()Z')
    getPurchaseInfo = JavaMethod('(Ljava/lang/String;)Lcom/anjlab/android/iab/v3/PurchaseInfo;')
    getSubscriptionPurchaseInfo = JavaMethod('(Ljava/lang/String;)Lcom/anjlab/android/iab/v3/PurchaseInfo;')

    def __init__(
        self,
        license_key,
        onProductPurchasedMethod,
        onBillingErrorMethod,
        onPurchaseHistoryRestoredMethod=None,
        onBillingInitializedMethod=None,
    ):
        self.billing_handler = PythonBillingHandler(
            onProductPurchasedMethod,
            onBillingErrorMethod,
            onPurchaseHistoryRestoredMethod,
            onBillingInitializedMethod,
        )

        super().__init__(context, license_key, self.billing_handler)

    def purchase_product(self, product_id):
        self.purchase(context, product_id)

    def consume_purchase_async(
        self, product_id, success_listener=None, error_listener=None
    ):
        purchases_response_listener = PythonIPurchasesResponseListener(
            success_listener, error_listener
        )
        self.consumePurchaseAsync(product_id, purchases_response_listener)

    def get_purchase_listing_async(
        self, product_id, success_listener=None, error_listener=None
    ):
        sku_details_listener = PythonISkuDetailsResponseListener(
            success_listener, error_listener
        )
        self.getPurchaseListingDetailsAsync(product_id, sku_details_listener)

    def subscribe_product(self, subscription_id):
        self.subscribe(context, subscription_id)

    def load_owned_purchases_async(
        self, success_listener=None, error_listener=None
    ):
        purchases_response_listener = PythonIPurchasesResponseListener(
            success_listener, error_listener
        )
        self.loadOwnedPurchasesFromGoogleAsync(purchases_response_listener)

    def get_subscription_listing_async(
        self, subscription_id, success_listener=None, error_listener=None
    ):
        sku_details_listener = PythonISkuDetailsResponseListener(
            success_listener, error_listener
        )
        self.getSubscriptionListingDetailsAsync(
            subscription_id, sku_details_listener
        )
    
    def is_initialized(self):
        return self.isInitialized()
    
    def is_purchased(self, product_id):
        return self.isPurchased(product_id)
    
    def is_subscribed(self, subscription_id):
        return self.isSubscribed(subscription_id)
    
    def is_subscription_update_supported(self):
        return self.isSubscriptionUpdateSupported()
    
    def is_iab_service_available(self):
        return self.isIabServiceAvailable(context)
    
    def list_owned_products(self):
        return self.listOwnedProducts()
    
    def list_owned_subscriptions(self):
        return self.listOwnedSubscriptions()
    
    def is_connected(self):
        return self.isConnected()
    
    def get_purchase_info(self, product_id):
        return self.getPurchaseInfo(product_id)
    
    def get_subscription_purchase_info(self, subscription_id):
        return self.getSubscriptionPurchaseInfo(subscription_id)

    def __del__(self):
        self.release()
