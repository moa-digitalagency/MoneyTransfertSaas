import math

def get_transaction_fee(amount, direction, config):
    fees = config.get('transaction_fees', {}).get(direction, [])
    if not fees:
        return 0
    for tier in fees:
        if tier['min'] <= amount < tier['max']:
            return tier['fee']
    return fees[-1]['fee'] if fees else 0

def round_up_to_cents(amount):
    return math.ceil(amount * 100) / 100

def calculate_transfer(direction, amount, calculation_type, config):
    rates = config.get('rates', {})
    
    country1_currency = config.get('countries', {}).get('country1', {}).get('currency_code', 'USD')
    country2_currency = config.get('countries', {}).get('country2', {}).get('currency_code', 'MAD')
    
    rate_1to2 = rates.get('country1_to_country2', 0)
    rate_2to1 = rates.get('country2_to_country1', 0)
    
    if rate_1to2 == 0 or rate_2to1 == 0:
        return {
            'send_amount': 0,
            'receive_amount': 0,
            'send_currency': country1_currency,
            'receive_currency': country2_currency,
            'rate': 0,
            'fee': 0,
            'fee_currency': country2_currency,
            'error': 'Taux de change non configuré'
        }
    
    if direction == 'country1_to_country2':
        if calculation_type == 'send':
            send_amount = round_up_to_cents(amount)
            fee = get_transaction_fee(send_amount, direction, config)
            net_amount = send_amount - fee
            receive_amount = round_up_to_cents(net_amount * rate_1to2)
        else:
            receive_amount = amount
            send_amount = (receive_amount / rate_1to2)
            
            for _ in range(10):
                fee = get_transaction_fee(send_amount, direction, config)
                new_send_amount = (receive_amount / rate_1to2) + fee
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
                actual_receive = round_up_to_cents((test_send - fee) * rate_1to2)
                
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
            receive_amount = round_up_to_cents((send_amount - fee) * rate_1to2)
            
            while receive_amount < target_receive:
                send_amount += 0.01
                fee = get_transaction_fee(send_amount, direction, config)
                receive_amount = round_up_to_cents((send_amount - fee) * rate_1to2)
        
        send_currency = country1_currency
        receive_currency = country2_currency
        fee_currency = country1_currency
        
    else:
        if calculation_type == 'send':
            send_amount = round_up_to_cents(amount)
            fee = get_transaction_fee(send_amount, direction, config)
            net_amount = send_amount - fee
            receive_amount = round_up_to_cents(net_amount * rate_2to1)
        else:
            receive_amount = amount
            send_amount = (receive_amount / rate_2to1)
            for _ in range(10):
                fee = get_transaction_fee(send_amount, direction, config)
                new_send_amount = (receive_amount / rate_2to1) + fee
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
                actual_receive = round_up_to_cents((test_send - fee) * rate_2to1)
                
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
            receive_amount = round_up_to_cents((send_amount - fee) * rate_2to1)
            
            while receive_amount < target_receive:
                send_amount += 0.01
                fee = get_transaction_fee(send_amount, direction, config)
                receive_amount = round_up_to_cents((send_amount - fee) * rate_2to1)
        
        send_currency = country2_currency
        receive_currency = country1_currency
        fee_currency = country2_currency
    
    return {
        'send_amount': send_amount,
        'receive_amount': receive_amount,
        'send_currency': send_currency,
        'receive_currency': receive_currency,
        'rate': rate_1to2 if direction == 'country1_to_country2' else rate_2to1,
        'fee': fee,
        'fee_currency': fee_currency
    }
