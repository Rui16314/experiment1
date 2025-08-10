from firebase_setup import db
from datetime import datetime

def send_message(room_id, sender, message):
    chat_ref = db.collection('chat_rooms').document(room_id).collection('messages')
    chat_ref.add({
        'sender': sender,
        'message': message,
        'timestamp': datetime.utcnow()
    })

def get_messages(room_id):
    chat_ref = db.collection('chat_rooms').document(room_id).collection('messages')
    messages = chat_ref.order_by('timestamp').stream()
    return [{'sender': msg.get('sender'), 'message': msg.get('message')} for msg in messages]
