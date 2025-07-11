from rest_framework import serializers
from .models import Listing, Bid, Comment, User

class ListingSerializer(serializers.ModelSerializer):
  class Meta:
    model = Listing
    fields = '__all__'

class BidSerializer(serializers.ModelSerializer):
  class Meta:
    model = Bid
    fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'email']
