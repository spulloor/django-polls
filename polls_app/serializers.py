from rest_framework import serializers
from polls_app.models import Poll, PollChoice

from polls_app.models import CustomUser


class PollChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollChoice
        fields = ['id', 'choice_title', 'votes']

    def update(self, instance, validated_data):
        user = self.context['request'].user

        # Check if the user is the creator of the poll
        if user != instance.poll_creation_user:
            raise serializers.ValidationError("You are not allowed to update this choice.")

        instance.choice_title = validated_data['choice_title']
        instance.save()
        return instance




class PollSerializer(serializers.ModelSerializer):

    options = PollChoiceSerializer(many=True)

    class Meta:
        model = Poll
        fields = ['id', 'title', 'options']


    def create(self, validated_data):
        
        options_data = validated_data.pop('options')
        poll = Poll.objects.create(**validated_data, user=self.context['request'].user)

        for option_data in options_data:
            choice = PollChoice.objects.create(**option_data, poll_creation_user=self.context['request'].user)
            poll.options.add(choice)

        return poll
    

# User login & registration classes
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email')


class PasswordConfirmationField(serializers.CharField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.error_messages['password_mismatch'] = "Passwords do not match."

    def run_validation(self, value):
        password = self.parent.initial_data.get('password')
        if value != password:
            self.fail('password_mismatch')
        return value

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = PasswordConfirmationField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        print(password)
        print(validated_data['email'])
        user = CustomUser(username=validated_data['username'], email=validated_data['email'])
        user.set_password(password)
        user.save()
        return user