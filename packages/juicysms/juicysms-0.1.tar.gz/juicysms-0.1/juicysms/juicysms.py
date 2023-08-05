#!/usr/bin/env python

import requests

class JuicySMS:

    API_KEY = ''
    
    def get_balance(self):
        url = 'https://juicysms.com/api/getbalance?key={}'.format(self.API_KEY)
        r = requests.get(url)
        if 'UNAUTHORIZED' in r.text:
            return {
                'status' : 'error',
                'error' : 'Invalid API Key'
            }
        else: 
            return {
                'status' : 'success',
                'balance' : r.text
            }
        
    def make_order(self, serivce_id):
        url = 'https://juicysms.com/api/makeorder?key={}&serviceId={}'.format(self.API_KEY, serivce_id)
        r = requests.get(url)
        if 'UNAUTHORIZED' in r.text:
            return {
                'status' : 'error',
                'error' : 'Invalid API Key'
            }
        elif 'NO_PHONE_AVAILABLE ' in r.text:
            return {
                'status' : 'error',
                'error' : 'There is unfortunately no phone available for the specified service.'
            }
        elif 'NO_BALANCE' in r.text:
            return {
                'status' : 'error',
                'error' : 'There is unfortunately not enough balance on your account for this order.'
            }
        elif 'ORDER_ALREADY_OPEN_' in r.text:
            existing_number = r.text.replace('ORDER_ALREADY_OPEN_', '')
            return {
                'status' : 'error',
                'error' : 'There is an order already open. Please finish or cancel this one before making a new order.',
                'number' : existing_number
            }
        elif 'ORDER_ID_' in r.text and '_NUMBER_' in r.text:
            data = r.text.replace('ORDER_ID_', '').replace('_NUMBER_', ':').split(':')
            return {
                'status' : 'success',
                'order_id' : data[0],
                'number' : data[1]
            }
    
    def cancel_order(self, order_id):
        url = 'https://juicysms.com/api/cancelorder?key={}&orderId={}'.format(self.API_KEY, order_id)
        r = requests.get(url)
        if 'UNAUTHORIZED' in r.text:
            return {
                'status' : 'error',
                'error' : 'Invalid API Key'
            }
        elif 'ORDER_ALREADY_EXPIRED' in r.text:
            return {
                'status' : 'error',
                'error' : 'The order has already been expired.'
            }
        elif 'ORDER_ALREADY_COMPLETED' in r.text:
            return {
                'status' : 'error',
                'error' : 'he order has already been completed.'
            }
        elif 'ORDER_CANCELED' in r.text:
            return {
                'status' : 'success',
                'message' : 'Your order has been canceled.'
            }
        
           
    def cancel_order(self, order_id):
        url = 'https://juicysms.com/api/cancelorder?key={}&orderId={}'.format(self.API_KEY, order_id)
        r = requests.get(url)
        if 'UNAUTHORIZED' in r.text:
            return {
                'status' : 'error',
                'error' : 'Invalid API Key'
            }
        elif 'ORDER_ALREADY_EXPIRED' in r.text:
            return {
                'status' : 'error',
                'error' : 'The order has already been expired.'
            }
        elif 'ORDER_ALREADY_COMPLETED' in r.text:
            return {
                'status' : 'error',
                'error' : 'he order has already been completed.'
            }
        elif 'NUMBER_SKIPPED_ORDER_CANCELED ' in r.text:
            return {
                'status' : 'success',
                'message' : 'Your order has been canceled and the number has been skipped. You can make a new order with a fresh number.'
            } 