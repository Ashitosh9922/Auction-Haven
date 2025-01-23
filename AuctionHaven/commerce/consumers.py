import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.core.mail import send_mail
from django.conf import settings
from auctions.models import Listing, Bid, User

class BidConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Set up the WebSocket connection
        self.room_name = "auction_room"  
        self.room_group_name = f"auction_{self.room_name}"

        # Add the WebSocket connection to the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Remove the WebSocket connection from the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Parse the incoming WebSocket message
        text_data_json = json.loads(text_data)
        action = text_data_json.get("action", "")
        data = text_data_json.get("data", {})

        if action == "place_bid":
            await self.handle_bid(data)
        elif action == "create_listing":
            await self.handle_new_listing(data)

    async def handle_bid(self, data):
        """
        Handle a new bid placed by a user.
        """
        try:
            listing_id = data.get("listing_id")
            user_id = data.get("user_id")
            bid_value = data.get("bid_value")

            # Validate and save the bid
            listing = await sync_to_async(Listing.objects.get)(id=listing_id)
            user = await sync_to_async(User.objects.get)(id=user_id)

            # Check if the bid is valid (greater than the starting value and current bids)
            highest_bid = await sync_to_async(listing.bids.order_by('-value').first)()
            if highest_bid and bid_value <= highest_bid.value:
                await self.send(json.dumps({
                    "error": "Bid must be higher than the current highest bid."
                }))
                return

            # Save the new bid
            bid = await sync_to_async(Bid.objects.create)(
                listing=listing,
                user=user,
                value=bid_value
            )

            # Send email notification to the listing owner
            await self.send_email_notification(bid)

            # Notify all users in the group about the new bid
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "new_bid",
                    "bid": {
                        "user": user.username,
                        "value": bid_value,
                        "timestamp": str(bid.created_at),
                    }
                }
            )

        except Exception as e:
            await self.send(json.dumps({"error": str(e)}))

    async def handle_new_listing(self, data):
        """
        Handle a new listing creation.
        """
        try:
            title = data.get("title")
            description = data.get("description")
            user_id = data.get("user_id")

            # Validate and create the new listing
            user = await sync_to_async(User.objects.get)(id=user_id)

            listing = await sync_to_async(Listing.objects.create)(
                title=title,
                description=description,
                user=user
            )

            # Broadcast the new listing to all users in the group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "new_listing",
                    "listing": {
                        "title": listing.title,
                        "description": listing.description,
                        "user": listing.user.username,
                        "created_at": str(listing.created_at),
                    }
                }
            )

            # Send email notification to all users
            await self.send_listing_email_notification(listing)

        except Exception as e:
            await self.send(json.dumps({"error": str(e)}))

    async def send_email_notification(self, bid):
        """
        Send an email notification to the listing owner when a new bid is placed.
        """
        listing = bid.listing
        user = bid.user

        # Get the listing owner's email
        owner_email = listing.user.email

        subject = f"New Bid on Your Listing: {listing.title}"
        message = f"A new bid of ${bid.value} has been placed by {user.username} for your auction item '{listing.title}'."

        # Send email asynchronously
        await sync_to_async(send_mail)(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [owner_email]
        )

    async def send_listing_email_notification(self, listing):
        """
        Send an email notification to all users when a new listing is created.
        """
        users = await sync_to_async(User.objects.all)()

        subject = f"New Listing Created: {listing.title}"
        message = f"A new listing has been created: {listing.title}. Check it out!"

        # Send email asynchronously to all users
        for user in users:
            await sync_to_async(send_mail)(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email]
            )

    async def new_bid(self, event):
        """
        Broadcast the new bid to all WebSocket clients in the group.
        """
        bid = event["bid"]
        await self.send(text_data=json.dumps({
            "action": "new_bid",
            "bid": bid
        }))

    async def new_listing(self, event):
        """
        Broadcast the new listing to all WebSocket clients in the group.
        """
        listing = event["listing"]
        await self.send(text_data=json.dumps({
            "action": "new_listing",
            "listing": listing
        }))
