from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

session_data = {
    "session_id": None,
    "access_token": None,
    "last_transaction_id": None
}

api_history = []

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/test-login', methods=['POST'])
def test_login():
    url = 'https://rgw.8798-f464fa20.eu-de.ri1.apiconnect.appdomain.cloud/tmfb/dev-catalog/RetailerBVSLogin'
    headers = {
        'Content-Type': 'application/json',
        'X-Channel': 'bvsgateway',
        'X-IBM-Client-Id': '924726a273f72a75733787680810c4e4',
        'X-IBM-Client-Secret': '7154c95b3351d88cb31302f297eb5a9c',
        'Cookie': 'TS0142f610=011c1a8db649b1ebd0c6e0e50c829b8ee742dfe0bbd9f48da17ae7cd257af3573532dc134e4add93ae159857835a033b179cf9fd617286e0289bc94014ba9235fc06f3ca07',
        'User-Agent': 'PostmanRuntime/7.32.3',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
    }
    payload = {
        "OTP": "264891",
        "User": "923431664399@1010",
        "Pin": "12121"
    }
    response = requests.post(url, headers=headers, json=payload)
    try:
        data = response.json()
    except ValueError:
        data = {
            "error": "Non-JSON response received",
            "status_code": response.status_code,
            "response_text": response.text
        }

    if isinstance(data, dict):
        session_data["session_id"] = data.get("SessionID")
        session_data["access_token"] = data.get("AccessToken")

    api_history.append({
        "type": "login",
        "timestamp": datetime.now().isoformat(),
        "response": data
    })

    return jsonify({"status": "Login API tested", "response": data})


@app.route('/test-deposit', methods=['POST'])
def test_deposit():
    if not session_data["session_id"] or not session_data["access_token"]:
        return jsonify({"error": "Run login first!"}), 400

    url = 'https://rgw.8798-f464fa20.eu-de.ri1.apiconnect.appdomain.cloud/tmfb/dev-catalog/BVSCashDeposit/CashDepositBVS'
    headers = {
        'X-Username': '923440438216@1010',
        'X-Password': '12121',
        'Sessionid': session_data["session_id"],
        'Authorization': f"Bearer {session_data['access_token']}",
        'X-Channel': 'bvsgateway',
        'X-IBM-Client-Id': '924726a273f72a75733787680810c4e4',
        'X-IBM-Client-Secret': '7154c95b3351d88cb31302f297eb5a9c',
        'Content-Type': 'application/json',
        'User-Agent': 'PostmanRuntime/7.32.3',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'TS0142f610=011c1a8db649b1ebd0c6e0e50c829b8ee742dfe0bbd9f48da17ae7cd257af3573532dc134e4add93ae159857835a033b179cf9fd617286e0289bc94014ba9235fc06f3ca07'
    }
    payload = {
        "DepositAmount": "100",
        "Longitude": "31.5686808",
        "Latitude": "74.3000874",
        "CustomerCNIC": "3740577357058",
        "CustomerMSISDN": "923376246667"
    }
    response = requests.post(url, headers=headers, json=payload)
    try:
        data = response.json()
        if isinstance(data, dict):
            session_data["last_transaction_id"] = data.get("TransactionID")
    except ValueError:
        data = {
            "error": "Non-JSON response received",
            "status_code": response.status_code,
            "response_text": response.text
        }

    api_history.append({
        "type": "deposit",
        "timestamp": datetime.now().isoformat(),
        "response": data
    })

    return jsonify({"status": "Deposit API tested", "response": data})


@app.route('/test-deposit-confirmation', methods=['POST'])
def test_deposit_confirmation():
    if not session_data["session_id"] or not session_data["access_token"] or not session_data["last_transaction_id"]:
        return jsonify({"error": "Missing session, auth, or transaction ID. Run login and deposit first."}), 400

    url = 'https://rgw.8798-f464fa20.eu-de.ri1.apiconnect.appdomain.cloud/tmfb/dev-catalog/BVSCashDeposit/CashDepositBVS/Confirmation'
    headers = {
        'X-Username': '923440438216@1010',
        'X-Password': '12121',
        'Sessionid': session_data["session_id"],
        'Authorization': f"Bearer {session_data['access_token']}",
        'X-Channel': 'bvsgateway',
        'X-IBM-Client-Id': '924726a273f72a75733787680810c4e4',
        'X-IBM-Client-Secret': '7154c95b3351d88cb31302f297eb5a9c',
        'Content-Type': 'application/json',
        'Cookie': 'TS0142f610=011c1a8db649b1ebd0c6e0e50c829b8ee742dfe0bbd9f48da17ae7cd257af3573532dc134e4add93ae159857835a033b179cf9fd617286e0289bc94014ba9235fc06f3ca07',
        'MPOS': '1111@923355923388'
    }
    payload = {
        "TransactionID": session_data["last_transaction_id"],
        "TermsAccepted": "true",
        "DepositAmount": "100",
        "Longitude": "31.5686808",
        "Latitude": "74.3000874",
        "CustomerMSISDN": "923376246667",
        "AcquiredAfis": "test",
        "BioDeviceName": "test",
        "FingerNumber": "2",
        "ImageType": "4",
        "MPOS": "1111@923355923388"
    }
    response = requests.post(url, headers=headers, json=payload)
    try:
        data = response.json()
    except ValueError:
        data = {
            "error": "Non-JSON response received",
            "status_code": response.status_code,
            "response_text": response.text
        }

    api_history.append({
        "type": "deposit-confirmation",
        "timestamp": datetime.now().isoformat(),
        "response": data
    })

    return jsonify({"status": "Deposit Confirmation API tested", "response": data})


@app.route('/test-withdrawal', methods=['POST'])
def test_withdrawal():
    if not session_data["session_id"] or not session_data["access_token"]:
        return jsonify({"error": "Run login first!"}), 400

    url = 'https://rgw.8798-f464fa20.eu-de.ri1.apiconnect.appdomain.cloud/tmfb/dev-catalog/BVSCashWithdrawal/CashWithdrawalBVS'
    headers = {
        'X-Username': '923440438216@1010',
        'X-Password': '12121',
        'Sessionid': session_data["session_id"],
        'Authorization': f"Bearer {session_data['access_token']}",
        'X-Channel': 'bvsgateway',
        'X-IBM-Client-Id': '924726a273f72a75733787680810c4e4',
        'X-IBM-Client-Secret': '7154c95b3351d88cb31302f297eb5a9c',
        'Content-Type': 'application/json',
        'User-Agent': 'PostmanRuntime/7.32.3',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'TS0142f610=011c1a8db649b1ebd0c6e0e50c829b8ee742dfe0bbd9f48da17ae7cd257af3573532dc134e4add93ae159857835a033b179cf9fd617286e0289bc94014ba9235fc06f3ca07'
    }
    payload = {
        "WithdrawAmount": "10",
        "Longitude": "31.5686808",
        "Latitude": "74.3000874",
        "CustomerCNIC": "6110132583649",
        "CustomerMSISDN": "923376246667",
        "AcquiredAfis": "test",
        "FingerNumber": "2",
        "ImageType": "4",
        "BioDeviceName": "test"
    }
    response = requests.post(url, headers=headers, json=payload)
    try:
        data = response.json()
        if isinstance(data, dict):
            session_data["last_transaction_id"] = data.get("TransactionID")
    except ValueError:
        data = {
            "error": "Non-JSON response received",
            "status_code": response.status_code,
            "response_text": response.text
        }

    api_history.append({
        "type": "withdrawal",
        "timestamp": datetime.now().isoformat(),
        "response": data
    })

    return jsonify({"status": "withdrawal API tested", "response": data})


@app.route('/test-withdrawal-confirmation', methods=['POST'])
def test_withdrawal_confirmation():
    if not session_data["session_id"] or not session_data["access_token"] or not session_data["last_transaction_id"]:
        return jsonify({"error": "Missing session, auth, or transaction ID. Run login and deposit first."}), 400

    url = 'https://rgw.8798-f464fa20.eu-de.ri1.apiconnect.appdomain.cloud/tmfb/dev-catalog/BVSCashWithdrawal/CashWithdrawalBVS/Confirmation'
    headers = {
        'X-Username': '923440438216@1010',
        'X-Password': '12121',
        'Sessionid': session_data["session_id"],
        'Authorization': f"Bearer {session_data['access_token']}",
        'X-Channel': 'bvsgateway',
        'X-IBM-Client-Id': '924726a273f72a75733787680810c4e4',
        'X-IBM-Client-Secret': '7154c95b3351d88cb31302f297eb5a9c',
        'Content-Type': 'application/json',
        'Cookie': 'TS0142f610=011c1a8db649b1ebd0c6e0e50c829b8ee742dfe0bbd9f48da17ae7cd257af3573532dc134e4add93ae159857835a033b179cf9fd617286e0289bc94014ba9235fc06f3ca07',
        'MPOS': '1111@923355923388'
    }
    payload = {
        "TransactionID": session_data["last_transaction_id"],
        "TermsAccepted": "true",
        "WithdrawAmount": "100",
        "Longitude": "31.5686808",
        "Latitude": "74.3000874",
        "CustomerCNIC": "3740591321235",
        "CustomerMSISDN": "923481565391",
        "AcquiredAfis": "abcd",
        "FingerNumber": "2",
        "ImageType": "4",
        "BioDeviceName": "test"
    }
    response = requests.post(url, headers=headers, json=payload)
    try:
        data = response.json()
    except ValueError:
        data = {
            "error": "Non-JSON response received",
            "status_code": response.status_code,
            "response_text": response.text
        }

    api_history.append({
        "type": "withdrawal-confirmation",
        "timestamp": datetime.now().isoformat(),
        "response": data
    })

    return jsonify({"status": "withdrawal Confirmation API tested", "response": data})

@app.route('/test-CNICtoMA', methods=['POST'])
def test_CNICtoMA():
    if not session_data["session_id"] or not session_data["access_token"]:
        return jsonify({"error": "Run login first!"}), 400

    url = 'https://rgw.8798-f464fa20.eu-de.ri1.apiconnect.appdomain.cloud/tmfb/dev-catalog/BVSCNICtoMA/CNICtoMABVS'
    headers = {
        'X-Username': '923440438216@1010',
        'X-Password': '12121',
        'Sessionid': session_data["session_id"],
        'Authorization': f"Bearer {session_data['access_token']}",
        'X-Channel': 'bvsgateway',
        'X-IBM-Client-Id': '924726a273f72a75733787680810c4e4',
        'X-IBM-Client-Secret': '7154c95b3351d88cb31302f297eb5a9c',
        'Content-Type': 'application/json',
        'User-Agent': 'PostmanRuntime/7.32.3',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'TS0142f610=011c1a8db649b1ebd0c6e0e50c829b8ee742dfe0bbd9f48da17ae7cd257af3573532dc134e4add93ae159857835a033b179cf9fd617286e0289bc94014ba9235fc06f3ca07'
    }
    payload = {
        "ReceiverAccountNumber":"923345876677",
        "TermsAccepted": "true",
        "DepositAmount": "100",
        "DepositReason":"Education",
        "Longitude": "31.5686808",
        "Latitude": "74.3000874",
        "SenderMSISDN": "923376246667",
        "SenderCNIC": "3740577357007",
        "AcquiredAfis": "test",
        "BioDeviceName": "test",
        "FingerNumber": "1",
        "ImageType": "4"
    }
    response = requests.post(url, headers=headers, json=payload)
    try:
        data = response.json()
        if isinstance(data, dict):
            session_data["last_transaction_id"] = data.get("TransactionID")
    except ValueError:
        data = {
            "error": "Non-JSON response received",
            "status_code": response.status_code,
            "response_text": response.text
        }

    api_history.append({
        "type": "CNICtoMA",
        "timestamp": datetime.now().isoformat(),
        "response": data
    })

    return jsonify({"status": "CNICtoMA API tested", "response": data})

@app.route('/test-CNICtoMA-confirmation', methods=['POST'])
def test_CNICtoMA_confirmation():
    if not session_data["session_id"] or not session_data["access_token"] or not session_data["last_transaction_id"]:
        return jsonify({"error": "Missing session, auth, or transaction ID. Run login and deposit first."}), 400

    url = 'https://rgw.8798-f464fa20.eu-de.ri1.apiconnect.appdomain.cloud/tmfb/dev-catalog/BVSCNICtoMA/CNICtoMABVSConfirmation'
    headers = {
        'X-Username': '923440438216@1010',
        'X-Password': '12121',
        'Sessionid': session_data["session_id"],
        'Authorization': f"Bearer {session_data['access_token']}",
        'X-Channel': 'bvsgateway',
        'X-IBM-Client-Id': '924726a273f72a75733787680810c4e4',
        'X-IBM-Client-Secret': '7154c95b3351d88cb31302f297eb5a9c',
        'Content-Type': 'application/json',
        'Cookie': 'TS0142f610=011c1a8db649b1ebd0c6e0e50c829b8ee742dfe0bbd9f48da17ae7cd257af3573532dc134e4add93ae159857835a033b179cf9fd617286e0289bc94014ba9235fc06f3ca07',
        'MPOS': '1111@923355923388'
    }
    payload = {
        "TransactionID": session_data["last_transaction_id"],
        "ReceiverAccountNumber":"923345876677",
        "TermsAccepted": "true",
        "DepositAmount": "100",
        "DepositReason":"Education",
        "Longitude": "31.5686808",
        "Latitude": "74.3000874",
        "SenderMSISDN": "923376246667",
        "SenderCNIC":"3740577357007",
        "AcquiredAfis": "test",
        "BioDeviceName": "test",
        "FingerNumber": "1",
        "MPOS":"1233@923457685757",
        "ImageType": "4"
    }
    response = requests.post(url, headers=headers, json=payload)
    try:
        data = response.json()
    except ValueError:
        data = {
            "error": "Non-JSON response received",
            "status_code": response.status_code,
            "response_text": response.text
        }

    api_history.append({
        "type": "CNICtoMA-confirmation",
        "timestamp": datetime.now().isoformat(),
        "response": data
    })

    return jsonify({"status": "CNICtoMA Confirmation API tested", "response": data})


@app.route('/test-OTP-flow', methods=['POST'])
def test_otp_flow():
    if not session_data["session_id"] or not session_data["access_token"]:
        return jsonify({"error": "Missing session or access token. Run login first."}), 400

    base_url = 'https://rgw.8798-f464fa20.eu-de.ri1.apiconnect.appdomain.cloud/tmfb/dev-catalog/BVSAccountRegistration/OTP'
    headers = {
        'X-Username': '923481565391@1010',
        'X-Password': '12786',
        'Sessionid': session_data["session_id"],
        'Authorization': f"Bearer {session_data['access_token']}",
        'X-Channel': 'bvsgateway',
        'X-IBM-Client-Id': '924726a273f72a75733787680810c4e4',
        'X-IBM-Client-Secret': '7154c95b3351d88cb31302f297eb5a9c',
        'Content-Type': 'application/json',
        'User-Agent': 'PostmanRuntime/7.32.3',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'TS0142f610=011c1a8db65e30929afb92929b16caf8ac9c0fd7f258bc647aefbecdedc15556f2a9dee692eb2b756efb560a38ae5b610bb207782a1b88e6959e0e0dde0b22ef3842271c9e'
    }

    transaction_id = "0"
    all_responses = []

    for i in range(4):  # Hit API 3 times
        payload = {
            "TransactionID": transaction_id,
            "Longitude": "31.5686808",
            "Latitude": "74.3000874",
            "CustomerCNIC": "6110139987000",
            "CustomerMSISDN": "923400007553",
            "AcquiredAfis": "test",
            "FingerNumber": "2",
            "ImageType": "4",
            "BioDeviceName": "Gussie Hogan",
            "OTP": ""
        }

        response = requests.post(base_url, headers=headers, json=payload)

        try:
            data = response.json()
        except ValueError:
            data = {
                "error": "Non-JSON response received",
                "status_code": response.status_code,
                "response_text": response.text
            }

        # Extract new TransactionID from response if available
        transaction_id = data.get("TransactionID") or transaction_id

        api_history.append({
            "type": f"OTP API - Step {i+1}",
            "timestamp": datetime.now().isoformat(),
            "response": data
        })

        all_responses.append({
            "step": i + 1,
            "transaction_id": transaction_id,
            "response": data
        })

        # Stop flow if the response wasn't successful
        if response.status_code != 200:
            break

    return jsonify({"status": "BVSAccountRegistration flow tested", "steps": all_responses})



@app.route('/history')
def history():
    return jsonify(api_history)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
