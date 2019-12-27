import time
import datetime as dt

class Thought:
    def __init__(self,id,time,thought):
        self.user_id = id
        self.timestamp = time
        self.thought = thought
    
    def __repr__(self):
        return f'Thought(user_id={self.user_id!r},timestamp={self.timestamp!r} , thought={self.thought!r})'
    
    def __str__(self):
        return f'{self.timestamp.strftime("[%m-%d-%Y %H:%M:%S]")} user {self.user_id}: "{self.thought}"'
        # return f'{self.timestamp}'
    
    def __eq__(self,other):
        return isinstance(other,Thought) and (self.user_id == other.user_id) \
            and (self.timestamp == other.timestamp) and (self.thought == other.thought)

    def serialize(self):
        msg = (self.thought).encode()  
        data = b''
        data += self.user_id.to_bytes(8,byteorder='little',signed=False)
        t = int(self.timestamp.timestamp())
        data += t.to_bytes(8,byteorder='little',signed=False)
        data +=(len(msg)).to_bytes(4,byteorder='little',signed=False)
        data += msg
        return data

    def deserialize(data):
        userID = int.from_bytes(data[0:7],byteorder='little')
        epoch_time = int.from_bytes(data[8:15],byteorder='little')
        time_stamp = dt.datetime.fromtimestamp(epoch_time)
        msgLen = int.from_bytes(data[16:19],byteorder='little')
        msg = data[20::].decode()
        return Thought(userID, time_stamp, msg)



