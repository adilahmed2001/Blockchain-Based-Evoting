from flask import Flask, render_template, request, redirect, url_for, session
from web3 import Web3
from functools import wraps
from read_abi import read_abi
from relation import *
import re

app = Flask(__name__)
w3 = Web3(Web3.HTTPProvider('<paste infura key here>'))
contract_address = "<paste smart contract address here>"
contract_abi = read_abi()

contract_present = True

def check_contract_status(contract_address,contract_abi):
    try:
        return w3.eth.contract(address=contract_address, abi=contract_abi), True

    except Exception as e:
        print('Contract does not exist or incorrect abi or incorrct smart contract address')
        return None, False

(contract, contract_present) = check_contract_status(contract_address, contract_abi)

if not contract_present:
    print('smart contract not present or address incorrect or abi incorrect')
    print('Exiting...')
    raise KeyboardInterrupt("")

try:
	election_title = contract.functions.electionTitle().call()
except:
    print('Contract Not Found, Please deploy and replace address and abi with corresponsing values')
app.secret_key = 'adasdasdasdada*#$9ad&0afa9ADasasebvmdkfbdngMA0dzasd0fda09c'

admin_credentials = get_admin_credentials()

def read_election_end():
	with open('election_end.txt', 'r') as file:
		return file.read()

def toggle_end():
	k = read_election_end()
	with open('election_end.txt', 'w') as file:
		file.write("True" if k == "False" else "False")

def read_election_destroy():
	with open('election_destroy.txt', 'r') as file:
		return file.read()

def toggle_destroy():
	k = read_election_destroy()
	with open('election_destroy.txt', 'w') as file:
		file.write("True" if k == "False" else "False")

def check_address_change(contract_address):
	text = ''
	with open('previous_address.txt', 'r') as file:
		text = file.read()
	return text != contract_address

def reset():
    reset_database()
    toggle_destroy()

if check_address_change(contract_address):
    reset_database()
    if read_election_destroy() != "False":
        toggle_destroy()

    if read_election_end != "False":
        toggle_end()

    with open('previous_address.txt', 'w') as file:
        file.write(contract_address)


def get_descriptions(candidates):
	cd = get_candidates_description()
	candidates_1 = [entry['candidate'] for entry in cd]
	cd1 = [candidate[0] for candidate in candidates]
	return [cd[candidates_1.index(candidate)]['description'] if candidate in candidates_1 else 'No Description' for candidate in cd1]

def get_winner(candidates):
	index = 0
	count = 0
	for i in range(0, len(candidates)):
		if int(candidates[i][1]) > count:
			count = int(candidates[i][1])
			index = i

	return candidates[index][0]

def is_voter_eligible(voter_address):
    try:
        voter_info = contract.functions.eligibleVoters(voter_address).call()

        is_authorized = voter_info[0]

        return is_authorized

    except Exception as e:
        return False

def get_voters_una():
    voters = []
    for voter in get_all_voters():
        if not is_voter_eligible(voter['metamask_id']):
            voters.append(voter)

    return voters

def is_valid_ethereum_address(address):
    ethereum_address_regex = re.compile(r'^0x[a-fA-F0-9]{40}$')

    return bool(ethereum_address_regex.match(address))

def login_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'user' in session and session['user'] == role:
                return func(*args, **kwargs)
            else:
                return redirect(url_for('login'))
        return wrapper
    return decorator

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        credentials = get_voter_credentials(username)

        if credentials != ():
            if username == credentials[0]['username'] and password == credentials[0]['password']:
                session['user'] = 'voter'
                if read_election_end() == 'True':
                    return redirect(url_for('voter_election_result'))
                return redirect(url_for('voter_dashboard'))
            else:
                error_message = 'Password Incorrect'
                return render_template('start_page.html', error_message=error_message)

        else:
            if username == admin_credentials['username'] and password == admin_credentials['password']:
                session['user'] = 'admin'
                if read_election_destroy() == 'True':
                    return render_template('destroy.html')
                if read_election_end() == 'True':
                    candidates = contract.functions.getCandidates().call()
                    session.pop('user', None)
                    return render_template('election_result_admin.html', candidates = candidates, election_title=election_title, winner = get_winner(candidates), abi = contract_abi, address = contract_address)
                return redirect(url_for('admin_home'))
            error_message = 'Account does not exist'
            return render_template('start_page.html', error_message=error_message)

    return render_template('start_page.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        metamask_id = request.form['userid']
        username = request.form['email']
        phoneno = request.form['phoneno']
        password = request.form['password']
        if not is_valid_ethereum_address(metamask_id):
            return render_template('start_page.html', error_message='Invalid Metamask ID Please Retry')
        try:
            add_user(username, password, metamask_id, phoneno)
            return render_template('start_page.html', error_message='Registration Successful')
        except Exception as e:
            print(e)
            return render_template('start_page.html', error_message='Username or Metamask ID Already exists Please Retry')
    return render_template('start_page.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/voter')
@login_required('voter')
def voter_dashboard():
    candidates = contract.functions.getCandidates().call()
    d = get_descriptions(candidates)
    cn = [{'name':candidates[i][0], 'description': d[i] } for i in range(0, len(candidates))]
    return render_template('dashboard_voter.html', candidates = cn, address = contract_address, abi = contract_abi)

@app.route('/admin/home')
@login_required('admin')
def admin_home():
    candidates = contract.functions.getCandidates().call()
    d = get_descriptions(candidates)
    cn = [{'candidate':candidates[i], 'description': d[i] } for i in range(0, len(candidates))]
    return render_template('dashboard_admin_home.html', candidates = cn, election_title=election_title)

@app.route('/admin/add_candidate', methods=['GET', 'POST'])
@login_required('admin')
def add_candidate():
    if request.method == 'POST':
        print('executed')
        data = request.get_json()
        print(data)
        add_candidate_description(data['name'], data['description'])
        print('executed')
        return {'status': 'success', 'message': 'Candidate added successfully'}

    return render_template('dashboard_add_candidate.html', address = contract_address, abi = contract_abi)

@app.route('/admin/authorize_voter')
@login_required('admin')
def authorize():
    return render_template('dashboard_authorize.html', voters = get_voters_una(), address = contract_address, abi = contract_abi)

@app.route('/blocks')
def display_blocks():
	return redirect(f"https://sepolia.etherscan.io/address/{contract_address}")

@app.route('/election/result')
@login_required('admin')
def end_election():
	candidates = contract.functions.getCandidates().call()
	toggle_end()
	return render_template('election_result_admin.html', candidates = candidates, election_title=election_title, winner = get_winner(candidates),  abi = contract_abi, address = contract_address)

@app.route('/election/result/voter')
@login_required('voter')
def voter_election_result():
	candidates = contract.functions.getCandidates().call()
	return render_template('election_result_voter.html', candidates = candidates, election_title=election_title, winner = get_winner(candidates))

@app.route('/admin/destroy',  methods=['POST'])
@login_required('admin')
def destroy():
    print('Resetting Database...')
    reset()
    print('Database Reset Successful')
    session.pop('user', None)
    return {'status': 'success', 'message': 'Destroyed'}
