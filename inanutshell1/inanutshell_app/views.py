from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import default_storage
from inanutshell_app.models import files
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
import boto3

from .forms import frm_docupload
from inanutshell import settings

def login(request):
    return render(request,'inanutshell_app/login.html', {})


def delete_doc(request,un, fn):
    user_objects=files.objects.all().filter(username=request.session['username'])
    dbs=user_objects.order_by('-id')

    if request.method == 'POST':
        client=boto3.client('s3')

        doc_obj= files.objects.get(pk=fn)
        response = client.delete_object(
            Bucket='inanutshell-docfiles',
            Key=doc_obj.docs.name,
        )

        doc_obj.delete()
    
    if('_auth_user_id' not in request.session):
        return render(request,'inanutshell_app/login.html', {})

    return render(request,'inanutshell_app/documents.html',{'db':dbs, "username":request.session['username']})

def documents(request,un):
   
    if('_auth_user_id' not in request.session):
        return render(request,'inanutshell_app/login.html', {})
    user_objects=files.objects.all().filter(username=request.session['username'])
    dbs=user_objects.order_by('-id')

    return render(request,'inanutshell_app/documents.html',{'db':dbs, "username":request.session['username']})

def category(request,un, cy):
  
    if('_auth_user_id' not in request.session):
        return render(request,'inanutshell_app/login.html', {})
    user_objects=files.objects.all().filter(username=request.session['username'])
    dbs=user_objects.order_by('-id')
   
    return render(request,'inanutshell_app/category.html',{'db':dbs, "username":request.session['username'], "cty":cy})

def webview(request,un, fn):
   
    if('_auth_user_id' not in request.session):
        return render(request,'inanutshell_app/login.html', {})
    ids=fn
    dbs= files.objects.get(pk=ids)

    file_str =str(dbs.docs)
    audio_list=file_str.split(".")

    docs_link="https://inanutshell-docfiles.s3.amazonaws.com/"+file_str+"#toolbar=0"
    audio_link_full="https://inanutshell-mediafiles.s3.amazonaws.com/"+audio_list[0]+".mp3"+"#toolbar=0"
    audio_link_summ="https://inanutshell-mediafiles.s3.amazonaws.com/"+audio_list[0]+"_summarized.mp3"+"#toolbar=0"
    return render(request,'inanutshell_app/webview.html',{'username':un, 'req_fn':dbs.filename, 'req_doc':docs_link, 'req_audio_full':audio_link_full, 'req_audio_summ':audio_link_summ, 'req_summry':dbs.summary, "username":request.session['username'], 'id':fn })

def about(request,un):
    test_dict= {'test_dict': 'HELP PAGE', 'username':un}
    return render(request,'inanutshell_app/about.html',context=test_dict)

def contact(request,un):
    test_dict= {'test_dict': 'HELP PAGE', 'username':un}
    return render(request,'inanutshell_app/contact.html',context=test_dict)

def frm_docupload_view(request,un):
    print(request.session)
    if('_auth_user_id' not in request.session):
        return render(request,'inanutshell_app/login.html', {})
    request.session['username']=un

    rp=un.replace(".", "_")
    rs=rp+"@gmail.com"
    user_objects=files.objects.all().filter(username=request.session['username'])

    dbs=user_objects.order_by('-id')

    tags_lst=get_tags(dbs)

    form=frm_docupload()
    if request.method=='POST':

        form=frm_docupload(request.POST,request.FILES)

        if form.is_valid():
            print(' data sucessfully uploaded')

            username = request.session['username']
            email = rs
            filename = form.cleaned_data['filename']
            docs = form.cleaned_data['docs']

            instance = files(username=username, user_email=email, filename=filename, docs=docs)
            instance.save()

            print(request.FILES.keys())
            messages.success(request, 'Form successfully submitted....!')

            return HttpResponseRedirect('/'+request.session['username'])
        else :
            messages.error(request, 'Failed to Upload. Please try again....!')
            return HttpResponseRedirect('/'+request.session['username'])

    return render(request,'inanutshell_app/index.html', {'form':form, 'db':dbs, 'tags_lst':tags_lst, "username":request.session['username'], "test_s":request.session.keys()})

def get_tags(dbs):
    tags_lst=[]
    for key in dbs:
        tags_set=set(tags_lst)
        if key.tag not in tags_set:
            tags_lst.append(key.tag)

    return tags_lst
