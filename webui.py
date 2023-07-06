import json
import string
from pprint import pprint
from time import sleep as nap
import random

import streamlit as st

# Load the JSON file


# Save the JSON file
def save_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def main():
    st.title("Resume Curator")

    # ask for template file to add
    data = {}

    # st.write("filename:", uploaded_file.name)
    st.write(data)

    # file_path = st.text_input(
    #     "Enter the path of the JSON file:") or 'template.json'
    # data = load_json_file(file_path )

    # if data:
    #     st.subheader("Personal Information")
    #     data['basics']['name'] = st.text_input("Name", data['basics']['name'])
    #     data['basics']['label'] = st.text_input(
    #         "Label", data['basics']['label'])
    #     data['basics']['image'] = st.text_input(
    #         "Image URL", data['basics']['image'])
    #     data['basics']['email'] = st.text_input(
    #         "Email", data['basics']['email'])
    #     data['basics']['phone'] = st.text_input(
    #         "Phone", data['basics']['phone'])
    #     data['basics']['url'] = st.text_input("URL", data['basics']['url'])
    #     data['basics']['summary'] = st.text_area(
    #         "Summary", data['basics']['summary'])

    #     st.subheader("Location")
    #     data['basics']['location']['address'] = st.text_input(
    #         "Address", data['basics']['location']['address'])
    #     data['basics']['location']['postalCode'] = st.text_input(
    #         "Postal Code", data['basics']['location']['postalCode'])
    #     data['basics']['location']['city'] = st.text_input(
    #         "City", data['basics']['location']['city'])
    #     data['basics']['location']['countryCode'] = st.text_input(
    #         "Country Code", data['basics']['location']['countryCode'])
    #     data['basics']['location']['region'] = st.text_input(
    #         "Region", data['basics']['location']['region'])

    #     st.header("Experience")
    #     for index,work in enumerate(data['work']):
    #         with st.expander(f"Work Experience {index+1}"):
    #             work['name'] = st.text_input("Company Name", work['name'])
    #             work['position'] = st.text_input("Position", work['position'])
    #             work['url'] = st.text_input("URL", work['url'])
    #             work['startDate'] = st.text_input(
    #                 "Start Date", work['startDate'])
    #             work['isWorkingHere'] = st.checkbox(
    #                 "Currently Working Here", value=work['isWorkingHere'])
    #             if not work['isWorkingHere']:
    #                 work['endDate'] = st.text_input(
    #                     "End Date", work['endDate'])
    #             work['summary'] = st.text_area("Summary", work['summary'])

    #     # ... Add other fields and sections as per your resume structure

    #     if st.button("Save"):
    #         # print(data)on screen
    #         st.text_area("JSON Output", json.dumps(data, indent=4))
    #         # save_json_file(file_path, data)
    #         # st.success("Resume saved successfully!")


class ResumeCurator:
    def __init__(self, templateFile='template.json'):
        st.set_page_config(
            layout='wide'
        )

        self.templateFileName = templateFile

        # local copy of template file
        self.template = self.load_json_file(self.templateFileName)

        # first instance of the uploaded file to check for updates
        self.UploadedFileData = self.template.copy()

        # data variable to store the resume updated data
        if 'data' not in st.session_state:
            st.session_state.data = self.template.copy()

        st.session_state.title = f"Resume Curator"
        self.possibleKeys = ['title', 'name', 'institution', 'network']

        self.mustHaveFiels = list(self.template.keys())

    # utils functions
    def load_json_file(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    def verify_json_data(self, jsonData):
        # get all the keys in template
        templateKeys = self.template.keys()
        placeholder = st.empty()
        with placeholder.container():
            counter = 0
            for key in self.mustHaveFiels:
                if key in templateKeys:
                    # print(key)
                    counter += 1
                    string = f"📗 {counter}. key : {str(key)} not found in json data, added with default value"
                    st.write(string)
                    jsonData[key] = self.template[key]
                    nap(.05)
            nap(1)
        placeholder.empty()
        return jsonData

    def generateUUID(self, length=6):
        # Generate a random string of specified length
        letters_and_digits = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(letters_and_digits)
                                for _ in range(length))
        return random_string

    def ifDataEdited(self):
        return st.session_state.data != self.UploadedFileData

    # element functions
    def upload_resumeJson(self):
        # heading to upload resume json
        st.subheader("Upload Resume JSON")
        uploaded_file = st.file_uploader(
            "Choose your template file or start editing this one to create a new template 😎",
            type="json",
            key="upload_resumeJson",
            accept_multiple_files=False
            # on_change=lambda file: st.session_state.data := json.loads(file.read())
        )

        if uploaded_file is None:
            st.session_state.data = self.load_json_file(self.templateFileName)
        else:
            # process the upload file
            bytes_data = uploaded_file.read()
            # convert the bytes to json data
            josnData = json.loads(bytes_data)
            # verify if all the fields are present
            # if not add them with default values
            josnData = self.verify_json_data(josnData)
            # print(josnData.keys())

            # cheeck if user has unsaved changes else pass
            if self.ifDataEdited():
                # ask for confirmation
                warn = st.warning(
                    "You have unsaved changes. Uploading a new file will discard the current changes. Do you want to continue editing?, click save to save files or generate resume")

                button_placeholder = st.empty()
                if button_placeholder.button("Yes, continue without saving (not recommended)", use_container_width=True):
                    warn.empty()
                    # print(dir(uploaded_file))
                    uploaded_file.close()

                    # Remove the button
                    button_placeholder.empty()

            # update the data variables with the new uploaded file data
            st.session_state.data = josnData.copy()
            self.UploadedFileData = josnData.copy()

    def JsonRender(self, label):
        possibleKeys = ['title', 'name', 'institution', 'network']

        def listWithDictAsValue(*subLabel, data=""):
            if len(subLabel) == 1:
                dataSouce = data or st.session_state.data[subLabel[0]]
            else:
                dataSouce = data or st.session_state.data[subLabel[0]
                    ][subLabel[1]]
            # dataSouce = data or st.session_state.data[subLabel]
            tabs = st.tabs(
                [data[i] for data in dataSouce for i in data.keys() if i in possibleKeys])
            for index, tab in enumerate(tabs):
                with tab:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.button("Edit", key=self.generateUUID())
                    with col2:
                        st.button("delete", key=self.generateUUID())
                    entry = dataSouce[index]
                    for key, val in entry.items():
                        if len(subLabel) == 1:
                            st.session_state.data[subLabel[0]][index][key] = st.text_input(
                                key, val, key=self.generateUUID())
                        else:
                            st.session_state.data[subLabel[0]][subLabel[1]][index][key] = st.text_input(
                                key, val, key=self.generateUUID())

        st.header(label.capitalize(), anchor=False)
        with st.expander("Edit", expanded=False):
            dataSouce = st.session_state.data[label]

            if type(dataSouce) == list:
                listWithDictAsValue(label, data=dataSouce)
            else:
                for key, val in dataSouce.items():
                    if type(val) == dict:
                        st.subheader(key.capitalize(), anchor=False)
                        for key2, val2 in val.items():
                            st.session_state.data[label][key][key2] = st.text_input(
                                key2, val2, key=self.generateUUID())
                    elif type(val) == list:
                        st.subheader(key.capitalize(), anchor=False)
                        listWithDictAsValue(label, key, data=val)
                    else:
                        st.session_state.data[label][key] = st.text_input(
                            key.capitalize(), val, key=self.generateUUID())

    def staticJsonRender(self, data):
        # globals data
        # basic
        st.subheader("Personal Information")
        with st.expander("Edit", expanded=False):
            data['basics']['name'] = st.text_input(
                "Name", data['basics']['name'])
            data['basics']['label'] = st.text_input(
                "Label", data['basics']['label'])
            data['basics']['image'] = st.text_input(
                "Image URL", data['basics']['image'])
            data['basics']['email'] = st.text_input(
                "Email", data['basics']['email'])
            data['basics']['phone'] = st.text_input(
                "Phone", data['basics']['phone'])
            data['basics']['url'] = st.text_input("URL", data['basics']['url'])
            data['basics']['summary'] = st.text_area(
                "Summary", data['basics']['summary'])

        st.subheader("Location")
        with st.expander("Edit", expanded=False):
            data['basics']['location']['address'] = st.text_input(
                "Address", data['basics']['location']['address'])
            data['basics']['location']['postalCode'] = st.text_input(
                "Postal Code", data['basics']['location']['postalCode'])
            data['basics']['location']['city'] = st.text_input(
                "City", data['basics']['location']['city'])
            data['basics']['location']['countryCode'] = st.text_input(
                "Country Code", data['basics']['location']['countryCode'])
            data['basics']['location']['region'] = st.text_input(
                "Region", data['basics']['location']['region'])

        st.subheader("Social Profiles")
        profiles = st.session_state.data['basics']['profiles']        

        if st.session_state.data['basics']['profiles']:
            for index in range(len(st.session_state.data['basics']['profiles'])):
                with st.expander(profiles[index]['network'], expanded=False):                
                    *a, colx, col = st.columns([1]*10)
                    addProfile = colx.button('Add New', type='secondary', key=st.session_state.data['basics']['profiles'][index]['network'] + str(index))
                    deleteProfile = col.button('Delete', type='primary', key=st.session_state.data['basics']['profiles'][index]['network'] + str(index+879))
                    if addProfile:
                        st.session_state.data['basics']['profiles'].append({
                            "network": "new",
                            "username": "",
                            "url": ""
                        })

                    if deleteProfile:
                        st.session_state.data['basics']['profiles'].pop(index)

                    st.session_state.data['basics']['profiles'][index]['network'] = st.text_input(
                        "network", st.session_state.data['basics']['profiles'][index]['network'], key=st.session_state.data['basics']['profiles'][index]['network']+st.session_state.data['basics']['profiles'][index]['network'])
                    st.session_state.data['basics']['profiles'][index]['username'] = st.text_input(
                        "username", st.session_state.data['basics']['profiles'][index]['username'], key=st.session_state.data['basics']['profiles'][index]['network']+st.session_state.data['basics']['profiles'][index]['username'])
                    st.session_state.data['basics']['profiles'][index]['url'] = st.text_input(
                        "url", st.session_state.data['basics']['profiles'][index]['url'], key=st.session_state.data['basics']['profiles'][index]['network']+st.session_state.data['basics']['profiles'][index]['url'])
            # index += 1
        st.write(len(st.session_state.data['basics']['profiles']))
        #     # with tab:
        #     #     *a, colx, col = st.columns([1]*10)
        #     #     addProfile = colx.button(
        #     #         'Add New', type='secondary', key=self.generateUUID())
        #     #     deleteProfile = col.button(
        #     #         'Delete', type='primary', key=self.generateUUID())

        #         # create input for each element in the profile
            # val = 'kfalsjdkl'
            # justAtest = st.text_input(" Network", val, key=self.generateUUID())
            # val = justAtest
            # st.write(index,justAtest)
            # allProfiles[index]['network'] = st.text_input(" Network", allProfiles[index]['network'], key=self.generateUUID())
            # allProfiles[index]['username'] = st.text_input("Username", allProfiles[index]['username'], key=self.generateUUID())
            # allProfiles[index]['url'] = st.text_input("Url", allProfiles[index]['url'], key=self.generateUUID())

        #     # data['basics']['profiles'].insert(index, {
        #     #     'network': network,
        #     #     'username': username,
        #     #     'url': url,
        #     #     })
        # st.write(data['basics']['profiles'],allProfiles)

        # st.write(data['basics']['profiles'])

        # with st.expander("Edit", expanded=False):
        #     # create columns for edit button and add more btn then make tabs
        #     # for each social profile

        #     st.write("Social Profiles will be rendered here")

        return data

    def runner(self):
        st.title(st.session_state.title)

        # col1,col2 = st.columns(2)
        # with col1:
        self.upload_resumeJson()

        if self.ifDataEdited():
            st.write('changes are there download the updated file', anchor=False)
        st.session_state.data = self.staticJsonRender(st.session_state.data)
        st.write(st.session_state.data['basics']['name'])

        
        # try forms
        # data = st.session_state.data
        # st.session_state.data = self.JsonRender2(data)
        # if st.session_state.data:
        #     for filed in self.mustHaveFiels:
        #         self.JsonRender(filed)
        # with col2:
        #     st.subheader("Preview", anchor=False)
        #     st.write("preview will be rendered here")


if __name__ == "__main__":
    # main()
    ct = ResumeCurator()
    ct.runner()
