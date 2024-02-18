For this project you need to have metamask extension installed, you can get sepolia test network faucets online for ETH balance.

->setting up EC2:
choose launch instance
give some name to webserver
in Application and OS Images choose ubuntu
If you want to operate remotely using ssh create a key pair and save it.
In Network settings check the boxes Allow HTTPS traffic from the internet and Allow HTTP traffic from the internet
select Launch Instance. This would create the instance. 

see the requirements.txt file and setup appropiate node, npm and truffle versions. and also install the python modules given.(to do this you have to use nvm)

run 'sudo curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash'

restart the terminal and see if nvm is working (just type nvm it should give you example usage)

run 'nvm install 21.3.0'

this would install node.js version 21.3.0 and npm version 10.2.4 (you can cross check using 'node -v' and 'npm -v')

run 'echo $PATH'

copy the path from entries (which looks like:/home/ubuntu/.nvm/versions/node/v21.3.0/bin)

run 'sudo visudo'

in Defaults 'secure_path' variable add with bin directory you copied in above step. save the file(".... :/home/ubuntu/.nvm/versions/node/v21.3.0/bin") 

now run 'sudo npm install -g truffle'

see that truffle version installed is 'v5.11.5' by executing 'truffle -v'

clone the repository which we have submitted in the git hub in the '/home' directory ('cd /home') it will have two folders 
(Evoting_app_Flask and smart_contract)

install following python modules using 'sudo pip':

flask, web3 and pymysql.

note: do not forget to use sudo in ay command.

install gunicorn webserver using following command:
sudo pip install gunicorn

while in smart_contract directory run following command:(to access the wallet)
sudo npm install @truffle/hdwallet-provider

while in the 'Evoting_app_Flask' directory run the following commands:
sudo chmod +x create_database_tables.py
sudo chmod +x relation.py
sudo chmod 777 election_destroy.txt
sudo chmod 777 previous_address.txt
sudo chmod 777 election_end.txt

keep your EC2 instance running do not turn it off.



-> Next steps are for setting up the database:

go to RDS service and select create database
Choose database creation method as Easy create
In configuration section do following:
-choose Engine type as MySQL in .
-DB instance size as free tier
-set appropiate db identifier
-set master username and password. (these are very important to access the database do not forget)
In Set up EC2 connection section choose Connect to an EC2 compute resource and
choose the EC2 instance name we created in above steps. this would automatically add
a security group in the EC2 to access the database.  

wait till status of database is Available.

copy the Endpoint from connectivity and security section (looks like :database-1.cb64xylaktzx.us-east-2.rds.amazonaws.com).

open 'create_database_tables.py' file in 'Evoting_app_Flask' directory and paste the 
endpoint link in the host variable. and also type the master username and password we 
created above in the user and password variables respectively. Do not change the database variable (it should have value 'election'), keep it as it is.

repeat the above step for 'relation.py' file as well present in the 'Evoting_app_Flask' directory.

now run the command 'sudo python3 create_database_tables.py', ths will create a database election and two tables 'voter' and 'candidates'.



-> deploying smart contract and starting the website:

You need to have an infura api key for sepolia network and the mnemonic of owner account on which you are going to deploy the contract.
to get an infura key for sepolia test network you can take refrence https://docs.infura.io/getting-started.
to get secret recovery key you can refer to this link : https://support.metamask.io/hc/en-us/articles/360015290032-How-to-reveal-your-Secret-Recovery-Phrase

Execute the smart contract:
Go to smart_contract directory 
To specify name of election you want to deploy go to deploy_contract.js present in smart_contract/migrations directory, 
type the name of election in election_name variable (variable is set to 'My Election' by default).

In smart_contract directory go to truffle-config.js and copy paste the above two in following variables
INFURA_API_KEY -> the api key you obtained
MNEMONIC -> secret recovery key (This is the owner account on which you are going to deploy the contract)

Also paste the same infura api key obtained above in the app.py file present in 'Evoting_app_Flask' directory.

now to deploy run (while being in smart_contract directory):
sudo truffle migrate --network sepolia
(we are using sepolia test network)

You will get the details of deployment. copy the 'contract address' under the  '1_deploy_contract.js'.
in Evoting_app_Flask directory open app.py paste the contract address (contract_address variable).

copy path of Election.json file (which consists of abi) from smart_contract/build/contracts directory. 
(.../smart_contract/build/contracts/Election.json).

In Evoting_app_Flask directory open 'read_abi.py' paste the path of Election.json file  (in json_file_path variable).

you can change admin credentials if you want in admin_credentials.json present in Evoting_app_Flask directory. (admin or owner of contract can login using this credentials)
in order to any operations on the admin dashboard make sure you are using the same account with which you deployed the smart contract as it is the owner of election and only
that account has access to admin functionalities. if you use any other account transaction wont go through.

to run the app publicly you need to run following command while being present in the Evoting_app_Flask directory. 

sudo gunicorn -b 0.0.0.0:80 app:app

this will start gunicorn web server if any errors are being displayed then there is something wrong with the configuration.

got to http://<ec2 instance public ipv4> address and check whether the website is running.