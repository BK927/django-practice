from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from shareRes.models import *
from .models import *
import keyring


# Create your views here.
def sendEmail(request):
    checked_res_list = request.POST.getlist('checks')
    inputReciever = request.POST['inputReceiver']
    inputTitle = request.POST['inputTitle']
    inputContent = request.POST['inputContent']

    mail_html = f"<html><body>\
                  <h1>맛집 공유</h1>\
                  <p>{inputContent}</br>\
                  발신자님께서 공유하신 맛집은 다음과 같습니다</p>"
    for checked_res_id in checked_res_list:
        restaurant = Restaurant.objects.get(id=checked_res_id)
        mail_html += f"<h2>* 관련 링크</h2>\
                        <p>{restaurant.restaurant_link}</p></br>\
                       <h2>* 상세 내용</h2>\
                        <p>{restaurant.restaurant_content}</p></br>\
                       <h2>* 관련 키워드</h2>\
                        <p>{restaurant.restaurant_keyword}</p></br>\
                    "
    mail_html += "</body></html>"

    #smtp using
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    account = SMTP_Account.objects.get(id=1)
    server.login(user=account.user_name, password=account.password)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = inputTitle
    msg['From'] = "dead4bees927@gmail.com"
    msg['To'] = inputReciever
    mail_html = MIMEText(mail_html, 'html')
    msg.attach(mail_html)
    print(msg['To'], type(msg['To']))
    server.sendmail(msg['From'],msg['To'].split(','),msg.as_string())
    server.quit()
    return HttpResponseRedirect(reverse('index'))
