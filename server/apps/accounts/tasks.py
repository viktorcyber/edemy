import inngest
from accounts.services import ClerkWebhookService
from django.contrib.auth import get_user_model

from config.client import inngest_client

User = get_user_model()


@inngest_client.create_function(
    fn_id="sync-user-from-clerk",
    trigger=[inngest.TriggerEvent(event="clerk/user.*")],
)
def sync_user_from_clerk(ctx: inngest.Context) -> str:
    evt = ctx.event
    data = evt.data

    match evt.name:
        case "clerk/user.created" | "clerk/user.updated":
            ClerkWebhookService.handle_user_created_or_updated(data)
            return f"Successfully processed {evt.name} for user {data.get('id')}"
        case "clerk/user.deleted":
            clerk_id = data.get("id")
            if clerk_id:
                ClerkWebhookService.handle_user_deleted(clerk_id=clerk_id)
                return f"Successfully deleted user {clerk_id}"
            return "Skipped: Missing user ID for deletion"
        case _:
            return f"Unhandled event type: {evt.name}"
