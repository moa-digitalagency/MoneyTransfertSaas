"""
MoneyTransfert
By MOA Digital Agency LLC
Developed by : Aisance KALONJI
Contact : moa@myoneart.com
www.myoneart.com
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
