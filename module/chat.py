from firebase_setup import db
from datetime import datetime

def send_message(room_id: str, sender: str, message: str) -> None:
    """
    Sends a message to the specified chat room.

    Args:
        room_id (str): Unique ID of the chat room.
        sender (str): Username or ID of the sender.
        message (str): Message content.
    """
    chat_ref = db.collection('chat_rooms').document(room_id).collection('messages')
    chat_ref.add({
        'sender': sender,
        'message': message,
        'timestamp': datetime.utcnow()
    })

def get_messages(room_id: str, limit: int = 50) -> list:
    """
    Retrieves messages from the specified chat room, ordered by timestamp.

    Args:
        room_id (str): Unique ID of the chat room.
        limit (int): Maximum number of messages to retrieve.

    Returns:
        List[dict]: List of messages with sender, content, and timestamp.
    """
    chat_ref = db.collection('chat_rooms').document(room_id).collection('messages')
    messages = chat_ref.order_by('timestamp').limit(limit).stream()
    return [{
        'sender': msg.get('sender'),
        'message': msg.get('message'),
        'timestamp': msg.get('timestamp')
    } for msg in messages]

