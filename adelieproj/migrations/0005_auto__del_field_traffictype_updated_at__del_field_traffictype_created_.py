# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'TrafficType.updated_at'
        db.delete_column(u'adelieproj_traffictype', 'updated_at')

        # Deleting field 'TrafficType.created_at'
        db.delete_column(u'adelieproj_traffictype', 'created_at')

        # Adding field 'Arrival.ip'
        db.add_column(u'adelieproj_arrival', 'ip',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True),
                      keep_default=False)

        # Deleting field 'ProductArrivalType.updated_at'
        db.delete_column(u'adelieproj_productarrivaltype', 'updated_at')

        # Deleting field 'ProductArrivalType.created_at'
        db.delete_column(u'adelieproj_productarrivaltype', 'created_at')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'TrafficType.updated_at'
        raise RuntimeError("Cannot reverse this migration. 'TrafficType.updated_at' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'TrafficType.created_at'
        raise RuntimeError("Cannot reverse this migration. 'TrafficType.created_at' and its values cannot be restored.")
        # Deleting field 'Arrival.ip'
        db.delete_column(u'adelieproj_arrival', 'ip')


        # User chose to not deal with backwards NULL issues for 'ProductArrivalType.updated_at'
        raise RuntimeError("Cannot reverse this migration. 'ProductArrivalType.updated_at' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'ProductArrivalType.created_at'
        raise RuntimeError("Cannot reverse this migration. 'ProductArrivalType.created_at' and its values cannot be restored.")

    models = {
        u'adelieproj.arrival': {
            'Meta': {'object_name': 'Arrival'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'traffic_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adelieproj.TrafficType']", 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'adelieproj.billingaddress': {
            'Meta': {'object_name': 'BillingAddress'},
            'addressOne': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'addressTwo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'adelieproj.cart': {
            'Meta': {'object_name': 'Cart'},
            'checkedOut': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['adelieproj.CartItem']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'adelieproj.cartitem': {
            'Meta': {'object_name': 'CartItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adelieproj.Product']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'adelieproj.credit': {
            'Meta': {'object_name': 'Credit'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'credit': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adelieproj.Order']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adelieproj.Product']"}),
            'tier': ('django.db.models.fields.IntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'used': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'adelieproj.creditcard': {
            'Meta': {'object_name': 'CreditCard'},
            'billingAddress': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adelieproj.BillingAddress']"}),
            'cardNum': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cvc': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'expirationMonth': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'expirationYear': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'adelieproj.order': {
            'Meta': {'object_name': 'Order'},
            'billingAddress': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adelieproj.BillingAddress']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creditCard': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adelieproj.CreditCard']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shippingAddress': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adelieproj.ShippingAddress']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'adelieproj.picture': {
            'Meta': {'object_name': 'Picture'},
            'caption': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'adelieproj.product': {
            'Meta': {'object_name': 'Product'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'credited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'endTime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '100'}),
            'orders': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['adelieproj.Order']", 'symmetrical': 'False'}),
            'pictures': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['adelieproj.Picture']", 'symmetrical': 'False'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'shipDate': ('django.db.models.fields.DateField', [], {}),
            'startTime': ('django.db.models.fields.DateTimeField', [], {}),
            'tagLine': ('django.db.models.fields.TextField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'adelieproj.productarrivaltype': {
            'Meta': {'object_name': 'ProductArrivalType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'adelieproj.productview': {
            'Meta': {'object_name': 'ProductView'},
            'arrival': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adelieproj.Arrival']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adelieproj.Product']"}),
            'product_arrival_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adelieproj.ProductArrivalType']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'})
        },
        u'adelieproj.shippingaddress': {
            'Meta': {'object_name': 'ShippingAddress'},
            'addressOne': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'addressTwo': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'adelieproj.traffictype': {
            'Meta': {'object_name': 'TrafficType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['adelieproj']