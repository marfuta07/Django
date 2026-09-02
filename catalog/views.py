from django.shortcuts import render
from django.contrib import messages


def home(request):
    return render(request, 'catalog/home.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        if name and phone and message:
            # Обработка данных
            print(f'Сообщение от {name} ({phone}): {message}')

            # Добавляем успешное сообщение
            messages.success(request, 'Ваше сообщение успешно отправлено! Спасибо! ✅')
        else:
            # Добавляем сообщение об ошибке
            messages.error(request, 'Пожалуйста, заполните все поля! ⚠️')

    return render(request, 'catalog/contacts.html')