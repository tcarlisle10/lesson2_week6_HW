from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from connection import connection, Error

app = Flask(__name__)
ma = Marshmallow()


class MembersSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    user_name = fields.String(required=True)
    email = fields.String()
    address = fields.String()
    phone = fields.String()

    class Meta:
        fields = ("user_id", "email", "address", "phone")

members_schema = MembersSchema() 
members_schema = MembersSchema(many=True)

@app.route('/') 
def home():
    return "Hello"

@app.route('/page2') 
def cool():
    return "New Page!"

@app.route('/members', methods = ['GET'])
def get_member():
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary=True) 
            
            
            query = "SELECT * FROM users;"

            cursor.execute(query)

            member = cursor.fetchall()

        

        except Error as e:
            print(f"Error: {e}")
            
        
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return members_schema.jsonify(member)
            

@app.route("/members", methods=['POST'])
def add_member():
    try:
        members_data = members_schema.load(request.json)
    
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()

           
            new_member = (members_data['user_name'], members_data['email'], members_data['address'], members_data['phone'])

            
            query = "INSERT INTO users (user_name, email, address, phone) VALUES  (%s, %s, %s)"

            
            cursor.execute(query, new_member)
            conn.commit()

            return jsonify({'message': 'New member added successfully!'}), 201
        
        except Error as e:
            return jsonify(e.messages), 500
        
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({'error': 'Database connection failed'}), 500
    

@app.route('/members/<int:id>', methods = ['PUT']) 
def update_members(id):
    try:
        member_data = members_schema.load(request.json)

    except ValidationError as e:
        return jsonify(e.messages), 400
    
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()

            
            check_query = "SELECT * FROM users WHERE id = %s;"
            cursor.execute(check_query, (id,))
            members = cursor.fetchone()
            if not members:
                return jsonify({"error": "Member was not found"}), 404

            
            updated_member = (member_data['user_name'], member_data['email'], member_data['address'], member_data['phone'])

            query = "UPDATE user SET user_id = %s, email = %s, address = %s, phone = %s WHERE id = %s;"
            cursor.execute(query, updated_member)
            conn.commit()

            return jsonify({'message': f"Successfully updated member, id= {id}"}), 200
        
        except Error as e:
            return jsonify(e.messages), 500
        
        finally:
            cursor.close()
            conn.close()

    else:
        return jsonify({"error": "Database connection failed"}), 500
    


@app.route("/members/<int:id>", methods = {'DELETE'})
def delete_member(id):

    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()

            check_query = "SELECT * FROM users WHERE id = %s;"
            cursor.execute(check_query, (id,))
            member = cursor.fetchone()
            if not member:
                return jsonify({"error": "Member was not found"}), 404
            
            query = "DELETE FROM users WHERE id = %s;"
            cursor.execute(query, (id,))
            conn.commit()

            return jsonify({"message": f"Member {id} was successfully deleted"})
        
        except Error as e:
            return jsonify(e.messages), 500

        finally:
            cursor.close()
            conn.close()

    else:
        return jsonify({"error": "Database connection failed"}), 500


if __name__ == '__main__':
    app.run(debug=True)


@app.route("/workouts", methods=['POST'])
def schedule_workout():
    data = request.get_json()
    user_id = data.get('user_id')
    type_id = data.get('type_id')
    session_date = data.get('session_date')
    duration = data.get('duration')
    
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO workout_sessions (user_id, type_id, session_date, duration) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (user_id, type_id, session_date, duration))
            conn.commit()
            
            return jsonify({"message": "Workout session scheduled successfully"}), 201
        
        except Error as e:
            return jsonify(e.messages), 500
        
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500

@app.route("/workouts/<int:session_id>", methods=['PUT'])
def update_workout(session_id):
    data = request.get_json()
    type_id = data.get('type_id')
    session_date = data.get('session_date')
    duration = data.get('duration')
    
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "UPDATE workout_sessions SET type_id = %s, session_date = %s, duration = %s WHERE session_id = %s"
            cursor.execute(query, (type_id, session_date, duration, session_id))
            conn.commit()
            
            if cursor.rowcount == 0:
                return jsonify({"error": "Workout session not found"}), 404
            
            return jsonify({"message": "Workout session updated successfully"})
        
        except Error as e:
            return jsonify(e.messages), 500
        
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500

@app.route("/workouts/<int:session_id>", methods=['GET'])
def view_workout(session_id):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM workout_sessions WHERE session_id = %s"
            cursor.execute(query, (session_id,))
            workout = cursor.fetchone()
            
            if workout is None:
                return jsonify({"error": "Workout session not found"}), 404
            
            return jsonify({
                "session_id": workout[0],
                "user_id": workout[1],
                "type_id": workout[2],
                "session_date": workout[3],
                "duration": workout[4]
            })
        
        except Error as e:
            return jsonify(e.messages), 500
        
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500
    
@app.route("/members/<int:user_id>/workouts", methods=['GET'])
def get_member_workouts(user_id):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = """
                SELECT session_id, type_id, type_name, session_date, duration
                FROM workout_sessions 
                JOIN workout_types  ON type_id = type_id
                WHERE user_id = %s
            """
            cursor.execute(query, (user_id,))
            workouts = cursor.fetchall()
            
            if not workouts:
                return jsonify({"message": "No workouts found for this member"}), 404
            
            workout_list = []
            for workout in workouts:
                workout_list.append({
                    "session_id": workout[0],
                    "type_id": workout[1],
                    "type_name": workout[2],
                    "session_date": workout[3],
                    "duration": workout[4]
                })
            
            return jsonify({"workouts": workout_list})
        
        except Error as e:
            return jsonify(e.messages), 500
        
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500