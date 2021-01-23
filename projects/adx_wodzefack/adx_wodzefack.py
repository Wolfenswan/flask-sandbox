from dataclasses import dataclass

@dataclass
class WoD:
    belastung:int
    pause:int
    exc1:str
    exc2:str
    exc3:str
    video:str = ''
    online_training:str = ''

    def video_url(self):
        if (self.video != ''):
            return f'<a href="{self.video}" target="_blank">Video</a>'
        else:
            return 'Noch keins!'

# Who needs databases if they got a dictionary?
WORKOUTS = {
    'default': WoD(99,99,'Liegestütz','Liegestütz','Liegestütz'),
    '23.01': WoD(20,10,'Kniebeuge','Liegestütz','Bodenklimmzug'),
    '24.01': WoD(20,10,'Klapplanke','Seestern','Russian Twist'),
    '25.01': WoD(99,99,'Klapplanke','Seestern','Russian Twist', '', '11:30'),
}

def get_workout(date):
    key = date.strftime("%d.%m")
    return WORKOUTS.get(key,WORKOUTS['default'])