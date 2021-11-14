from jnius import PythonJavaClass, autoclass, java_method
from kivy.logger import Logger

PythonActivity = autoclass("org.kivy.android.PythonActivity")

BillingProcessor = autoclass("com.anjlab.android.iab.v3.BillingProcessor")
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
        Logger.info("onBillingInitialized")
        if self.onBillingInitializedMethod:
            self.onBillingInitializedMethod()

    @java_method("(Ljava/lang/String;Lcom/anjlab/android/iab/v3/PurchaseInfo;)V")
    def onProductPurchased(self, productId, purchaseInfo):
        Logger.info("onProductPurchased: " + productId)
        self.onProductPurchasedMethod(productId, purchaseInfo)

    # Java method that takes an int and a Throwable
    @java_method("(Ljava/lang/Integer;Ljava/lang/Throwable;)V")
    def onBillingError(self, errorCode, error):
        Logger.info("onBillingError: " + str(errorCode))
        self.onBillingErrorMethod(errorCode, error)

    @java_method("()V")
    def onPurchaseHistoryRestored(self):
        Logger.info("onPurchaseHistoryRestored")
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
        Logger.info("onPurchasesSuccess")
        if self.onPurchasesSuccessMethod:
            self.onPurchasesSuccessMethod()

    @java_method("()V")
    def onPurchasesError(self):
        Logger.info("onPurchasesError")
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

    @java_method("(Ljava/lang/Object;)V")
    def onSkuDetailsResponse(self, products):
        Logger.info("onSkuDetailsResponse")
        if self.onSkuDetailsSuccessMethod:
            self.onSkuDetailsSuccessMethod(products)

    @java_method("(Ljava/lang/String;)V")
    def onSkuDetailsError(self, error):
        Logger.info("onSkuDetailsError")
        if self.onSkuDetailsErrorMethod:
            self.onSkuDetailsErrorMethod(error)


class PythonBillingProcessor(BillingProcessor):
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
        self.initialize()

    def purchase(self, product_id):
        super().purchase(context, product_id)

    def consumePurchaseAsync(
        self, product_id, success_listener=None, error_listener=None
    ):
        purchases_response_listener = PythonIPurchasesResponseListener(
            success_listener, error_listener
        )
        super().consumePurchaseAsync(product_id, purchases_response_listener)

    def getPurchaseListingDetailsAsync(
        self, product_id, success_listener=None, error_listener=None
    ):
        sku_details_listener = PythonISkuDetailsResponseListener(
            success_listener, error_listener
        )
        super().getPurchaseListingDetailsAsync(product_id, sku_details_listener)

    def subscribe(self, subscription_id):
        super().subscribe(context, subscription_id)

    def loadOwnedPurchasesFromGoogleAsync(
        self, success_listener=None, error_listener=None
    ):
        purchases_response_listener = PythonIPurchasesResponseListener(
            success_listener, error_listener
        )
        super().loadOwnedPurchasesFromGoogleAsync(purchases_response_listener)

    def getSubscriptionListingDetailsAsync(
        self, subscription_id, success_listener=None, error_listener=None
    ):
        sku_details_listener = PythonISkuDetailsResponseListener(
            success_listener, error_listener
        )
        super().getSubscriptionListingDetailsAsync(
            subscription_id, sku_details_listener
        )

    def __del__(self):
        self.release()
