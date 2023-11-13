## Resume curator 🎯
An automated python-latex workflow to curate resume from some most successful templates 📄

Create your own templates and build your own template with latex and python 💻


## To Run Project
- [ ] clone the repo 👯‍♀️
- [ ] make setup.sh executable and run it (installing smallest version of pdflatex possible)
    ```bash
    sudo chmod +x ./scripts/setup.sh && sudo ./scripts/setup.sh
    ```
- [ ] make path available
    ```bash
    source ~/.bashrc
    source ~/.zshrc # only if you are using zsh
    ```
- [ ] edit the existing `tempalte.json`
- [ ] setup the flask on production server or activate python virtural environment (auto generated in previous steps)
- [ ] run the flask app ```python3 app.py``` || ```python3 main.py```


## How to run for local development
    - server -> `python wsgi.py`
    - locally - > `python main.py` # for just create a pdf from data and all templates
    - test -> `pytest`


## To Running the Project on server env (production server)
- [ ] clone the repo 👯‍♀️
- [ ] edit the `/scripts/constants.sh` file and add the server domain name 
- [ ] make setup.sh executable and run it 
    ```bash
    sudo chmod +x ./scripts/oneForAll.sh && sudo ./scripts/oneForAll.sh
    ```
- [ ] make path available 
    ```bash
    source ~/.bashrc
    source ~/.zshrc #if you are using zsh
    ```
- [ ] use it on the server
```bash
routes - 
/test - GET - (only works in debug mode )
/templates - GET - return list of all templates avilable 
/getTemplatePreview - GET and argument of templateName - return base64 image path
/download_template - GET  - returns the template file json
/create_resume - POST and expects {template,data} - returns pdf file with your template and data
```



---
## Open to contribution 🤝
0. fork the repo
1. clone the repo
3. create a new issue 
3. make changes
4. push the changes
5. create a pull request


---
**Note:**
Any template name which cointains `test` in name will be executed by default🛡️


### Have fun curating your resume! 🎉
