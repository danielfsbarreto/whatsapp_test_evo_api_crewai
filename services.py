from uuid import NAMESPACE_DNS, uuid5

from clients import CrewaiClient, WhatsappClient
from models import Message, WhatsappRequestBody


class MessageSubmissionService:
    def __init__(self):
        self._crewai_client = CrewaiClient()
        self._whatsapp_client = WhatsappClient()

    def kickoff_interaction(self, request: WhatsappRequestBody):
        if request.data.get("key", {}).get("fromMe") or not request.data.get(
            "message", {}
        ).get("conversation"):
            return

        response = self._create_response(request)
        self._submit_response(request, response)

    def _create_response(self, request: WhatsappRequestBody):
        conversation_id = self._conversation_id(request)
        message = Message(role="user", content=self._user_message(request))
        inputs = {"id": conversation_id, "user_message": message.model_dump()}
        kickoff_id = self._crewai_client.kickoff(inputs)
        result_json = self._crewai_client.status(kickoff_id)
        return Message(**result_json["history"][-1])

    def _conversation_id(self, request: WhatsappRequestBody):
        return str(uuid5(NAMESPACE_DNS, request.data["key"]["senderLid"]))

    def _user_message(self, request: WhatsappRequestBody):
        return request.data["message"]["conversation"]

    def _submit_response(self, request: WhatsappRequestBody, response: Message):
        self._whatsapp_client.send_text(
            number=self._number(request), text=response.content
        )

    def _number(self, request: WhatsappRequestBody):
        return request.data["key"]["remoteJid"].split("@")[0]
