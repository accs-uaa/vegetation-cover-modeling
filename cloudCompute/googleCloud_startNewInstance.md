# Starting a New Modeling Instance on Google Cloud Compute Engine

*Author*: Timm Nawrocki, Alaska Center for Conservation Science

*Created on*: 2018-08-20

*Description*: Instructions to create a virtual machine (vm) instance configured with 64 vCPUs, 57.6 GB of CPU memory, a 100 GB persistent disk, and Ubuntu 18.04 LTS operating system. The machine will be capable of running Jupyter Notebooks from an Ananconda3 installation through a web browser.

## Create a new project on Google Cloud Compute Engine and configure project firewall and storage.
Create a new project and enable API access for Google Cloud Compute Engine.

The storage bucket in this example is named "accs-machine-learning-bucket".

### Configure a firewall rule to allow browser access of Jupyter Notebooks
The firewall rule must be configured once per project. Navigate to VPC Network -> Firewall Rules and create new firewall rule with the following features:

*Name*: jupyter-rule

*Type*: Ingress

*IP ranges*: 0.0.0.0/0

*Protocols/ports*: tcp:8888

*Action*: Allow

*Targets*: All instances in the network

*Priority*: 1000

*Network*: Default

*Deletion Rule*: Uncheck

### Create a new bucket
Create a new bucket for the project. The bucket must be located in the same region and zone as the virtual machines. Folders and files can be uploaded to the bucket using the browser interface.

## Configure a new vm instance using the browser interface
The following steps must be followed every time a new instance is provisioned. The software set up must be completed for each vm unless you create a custom disk image with the software already installed.

### Use the Google Cloud Compute interface to create a new instance with the following features:

*Name*: <taxon>

*Region*: us-west1 (Oregon) **Region should change depending on closest infrastructure center**

*Zone*: us-west1-b **Zone should change depending on closest infrastructure center**

*Machine Type*: 64 vCPUs (57.6 GB memory)

*Boot Disk*: Ubuntu 18.04 LTS

*Boot Disk Type*: Standard Persistent Disk

*Delete Disk*: Uncheck

*Size (GB)*: 100

*Service Account*: Compute Engine default service account

*Access scopes*: Allow full access to all Cloud APIs

*Firewall*: Allow HTTP Traffic, Allow HTTPS traffic

### After hitting the create button, the new instance will start automatically

### Navigate to VPC Network -> External IP Addresses
Change the instance IP Address to static from ephemeral and assign a name that matches the vm instance.

### Launch the terminal in a browser window using ssh
Using ssh for the first time will create an SSH directory and key with optional password.

#### Update the Linux apt-get
`sudo apt-get update`

#### Install bzip2, git, and libxml2-dev
`sudo apt-get install bzip2 git libxml2-dev`

#### Install latest Anaconda release
```wget https://repo.continuum.io/archive/Anaconda3-5.2.0-Linux-x86_64.sh
bash Anaconda3-5.2.0-Linux-x86_64.sh
```

At the option to prepend the Anaconda3 install location to PATH in your /home... enter yes.

At the option to install Microsoft VSCode enter no.

#### Remove the installation file and start bashrc
```rm Anaconda3-5.2.0-Linux-x86_64.sh
source ~/.bashrc
```

# Add a certificate to allow access to notebook via https
```mkdir certs
cd ~/certs/
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout mykey.key -out mycert.pem
```

Follow the prompts to create a self-signed certificate.

If self-signed certificate fails or does not function, then comment out the certfile and keyfile in the Jupyter configuration and access the notebook via http.

# Configure Jupyter Notebook
`jupyter notebook --generate-config`

```jupyter notebook password
Enter Password: !!387#CFpxxNm7632!
Confirm Password: !!387#CFpxxNm7632!
```
Use vi to edit the jupyter notebook configuration file to allow access from all IP addresses. To insert in vi, enter "i" and type or paste edits. When finished editting, enter ESC the ":wq" to end inserting, save, and quit.

```cd ~/.jupyter/
vi jupyter_notebook_config.py
```

Add the following to the top of jupyter_notebook_config.py:

```c = get_config()

# Support inline plotting by default
c.IPKernelApp.pylab = 'inline'
# Location of certificate file
c.NotebookApp.certfile = u'/home/twnawrocki/certs/mycert.pem'
c.NotebookApp.keyfile = u'/home/twnawrocki/certs/mykey.key'
# Allow access from any IP address
c.NotebookApp.ip = '*'
# Do not open browser by default
c.NotebookApp.open_browser = False
# Set the port to the same port that the firewall rule designates
c.NotebookApp.port = 8888
```

#### Download the Google Storage bucket contents to the virtual machine
```cd ~
mkdir watershedData
mkdir speciesData
mkdir notebooks
mkdir <output_taxon>
mkdir <prediction_taxon>
gsutil cp -r gs://accs-machine-learning-bucket/watershedData/* ~/watershedData/
gsutil cp -r gs://accs-machine-learning-bucket/speciesData/* ~/speciesData/
gsutil cp -r gs://accs-machine-learning-bucket/notebooks/* ~/notebooks/
```

The vm instance is now configured and ready for use in the model train, test, and predict steps.

## Start the Jupyter Notebook
The following commands must be run every time the instance is started to launch the Jupyter Notebook server. These commands must be run from the instance terminal.

### Start jupyter notebook server
```cd notebooks
jupyter notebook
```

### Open jupyter notebook
In a browser, navigate to https://<your_VM_IP>:8888/. If the certificate does not work, then access using http.

### Upload predictions to Google Cloud storage bucket
`gsutil cp -r ~/<predictions_folder>/* gs://accs-machine-learning-bucket/<predictions_folder>`

Make sure that the predictions folder exists in the storage bucket prior to upload.

# IMPORTANT: When finished, the instance must be stopped to prevent being billed additional time
The instance can be stopped in the browser interface or by typing the following command into the Google Cloud console:

`gcloud compute instances stop --zone=us-west1-b <instance_name>`

# IMPORTANT: Release static ip address after instance is deleted to avoid being billed for reserving an unattached static ip.
