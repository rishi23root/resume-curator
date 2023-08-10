## Resume curator
an automated python-latex workflow to curate resume from a 2 most successful templates
create your own templates and build your own template with latex and python

tested and seems to be working on ubuntu 20.04
---
## To Running the Project locally
0. clone the repo
1. make setup.sh executable and run it ```sudo chmod +x ./scripts/setup.sh && sudo ./scripts/setup.sh```
2. ```bash
    source ~/.bashrc
    source ~/.zshrc #if you are using zsh
    ```
2. edit the existing `tempalte.json`
3. setup the flask on production server 
4. run the flask app ```python3 app.py```

## To Running the Project on server
0. clone the repo
0.5. edit the /scripts/constants.sh file and add the server domain name 
1. make setup.sh executable and run it ```sudo chmod +x ./scripts/oneForAll.sh && sudo ./scripts/oneForAll.sh```
2. ```bash
    source ~/.bashrc
    source ~/.zshrc #if you are using zsh
    ```
3. use it on the server


# To-do:
- [x] add 1 column resume
- [x] add 2 column resume
- [x] add api to edit the template and download the resume
    - [x] give option to upload json file
    - [x] add error if all the fields are not filled or found in the uploaded json
- [x] setup the flask on production server
- [ ] add more templates
- using docker is promissing - mrchoke/texlive:latest or 2023 (version 2023 cheked)


<!-- open to contribution section -->
---
## Open to contribution 
1. fork the repo
2. clone the repo
3. make changes
4. push the changes
5. create a pull request


<!-- todos -->

## Todos errors and bugs solving
1. server is not making logs in the log file
2. gunicorn is responsible ? if not then what is the problem
3. maybe gunicorn is taking logs in the logs files 