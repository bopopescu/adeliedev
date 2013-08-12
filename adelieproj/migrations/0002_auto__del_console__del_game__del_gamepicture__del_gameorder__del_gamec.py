# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Console'
        db.delete_table(u'adelieproj_console')

        # Deleting model 'Game'
        db.delete_table(u'adelieproj_game')

        # Removing M2M table for field pictures on 'Game'
        db.delete_table(db.shorten_name(u'adelieproj_game_pictures'))

        # Removing M2M table for field orders on 'Game'
        db.delete_table(db.shorten_name(u'adelieproj_game_orders'))

        # Removing M2M table for field consoles on 'Game'
        db.delete_table(db.shorten_name(u'adelieproj_game_consoles'))

        # Deleting model 'GamePicture'
        db.delete_table(u'adelieproj_gamepicture')

        # Deleting model 'GameOrder'
        db.delete_table(u'adelieproj_gameorder')

        # Deleting model 'GameCredit'
        db.delete_table(u'adelieproj_gamecredit')

        # Adding model 'Product'
        db.create_table(u'adelieproj_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')(max_length=100)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('tagLine', self.gf('django.db.models.fields.TextField')()),
            ('startTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('endTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('shipDate', self.gf('django.db.models.fields.DateField')()),
            ('credited', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'adelieproj', ['Product'])

        # Adding M2M table for field pictures on 'Product'
        m2m_table_name = db.shorten_name(u'adelieproj_product_pictures')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm[u'adelieproj.product'], null=False)),
            ('picture', models.ForeignKey(orm[u'adelieproj.picture'], null=False))
        ))
        db.create_unique(m2m_table_name, ['product_id', 'picture_id'])

        # Adding model 'Order'
        db.create_table(u'adelieproj_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('creditCard', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adelieproj.CreditCard'])),
            ('shippingAddress', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adelieproj.ShippingAddress'])),
            ('billingAddress', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adelieproj.BillingAddress'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adelieproj.Product'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'adelieproj', ['Order'])

        # Adding model 'Credit'
        db.create_table(u'adelieproj_credit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('credit', self.gf('django.db.models.fields.FloatField')()),
            ('used', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('tier', self.gf('django.db.models.fields.IntegerField')()),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adelieproj.Product'])),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adelieproj.Order'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'adelieproj', ['Credit'])

        # Adding model 'Picture'
        db.create_table(u'adelieproj_picture', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('caption', self.gf('django.db.models.fields.TextField')()),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('main', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'adelieproj', ['Picture'])

        # Deleting field 'CartItem.console'
        db.delete_column(u'adelieproj_cartitem', 'console_id')

        # Deleting field 'CartItem.game'
        db.delete_column(u'adelieproj_cartitem', 'game_id')

        # Adding field 'CartItem.product'
        db.add_column(u'adelieproj_cartitem', 'product',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['adelieproj.Product']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Console'
        db.create_table(u'adelieproj_console', (
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'adelieproj', ['Console'])

        # Adding model 'Game'
        db.create_table(u'adelieproj_game', (
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('shipDate', self.gf('django.db.models.fields.DateField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('credited', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('startTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('tagLine', self.gf('django.db.models.fields.TextField')()),
            ('endTime', self.gf('django.db.models.fields.DateTimeField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trailerUrl', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
        ))
        db.send_create_signal(u'adelieproj', ['Game'])

        # Adding M2M table for field pictures on 'Game'
        m2m_table_name = db.shorten_name(u'adelieproj_game_pictures')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('game', models.ForeignKey(orm[u'adelieproj.game'], null=False)),
            ('gamepicture', models.ForeignKey(orm[u'adelieproj.gamepicture'], null=False))
        ))
        db.create_unique(m2m_table_name, ['game_id', 'gamepicture_id'])

        # Adding M2M table for field orders on 'Game'
        m2m_table_name = db.shorten_name(u'adelieproj_game_orders')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('game', models.ForeignKey(orm[u'adelieproj.game'], null=False)),
            ('gameorder', models.ForeignKey(orm[u'adelieproj.gameorder'], null=False))
        ))
        db.create_unique(m2m_table_name, ['game_id', 'gameorder_id'])

        # Adding M2M table for field consoles on 'Game'
        m2m_table_name = db.shorten_name(u'adelieproj_game_consoles')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('game', models.ForeignKey(orm[u'adelieproj.game'], null=False)),
            ('console', models.ForeignKey(orm[u'adelieproj.console'], null=False))
        ))
        db.create_unique(m2m_table_name, ['game_id', 'console_id'])

        # Adding model 'GamePicture'
        db.create_table(u'adelieproj_gamepicture', (
            ('main', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('caption', self.gf('django.db.models.fields.TextField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'adelieproj', ['GamePicture'])

        # Adding model 'GameOrder'
        db.create_table(u'adelieproj_gameorder', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('shippingAddress', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adelieproj.ShippingAddress'])),
            ('console', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adelieproj.Console'])),
            ('billingAddress', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adelieproj.BillingAddress'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creditCard', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adelieproj.CreditCard'])),
        ))
        db.send_create_signal(u'adelieproj', ['GameOrder'])

        # Adding model 'GameCredit'
        db.create_table(u'adelieproj_gamecredit', (
            ('credit', self.gf('django.db.models.fields.FloatField')()),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adelieproj.Game'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('gameOrder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adelieproj.GameOrder'])),
            ('tier', self.gf('django.db.models.fields.IntegerField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('used', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'adelieproj', ['GameCredit'])

        # Deleting model 'Product'
        db.delete_table(u'adelieproj_product')

        # Removing M2M table for field pictures on 'Product'
        db.delete_table(db.shorten_name(u'adelieproj_product_pictures'))

        # Deleting model 'Order'
        db.delete_table(u'adelieproj_order')

        # Deleting model 'Credit'
        db.delete_table(u'adelieproj_credit')

        # Deleting model 'Picture'
        db.delete_table(u'adelieproj_picture')


        # User chose to not deal with backwards NULL issues for 'CartItem.console'
        raise RuntimeError("Cannot reverse this migration. 'CartItem.console' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'CartItem.game'
        raise RuntimeError("Cannot reverse this migration. 'CartItem.game' and its values cannot be restored.")
        # Deleting field 'CartItem.product'
        db.delete_column(u'adelieproj_cartitem', 'product_id')


    models = {
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
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adelieproj.Product']"}),
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
            'pictures': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['adelieproj.Picture']", 'symmetrical': 'False'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'shipDate': ('django.db.models.fields.DateField', [], {}),
            'startTime': ('django.db.models.fields.DateTimeField', [], {}),
            'tagLine': ('django.db.models.fields.TextField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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