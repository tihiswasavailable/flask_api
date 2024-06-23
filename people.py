from datetime import datetime
from flask import jsonify, request

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

PEOPLE = {}
current_id = 0
def read_all():
    return list(PEOPLE.values())

def create():
    global current_id
    try:
        data = request.get_json()

        if not data or 'fname' not in data or 'lname' not in data:
            raise ValueError("First name and last name are required")
        
        fname = data['fname']
        lname = data['lname']
        
        new_id = 1
        while new_id in PEOPLE:
            new_id += 1

        current_id = new_id
        new_person = {
            "id": new_id,
            "fname": fname,
            "lname": lname,
        }
        PEOPLE[new_id] = new_person

        return jsonify({"message": "Person created successfully", "person": new_person}), 201

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        return jsonify({"error": "Failed to process request", "details": str(e)}), 500
    

def read_by_id(id):
    try:
        person = PEOPLE[int(id)]
        return jsonify(person), 200
    except KeyError:
        return jsonify({"error": f"Person with ID = {id} not found"}), 404

def read_by_fname(fname):
    people = [person for person in PEOPLE.values() if person['fname'] == fname]
    if people:
        return jsonify(people), 200
    else:
        return jsonify({"error": f"Person with first name = {fname} not found"})

def read_by_lname(lname):
    people = [person for person in PEOPLE.values() if person['lname'] == lname]
    if people:
        return jsonify(people), 200
    else:
        return jsonify({"error": f"Person with last name = {lname} not found"})
    
def update(id):
    try:
        data = request.get_json()
        if not data or 'fname' not in data or 'lname' not in data:
            raise ValueError("First name and last name are required")
        
        fname = data['fname']
        lname = data['lname']
        person = PEOPLE[int(id)]
        person['fname'] = fname
        person['lname'] = lname
        PEOPLE[int(id)] = person

        return jsonify({"message": "Person updates successfully"}), 200
    except KeyError:
        return jsonify({"error": f"Person with ID = {id} not found"}), 404
    
    except ValueError as value:
        return jsonify({"error": str(value)}), 400
    
    except Exception as e: 
        return jsonify({"error": "Failed to process request", "details": str(e)}), 500

def delete(id):
    try:
        print(f"Deleting person with ID: {id}")

        id = int(id)
        if id not in PEOPLE:
            return jsonify({"error": f"Person with ID = {id} not found", "id": id}), 404
        
        del PEOPLE[id]
        return jsonify({"message": "Person wit ID = {id} was successfully deleted"}), 204
    
    except ValueError:
        return jsonify({"error": "Invalid ID provided"}), 400
    
    except Exception as e:
        return jsonify({"error": "Faild to process request", "details":str(e)}), 500