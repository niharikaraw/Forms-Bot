from telnetlib import LOGOUT
import uuid
from django.forms import model_to_dict
from django.shortcuts import render
from requests import delete
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Feedback, Options, Questions, Responses
from users.utils import validate_bots, validate_campaign, validate_signup_data
from users.models import Bots, Campaign, ContactUs, CustomUser
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class CreateUserView(APIView):
    
    def post(self, request):
        data = request.data
        print(data)
        first_name = data.get('first_name')
        email = data.get('email')
        phone_number = data.get('phone_number')
        organization = data.get('organization')

        '''if not (first_name and email and phone_number and organization):
            return Response({'message': 'Invalid body passed!'})'''
        validation = validate_signup_data(data)

        if validation:
            return Response({'message': 'Invalid payload', 'details': validation})
        
        user = CustomUser(
            first_name = first_name,
            last_name = data.get('last_name'),
            email = email,
            username = email,
            password = make_password(data.get('password')),
            phone_number = phone_number,
            organization = organization,
            is_premium = data.get('is_premium'),
            is_waitlisted = data.get('is_waitlisted'),
            date_joined = data.get('date_joined')
        )
        user.save()
        return Response({'message': 'User created successfully!'})


class ProfileView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        user = model_to_dict(request.user)
        print(user)
        del user['password']
        del user['is_premium']
        del user['is_waitlisted']
        del user['last_login']
        del user['is_superuser']
        del user['is_staff']
        del user['is_active']
        del user['groups']
        del user['date_joined']
        del user['user_permissions']
        
        return Response({'data': user})


class CampaignView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        data = request.GET
        title = data.get('title')
        campaign = Campaign.objects.filter(user=user).all()
        campaign_list = []
        if title:
            campaign = campaign.filter(title__icontains=title)
            campaign_list = list(campaign.values())
            print(campaign_list)
        else:
            for i in campaign:
                campaign_list.append(model_to_dict(i))
        return Response({'data': campaign_list})
    
    
    def post(self, request):
        user = request.user
        data = request.data
        print(data)
        title = data.get('title')
        description = data.get('description')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        end_message = data.get('end_message')

        validation = validate_campaign(data)

        if validation:
            return Response({'message': 'Invalid payload', 'details': validation})

        campaign = Campaign(
            user = user,
            title = title,
            description = description,
            start_date = start_date,
            end_date = end_date,
            end_message = end_message
        )
        campaign.save()
        return Response({'message': "Campaign created successfully"})


class BotsView(APIView):

    def get(self, request):
        user = request.user
        data = request.GET
        bot = Bots.objects.filter(user=user).all()
        title = data.get('title')
        bot_list = []
        if title:
            bot = bot.filter(title__icontains=title)
            bot_list = list(bot.values())
            print(bot_list)
        else:
            for i in bot:
                bot_obj = model_to_dict(i)
                bot_obj['avatar_image'] = bot_obj['avatar_image'].url if bot_obj['avatar_image'] else None
                bot_obj['intro_image'] = bot_obj['intro_image'].url if bot_obj['intro_image'] else None
                bot_list.append(bot_obj)
        return Response({'data': bot_list})


    def post(self, request):
        user = request.user
        data = request.data
        uid = uuid.uuid4()
        campaign_id = data.get('campaign_id')
        title = data.get('title')
        description = data.get('description')
        intro_text = data.get('intro_text')
        end_message = data.get('end_message')
        avatar_image = data.get('avatar_image')
        intro_image = data.get('intro_image')
        background_url = data.get('background_url')
        questions = data.get('questions')
        help_text = data.get('help_text')

        validation = validate_bots(data)

        if validation:
            return Response({'message': 'Invalid payload', 'details': validation})

        bot = Bots(
            user = user,
            uid = uid,
            campaign_id = campaign_id,
            title = title,
            description = description,
            intro_text = intro_text,
            end_message = end_message,
            avatar_image = avatar_image,
            intro_image = intro_image,
            background_url = background_url,
            questions = questions,
            help_text = help_text
        )

        bot.save()

        for q in questions:
            question = q.get('question')
            question_sequence = q.get('sequence')
            helper_text = q.get('helper_text')
            is_multiple = q.get('is_multiple')
            is_checkbox = q.get('is_required')

            question_obj = Questions(
                bot_id = bot,
                question = question,
                question_sequence = question_sequence,
                helper_text = helper_text,
                is_multiple = is_multiple,
                is_checkbox = is_checkbox
            )
            question_obj.save()
            if 'options' in q:
                options = q.get('options')
                for option in options:
                    options_obj = Options(
                        question_id = question_obj,
                        option_text = option.get('option_text'),
                        option_sequence =option.get('option_sequence')
                    )
                    options_obj.save()


        bot_dict = model_to_dict(bot)
        bot_dict['avatar_image'] = bot_dict['avatar_image'].url if bot_dict['avatar_image'] else None
        bot_dict['intro_image'] = bot_dict['intro_image'].url if bot_dict['intro_image'] else None
                    

        return Response({'message': 'Bot created successfully!'})


    def delete(self, request):
        data = request.data
        bot_id = data.get('bot_id')
        bot = Bots.objects.get(bot_id=bot_id)
        bot.delete()
        return Response({'message': 'Bot deleted successfully!'})

class ResponseView(APIView):

    def get(self,request):
        data = request.GET
        id = data.get('bot_id')
        bot = Bots.objects.filter(uid=id)
        questions = Questions.objects.filter(bot=bot).first()
        bot_obj = model_to_dict(bot)
        bot_obj['avatar_image'] = bot_obj['avatar_image'].url if bot_obj['avatar_image'] else None
        bot_obj['intro_image'] = bot_obj['intro_image'].url if bot_obj['intro_image'] else None
        bot_resp = {'bot': bot_obj}
        question_list = []
        for q in questions:
            question_dict = model_to_dict(q)
            question_dict['options'] = []
            if q.type in [1,2]:
                options = Options.objects.filter(question=q)
                for option in options:
                    opt = model_to_dict(option)
                    question_dict['options'].append(opt)
            question_list.append(question_dict)
            bot_resp['questions'] = question_list

            return Response({'data': bot_resp})
            

    def post(self, request):
        uid = uuid.uuid4()
        data = request.data
        bot_uuid = data.get('bot_uuid')
        bot = Bots.objects.filter(uid=bot_uuid)
        responses =  data.get('responses')
        
        for response in responses:
            response_list = []
            option_id = response.get('option_id')
            question_id = response.get('question_id')
            if option_id:
                response_list.extend(option_id)
                for r in response_list:
                    response_obj = Responses(
                        bot = bot,
                        option_id = r,
                        question_id=question_id,
                        uid = uid
                    )
                    response_obj.save()
        return Response({'message':'responses have been saved successfully'})

class ContactUsView(APIView):
    def post(self, request):
        data = request.data
       
        email = data.get('email')
        contact_number = data.get('contact_number')
        name = data.get('name')
        text = data.get('text')

        contact_us = ContactUs(
            email = email,
            contact_number = contact_number,
            name = name,
            text = text
        )

        contact_us.save()
        return Response({'message': 'Successful!'})


class FeedbackView(APIView):
    def post(self, request):
        data = request.data
        text = data.get('text')
        rating = data.get("rating")
        bot_uuid = data.get("bot_uuid")

        bot = Bots.objects.filter(uid=bot_uuid).first()
        feedback_obj = Feedback(
            bot = bot,
            text = text,
            rating = rating
        )
        feedback_obj.save()
        return Response({'message':'feedback submitted!'})