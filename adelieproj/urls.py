from django.conf.urls import patterns, url
from django.conf import settings

from adelieproj import views

urlpatterns = patterns('',

    ##HOME PAGE
      #PAGES
    url(r'^$', views.index),
      #AJAX CALLS

    ##ADMINISTRATION
      #PAGES
    url(r'^admin$', views.admin),
    url(r'^admin/showproduct/(?P<product_id>\d*)$', views.admin_show_product),
    url(r'^admin/showcredit/(?P<gameId>\d*)$', views.adminShowCredit),
    url(r'^admin/givecredit/(?P<product_id>\d*)$', views.admin_give_credit),
      #AJAX CALLS
    url(r'^ajax/checkproductname/(?P<name>.*)$', views.check_product_name),
    url(r'^ajax/saveproduct$', views.admin_save_product),
    url(r'^ajax/editproduct$', views.admin_edit_product),
    url(r'^ajax/deletepic$', views.admin_delete_pic),
    url(r'^ajax/changetiers$', views.admin_change_tiers),
    url(r'^ajax/givecredit$', views.admin_give_credit),

    ##CHECKING OUT
      #PAGES
    url(r'^cart$', views.show_cart),
    url(r'^checkout$', views.checkout_page),
      #AJAX CALLS
    url(r'^ajax/addtocart$', views.add_to_cart),
    url(r'^ajax/updatecart$', views.update_cart),

    ##SHOWING PRODUCTS
      #PAGES
    url(r'^products/show/(?P<name>.*)$', views.show_product),
    url(r'^products$', views.all_products),
    url(r'^upcoming$', views.upcoming_products),

    ##ACCOUNT INFORMATION
      #PAGES
    url(r'^account$', views.account_page),

    ##AUTHENTICATION SYSTEM
      #PAGES
    url(r'^logout$', views.logout),
      #AJAX CALLS
    url(r'^ajax/checkuser/(?P<username>.*)$', views.check_user),
    url(r'^ajax/checkemail/(?P<email>.*)$', views.check_email),
    url(r'^ajax/checkpassword$', views.check_password),
    url(r'^ajax/reguser$', views.reg_user),
    url(r'^ajax/login$', views.login),

    ##S3 HOSTING STATIC FILES
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
