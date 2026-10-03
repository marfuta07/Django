from django import forms
from catalog.models import ContactRequest, Product


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Контактный телефон',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше сообщение',
                'rows': 4,
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise forms.ValidationError('Телефон должен содержать только цифры')
        return phone

# Список запрещённых слов
FORBIDDEN_WORDS = [
    'казино',
    'криптовалюта',
    'крипта',
    'биржа',
    'дешево',
    'бесплатно',
    'обман',
    'полиция',
    'радар',
]


class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования товара"""

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def __init__(self, *args, **kwargs):
        """Стилизация формы через Bootstrap"""
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == 'category':
                field.widget.attrs['class'] = 'form-select'
            elif field_name == 'image':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

            # Placeholder для полей
            if field_name == 'name':
                field.widget.attrs['placeholder'] = 'Введите название товара'
            elif field_name == 'description':
                field.widget.attrs['placeholder'] = 'Введите описание товара'
                field.widget.attrs['rows'] = 5
            elif field_name == 'price':
                field.widget.attrs['placeholder'] = 'Введите цену'

    def clean_name(self):
        """Валидация названия на запрещённые слова"""
        name = self.cleaned_data.get('name')
        name_lower = name.lower()

        for word in FORBIDDEN_WORDS:
            if word in name_lower:
                raise forms.ValidationError(
                    f'Слово "{word}" запрещено использовать в названии товара!'
                )
        return name

    def clean_description(self):
        """Валидация описания на запрещённые слова"""
        description = self.cleaned_data.get('description')
        description_lower = description.lower()

        for word in FORBIDDEN_WORDS:
            if word in description_lower:
                raise forms.ValidationError(
                    f'Слово "{word}" запрещено использовать в описании товара!'
                )
        return description

    def clean_price(self):
        """Валидация цены — не может быть отрицательной"""
        price = self.cleaned_data.get('price')

        if price is not None and price < 0:
            raise forms.ValidationError(
                'Цена товара не может быть отрицательной!'
            )
        return price