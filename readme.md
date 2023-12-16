## Resume curator 🎯

LaTeX-Python Resume Curator 🚀
Empowers users to create custom resume or cover-letter LaTeX templates using Python 💻
An automated Python-LaTeX workflow to curate resumes.
Create your own templates and build your unique resume with LaTeX and Python 💻

### Key Features:

- Utilizes successful templates for inspiration 📄
- Provides a tool to easily convert LaTeX ideas to PDF 📄
- access to create new custom templates
- access to modify the existing templates

### API Integration:

- HTTP API for seamless and convenient access 🚀
- Checkout path `/swagger` for full API documentation 📖

## To Run Project ❓🔻

- [ ] clone the repo 👯‍♀️

### To Running on local env

- [ ] execute `scripts/setup.sh` script to install dependencies and setup the environment

  ```bash
  ./scripts/setup.sh
  ```

  - updating your system apt packages
  - install texlive (smallest version possible to run pdflatex)
  - updating pip
  - setup pip environment
  - install python dependencies

- [ ] Make path available

  ```bash
  source ~/.bashrc
  source ~/.zshrc # only if you are using zsh
  ```

- [ ] Edit the existing `tempalte.json` file to update it with your own data

- [ ] Activate environment (auto generated in previous steps)

  ```bash
  source venv/bin/activate # linux
  ```

- [ ] run the command to create pdf from the data
  ```bash
  python3 main.py # to create pdf from template.json data of each latex template
  python3 wsgi.py # to run the flask server locally
  ```
  **Note:** reopen the terminal if you are not able to use the command successfully

### To Running on server env (production server)

- [ ] edit the `/scripts/constants.sh` file and add your custom server specifications like - domain name, etc
- [ ] let's make it server ready

  ```bash
  sudo chmod +x ./scripts/oneForAll.sh && sudo ./scripts/oneForAll.sh
  ```

  - updating your system apt packages
  - install texlive (smallest version possible to run pdflatex)
  - updating pip
  - setup pip environment
  - install python dependencies
  - install nginx
  - install gunicorn
  - setup firewall (ufw) and allow ports 80 and 443
  - setup nginx configuration
  - setup gunicorn configuration
  - setup systemd service for gunicorn and nginx
  - setup ssl certificate using certbot

- [ ] and you are all set to go 🚀
      test the server by visiting the domain name you have provided in the `scripts/constants.sh` file

---

### for testing each api endpoint 🧪

```bash
pytest -v
```

---

## Open to contribution 🤝

### Steps to start contributing

0. fork the repo
1. clone the repo
2. create a new issue
3. make changes
4. push the changes
5. create a pull request

---

---

**Note:**
Any template name which cointains `test` in name will not be executed by default🛡️

---

# Have fun curating your resume! 🎉
