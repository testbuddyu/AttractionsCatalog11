from django.shortcuts import render, redirect
from FirstPage.models import *
from FirstPage.forms import CreateAttractionForm, CreatePhotoAttachmentsForm
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied

PAGE_SIZE = 2


def main_page(request, page_number=1):
    output = Attractions.objects.all().filter(is_approved=True)
    current_page = Paginator(output, PAGE_SIZE)
    return render(request, "mainpageMain.html",
                  {'attractions': current_page.page(page_number)})


def page_create_request(request):
    if request.user.is_authenticated:
        args = {'form1': CreateAttractionForm(), 'form2': CreatePhotoAttachmentsForm()}
        if request.method == 'POST':
            new_attraction = CreateAttractionForm(request.POST)
            attachments = CreatePhotoAttachmentsForm(request.POST, request.FILES)
            if new_attraction.is_valid() and attachments.is_valid():
                new_attraction.save()
                res = Attractions.objects.all().order_by('-id')[0]
                res.lower_city_name = res.city_name.lower()
                res.lower_name = res.name.lower()
                res.save()
                files = request.FILES.getlist('photo')
                for each in files:
                    att = Attachment.objects.create(photo=each, id_Attraction_id=res.id)
                return redirect('/profile')
            else:
                args['form'] = new_attraction
                args['valid_error'] = 'При добавлении Достопримечательности произошла ошибка. Пожалуйста, составляйте Заявку согласно правилам.'
                return render(request, "pageCreateRequest.html", args)
        return render(request, "pageCreateRequest.html", args)
    else:
        raise PermissionDenied


def page_profile_ap(request):
    if request.user.is_authenticated:
        session = Session.objects.get(session_key=request.session.session_key)
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(id=uid)
        if user.is_moderator:
            return render(request, "pageMyProfileManager.html", {'user': user})
        return render(request, "pageMyProfileAP.html", {'user': user})
    else:
        raise PermissionDenied


def filter_attr_mainpage(request, page_number=1):
    template_name = 'mainpageFilter.html'
    if request.method == 'GET':
        selectCity = request.GET.get('selectCity', '')
        selectCity = selectCity.lower()
        str(selectCity).strip()
        selectType = request.GET.get('selectType', '')
        str(selectType).strip()
        selectSort = request.GET.get('selectSort', '')
        result_bd_request = ''
        if selectSort == 'alphabetAZ':
            order_by_key = 'name'
            result_bd_request = Attractions.objects.all().filter(is_approved=True, type__contains=selectType,
                                                                 lower_city_name__contains=selectCity).order_by(
                order_by_key)
        elif selectSort == 'alphabetZA':
            order_by_key = '-name'
            result_bd_request = Attractions.objects.all().filter(is_approved=True, type__contains=selectType,
                                                                 lower_city_name__contains=selectCity).order_by(
                order_by_key)
        elif selectSort == 'markUp':
            selectCity = '%' + selectCity + '%'  # eto prikol
            selectType = '%' + selectType + '%'
            result_bd_request = Attractions.objects.raw(
                "SELECT id from FirstPage_attractions a join (select id_Attraction_id,avg(value) 'average' from FirstPage_mark group by id_Attraction_id) as m on a.id = m.id_Attraction_id where a.lower_city_name like %s and a.type like %s order by (m.average)",
                [selectCity, selectType])
        elif selectSort == 'markDown':
            selectCity = '%' + selectCity + '%'
            selectType = '%' + selectType + '%'
            result_bd_request = Attractions.objects.raw(
                "SELECT id from FirstPage_attractions a join (select id_Attraction_id,avg(value) 'average' from FirstPage_mark group by id_Attraction_id) as m on a.id = m.id_Attraction_id where a.lower_city_name like %s and a.type like %s order by (m.average)  desc",
                [selectCity, selectType])

        if len(result_bd_request) is 0:
            return render(request, template_name, {'bad_result_search': 'НЕ НАШЕЛ'})
        current_page = Paginator(result_bd_request, PAGE_SIZE)
        return render(request, template_name,
                      {'attractions': current_page.page(page_number), 'url_bonus': 'filter', 'selectSort': selectSort,
                       'selectCity': selectCity, 'selectType': selectType})


def search_attr_by_name(request, page_number=1):
    template_name = 'mainpageSearch.html'
    if request.method == 'GET':
        search_attr = request.GET.get('search_attr', '')
        search_attr = search_attr.lower()
        result_bd_request = Attractions.objects.all().filter(lower_name__contains=search_attr, is_approved=True)
        if result_bd_request.count() == 0:
            return render(request, template_name, {'bad_result_search': 'НЕ НАШЕЛ'})
        current_page = Paginator(result_bd_request, PAGE_SIZE)
        return render(request, template_name, {'attractions': current_page.page(page_number), 'url_bonus': 'search',
                                               'search_attr': search_attr})


def page_users_request(request, page_number=1):
    if request.user.is_authenticated:
        result_bd_request = Attractions.objects.all().filter(is_approved=False)
        current_page = Paginator(result_bd_request, PAGE_SIZE)
        return render(request, "pageUsersRequests.html",
                      {'attractions': current_page.page(page_number), 'url_bonus': 'users_requests',
                       'atr_count': current_page.count})
    else:
        raise PermissionDenied
