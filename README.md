<h1 align="center"> IABwrapper</h1>

<h4 align="center">Wrapper around <a href="https://github.com/anjlab/android-inapp-billing-v3">Anjlab's</a> Android In-app Billing Version 3 to be used in Kivy apps</h4>

<p align="center"><a href="https://app.travis-ci.com/shashi278/android-iab-v3-kivy"><img src="https://app.travis-ci.com/shashi278/android-iab-v3-kivy.svg?branch=main" alt="Build Status"/></a>
<a href="https://www.python.org/downloads/release/python-360/"><img src="https://img.shields.io/pypi/pyversions/kivymd" alt="Python 3.6"/></a>
<a href="https://pypi.org/project/IABwrapper/"><img src="https://img.shields.io/pypi/v/iabwrapper" alt="PyPI"/></a>
<a href="https://pypi.org/project/IABwrapper/"><img src="https://img.shields.io/pypi/format/iabwrapper" alt="format"/></a>
<a href="https://pypi.org/project/IABwrapper/"><img src="https://img.shields.io/pypi/dm/iabwrapper" alt="downloads"/></a>
<a href="https://pypi.org/project/IABwrapper/"><img src="https://img.shields.io/github/languages/code-size/shashi278/android-iab-v3-kivy" alt="code size"/></a>
<a href="https://pypi.org/project/IABwrapper/"><img src="https://img.shields.io/github/repo-size/shashi278/android-iab-v3-kivy" alt="repo size"/></a>

#
### Demo
<p align="center"><img src="https://raw.githubusercontent.com/shashi278/android-iab-v3-kivy/main/demo/iabwrapper_demo.gif" width=200 /></p>

### Install
```bash
pip install iabwrapper
```
#### or add it in buildozer.spec requirements
```bash
requirements = ..., iabwrapper==0.0.5
```
#
### Important ( Add these into your buildozer.spec )
*   ```python
    android.gradle_repositories = "mavenCentral()"
    ```

*   ```python
    android.gradle_dependencies = com.anjlab.android.iab.v3:library:2.0.0,
    ```

*   ```python
    android.meta_data = billing_pubkey = "Your License Key from Play Console"
    ```
* Necessary permissions:
    ```python
    android.permissions = INTERNET,ACCESS_NETWORK_STATE,com.android.vending.BILLING
    ```
#
### Usage
*   Import
    ```python
    from iabwrapper import BillingProcessor
    ```
*   Create an Instance
    ```python
    bp = BillingProcessor(
        license_key,
        onProductPurchasedMethod,
        onBillingErrorMethod,
        onPurchaseHistoryRestoredMethod=None,
        onBillingInitializedMethod=None,
    )

    # license_key is the license key string from Google Play Console

    # onProductPurchasedMethod expects two arguments: productId and purchaseInfo

    # onBillingErrorMethod expects two arguments: errorCode and error (use error.message to get the error message)

    # onPurchaseHistoryRestoredMethod does not expect any arguments

    # onBillingInitializedMethod does not expect any arguments

    ```
#### Useful Methods
*   Purchase a product
    ```python
    purchase_product(product_id)
    ```

*   Consume a product(non-subscription)
    ```python
    consume_purchase_async(product_id, success_listener=None, error_listener=None)

    # Both success_listener and error_listener doesn't take any arguments
    ```

*   Get details about a product (non-subscription)
    ```python
    get_purchase_listing_async(product_id, success_listener=None, error_listener=None)

    # Both success_listener and error_listener expects a single argument.

    # success_listener gets a list with one element. Following details are available:
    if product_info.size() != 0:
        product_info = product_info[0]
        details= {
            "productId":        product_info.productId,
            "title":            product_info.title,
            "description":      product_info.description,
            "isSubscription":   product_info.isSubscription,
            "currency":         product_info.currency,
            "priceValue":       product_info.priceValue,
            "priceText":        product_info.priceText,
        }
    
    # error_listener gets a string with error message.
    ```

*   Subscribe to a product
    ```python
    subscribe_product(product_id)
    ```

*   Get details about a subscription
    ```python
    get_subscription_listing_async(product_id, success_listener=None, error_listener=None)

    # Both success_listener and error_listener expects a single argument.

    # Same as get_purchase_listing_async
    ```

*   Update information about users owned purchases/subscriptions. Use it to restore Purchases & Subscriptions.
    ```python
    load_owned_purchases_async(success_listener=None, error_listener=None)

    # Both success_listener and error_listener doesn't take any arguments.
    ```

*   Check if service is initialized
    ```python
    is_initialized()
    ```

*   Check if a product is already purchased(non-subscription)
    ```python
    is_purchased(product_id)
    ```

*   Check if a product is already subscribed
    ```python
    is_subscribed(product_id)
    ```

*   > Before any usage it's good practice to check in-app billing services availability. In some older devices or chinese ones it may happen that Play Market is unavailable or is deprecated and doesn't support in-app billing.
    ```python
    is_iab_service_available()
    ```

*   > Please notice that calling BillingProcessor.isIabServiceAvailable() (only checks Play Market app installed or not) is not enough because there might be a case when it returns true but still payment won't succeed. Therefore, it's better to call bp.isConnected() after initializing BillingProcessor
    ```python
    is_connected()
    ```

*   List owned products(non-subscription)
    ```python
    list_owned_products()

    # Returns a list of product ids
    ```

*   List owned subscriptions
    ```python
    list_owned_subscriptions()

    # Returns a list of product ids
    ```

*   Get very detailed info about a product(non-subscription)
    ```python
    get_purchase_info(product_id)

    # Returns a `PurchaseInfo` object. Following details are available:
    purchase_info = bp.get_purchase_info(product_id)
    details = {
        "responseData": purchase_info.responseData,
        "signature": purchase_info.signature,
        "purchaseData":{
            "orderId": purchase_info.purchaseData.orderId,
            "productId": purchase_info.purchaseData.productId,
            "purchaseTime": purchase_info.purchaseData.purchaseTime,
            "purchaseToken": purchase_info.purchaseData.purchaseToken,
            "purchaseState": purchase_info.purchaseData.purchaseState,
            "autoRenewing": purchase_info.purchaseData.autoRenewing,
        }
    }
    ```

*   Get very detailed info about a subscription
    ```python
    get_subscription_purchase_info(product_id)

    # Returns a `PurchaseInfo` object. Same as get_purchase_info
    ```
### Example
See available demo application

### More
To know more about what a method does, please see [anjlab's android-inapp-billing-v3](https://github.com/anjlab/android-inapp-billing-v3) docs for reference.
