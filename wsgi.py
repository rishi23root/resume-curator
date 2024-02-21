from flaskApi import app 

if __name__ == '__main__':
    app.run(debug=False,port=5000)







# testing only
# import json
# from flaskApi.flaskUtils import varifyData 

# # read json file in this folder
# with open('./tests/data.json') as f:
#     data = json.load(f)
#     d = varifyData(data= data)
#     print(d)