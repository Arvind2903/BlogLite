# BlogLite

## Directory Structure
The directory structure is as follows 
```
.
├── README.md
├── main.py
├── frontend
    ├── Welcome.pdf
    └── src
        ├── assets
            ├── csvs
            ├── graphs
            ├── images
            └── pdfs
        ├── components
            ├── ActivityComponent.vue
            ├──CreateComp.vue
            ├──FollowersComp.vue
            ├──FollowingComp.vue
            ├──HomeComp.vue
            ├──LoginComp.vue
            ├──NavComp.vue
            ├──PostDetails.vue
            ├──PostEdit.vue
            ├──ProfileComp.vue
            ├──SignUpComp.vue
            ├──UserProfileComp.vue
            └──UserProfileEdit.vue
        ├── templates
            ├──CSVMessageTemplate.html
            ├──LoginReminderTemplate.html
            ├──PostReminderTemplate.html
            ├──ReportMessageTemplate.html
            ├──ReportTemplate.html
            └──WelcomeTemplate.html
        ├──App.vue
        ├──main.js
        ├──routers.js
        └──store.js
├── backend
    ├── __init__.py
    ├── api.py
    ├── config.py
    ├── database.db
    ├── database.py
    ├── workers.py
    ├── tasks.py
    └── models.py
├── local_end.sh
├── local_run.sh
├── local_setup.sh
├── local_end.sh
├── Project Report.pdf
└── requirements.txt
```

## Instructions

- Install the prerequisites from requirements.txt
```bash
pip install -r requirements.txt
```

- Make sure to have nodejs
```bash
sudo apt update
sudo apt install nodejs

# Check that the installation was successful by querying node for its version number:
node -v
```

- Make sure to have node package manager installed to set up Vue CLI
```bash
sudo apt install npm
```

- Install Vue CLI
```bash
npm install -g @vue/cli

# You can check you have the right version with this command:
vue --version

# Update the global package
npm update -g @vue/cli
```

- Create your frontend folder
```bash
# Navigate to project folder
vue create frontend
```


You will be prompted to choose whether to overwrite or merge the project. Choose merge.
 When prompted to choose the version of Vue, choose Vue2. Verify that the content in main.js 
and App.vue have been retained.

- Install Vuex, Vue-Routers and Bootstrap 
```bash
# Navigate to the frontend folder
npm install bootstrap popper query js
npm install vuex@3 --save 
npm install vue-router@2
```

- Bind your app to electron for a browser independent experience
```bash
# Navigate to the frontend folder
vue add electron-builder # Choose the latest version of electron
```

- Install MailHog
```bash
sudo apt-get -y install golang-go
go get github.com/mailhog/MailHog
```

- Install Redis from [here](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-database)
and RESP from [here](https://docs.redisdesktop.com/en/latest/install/)

- Navigate back to the root folder of your project and run the following scripts in separate terminals in the same order
```bash
bash local_setup.sh
```
```bash
bash local_workers.sh
```
```bash
# Electron needs node v16, so make sure to install it before running this
nvm install v16
nvm use v16
bash local_run.sh
```

- Once you are done using the app, run the following script to kill any existing processes
```bash
bash local_end.sh 
```
Close the electron terminal

## General Information

- You will need a Linux environment to run the app, because celery uses threads for its work. If you have Windows,
consider installing WSL or set up a Docker Container.
- **[For Windows Users Only]** If you are using WSL, be mindful while providing URLs in the csv used for importing and
creating a blog. If your image url is of the form "C://path" or "D://path", convert it to /mnt/c/path or /mnt/d/path.
Do not forget to use front slashes.