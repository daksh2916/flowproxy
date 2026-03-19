from ..models.api_models import RequestData
import uuid
import httpx

class Proxy:
    def __init__(self, event_bus, service_registry):
        self.event_bus = event_bus
        self.service_registry = service_registry
        self.client = httpx.AsyncClient()

    
    async def emit(self, event_type, data):
        await self.event_bus.emit(event_type, data)

    async def get_request_details(self, request)->RequestData:
        request_id = str(uuid.uuid4())
        request_body = await request.body()

        return RequestData(
        id=request_id,
        method=request.method,
        url=str(request.url),
        headers=dict(request.headers),
        query_parameter=dict(request.query_params),
        body=request_body
    )


    def handle_service(self):
        return "default_service"

   
    def handle_instance(self, instances):
        return instances[0]

    async def forward_request(self,instance, request_data):
        url = f"https://{instance['host']}:{instance['port']}/{request_data.url.path}"

        response = await self.client.request(
            method = request_data.method,
            url = url,
            headers = request_data.headers,
            content = request_data.body
        )

        return response
    

    async def handle_request(self, request):
        request_data = await self.get_request_details(request)

        await self.emit("REQUEST_RECEIVED", {
            "id": request_data.id,
            "path": request_data.url
        })

        service = self.handle_service(request)

        await self.emit("SERVICE_RESOLVED", {
            "request_id": request_data.id,
            "service": service
        })

        instances = self.service_registry.get_instances(service)

        if not instances:
            await self.emit("NO_INSTANCE_AVAILABLE", {
                "request_id": request_data.id,
                "service": service
            })
            return None

        instance = self.handle_instance(instances)

        await self.emit("INSTANCE_CHOSEN", {
            "request_id": request_data.id,
            "instance": instance
        })

        try:
            await self.emit("REQUEST_FORWARDED", {
                "request_id": request_data.id,
                "instance": instance
            })

            response = await self.forward_request(instance, request_data)

            await self.emit("RESPONSE_RECEIVED", {
                "request_id": request_data.id,
                "status_code": response.status_code
            })

            await self.emit("RESPONSE_SENT", {
                "request_id": request_data.id
            })

            return response

        except Exception as e:
            await self.emit("REQUEST_FAILED", {
                "request_id": request_data.id,
                "error": str(e)
            })
            return None