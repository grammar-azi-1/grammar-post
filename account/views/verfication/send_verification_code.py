import logging
from rest_framework.views import APIView, Response, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from account.serializers.verification import SendVerificationCodeSerializer
from account.models import DailyMessage
from account.tasks import send_verification_email

__all__ = ["SendVerificationCodeView"]

logger = logging.getLogger(__name__)


class SendVerificationCodeView(APIView):
    """
    View for handling the sending of verification codes via email.

    This view receives a POST request with an email address and sends a verification code
    to that email. It also ensures the number of requests is limited based on the daily
    message sending constraints.
    """

    @swagger_auto_schema(
        request_body=SendVerificationCodeSerializer,
        tags=["Verification"],
        operation_summary="Send verification code via email",
        operation_description=(
            "Receives an email address and sends a verification code to it. "
            "This operation is rate-limited by daily message constraints."
        ),
        responses={
            200: openapi.Response(description="Verification code sent successfully."),
            400: openapi.Response(description="Invalid input data."),
            429: openapi.Response(description="Too many requests. Daily limit reached."),
        },
    )
    def post(self, request) -> Response:
        """
        Handle POST request to send a verification code to the provided email address.

        Args:
            request (Request): The request object containing the email.

        Returns:
            Response: The response containing a success or error message.
        """
        logger.info(
            "Send verification code request received for email: %s", 
            request.data.get("email")
        ) 

        serializer = SendVerificationCodeSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            logger.info("Email validated: %s", email)

            message_response = DailyMessage.send_message(email)

            if message_response != "Message sent successfully!":
                logger.warning(
                    "Too many requests for email: %s. Response: %s", 
                    email,
                    message_response
                )

                return Response(
                    {"error": message_response},
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )

            send_verification_email.delay(email)
            logger.info("Verification code sent to email: %s", email)

            return Response(
                {"message": "Verification code sent."},
                status=status.HTTP_200_OK
            )

        logger.error(
            "Invalid data provided: %s",
            serializer.errors
        )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )