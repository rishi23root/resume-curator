## Resume curator
an automated python-latex workflow to curate resume from a 2 most successful templates
create your own templates and build your own template with latex and python

---
## To Running the Project
0. clone the repo
1. make setup.sh executable and run it ```sudo chmod +x ./scripts/setup.sh && sudo ./scripts/setup.sh```
2. ```bash
    source ~/.bashrc
    source ~/.zshrc #if you are using zsh
    ```
2. edit the existing `tempalte.json`
3. setup the flask on production server 
4. run the flask app ```python3 app.py```


# To-do:
- [x] add 1 column resume
- [x] add 2 column resume
- [ ] add more templates
- [x] add api to edit the template and download the resume
    - [x] give option to upload json file
    - [x] add error if all the fields are not filled or found in the uploaded json
- [ ] setup the flask on production server


<!-- open to contribution section -->
---
## Open to contribution 
1. fork the repo
2. clone the repo
3. make changes
4. push the changes
5. create a pull request
