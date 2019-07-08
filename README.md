# InnerEyeDeployment

Deployment codes:
    sudo pip3 install -r requirements
    export FLASK_APP=InnerEyeBackEnd.py
    flask run --host=0.0.0.0
  
Please visit http://192.168.0.101:5000/static/InnerEyeFrontEnd.html to access the site.

If you face problems runninh the flask servers, it is highly probable that your firewall is blocking the app. Please run the following code below to solve this:
    sudo apt install firewalld
    sudo firewall-cmd --zone=public --list-ports
    sudo firewall-cmd --zone=public --permanent --add-port=5000/tcp

Thank you.
