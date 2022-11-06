from flask import Flask, render_template, request
app = Flask(__name__)

todoList = [
 {'id' : 1, 'description' : 'SS1 Assignment 1', 'status' : 'Done'},
 {'id' : 2, 'description' : 'SS1 Assignment 2', 'status' : 'Doing'},
 {'id' : 3, 'description' : 'SS1 Final', 'status' : 'Doing'}
]

idSize=len(todoList)

@app.route('/')
def home():
    return render_template('index.html', todoList=todoList)

@app.route('/add', methods=['POST'])
def add():
    if len(todoList)==0:
        newId = 1
    else:
        newId=todoList[-1]['id']+1
    newItem={'id' : newId, 'description' : request.values['itemDescription'] , 'status' : 'Doing'}
    todoList.append(newItem)
    return render_template('index.html', todoList=todoList)

@app.route('/edit', methods=['POST'])
def edit():
    editItemId = int(request.values['itemID']) 
    editItemDesc = request.values['itemDescription']
    editAction = request.values['clickBtn']
    editStatus = request.form.get('itemStatus')
    if editAction=='delete':
        return remove()
    else:
        for i in range(len(todoList)):
            if todoList[i]['id']==editItemId:
                if request.form.get('itemStatus')=='Doing':
                    todoList[i] = {'id': editItemId,'description' : editItemDesc, 'status' : 'Done'}
                    break
                else:
                    todoList[i] = {'id': editItemId,'description' : editItemDesc, 'status' : 'Doing'}
                    break
        return render_template('index.html', todoList=todoList)

def remove():
    editItemId = int(request.values['itemID']) 
    for item in todoList:
        if item['id']==editItemId:
            todoList.remove(item)
            break
    return render_template('index.html', todoList=todoList)