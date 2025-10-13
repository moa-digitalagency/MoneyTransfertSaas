import math

def get_transaction_fee(amount, direction, config):
    fees = config['transaction_fees'][direction]
    for tier in fees:
        if tier['min'] <= amount < tier['max']:
            return tier['fee']
    return fees[-1]['fee']

def round_up_to_cents(amount):
    return math.ceil(amount * 100) / 100

def calculate_transfer(direction, amount, calculation_type, config):
    rates = config['rates']
    
    country1_currency = config['countries']['country1']['currency_code']
    country2_currency = config['countries']['country2']['currency_code']
    
    if direction == 'country1_to_country2':
        if calculation_type == 'send':
            send_amount = round_up_to_cents(amount)
            fee = get_transaction_fee(send_amount, direction, config)
            conversion = send_amount * rates['country1_to_country2']
            receive_amount = round_up_to_cents(conversion - fee)
        else:
            receive_amount = amount
            send_amount = (receive_amount / rates['country1_to_country2'])
            
            for _ in range(10):
                fee = get_transaction_fee(send_amount, direction, config)
                new_send_amount = (receive_amount + fee) / rates['country1_to_country2']
                if abs(new_send_amount - send_amount) < 0.01:
                    send_amount = new_send_amount
                    break
                send_amount = new_send_amount
            
            target_receive = receive_amount
            low = send_amount - 1
            high = send_amount + 1
            
            for _ in range(100):
                test_send = (low + high) / 2
                test_send = round(test_send, 3)
                fee = get_transaction_fee(test_send, direction, config)
                actual_receive = round_up_to_cents((test_send * rates['country1_to_country2']) - fee)
                
                if actual_receive == target_receive:
                    send_amount = test_send
                    break
                elif actual_receive < target_receive:
                    low = test_send
                else:
                    high = test_send
                
                if high - low < 0.0001:
                    send_amount = test_send
                    break
            
            send_amount = round_up_to_cents(send_amount)
            fee = get_transaction_fee(send_amount, direction, config)
            receive_amount = round_up_to_cents((send_amount * rates['country1_to_country2']) - fee)
            
            while receive_amount < target_receive:
                send_amount += 0.01
                fee = get_transaction_fee(send_amount, direction, config)
                receive_amount = round_up_to_cents((send_amount * rates['country1_to_country2']) - fee)
        
        send_currency = country1_currency
        receive_currency = country2_currency
        fee_currency = country2_currency
        
    else:
        if calculation_type == 'send':
            send_amount = round_up_to_cents(amount)
            fee = get_transaction_fee(send_amount, direction, config)
            conversion = send_amount * rates['country2_to_country1']
            receive_amount = round_up_to_cents(conversion - fee)
        else:
            receive_amount = amount
            send_amount = (receive_amount / rates['country2_to_country1'])
            for _ in range(10):
                fee = get_transaction_fee(send_amount, direction, config)
                new_send_amount = (receive_amount + fee) / rates['country2_to_country1']
                if abs(new_send_amount - send_amount) < 0.01:
                    send_amount = new_send_amount
                    break
                send_amount = new_send_amount
            
            target_receive = receive_amount
            low = send_amount - 1
            high = send_amount + 1
            
            for _ in range(100):
                test_send = (low + high) / 2
                test_send = round(test_send, 3)
                fee = get_transaction_fee(test_send, direction, config)
                actual_receive = round_up_to_cents((test_send * rates['country2_to_country1']) - fee)
                
                if actual_receive == target_receive:
                    send_amount = test_send
                    break
                elif actual_receive < target_receive:
                    low = test_send
                else:
                    high = test_send
                
                if high - low < 0.0001:
                    send_amount = test_send
                    break
            
            send_amount = round_up_to_cents(send_amount)
            fee = get_transaction_fee(send_amount, direction, config)
            receive_amount = round_up_to_cents((send_amount * rates['country2_to_country1']) - fee)
            
            while receive_amount < target_receive:
                send_amount += 0.01
                fee = get_transaction_fee(send_amount, direction, config)
                receive_amount = round_up_to_cents((send_amount * rates['country2_to_country1']) - fee)
        
        send_currency = country2_currency
        receive_currency = country1_currency
        fee_currency = country1_currency
    
    return {
        'send_amount': send_amount,
        'receive_amount': receive_amount,
        'send_currency': send_currency,
        'receive_currency': receive_currency,
        'rate': rates['country1_to_country2'] if direction == 'country1_to_country2' else rates['country2_to_country1'],
        'fee': fee,
        'fee_currency': fee_currency
    }
