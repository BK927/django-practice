from random import randint
from django.http import response
from django.shortcuts import redirect, render
from .models import *

# Create your views here.
def index(request):
  return render(request, 'main/index.html')

def signup(request):
  return render(request, 'main/signup.html')

def join(request):
  name = request.POST['signupName']
  email = request.POST['signupEmail']
  pw = request.POST['signupPW']
  user = User(user_name=name, user_email=email, user_password=pw)
  user.save()
  code = randint(1000, 9999)
  response = redirect('main_verifyCode')
  response.set_cookie('code', str(code))
  response.set_cookie('user_id',user.id)
  # 이메일 발송 함수 호출
  send_result = send(email,code)
  if send_result:
    return response
  else:
    return HttpResponse('이메일 발송에 실패했습니다')

def signin(request):
  return render(request, 'main/signin.html')

def verifyCode(request):
  return render(request, 'main/verifyCode.html')

def verify(request):
  return redirect('main_index.html')

def result(request):
  return render(request, 'main/result.html')

