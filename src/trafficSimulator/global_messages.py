import uuid

class Messaging():
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.active_agents = list()
        self.messages = list()

    def register_agent(self, agent_uuid):
        self.active_agents.append(agent_uuid)
    
    def unregister_agent(self, agent_uuid):
        self.active_agents.remove(agent_uuid)

    def send_message(self, content):
        self.messages.append(content)

    def read_messages(self):
        return self.messages
