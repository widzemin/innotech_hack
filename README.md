# innotech_hack

## Команда Балалар

### FaceBoxRecognition_mtcnn

Выделяем все лица с фотографии с помощью mtcnn. Каждое лицо выделяется в прямоугольник фиксированного размера.

### FaceVerification

Используя уже полученные лица от mtcnn делаем encoding их в вектор с помощью vggface2. Дальше сравниваем два лица, как два вектора находя между ними евклидову норму.

### FindProfile

Ищем совпадение лица с датасетом из ссылок на соцсеть, используя написанное в FaceVerification .


### vk.alg/ParsFromVK

Парсер оснойвной информации со страницы vk и всех групп, в которых состоит пользователь. 

### vk.alg/Aho-Coras

Алгоритм Ахо-Корасик для быстрого поиска слов по автомату.

### vk.alg/Graph

Построение графа ключевых слов используя dataset нескольких профессий полученный с помощью парсера ParsFromVK. Выделяем ключевые слова и смотрим количество для каждой професии.

### vk.alg/FirstChapter

Предсказание профессии и заработной платы по профилю. Конкретнее получаем человека, смотрим какие у него встречаются слова с помощью ParsFromVK. Дальше если слово ключевое, то прибавляем для соответствующей профессии вес рассчитаный по методу tf-idf.

### upload_images/run.py

Сервер для того, чтобы вы проверили работоспособность.

### ParserErgul/main.py

Парсер информации о человеке c pdf с сайта ergul.

### upload_images/parser_from_vk

Тоже самое, что и vk.alg/ParsFromVK

### final.py

Воссоединение всего воедино.

## Ссылка на сайт, для того, чтобы испытать

http://dc61c2e4d29c.ngrok.io/upload-image

Введите профиля через пробел в поле choose a username

Загрузите фото в форме правее
