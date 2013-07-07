# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BillingAddress'
        db.create_table(u'adelieproj_billingaddress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('addressOne', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('addressTwo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'adelieproj', ['BillingAddress'])

        # Adding model 'CreditCard'
        db.create_table(u'adelieproj_creditcard', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('cardNum', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('expirationMonth', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('expirationYear', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('cvc', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('billingAddress', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adelieproj.BillingAddress'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'adelieproj', ['CreditCard'])

        # Adding model 'ShippingAddress'
        db.create_table(u'adelieproj_shippingaddress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('addressOne', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('addressTwo', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'adelieproj', ['ShippingAddress'])

        # Adding model 'Console'
        db.create_table(u'adelieproj_console', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'adelieproj', ['Console'])

        # Adding model 'GamePicture'
        db.create_table(u'adelieproj_gamepicture', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('caption', self.gf('django.db.models.fields.TextField')()),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('main', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'adelieproj', ['GamePicture'])

        # Adding model 'GameOrder'
        db.create_table(u'adelieproj_gameorder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('creditCard', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adelieproj.CreditCard'])),
            ('shippingAddress', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adelieproj.ShippingAddress'])),
            ('billingAddress', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adelieproj.BillingAddress'])),
            ('console', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adelieproj.Console'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'adelieproj', ['GameOrder'])

        # Adding model 'Game'
        db.create_table(u'adelieproj_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('tagLine', self.gf('django.db.models.fields.TextField')()),
            ('startTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('endTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('shipDate', self.gf('django.db.models.fields.DateField')()),
            ('credited', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('trailerUrl', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
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

        # Adding model 'GameCredit'
        db.create_table(u'adelieproj_gamecredit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('credit', self.gf('django.db.models.fields.FloatField')()),
            ('used', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('tier', self.gf('django.db.models.fields.IntegerField')()),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adelieproj.Game'])),
            ('gameOrder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adelieproj.GameOrder'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'adelieproj', ['GameCredit'])

        # Adding model 'CartItem'
        db.create_table(u'adelieproj_cartitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adelieproj.Game'])),
            ('console', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adelieproj.Console'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'adelieproj', ['CartItem'])

        # Adding model 'Cart'
        db.create_table(u'adelieproj_cart', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('checkedOut', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'adelieproj', ['Cart'])

        # Adding M2M table for field items on 'Cart'
        m2m_table_name = db.shorten_name(u'adelieproj_cart_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cart', models.ForeignKey(orm[u'adelieproj.cart'], null=False)),
            ('cartitem', models.ForeignKey(orm[u'adelieproj.cartitem'], null=False))
        ))
        db.create_unique(m2m_table_name, ['cart_id', 'cartitem_id'])


    def backwards(self, orm):
        # Deleting model 'BillingAddress'
        db.delete_table(u'adelieproj_billingaddress')

        # Deleting model 'CreditCard'
        db.delete_table(u'adelieproj_creditcard')

        # Deleting model 'ShippingAddress'
        db.delete_table(u'adelieproj_shippingaddress')

        # Deleting model 'Console'
        db.delete_table(u'adelieproj_console')

        # Deleting model 'GamePicture'
        db.delete_table(u'adelieproj_gamepicture')

        # Deleting model 'GameOrder'
        db.delete_table(u'adelieproj_gameorder')

        # Deleting model 'Game'
        db.delete_table(u'adelieproj_game')

        # Removing M2M table for field pictures on 'Game'
        db.delete_table(db.shorten_name(u'adelieproj_game_pictures'))

        # Removing M2M table for field orders on 'Game'
        db.delete_table(db.shorten_name(u'adelieproj_game_orders'))

        # Removing M2M table for field consoles on 'Game'
        db.delete_table(db.shorten_name(u'adelieproj_game_consoles'))

        # Deleting model 'GameCredit'
        db.delete_table(u'adelieproj_gamecredit')

        # Deleting model 'CartItem'
        db.delete_table(u'adelieproj_cartitem')

        # Deleting model 'Cart'
        db.delete_table(u'adelieproj_cart')

        # Removing M2M table for field items on 'Cart'
        db.delete_table(db.shorten_name(u'adelieproj_cart_items'))


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
            'console': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adelieproj.Console']"}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adelieproj.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'adelieproj.console': {
            'Meta': {'object_name': 'Console'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
        u'adelieproj.game': {
            'Meta': {'object_name': 'Game'},
            'consoles': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['adelieproj.Console']", 'symmetrical': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'credited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'endTime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orders': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['adelieproj.GameOrder']", 'symmetrical': 'False'}),
            'pictures': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['adelieproj.GamePicture']", 'symmetrical': 'False'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shipDate': ('django.db.models.fields.DateField', [], {}),
            'startTime': ('django.db.models.fields.DateTimeField', [], {}),
            'tagLine': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'trailerUrl': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'adelieproj.gamecredit': {
            'Meta': {'object_name': 'GameCredit'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'credit': ('django.db.models.fields.FloatField', [], {}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adelieproj.Game']"}),
            'gameOrder': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adelieproj.GameOrder']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tier': ('django.db.models.fields.IntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'used': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'adelieproj.gameorder': {
            'Meta': {'object_name': 'GameOrder'},
            'billingAddress': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adelieproj.BillingAddress']"}),
            'console': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adelieproj.Console']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creditCard': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adelieproj.CreditCard']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shippingAddress': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adelieproj.ShippingAddress']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'adelieproj.gamepicture': {
            'Meta': {'object_name': 'GamePicture'},
            'caption': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
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