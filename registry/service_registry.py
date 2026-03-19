from collections import defaultdict

class ServiceRegistry:
    def __init__(self, event_bus):
        self.registry = defaultdict(list)
        event_bus.subscribe('INSTANCE_STARTED',)
        event_bus.subscribe('INSTANCE_STOPPED',)

    def handle_start_instance(self, data):
        service_name = data['service_name']
        instance_info = data['instance_info']

        for instance in self.registry[service_name]:
            if instance['id'] == instance_info['id']:
                return
            
        self.registry[service_name].append(instance_info)


    def handle_stop_instance(self, data):
        service_name = data['service_name']
        instance_id = data['instance_id']

        self.registry[service_name] = [instance for instance in self.registry[service_name] if instance['id'] != instance_id]

        if not self.registry[service_name]:
            del self.registry[service_name]


    def get_instances(self, service_name):
        return list(self.registry.get(service_name, []))


