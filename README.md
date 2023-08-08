# Группововой проект YaMDb. Яндекс Практикум - 12 спринт.
### Описание
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 

Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 

Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

Пользователи могут оставлять комментарии к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

### Запуск (ОС Windows)
```bash
git clone git@github.com:EgorIvanov96/api_yamdb.git
```
```bash
cd yamdb_final
```
### Создаем и активируем виртуальное окружение:
```bash
python -m venv venv
```
- Windows:
```bash
source venv/Scripts/activate
```
- Linux:
```bash
source venv/bin/activate
```

### Ставим зависимости из requirements.txt:
```bash
pip install -r requirements.txt 
```
### Переходим в папку с файлом manage.py и запускаем сервер
```bash
python manage.py runserver
```
